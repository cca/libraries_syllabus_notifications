#!/usr/bin/env python
from __future__ import print_function
import argparse
import csv
import smtplib
import webbrowser
from time import sleep
# my functions/data
from usernames import usernames
from has_syllabus import has_syllabus
from notify import notify

# CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', help='CSV of the Informer Report')
parser.add_argument('-o', '--open-report',
                    help='open the appropriate Informer report',
                    action='store_true')
parser.add_argument('--template', type=str,
                    choices=['initial', 'followup', 'final'],
                    help='which email template to utilize',
                    default='initial')
args = parser.parse_args()

if args.open_report:
    webbrowser.open('https://vault.cca.edu/access/reports.do')
    exit()

report = open(args.file, 'rb')
# the columns in the department-specific Informer CSV, in order
columns = [
    'semester',
    'dept',
    'title',
    'faculty',
    'section'
]  # we leave off last few columns because they're unused
reader = csv.DictReader(report, columns)

# filters for problematic rows
# we will trim & lowercase strings before comparison with these values
skipped_faculty = ('staff', 'standby')
# see also: has_syllabus.py, which is used to filter certain courses out

# SMTP server
server = smtplib.SMTP('localhost')

# output values
data = {}

for row in reader:
    # skip bad values for courses e.g. studio courses w/o syllabi
    if has_syllabus(row):
        # skip bad faculty values like "Standby" etc.
        names = filter(lambda f: f.strip().lower() not in skipped_faculty, row['faculty'].split(', '))
        for name in names:
            # initialize if not in output dict already
            if name not in data:
                data[name] = {'courses': [],
                              'username': usernames.get(name)}

            data[name]['courses'].append(row['section'] + ' ' + row['title'])

for faculty in data:
    print('notifying %s...' % faculty)
    notify(faculty, data[faculty]['username'], data[faculty]['courses'], server, args.template)
    # not sure if necessary but I'd rather not spew out emails so fast
    sleep(1)

server.quit()
