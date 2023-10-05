from xml.sax.saxutils import unescape

from reminders.config import logger
from reminders.has_syllabus import has_syllabus

try:
    from reminders.usernames import usernames
except ModuleNotFoundError:
    usernames = {}


def to_faculty_lists(reader):
    """map CSV reader to a dict with keys that are faculty usernames and
    values that are another dict with two properties: a 'course' list of
    sections with missing list and a 'username' string

    Args:
        reader (DictReader): a CSV DictReader instance
        e.g. from csv.DictReader(file)

    Returns:
        dict: dict of faculty section lists structured like
        { "faculty name": { "courses": [ course one, course two ],
        "username": "fname" }, ... }
    """
    output = {}

    # Filter out rows without a real faculty value. We trim & lowercase strings before
    # comparison with these values. Note that this last value comes from
    # github.com/cca/libraries_course_lists2
    # it is the fallback value of Course::instructor_names() when they're empty
    skipped_faculty = ("staff", "standby", "[instructors to be determined]")
    # see also: has_syllabus.py, which is used to filter certain courses out

    for row in reader:
        # skip bad values for courses e.g. studio courses w/o syllabi
        if has_syllabus(row):
            # skip bad faculty values like "Standby" etc.
            names = filter(
                lambda f: f.strip().lower() not in skipped_faculty,
                row["Instructor(s)"].split(", "),
            )
            for name in names:
                # if we have a username for the instructor...
                if usernames.get(name) is not None:
                    # initialize if not in output dict already
                    if name not in output:
                        output[name] = {"courses": [], "username": usernames.get(name)}
                    # either way, add the course to their list, unescape course title as a precaution
                    output[name]["courses"].append(
                        row["Section"] + " " + unescape(row["Course Title"])
                    )
                else:
                    logger.warning(
                        "No username for {name}, course row for CSV: {row}".format(
                            name=name, row="    ".join(row.values())
                        )
                    )

    return output
