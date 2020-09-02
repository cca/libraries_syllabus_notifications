#!/usr/bin/env python3
"""
Determine the collection percentage for syllabi for a given semester
We need to know a) the courses for a semester & b) the missing syllabi report

Usage: python status.py courses.json report.csv
"""
import csv
import json
import sys

from config import logger
from has_syllabus import has_syllabus

if len(sys.argv) == 3:
    courses_json = sys.argv[1]
    report_csv = sys.argv[2]
else:
    courses_json = 'data/courses.json'
    report_csv = 'data/report.csv'

total_courses = 0
courses_with_syllabi = 0
# make this a float so math later is also done in floats, needed for percentage
missing_syllabi = 0.0

def map_json(course):
    return {
        'Department Code': course['subject'],
        'Course Title': course['section_title'],
        'Section': course['section_code']
    }

with open(courses_json, 'r') as fh:
    courses = json.load(fh)
    total_courses = len(courses)
    courses_with_syllabi = len([c for c in courses if has_syllabus(map_json(c))])

with open(report_csv, 'r') as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        if has_syllabus(row):
            missing_syllabi += 1

percentage = round(100 * (courses_with_syllabi - missing_syllabi) / courses_with_syllabi, 2)
logger.info('Syllabi Collection Progress:\n\nTotal Courses:\t\t{}\nSyllabi Courses:\t{}\nMissing Syllabi:\t{}\nPercentage:\t\t{}%\n'.format(total_courses, courses_with_syllabi, int(missing_syllabi), percentage))
