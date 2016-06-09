import json
import datetime
import flask
import httplib2

from flask import render_template, request
from apiclient import discovery
from oauth2client import client

from kronos import app
from .models import department, division, Oral, Stu, Prof, Event


@app.route('/')
def schedule():

    # start time of first oral
    starttime = Oral.query.order_by(Oral.dtstart).all()[0].dtstart
    students = Stu.query.all()
    professors = Prof.query.all()

    return render_template(
        "schedule.html", department=department, division=division,
        students=students, professors=professors, starttime=starttime)


@app.route('/eventsjson')
def get_events_json():
    # getting querystring args
    start = request.args.get("start")
    end = request.args.get("end")
    div = str(request.args.get("division"))
    dept = str(request.args.get("department"))
    profs = request.args.getlist("professors[]")
    stus = request.args.getlist("students[]")

    eventobjs = Event.query
    # filtering by querystring args
    if ((profs != [] and profs != [''] and profs is not None) or
       (stus != [] and stus != [''] and stus is not None)):
        # make the query empty
        eventobjs = eventobjs.except_(eventobjs)
    for profid in profs:
        if profid == '':
            break
        # Events that the professor owns
        pf = Event.query.filter(Event.userid == profid)
        # Orals that the professor is going to
        ora = Event.query.join(Oral).\
            join(Oral.readers).join(Prof).\
            filter(Prof.id == profid)
        profevents = pf.union(ora)
        eventobjs = eventobjs.union(profevents)
    for stuid in stus:
        if stuid == '':
            break
        ora = Event.query.join(Oral).filter(Oral.stu_id == stuid)
        eventobjs = eventobjs.union(ora)
    if div in division:
        st = eventobjs.join(Oral).join(Oral.stu).\
           join(Stu).filter(Stu.division == div)
        pf = eventobjs.join(Event.user).\
           join(Prof).filter(Prof.division == div)
        eventobjs = st.union(pf)
    if dept in department:
        st = eventobjs.join(Oral).join(Oral.stu).\
                join(Stu).filter(Stu.department == dept)
        pf = eventobjs.join(Event.user).\
                join(Prof).filter(Prof.department == dept)
        eventobjs = st.union(pf)
    if start is not None:
        eventobjs = eventobjs.filter(Event.dtend >= start)
    if end is not None:
        eventobjs = eventobjs.filter(Event.dtstart <= end)
    # putting the events into the formal fullcalendar wants
    events = []
    for event in eventobjs:
        evjson = {
        "id": event.id,
        "title": event.summary,
        "start": str(event.dtstart),
        "end": str(event.dtend),
        "type": event.discriminator,
        "user": event.user.name,
        "student": "",
        "readers": [],
        }
        if type(event) is Oral:
            evjson["readers"] = [reader.name for reader in event.readers]
            evjson["student"] = event.stu.name
        events.append(evjson)
        
    return json.dumps(events)


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
