from kronos.models import Event, Prof
from datetime import datetime
from dateutil.parser import parse as dtparse
class TestEvent:
    class Test_validate_end_after_start:
        @classmethod
        def setup_class(cls):
            pearson = Prof('pearson', 'Pearson', 'asdf', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
            cls.event1 = Event('at home', dtparse('20160502 08:00:00 AM'), dtparse('20160502 10:00:00 AM'), pearson)
        
        def test_validator_returns_normally_when_end_is_after_start(self):
            field = datetime(2016, 5, 2, 10)
            returnval = self.event1.validate_end_after_start('dtend', field)
            assert field == returnval
            
        def test_validator_accepts_string_fields(self):
            field = "20160502 10:00"
            returnval = self.event1.validate_end_after_start('dtend', field)
            assert field == returnval
    
        def test_validator_rejects_integers(self):
            field = 127
            try:
                returnval = self.event1.validate_end_after_start('dtend', field)
            except (AssertionError, TypeError):
                pass
            else:
                raise AssertionError("Validator did not throw an AssertionError or TypeError when receiving and integer")

        def test_validator_rejects_malformed_strings(self):
            pass
    
