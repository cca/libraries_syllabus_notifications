from subprocess import call

import pytest

from reminders.notify import notify


def test_email():
    """
    Test sending actual reminder emails by using a sample CSV, the vault@cca.edu
    email, and my own email.
    """
    call(["python", "cli.py", "test/test.csv"])


# list of all templates
@pytest.mark.parametrize(
    "template",
    [
        ("initial"),
        ("followup"),
        ("final"),
        ("summer"),
    ],
)
def test_notify(template):
    """
    Test the notify function in app/notify.py that actually sends emails
    """
    assert (
        notify("me", "ephetteplace", ["ANIMA-1000-1 Animation 1"], None, template)
        == True
    )


def test_template_error():
    """
    Non-existent template logs an error and exits
    """
    with pytest.raises(SystemExit):
        notify(
            "me",
            "ephetteplace",
            ["ANIMA-1000-1 Animation 1"],
            None,
            "nonexistent template",
        )
