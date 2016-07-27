from icalendar import Calendar, Event
from datetime import datetime
from pandas import DataFrame
from sqlalchemy import create_engine
import pandas as pd
import pytz

# Remember to change user name and file path.
engine = create_engine('postgresql://Jiahui:pass@localhost/db_kronos')


# Import CSV files

# (Problem: For some reason dates will be saved as text when converted to CSV from Excel, 
# hence they cannot be appended to the event table.)

# df_csv = pd.read_csv('/Users/Jiahui/kronos/kronos/csvdata.csv')
# df_csv.to_sql('pandas', engine, if_exists='append')

# assert df_csv.query('dtstart > dtend').empty


# Import Excel files
df_xlsx = pd.read_excel('/Users/Jiahui/kronos/kronos/exceldata.xlsx')
df_xlsx.to_sql('event', engine, if_exists='append', index=False)

assert df_xlsx.query('dtstart > dtend').empty



# Import ics files

cal = Calendar() # Create a new empty calendar
cal = cal.from_ical(open('USHolidays.ics','rb').read()) # Open an existing calendar

# get data from ics files.

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


# import data to db

s = getsummary(cal)
start = getdtstart(cal)
end = getdtend(cal)

df = pd.DataFrame(dict(summary = s, dtstart = start, dtend = end, private = True))
df.to_sql('event', engine, if_exists='append', index=False)   




