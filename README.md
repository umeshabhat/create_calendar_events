# Create Google Calendar Events from ICS

## Run the program

### Ubuntu (WSL)

```bash
python3 -m venv ./venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
```

### Powershell

```bash
python -m venv venv_ps
.\venv_ps\Scripts\activate
python -m pip install --upgrade pip
python -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
python .\generate_token.py
python .\create_calendar_events.py
### Enter the folder path to monitor: C:\Users\xerac\Downloads

###
### Enter the folder path to monitor: C:\Users\xerac\Downloads
###Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=792218771561-u1ua5o3v8heghd1hdph703vmahra8r5f.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A52587%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&state=WNYdy2ImwmWRBqoeae9mnkSyxlI65j&access_type=offline
####
```


#### Trials [BROKEN]

```bash
sudo apt install pipx
pipx install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
```

```bash
python3 -m venv env
source env/bin/activate
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
python3 create_calendar_events.py
```

```bash
sudo apt-get remove pip
sudo apt-get remove pip3
sudo apt-get purge pip
sudo apt-get purge pip3
sudo apt-get remove python-setuptools
sudo apt-get remove python3-setuptools

python3 -m pip uninstall pip setuptools
sudo python -m pip uninstall pip
sudo python3 -m pip uninstall pip
```

#### Running

```bash
python3 generate_token.py
```

## Notes

You need these files to access Google Calendar API. Here's a breakdown of how to obtain credentials.json and token.json:

1. Set up a Google Cloud Project

    Go to the Google Cloud Console.
    Create a new project or select an existing one.

2. Enable the Google Calendar API

    In your project, navigate to "APIs & Services" > "Library".
    Search for "Google Calendar API" and enable it.

    Link: https://console.cloud.google.com/apis/library/calendar-json.googleapis.com

3. Create Credentials

    Go to "APIs & Services" > "Credentials".
    Click "Create Credentials" > "OAuth client ID".
    Choose `Desktop App` for the application type and give it a name (say, _Desktop Application_).    
    Give it a name (say, _Create Calendar Events_).
    Click "Create".

    Link: https://console.cloud.google.com/auth/overview
    Link: https://console.cloud.google.com/auth/clients/create

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