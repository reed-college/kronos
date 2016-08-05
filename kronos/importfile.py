import os
from icalendar import Calendar, Event
from datetime import datetime
from pandas import DataFrame
from sqlalchemy import create_engine
import pandas as pd
import pytz

# Remember to change user name and file path.
engine = create_engine('postgresql://Jiahui:pass@localhost/db_kronos')

# Import CSV files

def import_csv(path):
    df_csv = pd.read_csv(path)
    assert df_csv.query('dtstart > dtend').empty
    return df_csv.to_sql('event', engine, if_exists='append', index=False)

# Import Excel files

def import_excel(path):
    df_excel = pd.read_excel(path)
    assert df_excel.query('dtstart > dtend').empty
    return df_excel.to_sql('event', engine, if_exists='append', index=False)


# Import ics files

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
def import_ics(path):
    cal = Calendar().from_ical(open(path,'rb').read())

    s = getsummary(cal)
    start = getdtstart(cal)
    end = getdtend(cal)

    df = pd.DataFrame(dict(summary = s, dtstart = start, dtend = end, private = True))
    assert df.query('dtstart > dtend').empty

    return df.to_sql('event', engine, if_exists='append', index=False)   

# Import files from uploads folder

def import_from_uploads(path):
    files = os.listdir(path)[1:]
    for file in files:
        extension = os.path.splitext(file)[1]
        abspath = os.path.abspath(file)
        if extension == '.xlsx' or '.xls':
            return import_excel(abspath)
        elif extension == 'csv':
            return import_csv(abspath)
        elif extension == 'ics':
            return import_ics(abspath)





