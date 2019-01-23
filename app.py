#!/usr/bin/env python
from __future__ import print_function
import argparse
import csv
import os
import smtplib
from sys import stderr
import time
import webbrowser
# my functions/data
from usernames import usernames
from has_syllabus import has_syllabus
from notify import notify

debug = bool(os.environ.get('DEBUG'))

# CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', help='CSV of the Informer Report')
parser.add_argument('-o', '--open-report',
                    help='open the appropriate Informer report',
                    action='store_true')
parser.add_argument('--template', type=str,
                    choices=['initial', 'followup', 'final', 'summer'],
                    help='which email template to utilize',
                    default='initial')
args = parser.parse_args()

if args.open_report:
    webbrowser.open('https://vault.cca.edu/access/reports.do')
    exit()

report = open(args.file, 'rbU')
reader = csv.DictReader(report)

# filters for problematic rows
# we will trim & lowercase strings before comparison with these values
skipped_faculty = ('staff', 'standby')
# see also: has_syllabus.py, which is used to filter certain courses out

# SMTP server
if debug is True:
    server = None
else:
    server = smtplib.SMTP('localhost')

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
                # either way, add the course to their list
                data[name]['courses'].append(row['Section'] + ' ' + row['Course Title'])
            else:
                stderr.write(
                    'No username for %s, course row for CSV:\n%s' % (name, row)
                )

for faculty in data:
    print(time.strftime("%m/%d/%Y %H:%M:%S"), 'notifying %s...' % faculty)
    notify(faculty, data[faculty]['username'], data[faculty]['courses'], server, args.template)
    # not sure if necessary but I'd rather not spew out emails so fast
    time.sleep(1)

if server is not None:
    server.quit()
