from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Jiahui:password@localhost/db_kronos'
db = SQLAlchemy(app)
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.Text)
    email = db.Column(db.String(120), unique = True)
    department = db.Column(db.String(50))

    def __init__(self, username, name, password, email, department):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.department = department

    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    id = db.Column(db.String(40), primary_key = True)
    summary = db.Column(db.Text)
    dtstart = db.Column(db.DateTime)
    dtend = db.Column(db.DateTime)
    status = db.Column(db.Enum('busy', 'free'))
    private = db.Column(db.Boolean)
    oral = db.Column(db.Boolean)

    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('event')) # lazy???

    def __init__(self, summary, dtstart, dtend, user, private = True, oral = False):
        self.summary = summary
        self.dtstart = dtstart
        self.dtend = dtend
        self.status = status
        self.user = user
        
    def __repr__(self):
        return '<Event %r>' % self.summary

class Oral(db.Model):
    id = db.Column(db.String(40), primary_key = True)
    response = db.Column(db.Enum('Accepted', 'Declined'))

    attendee_userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('oral'))

    def __init__(self, user, response = None):
        self.user = user

    def __repr__(self):
        return '<Oral>'







