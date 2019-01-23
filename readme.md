# Faculty Syllabus Notifications

Take a CSV of our missing syllabi VAULT report and send emails to faculty about which syllabi we expect from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Steps

Note that this app needs to be run from a server with mail capabilities on CCA's network, so as to avoid getting flagged by Google as a potential phishing attempt.

- update the due date & other pieces of the email template in notify.py
- pull faculty usernames by running the included "faculty.sql" in the Portal database but updating the term to the current one, then saving the results as CSV
- create a python dict of new usernames merged with known ones using `python process-un-csv.py usernames.csv > tmp; mv tmp usernames.py`
- in VAULT, run the Missing Syllabi by Semester report (`./app.py --open-report` opens it)
- Export the report to Excel, then save it as a CSV after trimming off the useless bit at the top (but not column headers) & date at the bottom
- sync the local data to the mail server (our dev website server) with sync.sh, then SSH into that server to send the mail
- finally, run `./app.py report.csv >> log.txt` to send out emails, where log.txt is a log file
    + the `--template` flag lets you specify an email template out of the available choices of "initial", "followup", "final", and "summer" e.g. `./app.py report.csv --template followup`
    + you can monitor the emails as they go out using `mail-log.sh` which just continually inspects your system's mail.log file

The app logs faculty without usernames to stderr & they can then be manually added to usernames.py; if you filter report.csv to just their courses, you can simply rerun app.py. If you do this, remember to delete out the co-instructors who already received an email—e.g. if we don't have an email for J R & the faculty column for a course is "J R, Herb Somebody" then delete "Herb Somebody" before rerunning the app.

## Other Notes

If you export a shell environmental variable `DEBUG` to any non-empty value, e.g. "true", the main app will print emails to stdout instead of sending them via SMTP.

You can also use "has_syllabus.py" to count the number of rows in a CSV of courses which have syllabi, the syntax is `python has_syllabus courses.csv`.

## Report Format

Report CSV should have the following columns in this order:

> "semester","dept","title","faculty","section"

No header row, excess columns after "section" are fine and will be ignored.

## LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
