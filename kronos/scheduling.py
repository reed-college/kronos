from populatedb import *
from kronos import db
from collections import namedtuple

Range = namedtuple('Range', ['start', 'end'])

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

    i = 0
    ls = []
    while i < len(availstart):
        start = availstart[i]
        end = availend[i]
        ls.append(Range(start, end))
        i += 1
    return ls


# Given four professors' schedule, return time intervals when they are all available.

def all_avail(user1, user2, user3, user4):
    ls = []
    avail1 = available(user1)
    avail2 = available(user2)
    avail3 = available(user3)
    avail4 = available(user4)
    for range1 in avail1:
        for range2 in avail2:
            for range3 in avail3:
                for range4 in avail4:
                    latest_start = max(range1.start, range2.start, range3.start, range4.start)
                    earliest_end = min(range1.end, range2.end, range3.end, range4.end)
                    if latest_start <= earliest_end:
                        ls.append(Range(latest_start, earliest_end))
    return ls

