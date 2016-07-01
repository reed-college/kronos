import kronos

class LiveServerTest:
    @classmethod
    def setup_class(cls):
        cls.client = kronos.app.test_client()
        kronos.db.create_all()
    
    @classmethod
    def teardown_class(cls):
        kronos.db.drop_all()



class Test_with_populated_db(LiveServerTest):
    @classmethod
    def setup_class(cls):
        LiveServerTest.setup_class()
        import populatedb
    
    def test_gives_template(self):
        rv = self.client.get('/')    
        assert rv.status_code == 200
        

class Test_with_empty_db(LiveServerTest):
    def test_schedule_works_with_empty_db(self):
        rv = self.client.get('/')    
        assert rv.status_code == 200

