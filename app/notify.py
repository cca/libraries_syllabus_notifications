import os
import smtplib

from config import logger

debug = bool(os.environ.get('DEBUG'))


def notify(name, username, courses, server, msg_type='initial'):
    """
    Send an email to name <username@cca.edu> notifying them
    that we expect a list of courses to have syllabi uploaded to VAULT
    with handy contact and help information in the email template
    """
    list_item = '\n\t- '
    # these are filled into the templates below
    email_values = {
        # @TODO update the due date here each semester
        'due_date': 'Friday, February 14th',
        'from_name': 'Dominick Tracy',
        'from_address': 'dtracy@cca.edu',
        'reply_name': 'Eric Phetteplace',
        'reply_address': 'ephetteplace@cca.edu',
        'reply_phone': '510.594.3660 (ext. 3660 from campus)',
        'name': name,
        'email': username + '@cca.edu',
        'courses': list_item + list_item.join(courses),
        'signature': """\

        DOMINICK TRACY
        Director of Learning Assessment & Accreditation
        Deputy Title IX Coordinator for Faculty
        Academic Affairs

        dtracy@cca.edu | o 510.594.3794

        5212 Broadway | Oakland | CA | 94618
        """,
    }

    # initial email template, sent towards beginning of semester
    initial = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Submitting Syllabi to Portal

Hello {name},

Happy beginning of the semester! We expect syllabi from the following courses to be added to the Portal by {due_date}:
{courses}

Note that, for team taught sections, only one person needs to submit the syllabus. Uncertain how to submit? Follow these simple steps:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your sections under the "My Classes" list on the home page
\t3. Select a section, then **Edit** and **Upload Syllabus**
\t4. Use **Choose File** to find your syllabus PDF, then **Upload Syllabus** finishes the process

Here is the full documentation on the new Portal Course Section Pages: https://portal.cca.edu/teaching/academic-affairs/faculty-resources/course-section-pages-portal-faculty/

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}.

----------

{signature}

""".format(**email_values)

    # 2nd reminder
    followup = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {name},

The deadline for submitting your syllabi is {due_date}. We show the following sections as needing syllabi:
{courses}

Please contribute these to the Portal at your earliest convenience. If you're uncertain how to, follow these steps for **each** of your classes:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your class under the "My Classes" list on the home page
\t3. Select the class, on its page press **Edit** and then **Upload Syllabus**
\t4. Use **Choose File** to browse to your syllabus PDF
\t5. Press **Upload Syllabus** to complete the process

Here is the full documentation on the new Portal Course Section Pages: https://portal.cca.edu/teaching/academic-affairs/faculty-resources/course-section-pages-portal-faculty/

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}.

----------

{signature}

""".format(**email_values)

    # final (2nd) reminder to turn in syllabi
    final = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {name},

The Portal is still missing syllabi from the following sections:
{courses}

This is the last reminder that one syllabus for each section you instruct is needed. If you are struggling to upload your syllabus, please contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}. If another section's syllabus is supposed to act as your own, you still need to submit it on the Portal. Unfortunately, it's not possible to determine when one syllabus serves multiple sections.

Here are detailed instructions on uploading to VAULT:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Select one of your classes under the "My Classes" list on the home page
\t3. Press the **Edit** button below the course description
\t4. Select the **Upload Syllabus** button
\t5. Use the **Choose File** button to locate your syllabus PDF on your hard drive
\t\ta. If you do not have a PDF copy of your syllabus, you will need to create one.
\t\tb. If you don't know how to create a PDF copy, contact the Help Desk at helpdesk@cca.edu
\t6. Press **Upload Syllabus** to complete the process
\t7. Repeat this process for all classes with missing syllabi

Here is the full documentation on the new Portal Course Section Pages: https://portal.cca.edu/teaching/academic-affairs/faculty-resources/course-section-pages-portal-faculty/

----------

{signature}

""".format(**email_values)

    # summer courses have varied start dates so we don't reference a strict due date
    summer = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {name},

A friendly reminder that we anticipate syllabi for the following section(s) to be uploaded to Portal:
{courses}

Please upload these at your earliest convenience. We realize summer courses have varied schedules and may not have started yet. If you're uncertain how to submit, follow these steps for *each* of your sections:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your classes under the "My Classes" list on the home page
\t3. Select a class, on its page press **Edit** and then **Upload Syllabus**
\t4. Use **Choose File** to browse to your syllabus file
\t5. Press **Upload Syllabus** to complete the process

Here is the full documentation on the new Portal Course Section Pages: https://portal.cca.edu/teaching/academic-affairs/faculty-resources/course-section-pages-portal-faculty/

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}.

----------

%{signature}

""".format(**email_values)

    # send it, defaulting to localhost server if none passed in
    if server is None and debug is False:
        server = smtplib.SMTP('localhost')
        server_was_set = True
    else:
        server_was_set = False

    # select the template to use
    msg = locals()[msg_type]

    if debug:
        logger.debug('Email that would have been sent to {user}@cca.edu:\n{msg}'.format(user=username, msg=msg))
    else:
        server.sendmail(email_values["reply_address"], username + '@cca.edu', msg)

    if server_was_set is True:
        server.quit()

    return True
