import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import icalendar
import threading

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Shows basic usage of the Google Calendar API."""
    try:
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    except Exception as e:
        print(f"Error during Google Calendar authentication: {e}")
        return None

def create_event(service, event):
    """Create an event in Google Calendar."""
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating event: {e}")

def parse_ics_file(file_path):
    """Parse the .ics file and return event data."""
    try:
        with open(file_path, 'rb') as f:
            calendar = icalendar.Calendar.from_ical(f.read())
            for component in calendar.walk():
                if component.name == "VEVENT":
                    event = {
                        'summary': "Event - " + component.get('summary'),
                        'start': {
                            'dateTime': component.get('dtstart').dt.isoformat(),
                            'timeZone': 'UTC',
                        },
                        'end': {
                            'dateTime': component.get('dtend').dt.isoformat(),
                            'timeZone': 'UTC',
                        },
                    }
                    return event
    except Exception as e:
        print(f"Error parsing .ics file {file_path}: {e}")
    return None

def prompt_delete_file(file_path):
    """Prompt the user to delete the file with a timeout."""
    def input_with_timeout(prompt, timeout):
        print(prompt, end='', flush=True)
        result = [None]
        def get_input():
            result[0] = input()
        thread = threading.Thread(target=get_input)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print("\nNo response, continuing without deleting the file.")
            return 'n'
        return result[0]

    response = input_with_timeout(f"Do you want to delete the file {file_path} after importing? (y/n): ", 180)
    if response.lower() == 'y':
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted.")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

class IcsFileHandler(FileSystemEventHandler):
    def __init__(self, service):
        self.service = service

    def on_created(self, event):
        print(f"Event detected: {event.src_path}")
        if event.is_directory:
            return
        if event.src_path.endswith('.ics'):
            print(f"New .ics file detected: {event.src_path}")
            event_data = parse_ics_file(event.src_path)
            if event_data:
                create_event(self.service, event_data)
                prompt_delete_file(event.src_path)

def process_existing_files(service, folder_path):
    """Process existing .ics files in the directory."""
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.ics'):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing existing .ics file: {file_path}")
                event_data = parse_ics_file(file_path)
                if event_data:
                    create_event(service, event_data)
                    prompt_delete_file(file_path)
    except Exception as e:
        print(f"Error processing existing files in {folder_path}: {e}")

class IcsFileHandler(FileSystemEventHandler):
    def __init__(self, service):
        self.service = service

    def on_created(self, event):
        print(f"Event detected: {event.src_path}")
        if event.is_directory:
            return
        if event.src_path.endswith('.ics'):
            print(f"New .ics file detected: {event.src_path}")
            event_data = parse_ics_file(event.src_path)
            if event_data:
                create_event(self.service, event_data)
                prompt_delete_file(event.src_path)

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")
        # Handle any additional logic if needed when a file is deleted

def monitor_folder(folder_path):
    creds = authenticate_google_calendar()
    if not creds:
        print("Failed to authenticate with Google Calendar. Exiting.")
        return

    service = build('calendar', 'v3', credentials=creds)

    # Process existing .ics files
    process_existing_files(service, folder_path)

    event_handler = IcsFileHandler(service)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    print(f"Monitoring folder: {folder_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(f"Error during folder monitoring: {e}")
    finally:
        observer.join()

if __name__ == "__main__":
    try:
        folder_to_monitor = input("Enter the folder path to monitor: ")
        if not os.path.isdir(folder_to_monitor):
            print(f"The path {folder_to_monitor} is not a valid directory.")
        else:
            monitor_folder(folder_to_monitor)
    except Exception as e:
        print(f"Error in main execution: {e}")