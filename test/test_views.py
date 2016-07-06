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
        
        def test_oral_shows_up(self):
            # Assumes that there is an event titled 'Oral_Emma' in populatedb.py
            print(kronos.app.config['SQLALCHEMY_DATABASE_URI'])
            rv = self.client.get('/')    
            assert 'calendar' in str(rv.data)
            
    
    class Test_with_empty_db(LiveServerTest):
        def test_schedule_works_with_empty_db(self):
            rv = self.client.get('/')    
            assert rv.status_code == 200

