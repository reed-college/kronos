from kronos import util
from random import randint
import datetime

class TestUtil:
    def test_FreeTimeCalc(self):
        """
        Uses variously lengthed events and 2 hour orals placed throughout
        a week to test if FreeTimeCalc works as it should
        """
        events = []
        orals = []
        guess = []
        oralslength = datetime.timedelta(hours=2)
        for i in range(1,6):
            start = datetime.datetime(2017, 5, i, hour=10)
            length = datetime.timedelta(hours=i)
            events.append((start, start + length))
            oralstart = datetime.datetime(2017, 5, i, hour=13)
            orals.append((oralstart, oralstart + oralslength))
            #This guesses which orals won't intersect the events, since
            #the events increase in length over the week
            if i <= 3:
                guess.append((oralstart, oralstart + oralslength))
        assert guess == util.FreeTimeCalc(events,orals)
            
