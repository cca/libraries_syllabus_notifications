from __future__ import print_function
import os
import smtplib  # https://docs.python.org/2/library/email-examples.html
from sys import stderr

from_address = 'dtracy@cca.edu'
from_name = 'Dominick Tracy'
reply_address = 'ephetteplace@cca.edu'
reply_name = 'Eric Phetteplace'
list_item = '\n\t- '
signature = """\

DOMINICK TRACY
Director of Learning Assessment & Accreditation
Deputy Title IX Coordinator for Faculty
Academic Affairs

dtracy@cca.edu | o 510.594.3794




5212 Broadway | Oakland | CA | 94618
"""
debug = bool(os.environ.get('DEBUG'))


def notify(name, username, courses, server, msg_type='initial'):
    """
    Send an email to name <username@cca.edu> notifying them
    that we expect a list of courses to have syllabi uploaded to VAULT
    with handy contact and help information in the email template
    """

    # in a few edge cases we'll not have a faculty username
    # e.g. returning faculty with expired email, new faculty with unactivated email
    # see email thread from Lydia on 8/21/15
    if username is None:
        stderr.write('No username for %s, courses:%s\n' % (
            name,
            list_item + list_item.join(courses)
        ))
        return False

    # these are filled into the templates below
    # ordering is important
    email_values = (
        from_name,
        from_address,
        reply_name,
        reply_address,
        name,
        username + '@cca.edu',
        name,
        # format course list into list like:
        # - blah blah
        # - yada yada
        list_item + list_item.join(courses),
        reply_name,
        reply_address,
        signature,
    )

    # initial email template, sent towards beginning of semester
    # @TODO update the due date here each semester
    initial = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Submitting Syllabi to VAULT

Hello %s,

Happy beginning of the semester! We are expecting syllabi from the following courses to be uploaded to VAULT by Friday, February 8th:
%s

Note that, for team taught sections, only one person needs to contribute the syllabus. Uncertain how to submit to VAULT? Follow these simple steps:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Upload your PDF syllabus into the dotted box
\t4. Select your course section by clicking "Select terms"
\t5. Click on "Save" and then "Publish"

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

%s

""" % email_values

    # 2nd reminder, note we've sent this _after_ the deadline in the past
    followup = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Reminder: Submit Your Syllabi to VAULT

Hello %s,

The deadline for submitting your syllabi to VAULT is February 8th. We show the following sections as missing:
%s

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

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

%s

""" % email_values

    # final (2nd) reminder to turn in syllabi
    final = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Last Reminder: Submit Your Syllabi to VAULT

Hello %s,

VAULT is still missing syllabi from the following sections:
%s

This is the last reminder that one syllabus for each section you instruct is needed in VAULT. If you are struggling to upload your syllabus, please contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus). If another section's syllabus is supposed to act as your own, you still need to notify the library. Unfortunately, it's not possible to determine when one syllabus serves multiple sections.

Here are detailed instructions on uploading to VAULT:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA username
\t3. Upload a PDF syllabus by clicking where it says "Click to select files or drag and drop files here"
\t4. Add your course section by clicking "Select terms" under "Course Information"
\t\t...browse down from the semester (e.g. "Spring 2018")
\t\t...all the way to your specific section (e.g. "ARTED-101-01")
\t\t...and click the word "Select" beside your section's number
\t\t...the green "OK" button in the bottom right returns you to the form
\t5. Finally, click the green "Save" button and then the green "Publish" button

If successful, you will see a summary page displaying your course's details. This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload(2).gif

----------

%s

""" % email_values

    # summer courses have varied start dates so we don't reference a strict due date
    summer = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Reminder: Submit Your Syllabi to VAULT

Hello %s,

A friendly reminder that we anticipate syllabi for the following section(s) to be uploaded to VAULT:
%s

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

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

%s

""" % email_values

    # send it, defaulting to localhost server if none passed in
    if server is None and debug is False:
        server = smtplib.SMTP('localhost')
        server_was_set = True
    else:
        server_was_set = False

    # select the template to use
    msg = locals()[msg_type]

    if debug is False:
        server.sendmail(reply_address, username + '@cca.edu', msg)
    else:
        print('DEBUGGING MODE: email not sent')
        print('Email that would have been sent to %s@cca.edu:\n' % username)
        print(msg)

    if server_was_set is True:
        server.quit()

    return True
