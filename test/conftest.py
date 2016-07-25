import pytest
import kronos
import datetime
from kronos.models import Stu, Prof, Oral

@pytest.yield_fixture
def setup_db(request):
    #kronos.db.drop_all()
    kronos.db.create_all()
    yield None
    pass
    #kronos.db.drop_all()

@pytest.fixture
@pytest.mark.usefixtures("setup_db")
def populate_db():
    emma = Stu('erennie', 'Emma Rennie', '123', 'erennie@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
    richard = Stu('adcockr', 'Richard Adcock', 'asd', 'adcockr@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
    hovda = Prof('hovdap', 'Paul Hovda', 'asdf', 'hovdap@reed.edu', 'Philosophy', 'Philosophy, Religion, Psychology and Linguistics')
    hancock = Prof('hancockv', 'Ginny', 'asdf', 'hancockv@reed.edu', 'Music', 'The Arts')
    oral1 = Oral(emma, 'Oral_Emma', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), emma)
    oral1.readers = [hovda]
    oral2 = Oral(richard, 'Oral_Richard', datetime.datetime(2016,5,2,15), datetime.datetime(2016,5,2,17), richard)
    oral2.readers = [hancock]
    kronos.db.session.add(emma)
    kronos.db.session.add(richard)
    kronos.db.session.add(hovda)
    kronos.db.session.add(hancock)
    kronos.db.session.add(oral1)
    kronos.db.session.add(oral2)
    kronos.db.session.commit()


@pytest.fixture
def db():
    return kronos.db

@pytest.fixture
def client():
    return kronos.app.test_client()

