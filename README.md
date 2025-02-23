# Create Google Calendar Events from ICS

## Prerequisites

```bash
python3 -m venv env
source env/bin/activate
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
```

You need these files to access Google Calendar API. Here's a breakdown of how to obtain credentials.json and token.json:

1. Set up a Google Cloud Project

    Go to the Google Cloud Console.
    Create a new project or select an existing one.

2. Enable the Google Calendar API

    In your project, navigate to "APIs & Services" > "Library".
    Search for "Google Calendar API" and enable it.

3. Create Credentials

    Go to "APIs & Services" > "Credentials".
    Click "Create Credentials" > "OAuth client ID".
    Choose "Desktop app" as the application type.
    Give it a name (e.g., "My Calendar App").
    Click "Create".

4. Download credentials.json

    A screen will appear with your new client ID and client secret.
    Click "Download JSON".
    Save this file as credentials.json in your project directory.

5. Generate token.json

    This is where things get a bit more technical, as you'll need to write some code to generate the token.json. Here's a basic Python example using the Google Calendar API client library:

    ```python
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import os.path
    import pickle

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def main():
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
    ```

This code does the following:

Sets up the necessary libraries.
Defines the scopes your application needs (in this case, read-only access to the calendar).
Checks for an existing token.json file.
If no token.json exists or it's invalid:
Initiates an OAuth flow. This will open a browser window asking the user to grant your application access to their calendar.
Saves the generated token in token.json.

Important Notes:

Security: Keep your credentials.json and token.json files safe. Never commit them to public repositories.
Scopes: Request only the necessary scopes for your application to minimize security risks.
Refresh tokens: The token.json contains refresh tokens that allow your application to continue accessing the user's calendar without requiring them to re-authorize every time.
This process might seem a bit involved at first, but it's crucial for secure access to Google Calendar data. Once you have these files, you can use the Google Calendar API to interact with calendars programmatically. If you have any more questions, feel free to ask!# create_calendar_events

### References
- https://developers.google.com/calendar/api/v3/reference/events