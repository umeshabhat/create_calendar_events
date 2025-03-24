from __future__ import print_function
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def check_credentials_file():
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json file not found. Please make sure it's in the same directory as this script.")
        return False

    if os.path.getsize('credentials.json') == 0:
        print("Error: credentials.json file is empty. Please ensure it contains valid credentials.")
        return False

    try:
        with open('credentials.json', 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        print("Error: credentials.json file is not valid JSON. Please check its contents.")
        return False

    return True
def main():
    if not check_credentials_file():
        return
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except json.JSONDecodeError:
            print("Existing token.json is invalid. Recreating...")
            os.remove('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"An error occurred during authorization: {e}")
                return
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        print('Token generated successfully.')
        # You can add a test API call here if you want to verify the connection
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        print(f"Connection successful. Found {len(events_result.get('items', []))} events.")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()

