from datetime import timedelta, datetime

def FreeTimeCalc(events,orals):
    """
    the events and orals objects are tuples of datetimes where the first one is the start time and the second the end
    taken the events and the orals it returns the orals this person is free for
    """
    freeorals = [] #oral slots the prof could go to     

    for oral in orals:
        oralstart = oral[0]
        oralend = oral[1]
        available = True
        for event in events:
            start = event[0]
            end = event[1]
            if ((oralstart < start and oralend > start) or (end > oralstart and start < oralstart)): 
                available = False
        if available:
            freeorals.append(oral)
    return freeorals

def GetOralTable(orals):
    """
    This function takes a list of orals objects(ordered by start time) and gives back 
    a 2D array of strings that make a very pretty table
    This function assumes that orals do not start before midnight and 
    end after midnight
    """
    firstday = orals[0].dtstart.date()
    lastday = orals[-1].dtstart.date()
    #Creates the oral table
    oraltable = []
    while orals != []:
        earliestStart = min(oral.dtstart.time() for oral in orals)
        earliestEnd = orals[0].dtend.time()
        for oral in orals:
            if oral.dtstart.time() == earliestStart:
                earliestEnd = oral.dtend.time()
        currTimeslotOrals = [oral for oral in orals if oral.dtstart.time() == earliestStart and oral.dtend.time() == earliestEnd]
        orals = [oral for oral in orals if not (oral in currTimeslotOrals)]
        
        timerow = ["h"] # h for header
        delta = lastday - firstday
        for i in range(delta.days + 1):
            timerow.append(str(firstday + timedelta(days=i)) + str(earliestStart) + str(earliestEnd))
        oraltable.append(timerow)
        while currTimeslotOrals != []:
            oralrow = ["c"] # c for cell
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
    
