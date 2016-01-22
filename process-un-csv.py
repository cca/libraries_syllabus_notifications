'''
One-time script to process export from Faculty Usernames report
https://vm-informer-01.cca.edu/informer/?locale=en_US#action=ReportDetails&reportId=103645186
into a Python dict which can then be pasted into usernames.py
'''
import csv

# change filename to whatever the report CSV is
csvfile = open('Faculty Usernames.csv')
reader = csv.DictReader(csvfile, ['fname', 'lname', 'pname', 'username'])
out = {}

for row in reader:
    if row['username'] != '':
        if row['pname'] != '':
            out[row['pname']] = row['username']
        else:
            out[row['fname'] + ' ' + row['lname']] = row['username']

print(out)
