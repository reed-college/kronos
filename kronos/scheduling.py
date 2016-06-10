
from populatedb import *
from kronos import db
from sqlalchemy.orm import validates
events = Event.query.all()
class Event(db.Model):
    __tablename__ = 'event'
    @validates('dtstart', 'dtend')
    def validate_time(self, dtstart, dtend):
        if self.type != 'oral':
            orals = Oral.query.all()
            for oral in orals:
                if self.user in oral.readers:
                    assert self.dtstart > oral.dtend or self.dtend < oral.dtstart
