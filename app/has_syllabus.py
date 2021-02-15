from __future__ import print_function
import argparse
import csv
from datetime import date

# for CLI usage
parser = argparse.ArgumentParser(description='given a Missing Syllabi Report CSV, determine how many courses actually require syllabi (e.g. are not Grad Studio Practice, Mentored Study, etc.)')
parser.add_argument('file', help='CSV of the Informer Report')
parser.add_argument('--csv', '-c',
                    help='write filtered report to CSV named by the date',
                    action='store_true')


def has_syllabus(row):
    """
    Some courses, mostly Independent Study & Graduate Studio Practice, don't
    have syllabi & we don't want to annoy faculty asking for one. This fn takes
    a course, checks it against several possible attributes of courses that do
    not have syllabi, & returns False if it looks like a non-syllabus course.
    """
    # All COMIC courses, even "Mentored Study" etc., are an exception
    # & _do_ have syllabi, per Maya Lawrence on 2016-01-28
    if row['Department Code'] == 'COMIC':
        return True

    if row['Course Title'] in ('Independent Study', 'Graduate Studio Practice', 'Mentored Study'):
        return False

    coursenum = int(row['Section'].split('-')[1])
    course = '-'.join(row['Section'].split('-')[0:2])

    # (3|6)96(0) -> (Under)grad independent study
    # (3|6)98(0) -> (Under)grad internship
    if coursenum in (698, 398, 396, 696, 6980, 3980, 3960, 6960):
        return False

    # FINAR-660 is Graduate Studio Practice, no syllabus
    # WRITE-660 is Mentored Study which submits inidividual contracts
    # WRITE-608 is a thesis course & the faculty member submits a narrative
    # to VAULT in lieu of syllabi, per email from Gloria Fry 2016-09-06
    # Some of these should be caught above but just in case
    if course in ('FINAR-660', 'WRITE-660', 'WRITE-608', 'FINAR-6600', 'WRITE-6600', 'WRITE-6080'):
        return False

    # fallthrough; nothing else fired so it must have a syllabus
    return True

# if we run this on the cli & pass it a CSV
# it'll total up the number of courses in the CSV that should have syllabi
if __name__ == '__main__':
    args = parser.parse_args()
    reader = csv.DictReader(open(args.file, 'r'))
    if args.csv:
        # see readme, missing syllabi reports always contain these fields
        fields = ["Semester", "Department Code", "Course Title", "Instructor(s)", "Section"]
        writer = csv.DictWriter(open('{}-missing-syllabi.csv'.format(date.today().isoformat()), 'w'), fieldnames=fields)
        writer.writeheader()
        for row in reader:
            if has_syllabus(row):
                writer.writerow(row)
    else:
        syllabus_count = 0
        total_count = 0

        for row in reader:
            total_count += 1
            if has_syllabus(row):
                syllabus_count += 1

        print('%s courses have syllabi of %s total in the CSV' % (syllabus_count, total_count))
