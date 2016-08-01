# This file just makes droping the db when the tests fuck up slightly easier
# So that I don't need to open the shell every time the db refuses to drop
import test
from kronos import db
db.drop_all()
