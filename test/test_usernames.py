from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from reminders.config import config
from reminders.update_usernames import download_courses_file, what_term_is_it


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
    term = "Spring_2024"
    file_name = f"course_section_data_AP_{term}.json"
    local_file = Path("data") / f"{date.today().isoformat()}-{term}.json"

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
    mock_blob.download_to_filename.assert_called_once_with(str(local_file))
