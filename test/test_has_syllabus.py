from reminders.has_syllabus import has_syllabus

# @TODO parametrize
"""
Test the has_syllabus() function which determines which course sections we
filter out as not needing syllabi (because they're mentored study or grad
studio practice, for instance).
"""
def test_grad_studio():
    r = {'Section': 'ANIMA-270-09', 'Course Title': 'Graduate Studio Practice', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == False

def test_independent_study():
    r = {'Section': 'ANIMA-270-09', 'Course Title': 'Independent Study', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == False

def test_696():
    r = {'Section': 'ANIMA-696-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == False

def test_6960():
    r = {'Section': 'ANIMA-6960-9', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2019FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == False

def test_regular_course():
    r = {'Section': 'ANIMA-270-09', 'Course Title': 'Animation Course', 'Department Code': 'ANIMA', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == True

def test_mentored_study():
    r = {'Section': 'WRITE-660-09', 'Course Title': 'Mentored Study', 'Department Code': 'WRITE', 'Semester': '2015FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == False
    s = {'Section': 'WRITE-6600-9', 'Course Title': 'Mentored Study', 'Department Code': 'WRITE', 'Semester': '2019FA', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(s) == False

def test_comics():
    r = {'Section': 'COMIC-615-01', 'Course Title': 'Mentored Study', 'Department Code': 'COMIC', 'Semester': '2016SP', 'Instructor(s)': 'Anon Ymouse'}
    assert has_syllabus(r) == True
