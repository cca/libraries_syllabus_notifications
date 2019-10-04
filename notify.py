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
        'due_date': 'Friday, September 27th',
        'from_name': 'Dominick Tracy',
        'from_address': 'dtracy@cca.edu',
        'reply_name': 'Eric Phetteplace',
        'reply_address': 'ephetteplace@cca.edu',
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
Subject: Submitting Syllabi to VAULT

Hello {name},

Happy beginning of the semester! We are expecting syllabi from the following courses to be uploaded to VAULT by {due_date}:
{courses}

Note that, for team taught sections, only one person needs to contribute the syllabus. Uncertain how to submit to VAULT? Follow these simple steps:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Upload your PDF syllabus into the dotted box
\t4. Select your course section by clicking "Select terms"
\t5. Click on "Save" and then "Publish"

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, {reply_name} at {reply_address} or 510.594.3660 (ext. 3660 from campus).

----------

{signature}

""".format(**email_values)

    # 2nd reminder
    followup = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Submitting Syllabi to VAULT

Hello {name},

The deadline for submitting your syllabi to VAULT is {due_date}. We show the following sections as missing:
{courses}

Please contribute these to VAULT at your earliest convenience. If you're uncertain how to submit to VAULT, follow these steps for *each* of your sections:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Add a PDF syllabus first by clicking in the dotted box and finding the file, or dropping it directly onto the box
\t4. Next, select your course section by clicking "Select terms" under "Course Information"
\t\tTo do this, browse down from the semester (e.g. "Spring 2018")
\t\t...all the way to your specific section (e.g. ARTED-101-01)
\t\t...and click the word "Select" beside your section's number
\t5. Finally, click the green "Save" button and then the green "Publish" button

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, {reply_name} at {reply_address} or 510.594.3660 (ext. 3660 from campus).

----------

{signature}

""".format(**email_values)

    # final (2nd) reminder to turn in syllabi
    final = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Submitting Syllabi to VAULT

Hello {name},

VAULT is still missing syllabi from the following sections:
{courses}

This is the last reminder that one syllabus for each section you instruct is needed in VAULT. If you are struggling to upload your syllabus, please contact CCA's Systems Librarian, {reply_name} at {reply_address} or 510.594.3660 (ext. 3660 from campus). If another section's syllabus is supposed to act as your own, you still need to notify the library. Unfortunately, it's not possible to determine when one syllabus serves multiple sections.

Here are detailed instructions on uploading to VAULT:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Upload a PDF syllabus by clicking where it says "Click to select files or drag and drop files here"
\t4. Add your course section by clicking "Select terms" under "Course Information"
\t\t...browse down from the semester (e.g. "Fall 2019")
\t\t...all the way to your specific section (e.g. "ARTED-101-01")
\t\t...and click the word "Select" beside your section's number
\t\t...the green "OK" button in the bottom right returns you to the form
\t5. Finally, click the green "Save" button and then the green "Publish" button

If successful, you will see a summary page displaying your course's details. This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

----------

{signature}

""".format(**email_values)

    # summer courses have varied start dates so we don't reference a strict due date
    summer = """\
From: {from_name} <{from_address}>
Reply-To: {reply_name} <{reply_address}>
To: {name} <{email}>
Subject: Reminder: Submit Your Syllabi to VAULT

Hello {name},

A friendly reminder that we anticipate syllabi for the following section(s) to be uploaded to VAULT:
{courses}

Please contribute these to VAULT at your earliest convenience. We realize summer courses have varied schedules and may not have started yet.

If you're uncertain how to submit to VAULT, follow these steps for *each* of your sections:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Add a PDF syllabus first by clicking in the dotted box and finding the file, or dropping it directly onto the box
\t4. Next, select your course section by clicking "Select terms" under "Course Information"
\t\tTo do this, browse down from the semester (e.g. "Summer 2018")
\t\t...all the way to your specific section (e.g. ARTED-101-01)
\t\t...and click the word "Select" beside your section's number
\t5. Finally, click the green "Save" button and then the green "Publish" button

This animation demonstrates the process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, {reply_name} at {reply_address} or 510.594.3660 (ext. 3660 from campus).

----------

%s

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
