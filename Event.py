import requests
from requests.api import head 
from icalendar import Calendar, Event
from datetime import * 
from bs4 import BeautifulSoup as bs

class Event():
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
        'MW': 'MO,WE'
        }
    def __init__(self, courseNumber):
        """
        Intializes event object attributes and calls self.getClassData()
        Returns None
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
            'class_data[:STRM]': '2220',
            'class_data[:CLASS_NBR]': f'{self.courseNumber}', # class number 
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
        self.getClassData()
    def getClassData(self):
        """
        Grabs course data based on course number and saves them to their respective attributes.
        Returns True if course information is successfully retrieved; else returns False
        """
        search_url = "https://pisa.ucsc.edu/class_search/index.php"
        class_response = requests.post(search_url, headers=self.headers, verify=False, data=self.class_payload)
        # print(class_response.text)
        raw_HTML = bs(class_response.content, 'lxml')
        # Saving Course Name
        self.courseName = raw_HTML.find('h2').text
        # name_class.text
        courseInfo = raw_HTML.find_all('table')
        for child in courseInfo: 
            children = child.findAll("tr" , recursive=False)
            if len(children) == 2: 
                tableRow = children[1].find_all("td")
                #tableRow structure: 4x4
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
                count = len(self.days[daysToMeet].split(','))
                # Save all event attributes of concern
                self.meetingLocation = meetingPlace.text
                self.startDate = in_date_formatted
                self.meetingTime = (startTime, endTime)
                self.meetingDates = self.days[datesToMeet]
                self.meetingRecurrences = count * 10
                return True
        return False
    def getiCal(self):
        
        pass