import pytest
import kronos
import datetime
from kronos.models import Stu, Prof, Oral, OralStartDay


@pytest.yield_fixture
def setup_db(request):
    # kronos.db.drop_all()
    kronos.db.create_all()
    yield None
    pass
    kronos.db.session.remove()
    kronos.db.drop_all()


@pytest.fixture
@pytest.mark.usefixtures("setup_db")
def populate_db():
    emma = Stu(
        'erennie',
        'Emma Rennie',
        'erennie@reed.edu',
        'Linguistics',
        'Philosophy, Religion, Psychology, and Linguistics')
    richard = Stu(
        'adcockr',
        'Richard Adcock',
        'adcockr@reed.edu',
        'Linguistics',
        'Philosophy, Religion, Psychology, and Linguistics')
    hovda = Prof(
        'hovdap',
        'Paul Hovda',
        'hovdap@reed.edu',
        'Philosophy',
        'Philosophy, Religion, Psychology, and Linguistics')
    hancock = Prof(
        'hancockv',
        'Ginny',
        'hancockv@reed.edu',
        'Music',
        'The Arts')
    oral1 = Oral(
        emma, 'Oral_Emma', datetime.datetime(
            2016, 5, 2, 10), datetime.datetime(
            2016, 5, 2, 12), emma)
    oral1.readers = [hovda]
    oral2 = Oral(
        richard, 'Oral_Richard', datetime.datetime(
            2016, 5, 2, 15), datetime.datetime(
            2016, 5, 2, 17), richard)
    oral2.readers = [hancock]
    s16 = OralStartDay("Sprang 2016", datetime.date(2016, 5, 2))
    kronos.db.session.add(emma)
    kronos.db.session.add(richard)
    kronos.db.session.add(hovda)
    kronos.db.session.add(hancock)
    kronos.db.session.add(oral1)
    kronos.db.session.add(oral2)
    kronos.db.session.add(s16)
    kronos.db.session.commit()


@pytest.fixture
def db():
    return kronos.db


@pytest.fixture
def client():
    return kronos.app.test_client()


# Once we know what Prod auth will look like, change tests to remove this
@pytest.yield_fixture
def debug_auth(request, client):
    """
    This sets the config to have debug true and then logs in the client
    so that the client has FAC privileges
    """
    kronos.app.config['DEBUG'] = True
    client.get('/login')
    yield None
    client.get('/logout')
    kronos.app.config.from_object('kronos.config.TestConfig')
    
