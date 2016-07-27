from random import randint
import datetime
from dateutil import parser
from kronos import util
from kronos.models import Oral, Stu, Prof

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
    
    def test_GetOralTable(self):
        """
        Makes sure that the oral table has header and cell tags in the 
        first column of each row and that the orals are placed below the
        headers for their time slots
        """
        hovda = Prof('hovdap', 'Paul Hovda', 'hovdap@reed.edu', 'Philosophy', 'Philosophy, Religion, Psychology and Linguistics')
        pearson = Prof('pearson', 'Pearson', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
        emma = Stu('erennie', 'Emma Rennie', 'erennie@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
        richard = Stu('adcockr', 'Richard Adcock', 'adcockr@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')

        oral1 = Oral(emma, 'Oral_Emma', parser.parse('20160502 10:00:00 AM'), parser.parse('20160502 12:00:00 PM'), pearson)
        oral1.readers = [pearson]

        oral2 = Oral(richard, 'Oral_Richard', parser.parse('20160502 03:00:00 PM'), parser.parse('20160502 05:00:00 PM'), hovda)
        oral2.readers = [hovda]
        
        orals = [oral1, oral2]
        
        [['h', 'Monday, May 02 <br> 10:00 - 12:00'], ['c', 'Emma Rennie'], ['h', 'Monday, May 02 <br> 03:00 - 05:00'], ['c', 'Richard Adcock']]
        
        oraltable = util.GetOralTable(orals)
        oral1col = None
        oral2col = None
        for row in oraltable:
            # Assert that the first column of each row specifies whether its a header row or not
            assert row[0] == 'h' or row[0] == 'c'
            for i in range(len(row)):
                #If this is the header for the orals at 10:00 on monday may 2nd
                if ("Monday" in row[i] or "May 02" in row[i] or "May 2" in row[i]):
                    if "10:00" in row[i]:
                        oral1col = i
                    elif "3:00" in row[i]:
                        oral2col = i
                elif oral1col is not None and "Emma Rennie" in row[i]:
                    # making sure the oral is below its timeslot's header
                    assert oral1col == i
                    # assert the the for loop has not gotten to the second
                    # oral header since it's later in the day
                    assert oral2col is None
                elif oral2col is not None and "Richard Adcock" in row[i]:
                    # making sure the oral is below its timeslot's header
                    assert oral2col == i







