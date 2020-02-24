from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.


def add_note(data, row, List, SAMPLE_SPREADSHEET_ID):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    print('started')
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if os.path.exists('VKBot/token.pickle'):
        with open('VKBot/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    data = {'values' : [
                        tuple(str(x) for x in data)
                        ]}

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range = List + '!A' + str(int(row) + 1),
        body = data,
        valueInputOption = 'RAW'
    ).execute()
    print('done')
