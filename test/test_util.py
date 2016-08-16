import datetime as dt
from dateutil import parser
from kronos import util
from kronos.models import Oral, Stu, Prof, Event, FAC
from werkzeug.datastructures import ImmutableMultiDict
import pytest
from kronos.views import g


class TestUtil:

    def test_FreeTimeCalc(self):
        """
        Uses variously lengthed events and 2 hour orals placed throughout
        a week to test if FreeTimeCalc works as it should
        """
        events = []
        orals = []
        guess = []
        oralslength = dt.timedelta(hours=2)
        for i in range(1, 6):
            start = dt.datetime(2017, 5, i, hour=10)
            length = dt.timedelta(hours=i)
            events.append((start, start + length))
            oralstart = dt.datetime(2017, 5, i, hour=13)
            orals.append((oralstart, oralstart + oralslength))
            # This guesses which orals won't intersect the events, since
            # the events increase in length over the week
            if i <= 3:
                guess.append((oralstart, oralstart + oralslength))
        assert guess == util.FreeTimeCalc(events, orals)

    def test_GetOralTable(self):
        """
        Makes sure that the oral table has header and cell tags in the
        first column of each row and that the orals are placed below the
        headers for their time slots
        """
        hovda = Prof(
            'hovdap',
            'Paul Hovda',
            'hovdap@reed.edu',
            'Philosophy',
            'Philosophy, Religion, Psychology, and Linguistics')
        pearson = Prof(
            'pearson',
            'Pearson',
            'pearson@reed.edu',
            'Linguistics',
            'Philosophy, Religion, Psychology, and Linguistics')
        emma = Stu(
            'erennie',
            'Emma Rennie',
            'erennie@reed.edu')
        richard = Stu(
            'adcockr',
            'Richard Adcock',
            'adcockr@reed.edu')

        oral1 = Oral(
            emma,
            'Oral_Emma',
            parser.parse('20160502 10:00:00 AM'),
            parser.parse('20160502 12:00:00 PM'), 
            'Linguistics', 
            'Philosophy, Religion, Psychology, and Linguistics',
            pearson)
        oral1.readers = [pearson]

        oral2 = Oral(
            richard,
            'Oral_Richard',
            parser.parse('20160502 03:00:00 PM'),
            parser.parse('20160502 05:00:00 PM'), 
            'Linguistics', 
            'Philosophy, Religion, Psychology, and Linguistics',
            hovda)
        oral2.readers = [hovda]

        orals = [oral1, oral2]

        [['h', 'Monday, May 02 <br> 10:00 - 12:00'], ['c', 'Emma Rennie'],
         ['h', 'Monday, May 02 <br> 03:00 - 05:00'], ['c', 'Richard Adcock']]

        oraltable = util.GetOralTable(orals)
        oral1col = None
        oral2col = None
        for row in oraltable:
            # Assert that the first column of each row specifies whether its a
            # header row or not
            assert row[0] == 'h' or row[0] == 'c'
            for i in range(len(row)):
                # If this is the header for the orals at 10:00 on monday may
                # 2nd
                if ("Monday" in row[i] or "May 02" in row[
                        i] or "May 2" in row[i]):
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

    @pytest.mark.usefixtures("setup_db", "populate_db")
    class TestFilterEvents():

        def test_filter_professor(self, db):
            adcockid = Stu.query.filter(Stu.username == 'adcockr').first().id
            oral2 = Oral.query.filter(Oral.stu_id == adcockid).first()
            hovdaid = Prof.query.filter(Prof.username == 'hovdap').first().id
            args = ImmutableMultiDict({'professors[]': [hovdaid]})
            events = util.filter_events(Event.query, args)
            assert oral2 not in events.all()


    class TestOverlap:
        
        def test_end_of_first_event_after_start_of_second_overlaps(self):
            start1 = dt.datetime(2000,1,1,10)
            end1 = dt.datetime(2000,1,1,12)
            start2 = dt.datetime(2000,1,1,11)
            end2 = dt.datetime(2000,1,1,13)
            assert util.overlap(start1,end1,start2,end2)

        def test_first_event_inside_second(self):
            start1 = dt.datetime(2000,1,1,10)
            end1 = dt.datetime(2000,1,1,12)
            start2 = dt.datetime(2000,1,1,2)
            end2 = dt.datetime(2000,1,7,2)
            assert util.overlap(start1,end1,start2,end2)

        def test_first_event_end_equals_second_event_start(self):
            start1 = dt.datetime(2000,1,1,10)
            end1 = dt.datetime(2000,1,1,12)
            start2 = dt.datetime(2000,1,1,12)
            end2 = dt.datetime(2000,1,1,14)
            assert not util.overlap(start1,end1,start2,end2)

        def test_end_of_second_event_after_start_of_first(self):
            start1 = dt.datetime(2000,1,1,11)
            end1 = dt.datetime(2000,1,1,13)
            start2 = dt.datetime(2000,1,1,10)
            end2 = dt.datetime(2000,1,1,12)
            assert util.overlap(start1,end1,start2,end2)

    
    @pytest.mark.usefixtures("setup_db", "populate_db")
    class TestFreeProfessors():
        
        def test_professor_not_free_when_in_oral(self):
            start = dt.datetime(2016, 5, 2, 10)
            end = dt.datetime(2016, 5, 2, 12)
            hovda = Prof.query.filter(Prof.username == 'hovdap').first()
            profs = util.free_professors(start,end)
            assert hovda not in profs 
             
        
        def test_professor_free_when_not_in_oral(self):
            start = dt.datetime(2016, 5, 2, 12)
            end = dt.datetime(2016, 5, 2, 14)
            hovda = Prof.query.filter(Prof.username == 'hovdap').first()
            profs = util.free_professors(start,end)
            assert hovda in profs 
    
    class TestGetStartDay():

        @pytest.mark.usefixtures("setup_db", "populate_db")
        def test_get_only_start_day(self):
            day = util.get_start_day(None)
            assert day.description == "Sprang 2016"

        @pytest.mark.usefixtures("setup_db", "populate_db")
        def test_works_properly_when_given_id(self):
            day = util.get_start_day(1)
            assert day.description == "Sprang 2016"

        @pytest.mark.usefixtures("setup_db")
        def test_returns_none_on_empty_db(self):
            day = util.get_start_day(None)
            assert day is None
            
    class TestGetDivFromDept():
        def test_the_arts_division(self):
            assert util.get_div_from_dept("Art") == "The Arts"
            assert util.get_div_from_dept("Dance") == "The Arts"
            assert util.get_div_from_dept("Music") == "The Arts"
            assert util.get_div_from_dept("Theatre") == "The Arts"

        def test_HSS_division(self):
            assert util.get_div_from_dept("Anthropology") == "History and Social Sciences"
            assert util.get_div_from_dept("Economics") == "History and Social Sciences"
            assert util.get_div_from_dept("History") == "History and Social Sciences"
            assert util.get_div_from_dept("Political Science") == "History and Social Sciences"
            assert util.get_div_from_dept("Sociology") == "History and Social Sciences"

        def test_lit_lang_division(self):
            assert util.get_div_from_dept("Chinese") == "Literature and Languages"
            assert util.get_div_from_dept("Classics") == "Literature and Languages"
            assert util.get_div_from_dept("English") == "Literature and Languages"
            assert util.get_div_from_dept("Creative Writing") == "Literature and Languages"
            assert util.get_div_from_dept("French") == "Literature and Languages"
            assert util.get_div_from_dept("German") == "Literature and Languages"
            assert util.get_div_from_dept("Russian") == "Literature and Languages"
            assert util.get_div_from_dept("Spanish") == "Literature and Languages"

        def test_mns_division(self):
            assert util.get_div_from_dept("Biology") == "Mathematics and Natural Sciences"
            assert util.get_div_from_dept("Chemistry") == "Mathematics and Natural Sciences"
            assert util.get_div_from_dept("Mathematics") == "Mathematics and Natural Sciences"
            assert util.get_div_from_dept("Physics") == "Mathematics and Natural Sciences"

        def test_prpl_division(self):
            assert util.get_div_from_dept("Philosophy") == "Philosophy, Religion, Psychology, and Linguistics"
            assert util.get_div_from_dept("Religion") == "Philosophy, Religion, Psychology, and Linguistics"
            assert util.get_div_from_dept("Psychology") == "Philosophy, Religion, Psychology, and Linguistics"
            assert util.get_div_from_dept("Linguistics") == "Philosophy, Religion, Psychology, and Linguistics"

