'''
Process faculty information from Workday student JSON into a Python dict of
name:username mappings. The missing syllabi report only has faculty names and not
their usernames; we use the usernames.py dict to find out how to email them.

Usage:
> python update-usernames.py data/courses.json
'''
from datetime import datetime
import json
import sys

from google.cloud import storage

from config import config, logger
from usernames import usernames

today = datetime.now().date()


def what_term_is_it():
    """ determine current term (e.g. "Fall 2023", "Spring 2023") from the date
    """
    season = None
    year = today.year

    if today.month >= 8:
        season = 'Fall'
    elif today.month >= 5:
        season = 'Summer'
    else:
        season = 'Spring'

    return f"{season}_{year}"


def download_courses_file(term):
    client = storage.Client()
    file_name = f'course_section_data_AP_{term}.json'
    logger.info(f'Downloading {file_name} course data from Google Storage.')
    bucket = client.get_bucket(config['BUCKET_NAME'])
    blob = bucket.blob(file_name)
    local_file = f'data/{today.isoformat()}-{term}.json'
    blob.download_to_filename(local_file)


def update_usernames():
    term = what_term_is_it()

    download_courses_file(term)

    filename = f'data/{today.isoformat()}-{term}.json'

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

    if not config.get('DEBUG'):
        with open('reminders/usernames.py', 'w') as file:
            file.write('usernames = ' + str(usernames))
            logger.info(f'Added {new_users} new usernames to username.py list.')
    else:
        logger.info(f'Debugging: would\'ve added {new_users} new usernames to username.py list.')

if __name__ == '__main__':
    update_usernames()
