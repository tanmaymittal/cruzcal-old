from icalendar import Calendar
from Event import Event


class iCalendar():
    """
    Class responsible for creating calendar and exporting ICS file
    """
    def __init__(self):
        """
        Intializes event object attributes
        """
        self.events = []

    def addCourse(self, courseNumber):
        """
        Add class to calendar.
        """
        ev = Event(courseNumber)
        ev.generateEvent()
        self.events += ev.getEvents()
        return True

    def export(self, filepath):
        """
        Export calendar in ICS format
        """
        cal = Calendar()
        if len(self.events) == 0:
            return False
        for event in self.events:
            # package the events
            cal.add_component(event)
        f = open(filepath + '/calendar.ics', 'wb')
        f.write(cal.to_ical())
        f.close()
        return True
