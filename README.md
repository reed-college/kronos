# Kronos ![travisci-status](https://travis-ci.org/reed-college/kronos.svg?branch=master)
flask site for scheduling and viewing orals

## Setup
* Make sure you have python 3.5.1 and postgres 9.5.1
* make a new db in postgres, I called mine `kronos_dev`
* type `git clone https://github.com/reed-college/kronos.git`
* make a virtualenv see (here)[http://docs.python-guide.org/en/latest/dev/virtualenvs/]
  *  basically in this project directory run `virtualenv -p /path/to/python3 .`
* run `cp kronos/config.py.template kronos/config.py`
* edit `config.py` to have the correct postgres URI for the db you just created
  * Make sure the username and password you type in are for a user who can edit the db, such as the owner
* run `python manage.py db upgrade`
* then you should be good to go, run `python runserver.py` and go to `localhost:5000/`

## Running Tests
* Run `py.test` in the home directory
  * make sure you have a test database set up (see under 'More Detailed DB setup)
* If you're a contributor you don't *need* to do that as your tests will get run on Travis ([travis-ci.org](https://travis-ci.org/)), but that usually takes about a minute longer than running them locally

## More Detailed DB setup
This is exactly how I set my db, you don't need to follow it exactly for it to work, but it may be useful if you're not used to postgres
* launch `psql` in the command line
* typing `\conninfo` will tell you what port to enter into the URI under the `Config` class in `config.py`
  * with default postgres settings, the `host:port` section of the URI should be `localhost:5432`, but coninfo will tell you exactly what port if its not 5432
* type in `CREATE ROLE kronos_dev_user WITH LOGIN PASSWORD 'password' CREATEDB;`
  * then `username:password` in the URI should be `kronos_dev_user:password`
* enter in `CREATE DATABASE kronos_dev WITH OWNER kronos_dev_user;`
  * in this case the `/mydatabase` part of the URI should be `/kronos_dev`
* If you followed this guide exactly and used the default postgres port, the full URI would be, `postgresql+psycopg2://kronos_dev_user:password@localhost:5432/kronos_dev`
* You also should make a test database and enter its URI under `TestConfig` in `config.py`
  * if you type `CREATE DATABASE kronos_test WITH OWNER kronos_dev_user;` into psql, then the URI should be `postgresql+psycopg2://kronos_dev_user:password@localhost:5432/kronos_test`, assuming you did everything else in this guide the same

## Migrations
First time setup:
 * Start with empty db
 * run `python manage.py db upgrade`

After making any changes to  `models.py` you must:
 * run `python manage.py db migrate`
 * run `python manage.py db upgrade`
 * add the new migrations to source control (`git add -A` should do  it)
 * push changes to master soon after so that everyone else can get these changes before they change the models as well

After pulling someone elses new migrations:
 * run `python manage.py db upgrade`
