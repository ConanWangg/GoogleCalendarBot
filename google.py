import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define your Google Calendar scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    # Check if there are existing credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(service, summary, start_datetime, end_datetime):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/New York',
        },
        'end': {
            'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/New York',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def main():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    summary = input("Enter event summary: ")
    start_datetime = input("Enter start date and time (YYYY-MM-DD HH:MM): ")
    end_datetime = input("Enter end date and time (YYYY-MM-DD HH:MM): ")

    start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
    end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M")

    create_event(service, summary, start_datetime, end_datetime)

if __name__ == '__main__':
    main()
