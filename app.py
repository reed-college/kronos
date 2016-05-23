from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://kronos_dev_user:password@localhost:5432/kronos_dev'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/")
def hello():
    users = ""
    for user in User.query.all():
        users += user.username + "\n\n"
    return "Hello World!\n\n" + users

@app.route("/<name>")
def makeuser(name):
    db.session.add(User(name, name + '@example.com'))
    db.session.commit()
    return "created user " + name

if __name__ == "__main__":
    app.run()