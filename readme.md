# Faculty Syllabus Notifications

Take a CSV of our Informer course information report and send emails to faculty about which syllabi we're expecting from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Steps

- run Informer report (`./app.py --open-report` to open it in a browser) with the following settings: no header row, UTF-8, comma-separated multi-value fields
- (possibly unnecessary) update usernames.py with any new faculty usernames
- run `./app.py data/report.csv > log.txt` where report.csv is from Informer & log.txt is a log file
- the `--template` flag lets you specify an email template out of the available choices of "initial", "followup", and "final", e.g. `./app.py data.csv --template followup`
- faculty without usernames will be logged to stderr

## Report Format

Report CSV should have the following columns in this order:

> "semester","dept","title","faculty","section","course"

No header row, excess columns after "course" are fine and will be ignored.

## To Do / Future Considerations

**Recognize a `DEBUG` environment variable?** Could print mails to stdout instead of actually sending as well as log additional information.

**Multi-part HTML emails?** Would allow us to use hyperlinked text rather than plain text URLs, also some formatting to highlight important phrases. Not a high priority as Gmail does a decent job parsing and displaying plain text emails.
