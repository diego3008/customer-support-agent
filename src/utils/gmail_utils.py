import base64
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build 
import os

from state import Email

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify'
]

def _get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def _parse_email_message(message: str) -> Email:
    """
    Extracts email data from a Gmail API message resource.
    Returns a dict with id, subject, sender, date, and body.
    """
    headers_list = message.get('payload', {}).get('headers', [])
    headers = {header['name'].lower(): header['value'] for header in headers_list}
    subject = headers.get('subject', 'No Subject')
    sender = headers.get('from', 'No Sender')
    date = headers.get('date', 'No Date')
    message_id = headers.get('message-id', '')
    references = headers.get('references', '')
    body = ''
    payload = message.get('payload', {})
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                body = part.get('body', {}).get('data', '')
                break
    else:
        body = payload.get('body', {}).get('data', '')
    if body:
        try:
            body = base64.urlsafe_b64decode(body).decode('utf-8')
        except Exception:
            body = ''
    return Email(
        id=message["id"],
        subject=subject,
        sender=sender,
        date=date,
        body=body,
        message_id=message_id,
        references=references,
        thread_id=message['threadId']
    )

def get_most_recent_email() -> Email | str: 
    service = _get_gmail_service()
    today = datetime.datetime.now().date()
    query = f'after:{today.strftime("%Y/%m/%d")}' # after:18/07/2025
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        email_message_data = results.get('messages', [])[0]
        if not email_message_data:
            return ""
        message = service.users().messages().get(userId='me', id=email_message_data['id']).execute()
        return _parse_email_message(message=message)
    except Exception as error:
        print(f'An error occurred: {error}')
        return ""