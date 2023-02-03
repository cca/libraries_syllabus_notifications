import argparse
import csv
import smtplib
import time
import webbrowser

from reminders.config import config, logger
from reminders.map import to_faculty_lists
from reminders.update_usernames import update_usernames
from reminders.notify import notify


# Meant to run on the CLI, args is an argparse object cast to a dict
def main(args):
    if args['open_report']:
        webbrowser.open('https://vault.cca.edu/access/reports.do')
        exit()

    if args['update']:
        update_usernames()
        exit()

    with open(args['file'], 'r') as fh:
        reader = csv.DictReader(fh)
        data = to_faculty_lists(reader)

    # initialize SMTP server
    if config.get('DEBUG'):
        server = None
    else:
        server = smtplib.SMTP(config['SMTP_DOMAIN'], port=config['SMTP_PORT'])
        server.login(config['SMTP_USER'], config['SMTP_PASSWORD'])

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
