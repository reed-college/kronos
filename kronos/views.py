import json
import datetime
from dateutil import parser
import flask
import httplib2

from flask import render_template, request, redirect
from apiclient import discovery
from oauth2client import client

from kronos import app, db, util
from .models import department, division, Oral, Stu, Prof, Event, User, OralStartDay


@app.route('/')
def schedule():

    if OralStartDay.query.all() == []:
        return redirect('/oralweeks')

    startday = OralStartDay.query.\
               filter(OralStartDay.start >= (datetime.date.today() - datetime.timedelta(days=7))).\
               order_by(OralStartDay.start).first().start

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

    return render_template(
        "schedule.html", department=department, division=division,
        students=students, professors=professors, startday=startday,
        edit=edit)


@app.route('/oralweeks', methods=['GET', 'POST'])
def edit_start_days():
    """
    This page is for editing the oral start days so that the schedule page
    knows what week to go to for orals week
    """
    if request.method == 'POST':
        print(request.form)
        for day in OralStartDay.query.all():
            desc = request.form.get("desc--" + str(day.id))
            date = request.form.get("date--" + str(day.id))
            if desc is not None and date is not None:
                day.description = desc
                day.start = date
                db.session.commit()
        i = 0
        desc = request.form.get("desc-"+str(i))
        date = request.form.get("date-"+str(i))
        while desc is not None and desc is not "" and date is not None and date is not "":
            desc = request.form.get("desc-"+str(i))
            date = request.form.get("date-"+str(i))
            day = OralStartDay(desc, date)
            db.session.add(day)
            i += 1
        db.session.commit()
        return redirect('/oralweeks')
    else:
        oralstarts = OralStartDay.query.order_by(OralStartDay.start).all()
        return render_template("oralweeks.html", oralstarts=oralstarts)
 
@app.route('/print')
def print_schedule():
    """
    Gives a schedule table of orals that will look nice when printed
    """
    events = util.filter_events(Event.query, request.args)
    # This needs to be after filter_events because filter_events sometimes
    # adds non-oral events to the query
    orals = events.filter(Event.discriminator == 'oral')
    oraltable = util.GetOralTable(orals.order_by(Oral.dtstart).all())
    div = str(request.args.get("division")).upper() or None
    dept = str(request.args.get("department")).upper() or None
    # Getting the semester and year
    if orals.all() != []:
        starttime = orals.first().dtstart
        year = starttime.date().year
        if starttime.date().month <= 7:
            semester = 'SPRING'
        else:
            semester = 'FALL'
        time = semester + ' ' + str(year)
    else:
        time = ''
    return render_template('printsched.html', oraltable=oraltable, 
                           division=div, department=dept, time=time)

@app.route('/eventsjson')
def get_events_json():
    """
    Returns a json of events based on args in the querystring
    all of the args are listed below
    """
    eventobjs = util.filter_events(Event.query, request.args)
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
    eventid = request.form.get("event_id") or None
    userid = request.form.get("user_id") or None
    stuid = request.form.get("stu_id") or None
    summary = request.form.get("summary") or None
    readers = request.form.getlist("readers[]") or None
    start = request.form.get("start") or None
    end = request.form.get("end") or None
    # TODO: get current user from ldap
    user = User.query.first()
    if eventid is not None:
        event = Event.query.get_or_404(eventid)
    elif (start is not None) and (end is not None):
        event = Event('New Event', start, end, user)
        db.session.add(event)
        db.session.commit()
        return event.summary
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
        # need to update start and end in the right order so the validators don't freak out
        if parser.parse(end) < event.dtstart:
            event.dtstart = start
            event.dtend = end
        else: 
            event.dtend = end
            event.dtstart = start
        db.session.commit()
        return (str(event.dtstart.timestamp()), str(event.dtend.timestamp()))
    elif start is not None:
        event.dtstart = start
        db.session.commit()
        return event.dtstart.strftime("%-H:%M")
    elif end is not None:
        event.dtend = end
        db.session.commit()
        return event.dtend.strftime("%-H:%M")
    else:
        return "Something went wrong!"


@app.route('/deletevent', methods=['POST'])
def delete_event():
    print(request.form)
    eventid = request.form.get("event_id") or None
    event = Event.query.get_or_404(eventid)
    name = event.summary
    db.session.delete(event)
    db.session.commit()
    return "Event '" + name + "' deleted"
     

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
