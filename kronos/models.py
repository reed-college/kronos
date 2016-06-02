from kronos import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Enum, ForeignKey

department = ('Anthropology', 'Art', 'Biology', 'Chemistry', 'Chinese',
              'Classics', 'Dance', 'Economics', 'English', 'French', 'German',
              'History', 'Linguistics', 'Mathematics', 'Music', 'Philosophy',
              'Physics', 'Political Science', 'Psychology', 'Religion',
              'Russian', 'Sociology', 'Spanish', 'Theatre')
division = ('The Arts', 'History and Social Sciences',
            'Literature and Languages', 'Mathematics and Natural Sciences',
            'Philosophy, Religion, Psychology and Linguistics')

# The User class contains professors and students,
# but that does not mean that they are the actual "users" of this website
# (at least not for now).


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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


class FAC(User):
    def __init__(self, username, name, password, email):
        User.__init__(self, username, name, password, email)
        self.type = 'FAC'


class Prof(User):
    department = db.Column("department",
                           db.Enum(*department, name="department"))
    division = db.Column("division", db.Enum(*division, name="division"))
    __mapper_args__ = {'polymorphic_identity': 'professor'}
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)

    @declared_attr
    def department(cls):
        "Department column, if not present already."
        return User.__table__.c.get('department',
                                    Enum(*department, name="department"))

    @declared_attr
    def division(cls):
        "Division column, if not present already."
        return User.__table__.c.get('division',
                                    Enum(*division, name="division"))

    def __init__(self, username, name, password, email, department, division):
        User.__init__(self, username, name, password, email)
        self.department = department
        self.division = division
        self.type = 'professor'

    def __repr__(self):
        return '<%r>' % self.username


class Stu(User):
    department = db.Column("department",
                           db.Enum(*department, name="department"))
    division = db.Column("division", db.Enum(*division, name="division"))
    __mapper_args__ = {'polymorphic_identity': 'student'}
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)

    @declared_attr
    def department(cls):
        "Department column, if not present already."
        return User.__table__.c.get('department',
                                    Enum(*department, name="department"))

    @declared_attr
    def division(cls):
        "Division column, if not present already."
        return User.__table__.c.get('division',
                                    Enum(*division, name="division"))

    def __init__(self, username, name, password, email, department, division):
        User.__init__(self, username, name, password, email)
        self.department = department
        self.division = division
        self.type = 'student'

    def __repr__(self):
        return '<%r>' % self.username


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(40), primary_key=True)
    summary = db.Column(db.Text)
    dtstart = db.Column(db.DateTime, nullable=False)
    dtend = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('busy', 'free', name='status'))
    private = db.Column(db.Boolean)
    discriminator = db.Column('type', db.String(10))
    __mapper_args__ = {'polymorphic_on': discriminator}

    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('event'))  # lazy???

    def __init__(self, summary, dtstart, dtend, user,
                 private=True, status='busy'):
        self.summary = summary
        self.dtstart = dtstart
        self.dtend = dtend
        self.status = status
        self.user = user

    def __repr__(self):
        if self.private is False:
            return '<Event %r>' % self.summary
        else:
            return '<Not available>'

attendees = db.Table('attendees',
    db.Column('attendee_id', db.Integer, db.ForeignKey('prof.id')),
    db.Column('oral_id', db.String(40), db.ForeignKey('orals.id'))
    )



class Oral(db.Model):
    __tablename__ = 'orals'
    __mapper_args__ = {'polymorphic_identity': 'oral'}
    id = db.Column(db.String(40), ForeignKey('events.id'), primary_key=True)
    response = db.Column(db.Enum('Accepted', 'Declined', 'Tentative',
                                 name="response"))

    attendees = db.relationship('Prof', 
                                secondary = attendees, 
                                backref = db.backref('oral'))
    
    stu_id = db.Column(db.Integer, db.ForeignKey('stu.id'))
    stu = db.relationship('Stu', backref=db.backref('oral'))

    def __init__(self, stu, prof, summary, dtstart, dtend, user,
                 response=None):
        Event.__init__(self, summary, dtstart, dtend, user)
        self.user = user
        self.stu = stu
        self.prof = prof

    def __repr__(self):
        return '<%rs Oral>' % self.stu




# Example:
# Adding myself:
# me = Stu('weij', 'Jiahui', “asd", 'weij@reed.edu', 'Physics',
#          'Mathematics and Natural Sciences' )
