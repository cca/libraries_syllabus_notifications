#!/usr/bin/env python
import unittest
from has_syllabus import has_syllabus


class TestHasSyllabus(unittest.TestCase):

    def test_grad_studio(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Graduate Studio Practice', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_independent_study(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Independent Study', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_696(self):
        r = {'Section': 'ANIMA-696-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_regular_course(self):
        r = {'Section': 'ANIMA-270-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), True)

    def test_mentored_study(self):
        r = {'Section': 'WRITE-660-09', 'Course Title': 'Mentored Study', 'Department Code': 'WRITE', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), False)

    def test_comics(self):
        r = {'Section': 'COMIC-615-01', 'Course Title': 'Mentored Study', 'Department Code': 'COMIC', 'Semester': '2016SP', 'Instructor(s)': 'Anon Ymouse'}
        self.assertEqual(has_syllabus(r), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHasSyllabus)
    unittest.TextTestRunner(verbosity=2).run(suite)
