from icalendar import Calendar
from Event import Event
from pathlib import Path
import gc


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

    def addCourse(self, courseNumber):
        """
        Add class to calendar.
        """
        ev = Event(courseNumber)
        ev.generateEvent()
        self.events += ev.getEvents()
        return True

    def clear(self, uid):
        """
        Clears calendar data and runs garbage collection
        """
        self.events = []
        self.uid = uid
        gc.collect()
        return True

    def gc(self, uid_to_be_deleted):
        pass

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
                cal.add_component(event)
        f = open('{}/{}.ics'.format(Path.cwd(), self.uid), 'wb')
        f.write(cal.to_ical())
        f.close()
        return True
