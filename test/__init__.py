import kronos
# configure kronos for testing
kronos.app.config.from_object('kronos.config.TestConfig')
#makes errors made with test client get sent through
kronos.app.testing = True 
