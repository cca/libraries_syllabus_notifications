import pytest

from reminders.map import to_faculty_lists

@pytest.mark.parametrize("reader,output", [
    # course without a syllabus (because its ind. study)
    ([{ 'Instructor(s)': 'Audre Lorde', 'Section': 'ANIMA-1000-1',
    'Department Code': 'ANIMA', 'Course Title': 'Independent Study'}],
    {}),
    # one instructor
    ([{ 'Instructor(s)': 'Eric Phetteplace', 'Section': 'ILLUS-1160-1',
    'Department Code': 'ILLUS', 'Course Title': 'Drawing 1'}],
    { "Eric Phetteplace": { "courses": ['ILLUS-1160-1 Drawing 1'], "username": "ephetteplace" }, } ),
    # two instructors
    ([{ 'Instructor(s)': 'Eric Phetteplace, Annemarie Haar', 'Section': 'ILLUS-1160-1',
    'Department Code': 'ILLUS', 'Course Title': 'Drawing 1'}],
    { "Eric Phetteplace": { "courses": ['ILLUS-1160-1 Drawing 1'], "username": "ephetteplace" },
    "Annemarie Haar": { "courses": ['ILLUS-1160-1 Drawing 1'], "username": "ahaar" }, }),
    # placeholder instructors
    ([{ 'Instructor(s)': 'standby', 'Section': 'FASHN-3100-1',
    'Department Code': 'FASHN', 'Course Title': 'Fashion Illus 3'},
    { 'Instructor(s)': 'staff', 'Section': 'FASHN-3100-1',
    'Department Code': 'FASHN', 'Course Title': 'Fashion Illus 3'},
    { 'Instructor(s)': '[instructors to be determined]', 'Section': 'FASHN-3100-1',
    'Department Code': 'FASHN', 'Course Title': 'Fashion Illus 3'}],
    {}),
    # one real & one placeholder instructor
    ([ { 'Instructor(s)': 'Eric Phetteplace, staff', 'Section': 'FASHN-3100-1',
    'Department Code': 'FASHN', 'Course Title': 'Fashion Illus 3'}, ],
    { "Eric Phetteplace": { "courses": ['FASHN-3100-1 Fashion Illus 3'], "username": "ephetteplace" }, } ),
    # list of two courses
    ([{ 'Instructor(s)': 'Eric Phetteplace', 'Section': 'ILLUS-1160-1',
    'Department Code': 'ILLUS', 'Course Title': 'Drawing 1'},
    { 'Instructor(s)': 'Eric Phetteplace', 'Section': 'WRLIT-2020-2',
    'Department Code': 'WRLIT', 'Course Title': 'Poetry'}],
    { "Eric Phetteplace": { "courses": [ 'ILLUS-1160-1 Drawing 1',
    'WRLIT-2020-2 Poetry' ], "username": "ephetteplace" }, } ),
])
def test_to_faculty_list(reader, output):
    result = to_faculty_lists(reader)
    assert output == result
