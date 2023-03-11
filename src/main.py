#!/usr/bin/env python3

import requests
import json
import sys
import os.path
from datetime import date, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def assign_parameters(start, end):
    parameters = {
        "format": "json",
        "start": start,
        "end": end,
    }
    return parameters


def json_print(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def print_usage():
    print("\tUSAGE: ",
          "\t\tmain.py [COOKIE]",
          "\t\t[COOKIE] : your cookie connection to retrieve on "
          "https://intra.epitech.eu",
          sep='\n')


def parse_json(res):
    events = []
    for item in res:
        if item["event_registered"]:
            event = {
                'summary': '[' + item["titlemodule"] + '] ' + item[
                    "acti_title"],
                'location': item["room"]["code"].split('/')[-1]
                if item["room"] is not None
                and item["room"].get("code") is not None else None,
                'start': {
                    'dateTime': item["start"].replace(' ', 'T') + '.000+01:00'
                },
                'end': {
                    'dateTime': item["end"].replace(' ', 'T') + '.000+01:00'
                }
            }
            events.append(event)

    return events


def check_id(conn):
    if os.path.exists('data.json'):
        f = open("data.json", "r")
        id_json = json.loads(f.read())
    else :
        calendar = {
            'summary': 'Epitech',
            'timeZone': 'Europe/Paris'
        }
        created_calendar = conn.calendars().insert(body=calendar).execute()
        f = open("data.json", "w")
        id_json = {
            'id': created_calendar['id']
        }
        f.write(json.dumps(id_json))
    f.close()
    return id_json


def google_connection():
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
    service = build('calendar', 'v3', credentials=creds)
    return service


def is_in_list(items, events):
    for event in events:
        if event["summary"] == items["summary"]:
            return True
    return False


def remove_events_epicalendar(calendar_id, conn, epicalendar, start):
    start_date = str(start) + 'T00:00:00Z'
    end_date = str(start + timedelta(days=31 * 2)) + 'T23:59:59Z'
    events = conn.events().list(calendarId=calendar_id, timeMin=start_date,
                                timeMax=end_date).execute()
    new_calendar = []
    if len(events["items"]) != 0:
        for items in epicalendar:
            if not is_in_list(items, events["items"]):
                new_calendar.append(items)
        return new_calendar
    else:
        return epicalendar


def add_events_to_google(calendar_id, conn, epicalendar):
    for event in epicalendar:
        conn.events().insert(calendarId=calendar_id, body=event).execute()


def main():
    connection = google_connection()
    cookie = sys.argv[1]
    calendar_id = check_id(connection)
    while True:
        start_date = date.today()
        end_date = start_date + timedelta(days=31 * 2)
        jar = requests.cookies.RequestsCookieJar()
        jar.set("user", cookie, domain="intra.epitech.eu", path="/")
        try:
            response = requests.post("https://intra.epitech.eu/planning/load",
                                     params=assign_parameters(start_date, end_date),
                                     cookies=jar)
            response.raise_for_status()
            calendar = remove_events_epicalendar(calendar_id["id"], connection,
                                                 parse_json(response.json()),
                                                 start_date)
            add_events_to_google(calendar_id["id"], connection, calendar)

        except requests.exceptions.HTTPError as error:
            print(error, file=sys.stderr)
            raise SystemExit(error)
        except requests.exceptions.RequestException as error:
            print(error, file=sys.stderr)
            raise SystemExit(error)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print_usage()
        exit(0)
    if len(sys.argv) != 2:
        print(f"Wrong arguments. Run {sys.argv[0]} -h to see usage")
        exit(84)
    main()

