#!/usr/bin/env python
import unittest
from has_syllabus import has_syllabus

class TestHasSyllabus(unittest.TestCase):

  def test_grad_studio(self):
      r = {'usernames': 'amouse', 'xlist': '', 'course': 'ANIMA-270', 'section': 'ANIMA-270-09', 'title': 'Graduate Studio Practice', 'dept': 'ANIMA', 'semester': '2015FA', 'faculty': 'Anon Ymouse'}
      self.assertEqual(has_syllabus(r), False)

  def test_independent_study(self):
      r = {'usernames': 'amouse', 'xlist': '', 'course': 'ANIMA-270', 'section': 'ANIMA-270-09', 'title': 'Independent Study', 'dept': 'ANIMA', 'semester': '2015FA', 'faculty': 'Anon Ymouse'}
      self.assertEqual(has_syllabus(r), False)

  def test_696(self):
      r = {'usernames': 'amouse', 'xlist': '', 'course': 'ANIMA-696', 'section': 'ANIMA-696-09', 'title': 'Animation Course', 'dept': 'ANIMA', 'semester': '2015FA', 'faculty': 'Anon Ymouse'}
      self.assertEqual(has_syllabus(r), False)

  def test_regular_course(self):
      r = {'usernames': 'amouse', 'xlist': '', 'course': 'ANIMA-270', 'section': 'ANIMA-270-09', 'title': 'Animation Course', 'dept': 'ANIMA', 'semester': '2015FA', 'faculty': 'Anon Ymouse'}
      self.assertEqual(has_syllabus(r), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHasSyllabus)
    unittest.TextTestRunner(verbosity=2).run(suite)
