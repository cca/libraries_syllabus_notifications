import smtplib
from sys import stderr

from_address = 'ephetteplace@cca.edu'
from_name = 'Eric Phetteplace'
list_item = '\n\t- '


def notify(name, username, courses):
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

    # create formatted email
    msg = """\
From: %s <%s>
Reply-To: %s <%s>
To: %s <%s>
Subject: Submitting Syllabi to VAULT

Hello %s,

Happy beginning of the academic year! We are expecting syllabi from the following courses to be uploaded to VAULT:
%s

Note that, for team taught sections, only one person needs to contribute the syllabus. Uncertain how to submit to VAULT? Follow these simple steps:

\t1. Visit https://vault.cca.edu/s/upload-syllabus
\t2. Sign in with your CCA user name
\t3. Upload your PDF syllabus file by clicking 'Add a resource'
\t4. Select your course section by clicking 'Select terms'
\t5. Click on 'Save' and then 'Publish'

Still struggling? Have questions? Feel free to get in touch with me.

Sincerely,
%s
Systems Librarian
California College of the Arts
510.594.3660 (ext. 3660 from campus)
""" % (
    from_name,
    from_address,
    # repeated twice for From: & Reply-To:
    from_name,
    from_address,
    name,
    username + '@cca.edu',
    name,
    # format course list into list like:
    # - blah blah
    # - yada yada
    list_item + list_item.join(courses),
    from_name
)
    
    # send it
    server = smtplib.SMTP('localhost')
    # 2nd parameter must be a _list_ of recipients
    server.sendmail('from_address', [username + '@cca.edu'], msg)
    server.quit()
    return True
