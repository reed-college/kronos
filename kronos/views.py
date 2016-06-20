import json
import datetime
import flask
import httplib2

from flask import render_template, request
from apiclient import discovery
from oauth2client import client

from kronos import app, db
from .models import department, division, Oral, Stu, Prof, Event, User


@app.route('/')
def schedule():

    # start time of first oral
    starttime = Oral.query.order_by(Oral.dtstart).all()[0].dtstart
    students = Stu.query.all()
    professors = Prof.query.all()
    # TODO when we're gonna need each POST request from fullcalendar/jeditable
    # to be validated through ldap, because leaving it up to a javascript
    # variable is super insercure.
    # But we'll have to wait until someone gets around to helping us set up ldap
    # to do that.
    # and also hopefully the javascript variable will get set by ldap
    # authentication and not a querysting
    edit = request.args.get("edit") or "false" 
    print(edit, type(edit))

    return render_template(
        "schedule.html", department=department, division=division,
        students=students, professors=professors, starttime=starttime,
        edit=edit)


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


@app.route('/usersjson')
def get_users_json():
    """
    Returns a json of users for jeditable to use for the selects
    """
    usrtype = request.args.get("type") or ""
    usrqury = User.query.filter(User.discriminator.contains(usrtype))
    users = {usr.id : usr.name for usr in usrqury} 
    return json.dumps(users)


@app.route('/submitevent', methods=['POST'])
def update_event():
    """
    page for jeditable to send new event changes to the db
    """
    print(request.form)
    eventid = request.form.get("event_id")
    userid = request.form.get("user_id") or None
    stuid = request.form.get("stu_id") or None
    summary = request.form.get("summary") or None
    readers = request.form.getlist("readers[]") or None
    start = request.form.get("start") or None
    end = request.form.get("end") or None
    event = Event.query.get_or_404(eventid)
    if userid is not None:
        event.userid = userid
        db.session.commit()
        return event.user.name
    if stuid is not None:
        event.stu_id = stuid
        db.session.commit()
        return event.stu.name
    elif summary is not None:
        event.summary = summary
        db.session.commit()
        return event.summary
    elif readers is not None:
        readerobjs = [Prof.query.get(id) for id in readers]
        event.readers = readerobjs
        db.session.commit()
        return str(event.readers)
    elif (start is not None) and (end is not None):
        event.dtstart = start
        event.dtend = end
        db.session.commit()
        return (str(event.dtstart.timestamp()), str(event.dtend.timestamp()))
    else:
        return "Something went wrong!"

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
