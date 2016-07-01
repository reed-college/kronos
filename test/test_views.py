import kronos

class Test_shcedule:
    @classmethod
    def setup_class(cls):
        kronos.app.config.from_object('kronos.config.TestConfig')
        cls.client = kronos.app.test_client()
        import populatedb
    
    @classmethod
    def teardown_class(cls):
        kronos.db.drop_all()


    def test_gives_template(self):
        rv = self.client.get('/')    
        assert rv.status_code == 200
