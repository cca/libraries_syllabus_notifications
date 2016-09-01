# Faculty Syllabus Notifications

Take a CSV of our missing syllabi VAULT report and send emails to faculty about which syllabi we expect from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Steps

- update the due date & other pieces of the email template in notify.py
- pull all faculty usernames with [the Informer report](https://vm-informer-01.cca.edu/informer/?locale=en_US#action=ReportRun&reportId=103645186&launch=false)
- create a python dict of new usernames merged with known ones using `python process-un-csv.py data/faculty-usernames.csv > data/usernames-dict.txt`
- manually edit "usernames-dict.txt" such that it exports a `usernames` dict & is named "usernames.py"
- in VAULT, run the Missing Syllabi by Semester report (`./app.py --open-report` opens it)
- Export the report to Excel, then in Excel save it as a CSV after trimming off header rows & date at the bottom
- finally, run `./app.py data/report.csv >> data/log.txt` to send out emails, where log.txt is a log file
    + the `--template` flag lets you specify an email template out of the available choices of "initial", "followup", and "final", e.g. `./app.py data.csv --template followup`
    + faculty without usernames will be logged to stderr & can be manually added to usernames.py; if you filter report.csv to just their courses, you can simply rerun app.py

## Other Notes

If you export a shell environmental variable `DEBUG` to any non-empty value, e.g. "true", the main app will print emails to stdout instead of sending them via SMTP.

You can also use "has_syllabus.py" to count the number of rows in a CSV of courses which have syllabi, the syntax is `python has_syllabus courses.csv`.

## Report Format

Report CSV should have the following columns in this order:

> "semester","dept","title","faculty","section"

No header row, excess columns after "section" are fine and will be ignored.

## To Do / Future Considerations

**Multi-part HTML emails?** Would allow us to use hyperlinked text rather than plain text URLs, also some formatting to highlight important phrases. Not a high priority as Gmail does a decent job parsing and displaying plain text emails.

## LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
