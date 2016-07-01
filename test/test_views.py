import kronos

class Test_shcedule:
    @classmethod
    def setup_class(cls):
        kronos.app.config.from_object('kronos.config.TestConfig')
        cls.client = kronos.app.test_client()
        import populatedb

    def test_gives_template(self):
        self.client.get('/')    
