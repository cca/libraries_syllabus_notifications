from datetime import date
import os
import shlex

import pytest

from reminders.has_syllabus import has_syllabus, main, on_portal

"""
Test the has_syllabus() function which determines which course sections we
filter out as not needing syllabi (because they're mentored study or grad
studio practice, for instance).
"""


@pytest.mark.parametrize(
    "section,result",
    [
        (
            {
                "Section": "ANIMA-270-09",
                "Course Title": "Graduate Studio Practice",
                "Department Code": "ANIMA",
                "Semester": "2015FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "ANIMA-270-09",
                "Course Title": "Independent Study",
                "Department Code": "ANIMA",
                "Semester": "2015FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "ANIMA-696-09",
                "Course Title": "Animation Course",
                "Department Code": "ANIMA",
                "Semester": "2015FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "ANIMA-6960-9",
                "Course Title": "Animation Course",
                "Department Code": "ANIMA",
                "Semester": "2019FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "ANIMA-270-09",
                "Course Title": "Animation Course",
                "Department Code": "ANIMA",
                "Semester": "2015FA",
                "Instructor(s)": "Anon Ymouse",
            },
            True,
        ),
        (
            {
                "Section": "WRITE-660-09",
                "Course Title": "Mentored Study",
                "Department Code": "WRITE",
                "Semester": "2015FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "WRITE-6600-9",
                "Course Title": "Mentored Study",
                "Department Code": "WRITE",
                "Semester": "2019FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
        (
            {
                "Section": "COMIC-615-01",
                "Course Title": "Mentored Study",
                "Department Code": "COMIC",
                "Semester": "2016SP",
                "Instructor(s)": "Anon Ymouse",
            },
            True,
        ),
        (
            {
                "Section": "WRITE-6600-01",
                "Course Title": "Writing",
                "Department Code": "WRITE",
                "Semester": "2024FA",
                "Instructor(s)": "Anon Ymouse",
            },
            False,
        ),
    ],
)
def test_section(section, result):
    assert has_syllabus(section) == result


# note: no status=cancelled in our data, these courses are always hidden
@pytest.mark.parametrize(
    "section,result",
    [
        (
            {
                "hidden": "0",
                "status": "closed",
                "academic_units": [{"refid": "AU_ANIMA"}],
            },
            True,
        ),  # closed
        (
            {
                "hidden": "0",
                "status": "open",
                "academic_units": [{"refid": "AU_ILLUS"}],
            },
            True,
        ),  # open
        (
            {
                "hidden": "0",
                "status": "waitlist",
                "academic_units": [{"refid": "AU_FASHN"}],
            },
            True,
        ),  # waitlist
        (
            {
                "hidden": "1",
                "status": "waitlist",
                "academic_units": [{"refid": "AU_FASHN"}],
            },
            False,
        ),  # hidden
        (
            {
                "hidden": "0",
                "status": "preliminary",
                "academic_units": [{"refid": "AU_WRLIT"}],
            },
            False,
        ),  # preliminary
        (
            {
                "hidden": "0",
                "status": "open",
                "academic_units": [{"refid": "AU_EXTED"}],
            },
            False,
        ),  # extension
        (
            {"hidden": "0", "status": "open", "academic_units": [{"refid": "AU_CCA"}]},
            False,
        ),  # oddity
        (
            {
                "hidden": "0",
                "status": "open",
                "academic_units": [{"refid": "AU_PRECO"}],
            },
            False,
        ),  # pre-college
    ],
)
def test_on_portal(section, result):
    assert on_portal(section) == result


def test_cli(capsys):
    main(shlex.split("test/test.csv"))
    captured = capsys.readouterr()
    print(captured)
    assert "3 courses have syllabi of 3 total in the CSV" in captured.out
    assert captured.err == ""
    main(shlex.split("test/test.csv --csv"))
    csvfile = f"{date.today().isoformat()}-missing-syllabi.csv"
    assert os.path.exists(csvfile)
    # should be 1 header row + 3 data rows
    assert len(open(csvfile).readlines()) == 4
    os.remove(csvfile)
