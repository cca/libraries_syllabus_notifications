import argparse
import csv
import smtplib
import time
import webbrowser
from xml.sax.saxutils import unescape

from reminders.config import config, logger
from reminders.update_usernames import update_usernames
from reminders.usernames import usernames
from reminders.has_syllabus import has_syllabus
from reminders.notify import notify


# Meant to run on the CLI, args is an argparse object cast to a dict
def main(args):
    if args['open_report']:
        webbrowser.open('https://vault.cca.edu/access/reports.do')
        exit()

    if args['update']:
        update_usernames()
        exit()

    report = open(args['file'], 'r')
    reader = csv.DictReader(report)

    # Filter out rows without a real faculty value. We trim & lowercase strings before
    # comparison with these values. Note that this last value comes from
    # github.com/cca/libraries_course_lists2
    # it is the fallback value of Course::instructor_names() when they're empty
    skipped_faculty = ('staff', 'standby', '[instructors to be determined]')
    # see also: has_syllabus.py, which is used to filter certain courses out

    # SMTP server
    if config.get('DEBUG'):
        server = None
    else:
        server = smtplib.SMTP(config['SMTP_DOMAIN'], port=config['SMTP_PORT'])
        server.login(config['SMTP_USER'], config['SMTP_PASSWORD'])

    # output values
    data = {}

    for row in reader:
        # skip bad values for courses e.g. studio courses w/o syllabi
        if has_syllabus(row):
            # skip bad faculty values like "Standby" etc.
            names = filter(lambda f: f.strip().lower() not in skipped_faculty, row['Instructor(s)'].split(', '))
            for name in names:
                # if we have a username for the instructor...
                if usernames.get(name) is not None:
                    # initialize if not in output dict already
                    if name not in data:
                        data[name] = {'courses': [], 'username': usernames.get(name)}
                    # either way, add the course to their list, unescape course title as a precaution
                    data[name]['courses'].append(row['Section'] + ' ' + unescape(row['Course Title']))
                else:
                    logger.warning(
                        'No username for {name}, course row for CSV: {row}'.format(
                            name=name,
                            row='    '.join(row.values())
                        )
                    )

    for faculty in data:
        logger.info('notifying {faculty}...'.format(faculty=faculty))
        notify(faculty, data[faculty]['username'], data[faculty]['courses'], server, args['template'])
        # not sure if necessary but I'd rather not spew out emails so fast
        time.sleep(1)

    if server is not None:
        server.quit()


if __name__ == '__main__':
    # CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update',
                        help='update course data & faculty usernames',
                        action='store_true')
    parser.add_argument('-o', '--open-report',
                        help="open VAULT's Missing Syllabi report",
                        action='store_true')
    parser.add_argument('file', nargs='?', help='CSV of missing syllabi report')
    parser.add_argument('--template', type=str,
                        choices=['initial', 'followup', 'final', 'summer'],
                        help='which email template to utilize',
                        default='initial')
    args = parser.parse_args()
    main(vars(args))
