from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# creating the app
app = Flask(__name__)
app.config.from_object('kronos.config.DevelopmentConfig')
Bootstrap(app)
# initializing the db
db = SQLAlchemy(app)
from kronos.models import db
import kronos.models as models
db.create_all()
# importing the views
import kronos.views
