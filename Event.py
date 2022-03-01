import requests
from requests.api import head 
from icalendar import Event as EV
from datetime import * 
from bs4 import BeautifulSoup as bs
from calendar import monthrange

class Event():
    """
    Event class is responsible for grabbing, parsing, and saving relavent information
    relavent to the class given its course number. The event class is also responsible
    for generating iCalendar format events.
    """
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
    days = {
        'TuTh' : 'TU,TH',
        'MWF' : 'MO,WE,FR',
        'M': 'MO',
        'MW': 'MO,WE',
        'Tu': 'TU'
        }
    num_day = {
        0: 'MO',
        1: 'TU',
        2: 'WE',
        3: 'TH',
        4: 'FR',
        5: None,
        6: None
        }
    anchor = {
        0: 2,
        1: 0,
        2: 5,
        3: 3
    }
    def __init__(self, courseNumber):
        """
        Intializes event object attributes and calls self.getClassData()
        """
        self.courseNumber = courseNumber
        self.courseName = None
        self.startDate = None
        self.meetingTime = None
        self.meetingDates = None
        self.meetingLocation = None
        self.meetingRecurrences = 0
        self.instructor = None
        self.class_payload = {
            'action': 'detail', 
            'class_data[:STRM]': '2222',
            'class_data[:CLASS_NBR]': f'{self.courseNumber}', # class number 
            'binds[:term]': '2222', # probably term number 
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
        self.events = []

    def getClassData(self):
        """
        Grabs course data based on course number and saves them to their respective attributes.
        Returns True if course information is successfully retrieved; else returns False
        """
        search_url = "https://pisa.ucsc.edu/class_search/index.php"
        class_response = requests.post(search_url, headers=self.headers, verify=False, data=self.class_payload)
        raw_HTML = bs(class_response.content, 'lxml')
        # Saving Course Name
        self.courseName = ' '.join(raw_HTML.find('h2').text.split())
        courseInfo = raw_HTML.find_all('table')
        for child in courseInfo: 
            #parsing course information
            children = child.findAll("tr" , recursive=False)
            if len(children) == 2: 
                tableRow = children[1].find_all("td")
                meetingTimes = tableRow[0]
                meetingPlace = tableRow[1]
                instructor = tableRow[2]
                meetingDates = tableRow[3]
                meetingTimesList = meetingTimes.text.split()
                daysToMeet = meetingTimesList[0]
                timeToMeet = meetingTimesList[1].split('-')
                datesToMeet = meetingDates.text.split('-')
                in_time = datetime.strptime(timeToMeet[0], "%I:%M%p")
                startTime = datetime.strftime(in_time, "%H:%M")
                end_time = datetime.strptime(timeToMeet[1], "%I:%M%p")
                endTime = datetime.strftime(end_time, "%H:%M")
                in_date = datetime.strptime(datesToMeet[0], "%m/%d/%y ")
                in_date_formatted = datetime.strftime(in_date, "%Y-%m-%d")
                count = len(self.days[daysToMeet].split(','))
                # Save all event attributes of concern
                self.meetingLocation = meetingPlace.text
                self.startDate = in_date_formatted
                self.meetingTime = (startTime, endTime)
                self.meetingDates = self.days[daysToMeet]
                return True
        return False
    def getEvents(self):
        return self.events

    def generateEvent(self):
        """
        This method is responsible for generating iCalendar events for the
        meeting information associated with the given course number.
        """
        if self.meetingDates is not None:
            for day in self.meetingDates.split(','):
                # Determine first meeting date given the day of week
                curr_year, curr_month, curr_day = self.startDate.split('-')
                curr_year, curr_month, curr_day = int(curr_year), int(curr_month), int(curr_day)
                search_day, month_days = monthrange(curr_year, curr_month) # Get first day of mo and len(mo)
                search_day = (search_day + curr_day - 1) % 7 # Grabs day of week for first day of class
                while day != Event.num_day[search_day]:
                    curr_day += 1
                    search_day += 1
                    if curr_day > month_days:
                        # Move to next valid day
                        curr_day = 1
                        curr_month += 1
                        if curr_month > 12:
                            curr_month = 1
                            curr_year += 1
                        search_day, month_days = monthrange(curr_year, curr_month)
                # Creating the event for specified day of week
                event = EV()
                start, end = self.meetingTime
                # Adding corrected start date to start and end times
                start += ' {}-{}-{}'.format(curr_year, curr_month, curr_day)
                end += ' {}-{}-{}'.format(curr_year, curr_month, curr_day)
                event.add('summary', "{} - {}".format(day, self.courseName))
                event.add('description', 'Lecture for {}'.format(self.courseName))
                event.add('dtstart', datetime.strptime(start, '%H:%M %Y-%m-%d'))
                event.add('dtend', datetime.strptime(end, '%H:%M %Y-%m-%d'))
                event.add('dtstamp', datetime.now())
                event.add('location', self.meetingLocation)
                event.add('rrule', { 'FREQ': 'WEEKLY', 'BYDAY':day, 'COUNT': 10})
                self.events.append(event)
        else: 
            self.events.append(0)
