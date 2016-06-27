from populatedb import *
from kronos import db


# Print the available time given a user.

def available(user):
    start = datetime.datetime(2016,5,2,8)   # 8am on the Monday of oral's week.
    end = datetime.datetime(2016,5,6,20)    # 8pm on the Friday of oral's week.
    starttimes = []
    endtimes = []
    orals = Oral.query.all()
    for event in user.events:
        starttimes.append(event.dtstart)
        endtimes.append(event.dtend)
    for oral in orals:
        if user in oral.readers:
            starttimes.append(oral.dtstart)
            endtimes.append(oral.dtend)
    for dtend in endtimes:
        if dtend in starttimes:
            endtimes.remove(dtend)
            starttimes.remove(dtend)
    availstart = endtimes
    availend = starttimes
    if start < min(starttimes):
        availstart.append(start)
    else:
        availend.remove(min(starttimes))
    if end > max(endtimes):
        availend.append(end)
    else:
        availstart.remove(max(endtimes))
    availstart.sort()
    availend.sort()
    return availstart, availend

# Example:
# A result like (
# [datetime.datetime(2016, 5, 2, 9, 0), datetime.datetime(2016, 5, 2, 12, 0), datetime.datetime(2016, 5, 6, 19, 0)],
# [datetime.datetime(2016, 5, 2, 10, 0), datetime.datetime(2016, 5, 6, 10, 0), datetime.datetime(2016, 5, 6, 20, 0)])
# means that the input user is free from 20160502 9:00:00 to 20160502 10:00:00,
# from 20160502 12:00:00 to 20160506 10:00:00,
# and from 20160506 19:00:00 to 20160506 20:00:00.

