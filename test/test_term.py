from datetime import date

import pytest

from reminders.update_usernames import what_term_is_it


@pytest.mark.parametrize("date,term", [
    (date(2022, 8, 15), "Fall_2022"),
    (date(2023, 1, 5), "Spring_2023"),
    (date(2023, 5, 1), "Summer_2023"),
])
def test_what_term(date, term):
    assert what_term_is_it(date) == term
