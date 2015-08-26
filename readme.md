# Faculty Syllabus Notifications

Take a CSV of our Informer course information report and send emails to faculty about which syllabi we're expecting from them. We skip notifying faculty for courses which do not require syllabi (e.g. Graduate Studio Practice) and work around problematic faculty values like "Staff" and "Standby".

## Steps

- run Informer report (`./app.py --open-report` to open it in a browser) with the following settings: no header row, UTF-8, comma-separated multi-value fields
- (possibly unnecessary) update usernames.py with any new faculty usernames
- run `./app.py data/report.csv` where report.csv is from Informer
- faculty without usernames will be logged to stderr

## Report Format

Report CSV should have the following columns in this order:

"semester","dept","title","faculty","section","course","xlist","usernames"

No header row, excess columns after "usernames" are fine and will be ignored. "Usernames" must be a comma-separated list of usernames. Only course section and title are actually used but other columns are still expected to be present because that's the way the Informer report is structured.

## To Do / Future Considerations

**Recognize a `DEBUG` environment variable?** Could print mails to stdout instead of actually sending as well as log additional information.

**Multi-part HTML emails?** Would allow us to use hyperlinked text rather than plain text URLs. Not a high priority as Gmail does a decent job parsing and display plain text emails.
