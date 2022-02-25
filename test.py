from Calendar import iCalendar
from pathlib import Path
from random import randint

ical = iCalendar()
uid = randint(100000, 999999)
ical.clear(uid)
while True:
    a = input("Please enter course number to continue, e to export, or q to quit [q]\t")
    if a == 'e':
        ical.export()
    elif (''.join(a.split()) == '') or (a == 'q'):
        exit()
    else:
        courseNumber = int(a)
        if ical.addCourse(courseNumber):
            print("Success!")
        else:
            print("Failed")