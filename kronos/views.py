import json
import datetime
import flask
import httplib2

from flask import render_template
from apiclient import discovery
from oauth2client import client

from kronos import app


@app.route('/')
def index():
    return render_template("schedule.html") 


@app.route('/gcal')
def get_gcal():
    """
    Shows the user what events they have during orals week
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        # 'Z' indicates UTC time
        oralsweekstart = datetime.datetime(2017, 5, 1).isoformat() + 'Z'
        oralsweekend = datetime.datetime(2017, 5, 6).isoformat() + 'Z'

        print('Getting events during orals week')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=oralsweekstart, timeMax=oralsweekend,
            singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        return json.dumps(events)


@app.route('/oauth2callback')
def oauth2callback():
    """
    Connects to the google api
    copied almost etirely from:
    https://developers.google.com/api-client-library/python/auth/web-app#example
    """
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('get_gcal'))
