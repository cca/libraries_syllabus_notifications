import unittest
from reminders.has_syllabus import has_syllabus
from reminders.notify import notify
from subprocess import call


class TestHasSyllabus(unittest.TestCase):
    """
    Test the has_syllabus() function which determines which course sections we
    filter out as not needing syllabi (because they're mentored study or grad
    studio practice, for instance).
    """
    def test_grad_studio(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Graduate Studio Practice', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_independent_study(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Independent Study', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_696(self):
        r = {'Section': 'ANIMA-696-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_6960(self):
        r = {'Section': 'ANIMA-6960-9', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2019FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_regular_course(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), True)

    def test_mentored_study(self):
        r = {'Section': 'WRITE-660-09', 'Course Title': 'Mentored Study', 'Department Code': 'WRITE', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)
        s = {'Section': 'WRITE-6600-9', 'Course Title': 'Mentored Study', 'Department Code': 'WRITE', 'Semester': '2019FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(s), False)

    def test_comics(self):
        r = {'Section': 'COMIC-615-01', 'Course Title': 'Mentored Study', 'Department Code': 'COMIC', 'Semester': '2016SP', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), True)


class TestEmails(unittest.TestCase):
    """
    Test sending actual reminder emails by using a sample CSV, the vault@cca.edu
    email, and my own email.
    """
    # @TODO we want to import app.main & run it instead of this but that doesn't
    # work right now, see the comment in app/__init__.py
    def test_email(self):
        call(["python", "cli.py", "test/test.csv"])


class TestNotify(unittest.TestCase):
    """
    Test the notify function in app/notify.py that actually sends emails
    """
    def test_notify(self):
        # test every template
        self.assertTrue(notify('me', 'ephetteplace@cca.edu', ['ANIMA-1000-1 Animation 1'], None))
        self.assertTrue(notify('me', 'ephetteplace@cca.edu', ['ANIMA-1000-1 Animation 1'], None, 'followup'))
        self.assertTrue(notify('me', 'ephetteplace@cca.edu', ['ANIMA-1000-1 Animation 1'], None, 'final'))
        self.assertTrue(notify('me', 'ephetteplace@cca.edu', ['ANIMA-1000-1 Animation 1'], None, 'summer'))
        # self.assertRaises(KeyError, notify, 'name', 'username', ['course'], None, 'not a valid type')


# collect all the tests together
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHasSyllabus)
    suite.addTest(TestEmails('test_email'))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
