import os
import json
import datetime as dt
from dateutil import parser
import flask
import httplib2
from functools import wraps

from flask import Flask, flash, Markup, render_template, request, redirect, Response, url_for, send_from_directory, current_app, session, abort, g
from apiclient import discovery
from oauth2client import client
from werkzeug.utils import secure_filename

from kronos import app, db, util
from .models import Oral, Stu, FAC
from .academic_constants import DEPARTMENTS, DIVISIONS
from .models import Prof, Event, User, OralStartDay
from .util import authorize


@app.route('/')
def schedule():
    startdays = OralStartDay.query.all()
    if startdays == []:
        return redirect('/oralweeks')

    startdayid = request.args.get("startday") or None
    startday = util.get_start_day(startdayid).start

    # only get students who have orals
    students = Stu.query.filter(Stu.oral).all()
    professors = Prof.query.all()
    
    # Only FACs can edit
    edit = "false"
    if g.user and g.user.discriminator == "FAC":
        # need to have true and false as strings because javascript
        edit = "true"

    return render_template(
        "schedule.html", department=DEPARTMENTS, division=DIVISIONS,
        students=students, professors=professors, startday=startday,
        edit=edit, startdays=startdays)


@app.route('/oralweeks', methods=['GET', 'POST'])
def edit_start_days():
    """
    This page is for editing the oral start days so that the schedule page
    knows what week to go to for orals week
    """
    if request.method == 'POST':
        authorize()
        print(request.form)
        # editing existing oral days
        for day in OralStartDay.query.all():
            desc = request.form.get("desc--" + str(day.id))
            date = request.form.get("date--" + str(day.id))
            remove = request.form.get("remove--" + str(day.id))
            if desc is not None and date is not None:
                day.description = desc
                day.start = date
            elif remove == "True":
                print(remove)
                db.session.delete(day)
        # adding new oral days
        i = 1
        desc = request.form.get("desc-" + str(i))
        date = request.form.get("date-" + str(i))
        while (desc is not None and desc is not "" and
               date is not None and date is not ""):
            day = OralStartDay(desc, date)
            db.session.add(day)
            i += 1
            desc = request.form.get("desc-" + str(i))
            date = request.form.get("date-" + str(i))
        db.session.commit()
        return redirect('/oralweeks')
    else:
        if g.user and g.user.discriminator == "FAC":
            oralstarts = OralStartDay.query.order_by(OralStartDay.start).all()
            return render_template("oralweeks.html", oralstarts=oralstarts)
        else:
            return render_template("oralweekpublic.html")
            


UPLOAD_FOLDER = '/Users/Jiahui/kronos/kronos/static/uploads'
ALLOWED_EXTENSIONS = set(['ics', 'xls', 'xlsx', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(Markup('File uploaded. <a href="javascript:history.back()"> Back</a>'))
            return render_template('uploaded.html')
    return render_template("upload.html")


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

@app.route('/search')
def search():
    """
    allows you to search for what pofessors are free at a given time
    """
    startstr = request.args.get("start")
    endstr = request.args.get("end")
    stuid = request.args.get("student")
    if startstr is not None and endstr is not None:
        # gets profs based on given start and end
        start = dt.datetime.strptime(startstr,"%Y-%m-%dT%H:%M")
        end = dt.datetime.strptime(endstr,"%Y-%m-%dT%H:%M")
        profs = util.free_professors(start, end)
    elif stuid is not None:
        # Gets profs based on the start and end times of a given student's
        # oral
        oral = Oral.query.filter(Oral.stu_id == stuid).first()
        start = oral.dtstart
        end = oral.dtend
        profs = util.free_professors(start,end)
        startstr = oral.dtstart.strftime("%Y-%m-%dT%H:%M")
        endstr = oral.dtend.strftime("%Y-%m-%dT%H:%M")
    else:
        # if there is an oralstartday, this sets the default start and end
        # datetimes to that day
        if OralStartDay.query.all() != []:
            startday = util.get_start_day(None).start
            start = dt.datetime.combine(startday, dt.time(0,0,0))
            end = start + dt.timedelta(hours=2)
            startstr = start.strftime("%Y-%m-%dT%H:%M")
            endstr = end.strftime("%Y-%m-%dT%H:%M")
        profs = []
    # the the Stu object stores a list of its orals under Stu.oral, not
    # one singular oral, as a rational human being would expect
    students = Stu.query.filter(Stu.oral).all()
    return render_template("search.html", profs=profs, start=startstr,
           end=endstr, students=students)

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
            "location": event.location,
        }
        if isinstance(event, Oral):
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
    authorize()
    eventid = request.form.get("event_id") or None
    userid = request.form.get("user_id") or None
    stuid = request.form.get("stu_id") or None
    summary = request.form.get("summary") or None
    readers = request.form.getlist("readers[]") or None
    location = request.form.get("location") or None
    start = request.form.get("start") or None
    end = request.form.get("end") or None
    evtype = request.form.get("type") or None
    # TODO: get current user from ldap
    user = User.query.first()
    # if we're updating a current event
    if eventid is not None:
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
        elif location is not None:
            event.location = location
            db.session.commit()
            return event.location
        elif (start is not None) and (end is not None):
            # need to update start and end in the right order so the validators
            # don't freak out
            if parser.parse(end) < event.dtstart:
                event.dtstart = start
                event.dtend = end
            else:
                event.dtend = end
                event.dtstart = start
            db.session.commit()
            return (str(event.dtstart.timestamp()),
                    str(event.dtend.timestamp()))
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
    # new event
    elif (start is not None) and (end is not None):
        print(request.form)
        if evtype == "oral":
            event = Oral(Stu.query.first(), 'New Oral', start, end, user)
        else:
            event = Event('New Event', start, end, user)
        db.session.add(event)
        db.session.commit()
        return "Sucess!"


@app.route('/deletevent', methods=['POST'])
def delete_event():
    authorize()
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
        oralsweekstart = dt.datetime(2017, 5, 1).isoformat() + 'Z'
        oralsweekend = dt.datetime(2017, 5, 6).isoformat() + 'Z'

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


@app.route('/login')
def login():
    if session.get('user_id') is None:
        # When debuging, make the user a FAC
        if current_app.config['DEBUG']:
            if FAC.query.all() == []:
                gonyerk = FAC('gonyerk', 'Kristy', 'gonyerk@reed.edu')
                db.session.add(gonyerk)
                db.session.commit()
            session['user_id'] = FAC.query.first().id
            return redirect(util.redirect_url())   
        else:        
            return redirect(util.redirect_url())   
    else:
        # Can't log in again when you're already logged in
        abort(403)
    
@app.route('/logout')
def logout():
    if current_app.config['DEBUG']:
        del session['user_id']
        return redirect(util.redirect_url())   
    else:
        return redirect(util.redirect_url())   

@app.before_request
def load_user():
    """
    sets 'global' user variable based on user id stored in session variables
    stolen from: 
    http://stackoverflow.com/questions/13617231/how-to-use-g-user-global-in-flask
    """
    if session.get("user_id"):
        user = User.query.get(session["user_id"])
    else:
        user = None
    g.user = user


