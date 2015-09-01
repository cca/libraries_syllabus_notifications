def has_syllabus (row):
    """
    Some courses, mostly Independent Study & Graduate Studio Practice, don't
    have syllabi & we don't want to annoy faculty asking for one. This fn takes
    a course, checks it against several possible attributes of courses that do
    not have syllabi, & returns False if it looks like a non-syllabus course.
    """
    if row['title'] in ('Independent Study', 'Graduate Studio Practice', 'Mentored Study'):
        return False

    coursenum = int(row['course'].split('-')[1])

    # (3|6)96 -> (Under)grad independent study
    # (3|6)98 -> (Under)grad internship
    if coursenum in (698, 398, 396, 696):
        return False

    # FINAR-660 is Graduate Studio Practice, no syllabus
    # WRITE-660 is Mentored Study which submits inidividual contracts
    # both of these should be caught above but just in case
    if row['course'] in ('FINAR-660', 'WRITE-660'):
        return False

    # fallthrough; nothing else fired so it must have a syllabus
    return True
