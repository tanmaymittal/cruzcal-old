from icalendar import Calendar
from Event import Event
from pathlib import Path
import gc
import os
from settings import *


class iCalendar():
    """
    Class responsible for creating calendar and exporting ICS file
    """
    def __init__(self, uid = None):
        """
        Intializes event object attributes
        """
        self.events = []
        self.uid = uid
        self.count = 0

    def addCourse(self, courseNumber):
        """
        Add class to calendar.
        """
        ev = Event(courseNumber)
        if ev.getClassData():
            ev.generateEvent()
            self.events.append(ev)
            self.count += 1
            return True
        return False

    def clear(self, uid):
        """
        Clears calendar data and runs garbage collection
        """
        self.events = []
        self.uid = uid
        self.count = 0
        gc.collect()
        return True

    def export(self):
        """
        Export calendar in ICS format
        """
        cal = Calendar()
        if len(self.events) == 0:
            return False
        for event in self.events:
            # package the events
            if event != 0:
                cal.add_component(event.getEvents())
        f = open('{}/user_requests/{}.ics'.format(Path.cwd(), self.uid), 'wb')
        f.write(cal.to_ical())
        f.close()
        c, conn = connection()
        c.execute(
            "INSERT INTO sessions (uid) VALUES (%s)",
            [self.uid])
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        return True