from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('kronos.config.DevelopmentConfig')
db = SQLAlchemy(app)
from kronos.models import db
import kronos.models as models
db.create_all()
import kronos.views
