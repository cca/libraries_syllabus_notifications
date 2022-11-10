# Faculty Syllabus Notifications

Take a CSV of missing syllabi VAULT report and send emails to faculty about which syllabi we expect from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Setup

Usual Python projects steps and configure a .env file with values for SMTP domain, port, user, and password (see example.env). Consult Mailgun or the Moodle outgoing mail configuration for these values.

```sh
> pipenv install
> cp app/example.env app/.env
> vim app/.env # edit in real values
> pipenv shell # run inside the virtual environment
> python app/app.py -h # view usage information, see steps below
```

## Steps

- update the due date of the email template in notify.py
- download the JSON Workday course data (can use `gsutil` CLI, @TODO automate this)
- update the dict of faculty usernames using `python app/update-usernames.py courses.json`
- in VAULT, run the "Missing Syllabi by Semester" report (`python app/app.py -o` opens it)
- convert the report to CSV. Copy the HTML table and paste it into Google Sheets, then download as CSV. Alternatively, export to Excel then save as CSV after trimming the useless bit at the top (but not the column headers) & date at the bottom.
- (optional, but recommended) run summary stats on our collection progress with `python app/status.py courses.json report.csv`
- finally, run `python app/app.py report.csv` to send emails
  - the `--template` flag lets you specify an email template out of the available choices of "initial" (default), "followup", "final", and "summer" e.g. `python app/app.py report.csv --template followup`

## Other Notes

We can dry-run the app by setting a `DEBUG` environment variable (or .env value) to `True`. Run `DEBUG=true python app/app.py report.csv` to test the script, for instance. This is a great way to detect missing usernames because those are output to stderr before the samples of emails that would be sent. It gives us a chance to manually update usernames.py.

If we forget to update usernames.py with missing usernames before sending out the first batch, we can look at the errors, fill in missing names, and then rerun the app later by filtering report.csv to just the courses of these "missing" instructors. Remember to delete out the co-instructors who already received an email—e.g. if we don't have an email for "J R" & the faculty column for a course is "J R, Herb Somebody" then delete "Herb Somebody" before rerunning the app.

We can use "has_syllabus.py" to count the number of rows in a CSV of courses which have syllabi:

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
