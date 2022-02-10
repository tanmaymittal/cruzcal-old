from Calendar import iCalendar
from pathlib import Path

ical = iCalendar()
while True:
    a = input("Please enter course number to continue, e to export, or q to quit [q]")
    if a == 'e':
        file_path = input("Please enter export path for 'calendar.ICS', or q to exit [~/]")
        if (''.join(file_path.split()) == '') :
            file_path = str(Path.home() / "Downloads")
        ical.export(file_path)
    elif (''.join(a.split()) == '') or (a == 'q'):
        exit()
    else:
        courseNumber = int(a)
        if ical.addCourse(courseNumber):
            print("Success!")
        else:
            print("Failed")