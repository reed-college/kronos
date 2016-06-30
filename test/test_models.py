from kronos.models import Event, Prof
from datetime import datetime
from dateutil.parser import parse as dtparse
import random

class TestEvent:
    class Test_validate_end_after_start:
        @classmethod
        def setup_class(cls):
            random.seed()
            pearson = Prof('pearson', 'Pearson', 'asdf', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
            cls.event1 = Event('at home', dtparse('20160502 08:00:00 AM'), dtparse('20160502 10:00:00 AM'), pearson)
            # for tests where it doesn't matter if the field is a dtstart or dtend
            cls.key = random.choice(['dtend','dtstart'])
        
        def test_validator_returns_normally_when_end_is_after_start(self):
            field = datetime(2016, 5, 2, 10)
            returnval = self.event1.validate_end_after_start('dtend', field)
            assert field == returnval
            
        def test_validator_returns_normally_when_start_is_before_end(self):
            field = datetime(2016, 5, 2, 8)
            returnval = self.event1.validate_end_after_start('dtstart', field)
            assert field == returnval

        def test_validator_accepts_string_fields(self):
            field = "20160502 10:00"
            returnval = self.event1.validate_end_after_start('dtend', field)
            assert field == returnval
    
        def test_validator_rejects_end_before_start(self):
            field = datetime(2016, 5, 2, 6)
            try:
                self.event1.validate_end_after_start('dtend', field)
            except AssertionError:
                pass
            else:
                raise AssertionError("Validator didn't throw an AssertionError after receiving an end before the event's start")

        def test_validator_rejects_start_after_end(self):
            field = datetime(2016, 5, 2, 12)
            try:
                self.event1.validate_end_after_start('dtstart', field)
            except AssertionError:
                pass
            else:
                raise AssertionError("Validator didn't throw an AssertionError after receiving a start after the event's end")
            

        def test_validator_rejects_integers(self):
            field = 127
            try:
                self.event1.validate_end_after_start(self.key, field)
            except (AssertionError, TypeError):
                pass
            else:
                raise AssertionError("Validator did not throw an AssertionError or TypeError when receiving and integer")

        def test_validator_rejects_malformed_strings(self):
            field = "jwjncwnecwjc;we;fkwkle"
            try:
                self.event1.validate_end_after_start(self.key, field)
            except Exception:
                pass
            else:
                raise AssertionError("Validator did not throw an Error when receiving a malformed string")
    
