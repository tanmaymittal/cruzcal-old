from __future__ import print_function
from datetime import * 
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
from requests.api import head 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup as bs, element
import pandas as pd

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # print(pisa(44365))
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    more = True
    while more:
        # print('Do you want to add a class?')
        x = input('Do you want to add a class: Yes or No: ')
        if x.lower() != 'yes':
            more = False
            break
        class_number = int(input('Enter Class Number: '))
        
        className, meetingPlace, startDate, startTime, endTime, meetingDays, count = pisa(class_number)
        className = input('Enter Class Name: ')
        # className = 'PHIL 27'
        event = {
        'summary': f'{className}',
        'location' : f'{meetingPlace}',
        'start': {
            'dateTime': f'{startDate}T{startTime}:00',
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            # 'dateTime': '2021-10-3T16:30:00.000-07:00',
            'dateTime': f'{startDate}T{endTime}:00',
            'timeZone': 'America/Los_Angeles'
        },
        'recurrence': [
            f"RRULE:FREQ=WEEKLY;BYDAY={meetingDays};COUNT={count}"
        #                 
        ],
        }
        # print(event)
        event_one = service.events().insert(calendarId='primary', body=event).execute()
        print(event_one['summary'].encode('utf-8'), event_one['start']['dateTime'], event_one['end']['dateTime'])


def pisa(class_number): 
    headers = {
        'GET' : 'https://pisa.ucsc.edu/class_search/ HTTP/1.1', 
        'Host': 'pisa.ucsc.edu', 
        'Connection': 'keep-alive', 
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    class_payload = {
        'action': 'detail', 
        'class_data[:STRM]': '2220',
        'class_data[:CLASS_NBR]': f'{class_number}', # class number 
        'binds[:term]': '2220', # probably term number 
        'binds[:reg_status]': 'all',
        'binds[:subject]': '', 
        'binds[:catalog_nbr_op]': '=', 
        'binds[:catalog_nbr]': '', 
        'binds[:title]': '', 
        'binds[:instr_name_op]': '=', 
        'binds[:instructor]': '', 
        'binds[:ge]': '', 
        'binds[:crse_units_op]': '=', 
        'binds[:crse_units_from]': '', 
        'binds[:crse_units_to]': '',
        'binds[:crse_units_exact]': '', 
        'binds[:days]': '', 
        'binds[:times]': '', 
        'binds[:acad_career]': '', 
        'binds[:session_code]': '', 
        'rec_start': '0' , # dont know 
        'rec_dur': '25' # dont know 
    }
    search_url = "https://pisa.ucsc.edu/class_search/index.php"
    class_response = requests.post(search_url, headers=headers, verify=False, data=class_payload)
    # print(class_response.text)
    soup = bs(class_response.content, 'lxml')
    days = {
        'TuTh' : 'TU,TH',
        'MWF' : 'MO,WE,FR',
        'M': 'MO',
        'MW': 'MO,WE'
        }
    # fulldays = {
    #     'Tu' : 'TU', 
    #     'Th' : 'TH', 
    #     'M' : 'MO', 
    #     'W' : 'WE', 
    #     'F' : 'FR'
    # }
    name_class = soup.find('h2')
    # name_class.text
    info = soup.find_all('table')
    for child in info: 
        # print(child.text)
        children = child.findAll("tr" , recursive=False)
        # print(len(children))
        if len(children) == 2: 
            # print('hi')
            
            tableRow = children[1].find_all("td")
            # now i know that this should have 4 rows and 4 rows only
            meetingTimes = tableRow[0]
            meetingPlace = tableRow[1]
            instructor = tableRow[2]
            meetingDates = tableRow[3]
            # print(name_class.text)
            meetingTimesList = meetingTimes.text.split()
            # 
            daysToMeet = meetingTimesList[0]
            timeToMeet = meetingTimesList[1].split('-')
            
            datesToMeet = meetingDates.text.split('-')
            #
            in_time = datetime.strptime(timeToMeet[0], "%I:%M%p")
            startTime = datetime.strftime(in_time, "%H:%M")

            end_time = datetime.strptime(timeToMeet[1], "%I:%M%p")
            endTime = datetime.strftime(end_time, "%H:%M")

            in_date = datetime.strptime(datesToMeet[0], "%m/%d/%y ")
            in_date_formatted = datetime.strftime(in_date, "%Y-%m-%d")
            # print(daysToMeet)
            # print(timeToMeet)
            # exit()
            count = len(days[daysToMeet].split(','))
            return name_class.text, meetingPlace.text, in_date_formatted, startTime, endTime, days[daysToMeet], count*10

if __name__ == '__main__':
    main()

