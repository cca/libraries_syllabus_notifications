#!/usr/bin/env python3
'''
Process faculty information from Workday student JSON into a Python dict of
name:username mappings. The missing syllabi report only has faculty names and not
their usernames; we use the usernames.py dict to find out how to email them.

Usage:
> python process-un-csv.py data/courses.json
'''
import json
import sys
from usernames import usernames

# file name is passed on command line
with open(sys.argv[1], 'r') as file:
    courses = json.load(file)

new_usernames = {}
for course in courses:
    for i in course["instructors"]:
        if i['username']:
            new_usernames[i['first_name'] + ' ' + i['last_name']] = i['username']

# merge the report's usernames dict with the previous usernames, write to file
usernames.update(new_usernames)
with open('usernames.py', 'w') as file:
    file.write('usernames = ' + str(usernames))
