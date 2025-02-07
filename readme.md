# Faculty Syllabus Notifications

Take a CSV of missing syllabi VAULT report and send emails to faculty about which syllabi we expect from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Setup

Usual Python projects steps and configure a .env file with values for SMTP domain, port, user, and password (see example.env). Consult Mailgun or the Moodle outgoing mail configuration for these values.

```sh
> uv install
> cp reminders/example.env reminders/.env
> vim reminders/.env # edit in real values
> uv run python cli.py -h # run inside the virtual environment
```

We also need access to the "integration files source" Google Storage Bucket. Once our CCA account has access permission, we use [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) to allow this project access. This should be a matter of [installing `gcloud`](https://cloud.google.com/sdk/docs/install) and running `gcloud auth application-default login` once.

## Steps

- activate the virtual environment, `source .venv/bin/activate`
- update course data & faculty usernames, `python cli.py -u`
- run VAULT's "Missing Syllabi by Semester" report (`python cli.py -o` opens it)
- convert the report to CSV. Copy the HTML table and paste it into Google Sheets, then download as CSV. Alternatively, export to Excel then save as CSV after trimming the extraneous top rows (but not the column headers) & date at the bottom.
- (optional, but recommended) run summary stats on our collection progress with `python reminders/status.py data/2023-01-26-Spring_2023.json data/report.csv`
- finally, run `python cli.py data/report.csv` to send emails, use the `--template` flag to specify one of:
  - initial (default)
  - followup (sent ≈2 weeks later)
  - final (sent another ≈2 weeks later)
  - summer (exception because we only send one reminder)

## Testing

There are pytest tests, but not much coverage.

```sh
python -m pytest # run tests
coverage run -m pytest # test coverage
coverage report --omit test/*,reminders/usernames.py,reminders/__init__.py # coverage report
```

## Other Notes

We can dry-run the app by setting a `DEBUG` environment variable (or .env value) to `True`. Run `DEBUG=true python cli.py report.csv` to test the script, for instance. The `DEBUG` env var can also be used to debug issues with Google Cloud authentication, e.g. `DEBUG=True python reminders/update_usernames.py`.

We can use "has_syllabus.py" to count the number of rows in a CSV of courses which have syllabi:

```sh
> python reminders/has_syllabus.py data/report.csv
760 courses have syllabi of 806 total in the CSV
```

## Report Format

Report CSV should have the following columns with this exact header row

> "Semester","Department Code","Course Title","Instructor(s)","Section"

Some of the columns are not used but these are the ones typically contained in the VAULT report.

## LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
