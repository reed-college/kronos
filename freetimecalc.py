

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
