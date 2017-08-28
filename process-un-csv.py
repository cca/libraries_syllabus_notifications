'''
One-time script to process export from Faculty Usernames report
https://vm-informer-01.cca.edu/informer/?locale=en_US#action=ReportDetails&reportId=103645186
into a Python dict which can then be pasted into usernames.py
Usage:
> python process-un-csv.py data/faculty-usernames.csv > usernames.py
'''
import csv
import sys
from usernames import usernames

# file name is passed on command line
csvfile = open(sys.argv[1])
reader = csv.DictReader(csvfile)
report_usernames = {}

for row in reader:
    if row['Username'] != '':
        if row['Preferred Name'] != '':
            report_usernames[row['Preferred Name']] = row['Username']
        else:
            report_usernames[row['Givenname'] + ' ' + row['Surname']] = row['Username']

# merge the report's usernames dict with the previous usernames
usernames.update(report_usernames)
# output in a format suitable for saving to a python file
print('usernames = ' + str(usernames))
