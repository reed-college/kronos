import pytest


class TestViews:

    @pytest.mark.usefixtures("setup_db", "populate_db")
    class Test_with_populated_db:

        def test_oral_shows_up_on_schedule_page(self, client):
            # Assumes that there is an event titled 'Oral_Emma' in
            # populatedb.py
            rv = client.get('/')
            assert 'calendar' in str(rv.data)

        def test_oral_shows_up_in_events_json(self, client):
            rv = client.get('/eventsjson')
            assert 'Oral_Emma' in str(rv.data)

        def test_person_shows_up_in_users_json(self, client):
            rv = client.get('/usersjson')
            assert 'Emma' in str(rv.data)

        def test_student_doesnt_show_up_when_getting_professors(self, client):
            rv = client.get('/usersjson?type=professor')
            assert 'Emma' not in str(rv.data)

        def test_professor_does_show_up_when_getting_professors(self, client):
            rv = client.get('/usersjson?type=professor')
            assert 'Hovda' in str(rv.data)

        def test_print_schedule_shows_at_least_one_oral(self, client):
            rv = client.get('/print')
            assert 'Emma' in str(rv.data)

        @pytest.mark.usefixtures("setup_db", "populate_db","debug_auth")
        def test_oral_weeks_has_oral_week(self, client):
            rv = client.get('/oralweeks')
            assert 'Sprang 2016' in str(rv.data)

        def test_load_search(self, client):
            rv = client.get('/print')
            assert rv.status_code == 200

    @pytest.mark.usefixtures("setup_db")
    class Test_with_empty_db:

        def test_schedule_works_with_empty_db(self, client):
            rv = client.get('/')
            # greater than 400 are error codes
            assert rv.status_code < 400

        def test_events_json_returns_none(self, client):
            rv = client.get('/eventsjson')
            assert str(rv.data) == "b'[]'"

        def test_users_json_returns_none(self, client):
            rv = client.get('/usersjson')
            assert str(rv.data) == "b'{}'"

        def test_print_schedule_works_with_empty_db(self, client):
            rv = client.get('/print')
            assert rv.status_code == 200

        def test_oral_weeks_does_not_have_oral_week(self, client):
            rv = client.get('/oralweeks')
            assert 'Sprang 2016' not in str(rv.data)

        @pytest.mark.usefixtures("setup_db","debug_auth")
        def test_add_oral_week(self, client):
            name = 'the limit of characters for this field is 50'
            client.post(
                '/oralweeks',
                data={
                    'desc-1': name,
                    'date-1': '2017-05-01'})
            rv = client.get('/oralweeks')
            assert name in str(rv.data)
        
        def test_load_search(self, client):
            rv = client.get('/print')
            assert rv.status_code == 200
