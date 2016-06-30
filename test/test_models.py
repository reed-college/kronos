from kronos.models import Event, Prof
from datetime import datetime
from dateutil.parser import parse as dtparse

class Test_validate_end_after_start:
   
    def test_validator_returns_normally_when_end_is_after_start(self):
        field = datetime(2016, 5, 2, 10)
        pearson = Prof('pearson', 'Pearson', 'asdf', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
        event1 = Event('at home', dtparse('20160502 08:00:00 AM'), dtparse('20160502 10:00:00 AM'), pearson)
        returnval = event1.validate_end_after_start('dtend', field)
        assert field == returnval
