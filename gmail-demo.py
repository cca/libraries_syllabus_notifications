import base64
import os.path

from email.message import EmailMessage

import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_with_gmail():
    """Authenticate with Gmail API, based on example here:
    https://developers.google.com/gmail/api/quickstart/python
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def gmail_send_message(creds):
    """ Create and send an email message
    Prints the returned message info

    Args:
        creds (Credentials): Google API credentials

    Returns:
        Object: message object
    """
    # Load pre-authorized user credentials from the environment.
    if not creds:
        creds, _ = google.auth.default()

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message['To'] = 'vault@cca.edu'
        message['Reply-To'] = 'ephetteplace@cca.edu'
        message['From'] = 'dtracy@cca.edu'
        message['Subject'] = 'Test email with Gmail API'
        message.set_content('Test email body content')

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(send_message)
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    creds = authenticate_with_gmail()
    gmail_send_message(creds)
