import smtplib  # https://docs.python.org/2/library/email-examples.html
from sys import stderr

from_address = 'thaakenson@cca.edu'
from_name = 'Thomas Haakenson'
reply_address = 'ephetteplace@cca.edu'
reply_name = 'Eric Phetteplace'
list_item = '\n\t- '


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
    )

    # initial email template, sent towards beginning of semester
    initial = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Submitting Syllabi to VAULT

Hello %s,

Happy beginning of the academic year! We are expecting syllabi from the following courses to be uploaded to VAULT by Friday, September 11th:
%s

Note that, for team taught sections, only one person needs to contribute the syllabus. Uncertain how to submit to VAULT? Follow these simple steps:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA user name
\t3. Upload your PDF syllabus file by clicking 'Add a resource'
\t4. Select your course section by clicking 'Select terms'
\t5. Click on 'Save' and then 'Publish'

Still struggling? Have questions? Feel free to contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

Dr. Thomas O. Haakenson
Associate Provost
California College of the Arts

Mailing Address:
5212 Broadway
Oakland, California, U.S.A. 94618-1426

Email: thaakenson@cca.edu
Office Phone: 510.594.3655
Cellphone: 651.894.2894

Vice President, Fulbright Alumni Association, Northern California Chapter
Series Editors, German Visual Culture, Peter Lang Oxford
Co-Coordinator, Visual Culture Network, German Studies Association
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
\t3. Upload a PDF syllabus first by clicking 'Add a resource'
\t4. Next, select your course section by clicking 'Select terms' under 'Course Information'
\t\tTo do this, browse down from the semester (e.g. Fall 2015)
\t\t...all the way to your specific section (e.g. ARTED-101-01)
\t\t...and click word 'Select' beside your section's number
\t5. Finally, click the green 'Save' button and then the green 'Publish' button

If after the attempting the above steps you are still unable to upload your syllabus, you can contact CCA's Systems Librarian, %s at %s or 510.594.3660 (ext. 3660 from campus).

----------

Dr. Thomas O. Haakenson
Associate Provost
California College of the Arts

Mailing Address:
5212 Broadway
Oakland, California, U.S.A. 94618-1426

Email: thaakenson@cca.edu
Office Phone: 510.594.3655
Cellphone: 651.894.2894

Vice President, Fulbright Alumni Association, Northern California Chapter
Series Editors, German Visual Culture, Peter Lang Oxford
Co-Coordinator, Visual Culture Network, German Studies Association
""" % email_values

    # final (2nd) reminder to turn in syllabi, template TBD
    final = """\
"""  # % email_values

    # send it, defaulting to localhost server if none passed in
    if server is None:
        server = smtplib.SMTP('localhost')
        server_was_set = True
    else:
        server_was_set = False

    # choose which template to use
    if msg_type == 'initial':
        msg = initial
    elif msg_type == 'followup':
        msg = followup
    else:
        msg = final

    server.sendmail(reply_address, username + '@cca.edu', msg)

    if server_was_set is True:
        server.quit()

    return True
