# Taken from flask by example, part 2
# https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from kronos import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
