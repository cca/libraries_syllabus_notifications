from reminders.notify import notify
from subprocess import call


def test_email():
    """
    Test sending actual reminder emails by using a sample CSV, the vault@cca.edu
    email, and my own email.
    @TODO we want to import app.main & run it instead of this but that doesn't
    work right now, see the comment in app/__init__.py
    """
    call(["python", "cli.py", "test/test.csv"])


# @TODO parametrize
def test_notify():
    """
    Test the notify function in app/notify.py that actually sends emails
    """
    # test every template
    assert notify('me', 'ephetteplace', ['ANIMA-1000-1 Animation 1'], None) == True
    assert notify('me', 'ephetteplace', ['ANIMA-1000-1 Animation 1'], None, 'followup') == True
    assert notify('me', 'ephetteplace', ['ANIMA-1000-1 Animation 1'], None, 'final') == True
    assert notify('me', 'ephetteplace', ['ANIMA-1000-1 Animation 1'], None, 'summer') == True
    # self.assertRaises(KeyError, notify, 'name', 'username', ['course'], None, 'not a valid type')
