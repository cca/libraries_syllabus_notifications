from datetime import date
import json
import logging
from pathlib import Path
import tempfile
from unittest.mock import MagicMock, patch, mock_open

import pytest

from reminders.config import config
from reminders.update_usernames import (
    download_courses_file,
    update_usernames,
    what_term_is_it,
)
from reminders.usernames import usernames


@pytest.mark.parametrize(
    "date,term",
    [
        (date(2022, 8, 15), "Fall_2022"),
        (date(2023, 1, 5), "Spring_2023"),
        (date(2023, 5, 1), "Summer_2023"),
    ],
)
def test_what_term(date, term):
    assert what_term_is_it(date) == term


@pytest.fixture
def mock_storage_client():
    with patch("reminders.update_usernames.storage.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance


def test_download_courses_file(mock_storage_client, tmp_path):
    term: str = "Spring_2024"
    file_name: str = f"course_section_data_AP_{term}.json"
    local_file: Path = Path("data") / f"{date.today().isoformat()}-{term}.json"

    # Mock the bucket and blob
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_storage_client.get_bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    # Call the function
    download_courses_file(term)

    # Assertions
    mock_storage_client.get_bucket.assert_called_once_with(config["BUCKET_NAME"])
    mock_bucket.blob.assert_called_once_with(file_name)
    mock_blob.download_to_filename.assert_called_once_with(local_file)


def test_update_usernames(caplog) -> None:
    mock_courses_data: list[dict[str, list[dict[str, str]]]] = [
        {
            "instructors": [
                {"first_name": "John", "last_name": "Doe", "username": "jdoe"},
                {"first_name": "Jane", "last_name": "Smith", "username": "jsmith"},
            ]
        }
    ]
    existing_user: tuple[str, str] = next(iter(usernames.items()))
    existing_user_str: str = f"'{existing_user[0]}': '{existing_user[1]}'"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_un_path: Path = Path(tmp_dir) / "usernames.py"
        mock_file_path: Path = Path(tmp_dir) / "mocked_file.json"

        # Write mock JSON data to the temp file
        with open(mock_file_path, "w") as mock_file:
            json.dump(mock_courses_data, mock_file)

        with patch(
            "reminders.update_usernames.download_courses_file",
            return_value=mock_file_path,
        ):
            # test first with DEBUG (won't add usernames)
            with patch("reminders.update_usernames.config", {"DEBUG": True}):
                with caplog.at_level(logging.INFO):
                    update_usernames(tmp_un_path)
                    assert (
                        "Debugging: would've added 2 new usernames to username.py list."
                        in caplog.text
                    )

            update_usernames(tmp_un_path)
            with open(tmp_un_path, "r") as file:
                content: str = file.read()
                assert "usernames: dict[str, str] =" in content
                assert existing_user_str in content
                assert "'John Doe': 'jdoe'" in content
                assert "'Jane Smith': 'jsmith'" in content
