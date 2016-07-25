import datetime
from kronos import db
from sqlalchemy import Enum, ForeignKey, DateTime, event
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.ext.declarative import declared_attr
from dateutil import parser
from datetime import datetime


department = ('Anthropology', 'Art', 'Biology', 'Chemistry', 'Chinese',
              'Classics', 'Dance', 'Economics', 'English', 'French', 'German',
              'History', 'Linguistics', 'Mathematics', 'Music', 'Philosophy',
              'Physics', 'Political Science', 'Psychology', 'Religion',
              'Russian', 'Sociology', 'Spanish', 'Theatre')
division = ('The Arts', 'History and Social Sciences',
            'Literature and Languages', 'Mathematics and Natural Sciences',
            'Philosophy, Religion, Psychology and Linguistics')

readers = db.Table('readers',
       db.Column('prof_id', db.Integer, db.ForeignKey('prof.id')),
       db.Column('oral_id', db.Integer, db.ForeignKey('oral.id'))
       )



# The User class contains professors and students,
# but that does not mean that they are the actual "users" of this website


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True)
    discriminator = db.Column('type', db.String(20))
    __mapper_args__ = {'polymorphic_on': discriminator}

    def __init__(self, username, name, password, email):
        self.username = username
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email

class FAC(User):
    __mapper_args__ = {'polymorphic_identity': 'FAC'}
    def __init__(self, username, name, password, email):
        User.__init__(self, username, name, password, email)
        self.type = 'FAC'


class Prof(User):
    department = db.Column(db.Enum(*department, name="department"))
    division = db.Column(db.Enum(*division, name="division"))
    __mapper_args__ = {'polymorphic_identity': 'professor'}
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)

    def __init__(self, username, name, password, email, department, division):
        User.__init__(self, username, name, password, email)
        self.department = department
        self.division = division
        self.type = 'professor'

    def __repr__(self):
        return '<%r>' % self.username


class Stu(User):
    department = db.Column(db.Enum(*department, name="department"))
    division = db.Column(db.Enum(*division, name="division"))
    __mapper_args__ = {'polymorphic_identity': 'student'}
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)

    def __init__(self, username, name, password, email, department, division):
        User.__init__(self, username, name, password, email)
        self.department = department
        self.division = division
        self.type = 'student'

    def __repr__(self):
        return '<%r>' % self.username


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary = db.Column(db.Text)
    dtstart = db.Column(db.DateTime, nullable=False)
    dtend = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('busy', 'free', name='status'))
    private = db.Column(db.Boolean)
    discriminator = db.Column('type', db.String(10))
    __mapper_args__ = {'polymorphic_on': discriminator}
    __table_args__ = (
        CheckConstraint('dtstart <= dtend'),
        )


    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('events'))  # lazy???

    def __init__(self, summary, dtstart, dtend, user,
                 private=True, status='busy'):
        self.summary = summary
        self.dtstart = dtstart
        self.dtend = dtend
        self.status = status
        self.user = user
        self.private = private

    def __repr__(self):
        if self.private is False:
            return '<Event %r>' % self.summary
        else:
            return '<Not available>'

    @validates('dtstart', 'dtend')
    def validate_end_after_start(self, key, field):
        """
        Checks 2 things
        1. That either a string or a datetime was set to either dtstart or dtend
        2. That the end of this event is after the start
        """
        #if a string is submitted, it will now be converted to a datetime
        if type(field) is datetime:
            time = field
        elif type(field) is str:
            time = parser.parse(field)
        else:
            raise AssertionError(key + " must of type 'datetime.datetime' or type 'str'")
        if key is "dtstart" and isinstance(self.dtend, datetime):
            assert time < self.dtend
        elif key is "dtend" and isinstance(self.dtstart, datetime):
            assert time > self.dtstart
        return field

class Oral(Event):
    __tablename__ = 'oral'
    __mapper_args__ = {'polymorphic_identity': 'oral'}
    id = db.Column(db.Integer, ForeignKey('event.id'), primary_key=True, autoincrement=True)
    stu_id = db.Column(db.Integer, db.ForeignKey('stu.id'))
    stu = db.relationship('Stu', backref=db.backref('oral'))
    response = db.Column(db.Enum('Accepted', 'Declined', 'Tentative',
                                 name="response"))
    readers = db.relationship('Prof', secondary=readers,
           backref=db.backref('orals', lazy='dynamic'))

    def __init__(self, stu, summary, dtstart, dtend, user,
                 response=None):
        Event.__init__(self, summary, dtstart, dtend, user)
        self.user = user
        self.stu = stu
        self.type = 'oral'

    def __repr__(self):
        return '<%rs Oral>' % self.stu

    
    @validates('readers')
    def validate_orals(self, key, reader):
        for oral in reader.orals:
            # make sure readers won't be assigned to conflicting orals.
            if (oral.dtstart > self.dtstart and oral.dtstart <= self.dtend) or (
                oral.dtend > self.dtstart and oral.dtend <= self.dtend) or (
                oral.dtstart <= self.dtstart and oral.dtend >= self.dtend):
                raise ValueError('Conflicting orals are assigned to reader ' + str(reader) + ".")
            # make sure that each student is assigned for only one oral.
            if self.stu == oral.stu:
                    raise AssertionError('More than one oral are assigned to student ' + str(oral.stu) + ".")
            # refuse to add orals that conflict with personal events.
            for reader in oral.readers:
                if reader.events != []:
                    for event in reader.events:
                        if (oral.dtstart > event.dtstart and oral.dtstart <= event.dtend) or (
                            oral.dtend > event.dtstart and oral.dtend <= event.dtend) or (
                            oral.dtstart <= event.dtstart and oral.dtend >= event.dtend):
                            raise ValueError("Conflicting oral '"+oral.summary+"' and "+str(event.user)+"'s personal event '"+event.summary+"' are added.")
        return reader
    

class OralStartDay(db.Model):
    """
    Contains a description and a start day to select whichever oral week
    the user would want to see
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), unique=True) # ie 'Fall 2016'
    start = db.Column(db.Date, nullable=False)

    def __init__(self, desc, start):
        self.description = desc
        self.start = start

    def __repr__(self):
        return '<%r>' % self.description
