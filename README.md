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
  * Make sure the username and password you type in are for a user who can edit the db, like the owner
* then you should be good to go, run `python runserver.py` and go to `localhost:5000/`

## More Detailed DB setup
This is exactly how I set my db, you don't need to follow it exactly for it to work, but it may be useful if you're not used to postgres
* launch `psql` in the command line
* typing `\conninfo` will tell you what port to enter into the URI in `config.py`
  * with default postgres settings, the `host:port` section of the URI should be `localhost:5432`, but coninfo will tell you exactly what port if its not 5432
* type in `CREATE ROLE kronos_dev_user WITH LOGIN PASSWORD 'password' CREATEDB;`
  * then `username:password` in the URI should be `kronos_dev_user:password`
* enter in `CREATE DATABASE kronos_dev WITH OWNER kronos_dev_user;`
  * in this case the `/mydatabase` part of the URI should be `/kronos_dev`
* If you followed this guide exactly and used the default postgres port, the full URI would be, `postgresql+psycopg2://kronos_dev_user:password@localhost:5432/kronos_dev`
