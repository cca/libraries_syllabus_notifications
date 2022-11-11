import smtplib

from reminders.config import config, logger


def notify(name, username, courses, server, msg_type='initial'):
    """
    Send an email to name <username@cca.edu> notifying them
    that we expect a list of courses to have syllabi uploaded to Portal
    with handy contact and help information in the email template
    """
    list_item = '\n\t- '
    # these are filled into the templates below
    email_values = {
        # @TODO update the due date & email signature here each semester
        # as of 2021FA we don't specify a due date
        'due_date': None,
        'from_name': 'Dominick Tracy',
        'from_address': 'dtracy@cca.edu',
        'reply_name': 'Eric Phetteplace',
        'reply_address': 'ephetteplace@cca.edu',
        'reply_phone': '510.594.3660 (ext. 3660 from campus)',
        'to_name': name,
        'to_address': username + '@cca.edu',
        'courses': list_item + list_item.join(courses),
        'signature': """\

DOMINICK TRACY, Associate Provost for Educational Effectiveness
Chair, Upper-Division Interdisciplinary Studio Curriculum
Accreditation Liaison Officer (WSCUC)
Deputy Title IX Coordinator for Faculty
dtracy@cca.edu | o 510.594.3794

Pronouns: He/Him

CCA campuses are located in Huichin and Yelamu, also known as Oakland and San Francisco, on the unceded territories of Chochenyo and Ramaytush Ohlone peoples.""",
    }

    # initial email template, sent towards beginning of semester
    initial = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {to_name} <{to_address}>
Subject: Submitting Syllabi to Portal

Hello {to_name},

Happy beginning of the semester! We ask that you submit your syllabi to the Portal now. We expect syllabi from these courses:
{courses}

While your syllabus may continue to develop in the coming weeks, we ask that you submit an initial copy now. You can replace it later by following the same steps as below.

Uncertain how to submit? Follow these simple steps:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your sections under the "My Classes" list on the home page
\t3. Select a section, then **Edit** and **Upload Syllabus**
\t4. Use **Choose File** to find your syllabus PDF, then **Upload Syllabus** finishes the process

Read about setting up your Course Section Pages here: https://portal.cca.edu/knowledge-base/portal/set-up-your-course-section-page/

Note that, for team taught sections, only one person needs to submit.

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, {reply_name} at {reply_address}.

----------

{signature}

""".format(**email_values)

    # 2nd reminder
    followup = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {to_name} <{to_address}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {to_name},

The following sections need syllabi on Portal:
{courses}

Please upload soon. If you're uncertain how to, follow these steps for **each** of your classes:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your class under the "My Classes" list on the home page
\t3. Select the class, on its page press **Edit** and then **Upload Syllabus**
\t4. Use **Choose File** to browse to your syllabus PDF
\t5. Press **Upload Syllabus** to complete the process

Note that, for team taught sections, only one person needs to submit.

If after attempting the above steps you are still unable to upload, you can contact CCA's Systems Librarian, {reply_name} at {reply_address}.

----------

{signature}

""".format(**email_values)

    # final (2nd) reminder to turn in syllabi
    final = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {to_name} <{to_address}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {to_name},

The Portal is still missing syllabi from the following sections:
{courses}

This is the last reminder that one syllabus for each section you instruct is needed. If you are struggling to upload your syllabus, please contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}. If another section's syllabus is supposed to act as your own, you still need to submit it on the Portal. Unfortunately, it's not possible to determine when one syllabus serves multiple sections.

Here are detailed instructions on uploading to Portal:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Select one of your classes under the "My Classes" list on the home page
\t3. Press the **Edit** button below the course description
\t4. Select the **Upload Syllabus** button
\t5. Use the **Choose File** button to locate your syllabus PDF on your hard drive
\t\ta. If you do not have a PDF copy of your syllabus, you will need to create one.
\t\tb. If you don't know how to create a PDF copy, contact the Help Desk at helpdesk@cca.edu
\t6. Press **Upload Syllabus** to complete the process
\t7. Repeat this process for all classes with missing syllabi

Read about setting up your Course Section Pages here: https://portal.cca.edu/knowledge-base/portal/set-up-your-course-section-page/

----------

{signature}

""".format(**email_values)

    # summer courses have varied start dates so we don't reference a strict due date
    summer = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {to_name} <{to_address}>
Subject: Reminder: Submit Your Syllabi to Portal

Hello {to_name},

A friendly reminder that we anticipate syllabi for the following section(s) to be uploaded to Portal:
{courses}

Please upload these at your earliest convenience. We realize summer courses have varied schedules and may not have started yet. If you're uncertain how to submit, follow these steps for *each* of your sections:

\t1. Visit https://portal.cca.edu/login and log in
\t2. Find your classes under the "My Classes" list on the home page
\t3. Select a class, on its page press **Edit** and then **Upload Syllabus**
\t4. Use **Choose File** to browse to your syllabus file
\t5. Press **Upload Syllabus** to complete the process

Read about setting up your Course Section Pages here: https://portal.cca.edu/knowledge-base/portal/set-up-your-course-section-page/

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, {reply_name} at {reply_address} or {reply_phone}.

----------

{signature}

""".format(**email_values)

    # for sending a single message where app didn't define an SMTP server for us
    server_was_set = False
    if server is None and config['DEBUG'] is False:
        server = smtplib.SMTP(config['SMTP_DOMAIN'], port=config['SMTP_PORT'])
        server.login(config['SMTP_USER'], config['SMTP_PASSWORD'])
        server_was_set = True

    # select the template to use
    try:
        msg = locals()[msg_type]
    except KeyError:
        logger.error(f'Unrecognized message template "{msg_type}". \
            Please use one of initial, followup, final, or summer.')
        exit(1)

    if config['DEBUG']:
        logger.debug(f'Email that would have been sent to {username}@cca.edu:\n{msg}')
    else:
        server.sendmail(email_values['reply_address'], email_values['to_address'], msg)

    if server_was_set is True:
        server.quit()

    return True
