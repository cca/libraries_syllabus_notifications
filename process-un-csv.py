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
reader = csv.DictReader(csvfile, ['fname', 'lname', 'pname', 'username'])
report_usernames = {}

for row in reader:
    if row['username'] != '':
        if row['pname'] != '':
            report_usernames[row['pname']] = row['username']
        else:
            report_usernames[row['fname'] + ' ' + row['lname']] = row['username']

# merge the report's usernames dict with the previous usernames
usernames.update(report_usernames)
print(usernames)
