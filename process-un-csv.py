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
columns = ('username', 'name')
reader = csv.DictReader(csvfile, fieldnames=columns)
report_usernames = {}

for row in reader:
    if row['username'] != '':
        report_usernames[row['name']] = row['username']

# merge the report's usernames dict with the previous usernames
usernames.update(report_usernames)
# output in a format suitable for saving to a python file
print('usernames = ' + str(usernames))
