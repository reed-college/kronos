from datetime import timedelta, datetime
from .models import department, division, Event, Oral, Stu, Prof

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
                (firstday + timedelta(days=i)).strftime("%A, %B %d <br> ") +
                earliestStart.strftime("%I:%M - ") +
                earliestEnd.strftime("%I:%M"))
        oraltable.append(timerow)

        while currTimeslotOrals != []:
            oralrow = ["c"]  # c for cell
            for i in range(delta.days + 1):
                currday = firstday + timedelta(days=i)
                currstart = datetime.combine(currday, earliestStart)
                currend = datetime.combine(currday, earliestEnd)
                for oral in currTimeslotOrals:
                    if oral.dtstart == currstart and oral.dtend == currend:
                        oralrow.append(oral.stu.name)
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
