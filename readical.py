from icalendar import Calendar, Event
from datetime import datetime
from pandas import DataFrame
import pytz

cal = Calendar() # Create a new empty calendar
cal = cal.from_ical(open('USHolidays.ics','rb').read()) # Open an existing calendar

# Print starting time:
def pstart(cal):
    for event in cal.walk('vevent'):
        date = event.get('dtstart')
    return date.to_ical()

def getsummary(cal):
    ls = []
    for event in cal.walk('vevent'):
        ls.append(str(event.get('summary')))
    return ls

def getdtstart(cal):
    ls = []
    for event in cal.walk('vevent'):
        ls.append(event.get('dtstart').dt)
    return ls

def getdtend(cal):
    ls = []
    for event in cal.walk('vevent'):
        ls.append(event.get('dtend').dt)
    return ls