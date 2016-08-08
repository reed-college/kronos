import datetime as dt
from .models import department, division, Event, Oral, Stu, Prof, OralStartDay


def FreeTimeCalc(events, orals):
    """
    the events and orals objects are tuples of datetimes where the first one
    is the start time and the second the end
    taken the events and the orals it returns the orals this person is free for
    """
    freeorals = []  # oral slots the prof could go to

    for oral in orals:
        oralstart = oral[0]
        oralend = oral[1]
        available = True
        for event in events:
            start = event[0]
            end = event[1]
            if ((oralstart < start and oralend > start) or
                    (end > oralstart and start < oralstart)):
                available = False
        if available:
            freeorals.append(oral)
    return freeorals


def GetOralTable(orals):
    """
    This function takes a list of orals objects(ordered by start time)
    (VERY IMPORTANT THAT ITS ORDERED BY START TIME)
    and gives back a 2D array of strings that make a very pretty table
    This function assumes that orals do not start before midnight and
    end after midnight
    """
    if len(orals) == 0:
        return [[]]
    firstday = orals[0].dtstart.date()
    lastday = orals[-1].dtstart.date()
    # Creates the oral table
    oraltable = []
    while orals != []:
        earliestStart = min(oral.dtstart.time() for oral in orals)
        earliestEnd = orals[0].dtend.time()
        for oral in orals:
            if oral.dtstart.time() == earliestStart:
                earliestEnd = oral.dtend.time()
        currTimeslotOrals = [oral for oral in orals if
                             oral.dtstart.time() == earliestStart and
                             oral.dtend.time() == earliestEnd]
        orals = [oral for oral in orals if not (oral in currTimeslotOrals)]

        timerow = ["h"]  # h for header
        delta = lastday - firstday
        for i in range(delta.days + 1):
            timerow.append(
                (firstday + dt.timedelta(days=i)).strftime("%A, %B %d <br> ") +
                earliestStart.strftime("%I:%M - ") +
                earliestEnd.strftime("%I:%M"))
        oraltable.append(timerow)

        while currTimeslotOrals != []:
            oralrow = ["c"]  # c for cell
            for i in range(delta.days + 1):
                currday = firstday + dt.timedelta(days=i)
                currstart = dt.datetime.combine(currday, earliestStart)
                currend = dt.datetime.combine(currday, earliestEnd)
                for oral in currTimeslotOrals:
                    if oral.dtstart == currstart and oral.dtend == currend:
                        info = '<b>' + oral.stu.name + '</b><br>'
                        for reader in oral.readers:
                            info += reader.name + '<br>'
                        for i in range(len(oral.readers) + 1, 5):
                            info += ordinalize(i) + " Reader: <br>"
                        if oral.location is not None:
                            info += oral.location
                        else:
                            info += "Location:"
                        oralrow.append(info)
                        currTimeslotOrals.remove(oral)
                        break
                else:
                    oralrow.append("")
            oraltable.append(oralrow)

    return oraltable


def filter_events(eventobjs, args):
    """
    Takes a dictionary of querystring arguments and an event query
    and then filters it based on the args
    """
    # putting args into variables
    start = args.get("start")
    end = args.get("end")
    div = str(args.get("division"))
    dept = str(args.get("department"))
    profs = args.getlist("professors[]")
    stus = args.getlist("students[]")

    # filtering by querystring args
    if ((profs != [] and profs != [''] and profs is not None) or
            (stus != [] and stus != [''] and stus is not None)):
        # make the query empty
        eventobjs = eventobjs.except_(eventobjs)
    for profid in profs:
        if profid == '':
            break
        # Events that the professor owns
        pf = Event.query.filter(Event.userid == profid)
        # Orals that the professor is going to
        ora = Event.query.join(Oral).\
            join(Oral.readers).join(Prof).\
            filter(Prof.id == profid)
        profevents = pf.union(ora)
        eventobjs = eventobjs.union(profevents)
    for stuid in stus:
        if stuid == '':
            break
        ora = Event.query.join(Oral).filter(Oral.stu_id == stuid)
        eventobjs = eventobjs.union(ora)
    if div in division:
        st = eventobjs.join(Oral).join(Oral.stu).\
            join(Stu).filter(Stu.division == div)
        pf = eventobjs.join(Event.user).\
            join(Prof).filter(Prof.division == div)
        eventobjs = st.union(pf)
    if dept in department:
        st = eventobjs.join(Oral).join(Oral.stu).\
            join(Stu).filter(Stu.department == dept)
        pf = eventobjs.join(Event.user).\
            join(Prof).filter(Prof.department == dept)
        eventobjs = st.union(pf)
    if start is not None:
        eventobjs = eventobjs.filter(Event.dtend >= start)
    if end is not None:
        eventobjs = eventobjs.filter(Event.dtstart <= end)

    return eventobjs


def ordinalize(n):
    """
    I stole this function from here:
    http://codegolf.stackexchange.com/a/74047
    """
    return str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]


def overlap(start1, end1, start2, end2):
    """
    takes 4 datetimes of the starts and ends of 2 events and returns 
    whether or not they overlap
    """
    # assert start1 <= end1
    # assert start2 <= end2
    return ((start1 > start2 and start1 <= end2) or
            (end1 > start2 and end1 <= end2) or
            (start1 <= start2 and end1 >= end2))


def free_professors(start, end):
    """
    takes a time range and returns what professors are free during that time
    """
    overlaps = [event for event in Event.query
            if overlap(event.dtstart, event.dtend, start, end)
            ]
    # profs who are on an orals board at the given time
    readers = {reader.id for oral in overlaps 
           if oral.discriminator == "oral" for reader in oral.readers}

    # profs who have another event at the given time
    eventprofs = {event.user.id for event in overlaps 
              if event.discriminator == "event" and 
                 event.user.discriminator == "professor"}
    # combines the two sets of profs
    busyprofs = readers | eventprofs
    # getting every prof who isn't busy at the current time
    return Prof.query.filter(*[Prof.id != profid for profid in busyprofs]).\
            order_by(Prof.name).all()

def get_start_day(startdayid):
    """
    Returns the startday with id startdayid if startdayid is a number
    if startdayid is None, it gets the closest future startday
    """
    if startdayid is not None:
        return OralStartDay.query.get(startdayid)
    else:
        startoralday = OralStartDay.query.\
            filter(OralStartDay.start >=
                   (dt.date.today() -
                    dt.timedelta(days=7))).\
            order_by(OralStartDay.start).first()
        if startoralday is None:
            startoralday = OralStartDay.query.order_by(
                OralStartDay.start).first()
        return startoralday

def get_div_from_dept(dept):
    """
    Takes a string with the name of a department and returns the 
    division its in 
    """
    if dept not in department:
        raise AssertionError("Given dept not one of: " + str(department))
    if dept in {'Art', 'Dance', 'Music', 'Theatre'}:
        return 'The Arts'
    if dept in {'Anthropology', 'Economics', 'History', 'Political Science', 'Sociology'}:
        return 'History and Social Sciences'
    if dept in {'Chinese','Classics','English','French','German','Russian','Spanish'}:
        return 'Literature and Languages'    
    if dept in {'Biology', 'Chemisty', 'Physics', 'Mathematics'}:
        return 'Mathematics and Natural Sciences'
    if dept in {'Philosophy', 'Religion', 'Psychology', 'Linguistics'}:
        return 'Philosophy, Religion, Psychology and Linguistics'
    return 'Other'
