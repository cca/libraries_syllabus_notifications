from __future__ import print_function
import os
import smtplib  # https://docs.python.org/2/library/email-examples.html
from sys import stderr

from_address = 'thaakenson@cca.edu'
from_name = 'Thomas Haakenson'
reply_address = 'ephetteplace@cca.edu'
reply_name = 'Eric Phetteplace'
list_item = '\n\t- '
signature = """\
Dr. Thomas O. Haakenson
Associate Provost
Faculty, Visual Studies
California College of the Arts

"Birth astride of a grave, the light gleams an instant, then it's night once more." (Samuel Beckett)

See Also: Provost / Associate Provost / Director of Academic Administration Division of Responsibilities

Pronouns: he, him

Academic Year 2015-2016 Location Schedule:
- Mondays and Fridays: Oakland Campus
- Tuesdays, Wednesdays, and Thursdays: SF Campus

Mailing Address:
5212 Broadway
Oakland, California, U.S.A. 94618-1426

Email: thaakenson@cca.edu
Office Phone: 510.594.3655
Cellphone: 651.894.2894

Vice President, Fulbright Alumni Association, Northern California Chapter
Series Editors, German Visual Culture, Peter Lang Oxford
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

Happy beginning of the semester! We are expecting syllabi from the following courses to be uploaded to VAULT by Friday, January 27th:
%s

Note that, for team taught sections, only one person needs to contribute the syllabus. Uncertain how to submit to VAULT? Follow these simple steps:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA user name
\t3. Upload your PDF syllabus file by clicking "Add a resource"
\t4. Select your course section by clicking "Select terms"
\t5. Click on "Save" and then "Publish"

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload.gif

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

%s

""" % email_values

    # 2nd reminder, sent a few days after deadline
    followup = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Reminder: Submit Your Syllabi to VAULT

Hello %s,

The deadline for submitting your syllabi to VAULT has passed and we show the following sections as missing:
%s

Please contribute these to VAULT at your earliest convenience. If you're uncertain how to submit to VAULT, follow these steps for each of your sections:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA user name
\t3. Add a PDF syllabus first by clicking "Add a resource", using the "Browse" button to find the file, and then the "Next" and "Save" buttons in the bottom right to upload it
\t4. Next, select your course section by clicking "Select terms" under "Course Information"
\t\tTo do this, browse down from the semester (e.g. Spring 2016)
\t\t...all the way to your specific section (e.g. ARTED-101-01)
\t\t...and click the word "Select" beside your section's number
\t5. Finally, click the green "Save" button and then the green "Publish" button

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload.gif

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

This is the last reminder that one syllabus for each section you instruct is needed in VAULT. If you are struggling to upload your syllabus, please contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus). If another section's syllabus is supposed to act as your own, you still need to notify the library. Unfortunately, it's not possible to determine when one syllabus serves multiple sections, thus why you are receiving this reminder.

Here are detailed instructions on uploading to VAULT:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA user name
\t3. Upload a PDF syllabus first by clicking the green "Add a resource" button
\t\t...click "Browse" or the "Drag & Drop" box to find your syllabus on your computer
\t\t...a green bar will indicate when the file upload completes
\t\t...in the bottom right, click the gray "Next" button
\t\t...and then the green "Save" button to return to the form
\t4. Add your course section by clicking "Select terms" under "Course Information"
\t\t...browse down from the semester (e.g. "Spring 2016")
\t\t...all the way to your specific section (e.g. "ARTED-101-01")
\t\t...and click the word "Select" beside your section's number
\t\t...the green "OK" button in the bottom right returns you to the form
\t5. Finally, click the green "Save" button and then the green "Publish" button
\t\tIf successful, you are taken to an item summary page displaying your course's details

This animation demonstrates the complete process from start to finish: https://vault.cca.edu/file/4eb14fb4-1b10-4527-914c-85610df0fb61/1/syllabus-upload.gif

----------

%s

""" % email_values

    # send it, defaulting to localhost server if none passed in
    if server is None and debug is False:
        server = smtplib.SMTP('localhost')
        server_was_set = True
    else:
        server_was_set = False

    # choose which template to use
    if msg_type == 'final':
        msg = final
    elif msg_type == 'followup':
        msg = followup
    else:
        msg = initial

    if debug is False:
        server.sendmail(reply_address, username + '@cca.edu', msg)
    else:
        print('DEBUGGING MODE: email not sent')
        print('Email that would have been sent to %s@cca.edu:\n' % username)
        print(msg)

    if server_was_set is True:
        server.quit()

    return True
