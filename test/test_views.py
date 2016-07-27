import kronos
from kronos import models
import pytest

class LiveServerTest:
    @classmethod
    @pytest.mark.usefixtures("change_settings")
    def setup_class(cls):
        print(kronos.app.config['SQLALCHEMY_DATABASE_URI'])
        cls.client = kronos.app.test_client()
        kronos.db.create_all()
    
    @classmethod
    def teardown_class(cls):
        kronos.db.drop_all()

class TestViews:
    class Test_with_populated_db(LiveServerTest):
        @classmethod
        def setup_class(cls):
            LiveServerTest.setup_class()
            import populatedb
        
        def test_oral_shows_up_on_schedule_page(self):
            # Assumes that there is an event titled 'Oral_Emma' in populatedb.py
            rv = self.client.get('/')    
            assert 'calendar' in str(rv.data)

        def test_oral_shows_up_in_events_json(self):
            rv = self.client.get('/eventsjson')
            assert 'Oral_Emma' in str(rv.data)

        def test_person_shows_up_in_users_json(self):
            rv = self.client.get('/usersjson')
            assert 'Emma' in str(rv.data)

        def test_student_doesnt_show_up_when_getting_professors(self):
            rv = self.client.get('/usersjson?type=professor')
            assert 'Emma' not in str(rv.data)

        def test_professor_does_show_up_when_getting_professors(self):
            rv = self.client.get('/usersjson?type=professor')
            assert 'Hovda' in str(rv.data)

        def test_print_schedule_shows_at_least_one_oral(self):
            rv = self.client.get('/print')
            assert 'Emma' in str(rv.data)         
    
    class Test_with_empty_db(LiveServerTest):
        def test_schedule_works_with_empty_db(self):
            rv = self.client.get('/')    
            #greater than 400 are error codes
            assert rv.status_code < 400
        
        def test_events_json_returns_none(self):
            rv = self.client.get('/eventsjson')
            assert str(rv.data) == "b'[]'"
            
        def test_users_json_returns_none(self):
            rv = self.client.get('/usersjson')
            assert str(rv.data) == "b'{}'"
            
        def test_print_schedule_works_with_empty_db(self):
            rv = self.client.get('/print')
            assert rv.status_code == 200         

