from icalendar import Calendar, Event
from datetime import datetime
import pytz

cal = Calendar() # Create a new empty calendar
cal = cal.from_ical(open('WorkCalendar.ics','rb').read()) # Open an existing calendar


# Display calendar in the same format as the ics file.
def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()
# To print it out:
print display(cal)

# Print starting time:
def pstart(cal):
    for event in cal.walk('vevent'):
        date = event.get('dtstart')
        return date.to_ical()

command = raw_input('Enter your oral time (YYYYMMDDHHMMSS to YYYYMMDDHHMMSS): ')
oralstart = command[:14]
oralend = command[18:]

# Show if there is a time conflict.
def showconflict(cal):
    for event in cal.walk('vevent'):
        start = event.get('dtstart').to_ical()
        end = event.get('dtend').to_ical()
        # summary = event.get('summary').
        if int(start[:7]) == int(oralstart[:7]):
            if int(start[9:]) < int(oralend[8:]) and int(end[9:]) > int(oralend[8:]):
                print("There is a time conflict.")
            elif int(start[9:]) < int(oralstart[8:]) and int(end[9:]) > int(oralstart[8:]):
                print("There is a time conflict.")

# MIGHT need a way to print attendees' available time (using an interval tree?).

