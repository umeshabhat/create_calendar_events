# Create Google Calendar Events from ICS


## How to Run

1. Set up a Google Cloud Project
    1. Go to the Google Cloud Console.
    2. Create a new project or select an existing one.
    - Link: https://console.cloud.google.com
2. Enable the Google Calendar API
    1. In your project, navigate to "APIs & Services" > "Library".
    2. Search for "Google Calendar API" and enable it.
    - Link: https://console.cloud.google.com/apis/library/calendar-json.googleapis.com
3. Create Credentials
    1. Go to "APIs & Services" > "Credentials".
    2. Click "Create Credentials" > "OAuth client ID".
    3. Choose `Desktop App` for the application type and give it a name (say, _Desktop Application_).
    4. Give it a name (say, _Create Calendar Events_).
    5. Click "Create".
    - Link: https://console.cloud.google.com/auth/overview
    - Link: https://console.cloud.google.com/auth/clients/create
4. Download credentials.json
    1. A screen will appear with your new client ID and client secret.
    2. Click "Download JSON".
    3. Save this file as credentials.json in your project directory.
5. Generate token.json
    ```bash
    python3 generate_token.py
    ```
6. Install Prerequisites
    ```bash
    sudo apt install pipx
    pipx install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
    ```
    OR
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
    python3 create_calendar_events.py
    ```
7. Run the program
    ### Ubuntu (WSL)
    ```bash
    python3 -m venv ./venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
    ```
    ### Windows Powershell
    ```bash
    python -m venv venv_ps
    .\venv_ps\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog icalendar
    python .\generate_token.py
    python .\create_calendar_events.py
    ### Sample Output
    ### Enter the folder path to monitor: C:\Users\xerac\Downloads
    ### Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?XXXX
    ```
## References
- https://developers.google.com/calendar/api/v3/reference/events