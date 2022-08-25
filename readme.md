# Faculty Syllabus Notifications

Take a CSV of missing syllabi VAULT report and send emails to faculty about which syllabi we expect from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Steps

Note that this app needs to be run from a server with mail capabilities on CCA's network, so as to avoid getting flagged by Google as a potential phishing attempt.

- update the due date of the email template in notify.py
- download the JSON Workday course data (can use `gsutil` CLI)
- update the dict of faculty usernames using `app/update-usernames.py courses.json`
- in VAULT, run the "Missing Syllabi by Semester" report (`app/app.py -o` opens it)
- convert the report to CSV. Copy the HTML table and paste it into Google Sheets, then download as CSV. Alternatively, export to Excel then save as CSV after trimming the useless bit at the top (but not the column headers) & date at the bottom.
- (optional, but recommended) run summary stats on our collection progress with `app/status.py courses.json report.csv`
- sync the local data to the mail server (our dev website server) with `./sync.sh`, then SSH into that server to send the mail
- finally, run `app/app.py report.csv` to send out emails
  - the `--template` flag lets you specify an email template out of the available choices of "initial" (default), "followup", "final", and "summer" e.g. `app/app.py report.csv --template followup`
  - you can use "mail-log.sh" to monitor outgoing emails by continually inspecting the system's mail.log file

## Other Notes

The sync script relies on an SSH alias named "v1" to a server that can send internal CCA email.

You can dry-run the app by setting a `DEBUG` environment variable to `True`. You can run `DEBUG=true python app/app.py report.csv` to test the script, for instance. Note that this is a great way to detect missing usernames because those are output to stderr before the samples of emails that would be sent. This gives you a chance to manually update usernames.py.

The project is Python 2 because that's what we have on our local web servers but the data processing scripts run locally can be python3. Updating to 3 in the future should be trivial.

If you don't update usernames.py with missing faculty emails before sending out the first batch, you can look at the errors, fill in missing names, and then rerun the app later by filtering report.csv to just the courses of these "missing" instructors. If you do this, remember to delete out the co-instructors who already received an email—e.g. if we don't have an email for "J R" & the faculty column for a course is "J R, Herb Somebody" then delete "Herb Somebody" before rerunning the app.

You can use "has_syllabus.py" to count the number of rows in a CSV of courses which have syllabi:

```sh
> python app/has_syllabus.py data/report.csv
760 courses have syllabi of 806 total in the CSV
```

## Report Format

Report CSV should have the following columns with this exact header row

> "Semester","Department Code","Course Title","Instructor(s)","Section"

Some of the columns are not used but these are the ones typically contained in the VAULT report.

## LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
