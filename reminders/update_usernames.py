"""
Process faculty information from Workday student JSON into a Python dict of
name:username mappings. The missing syllabi report only has faculty names and not
their usernames; we use the usernames.py dict to find out how to email them.
"""

from datetime import date, datetime
import json
from pathlib import Path
from typing import Any

from google.cloud import storage

from reminders.config import config, logger

try:
    from reminders.usernames import usernames
except ModuleNotFoundError:
    usernames: dict[str, str] = {}

today: date = datetime.now().date()


def what_term_is_it(date=today) -> str:
    """determine current term (e.g. "Fall 2023", "Spring 2023") from the date"""
    season: str = ""
    year: int = date.year

    if date.month >= 8:
        season = "Fall"
    elif date.month >= 5:
        season = "Summer"
    else:
        season = "Spring"

    return f"{season}_{year}"


def download_courses_file(term) -> Path:
    client = storage.Client()
    file_name: str = f"course_section_data_AP_{term}.json"
    logger.info(f"Downloading {file_name} course data from Google Storage.")
    bucket: storage.Bucket = client.get_bucket(config["BUCKET_NAME"])
    blob: storage.Blob = bucket.blob(file_name)
    local_file: Path = Path("data") / f"{today.isoformat()}-{term}.json"
    blob.download_to_filename(local_file)
    return local_file


def update_usernames(un_py_path: Path = Path("reminders") / "usernames.py") -> None:
    term: str = what_term_is_it()

    file_path: Path = download_courses_file(term)

    with open(file_path, "r") as file:
        courses: list[dict[str, Any]] = json.load(file)

    user_count: int = len(usernames)
    new_usernames: dict[str, str] = {}
    for course in courses:
        for i in course["instructors"]:
            if i["username"]:
                new_usernames[i["first_name"] + " " + i["last_name"]] = i["username"]

    # merge the report's usernames dict with the previous usernames, write to file
    usernames.update(new_usernames)
    new_users: int = len(usernames) - user_count

    if not config.get("DEBUG"):
        un_py_path.parent.mkdir(parents=True, exist_ok=True)
        with open(un_py_path, "w") as file:
            file.write("usernames: dict[str, str] = " + str(usernames))
            logger.info(f"Added {new_users} new usernames to username.py list.")
    else:
        logger.info(
            f"Debugging: would've added {new_users} new usernames to username.py list."
        )
