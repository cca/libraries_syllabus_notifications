def has_syllabus (row):
    """
    Some courses, mostly Independent Study & Graduate Studio Practice, don't
    have syllabi & we don't want to annoy faculty asking for one. This fn takes
    a course, checks it against several possible attributes of courses that do
    not have syllabi, & returns False if it looks like a non-syllabus course.
    """
    if row['title'] == 'Independent Study' or row['title'] == 'Graduate Studio Practice':
        return False

    coursenum = int(row['course'].split('-')[1])

    # (3|6)96 -> (Under)grad independent study
    # (3|6)98 -> (Under)grad internship
    skipped_coursenums = (698, 398, 396, 696)

    if coursenum in skipped_coursenums:
        return False

    # FINAR-660 is Graduate Studio Practice, should be caught above but just in case
    if row['course'] == 'FINAR-660':
        return False

    # fallthrough; nothing else fired so it must have a syllabus
    return True
