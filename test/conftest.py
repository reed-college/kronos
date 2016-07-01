import pytest
import kronos

@pytest.fixture(autouse=True)
def change_settings():
    # configure kronos for testing
    kronos.app.config.from_object('kronos.config.TestConfig')
