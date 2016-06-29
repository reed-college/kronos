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

def overlap(avail1, avail2):
    ls = []
    for range1 in avail1:
        for range2 in avail2:
            latest_start = max(range1.start, range2.start)
            earliest_end = min(range1.end, range2.end)
            if latest_start <= earliest_end and (
                earliest_end - latest_start >= datetime.timedelta(hours=2)):    # if they intersect
                ls.append(Range(latest_start, earliest_end))
    return ls


def all_avail(user1, user2, user3, user4):
    ls = []
    avail1 = available(user1)
    avail2 = available(user2)
    avail3 = available(user3)
    avail4 = available(user4)
    r1 = overlap(avail1, avail2)
    r2 = overlap(avail3, avail4)
    return overlap(r1, r2)



# Return possible oral times given less than 4 professors' schedule
# Assume all orals take 2 hours

# Given two lists of ranges, return the overlap ranges.



# def possibletime(users):
#     i = 0
#     avails = []
#     while i < len(users):
#         avails.append(available(users[i]))
#         i += 1
#     for avail1, avail2 in zip(avails, avails):
#         if avail1 != avail2:
#             overlap(avail1, avail2)


# users = [pearson, becker, hovda, somda]
# possibletime(users)



# Assume all orals take 2 hours
# and the only starting times are 8am, 10am, 1pm, 3pm and 5pm.


# Given the schedule of one person (thesis advisor who has to be in the oral),
# return something like this:
# Time | Profs
#  8am | Hovda, Hancock, Pearson
# 10am | Hovda, Somda, Becker, Witt



events = Event.query.all()
