#!/usr/bin/env python3
'''
Process faculty information from Workday student JSON into a Python dict of
name:username mappings. The missing syllabi report only has faculty names and not
their usernames; we use the usernames.py dict to find out how to email them.

Usage:
> python update-usernames.py data/courses.json
'''
import json
import sys

from config import logger
from usernames import usernames


def update_usernames(filename):
    # file name is passed on command line
    with open(filename, 'r') as file:
        courses = json.load(file)

    user_count = len(usernames)
    new_usernames = {}
    for course in courses:
        for i in course["instructors"]:
            if i['username']:
                new_usernames[i['first_name'] + ' ' + i['last_name']] = i['username']

    # merge the report's usernames dict with the previous usernames, write to file
    usernames.update(new_usernames)
    new_users = len(usernames) - user_count
    with open('app/usernames.py', 'w') as file:
        # wow names aren't all in ASCII deal with it Python 2 sheesh
        file.write('# -*- coding: utf-8\n')
        file.write('usernames = ' + str(usernames))
        logger.info('Added {x} new usernames to username.py list.'.format(x=str(new_users)))

if __name__ == '__main__':
    update_usernames(sys.argv[1])
