# CSV PoC

This project provides a small, Flask-based API for processing CSV files.

## Getting Started - Docker
UPDATE THIS AREA ONCE DOCKER IS INVOLVED

## Getting Started - Local/Development

Required packages for this project are in `requirements.txt`, however if you choose to include the development-related tools there is a seperate `requirements_dev.txt`. To install these packages:

```shell script
# in the repository directory, set up the virtual environment
$ python3 -m venv venv

# activate the environment
$ . ./venv/bin/activate

# install deps
$ pip install -r requirements.txt
```

Next, you can set environment variables and run the Flask application:

```shell
# for more debug-related data in the logs, set the environment
$ export FLASK_ENV=development

# point the Flask CLI to the local run file
$ export FLASK_APP=autoapp.py

# the application defaults to a local SQLite database so this is NOT NEEDED, but if that needs
# to be changed to something else, set that here
$ export DATABASE_URI=<database URI string>

# set up the database tables
$ flask db migrate

# run the application
$ flask run
```

With all the defaults being used, the API Swagger page can now be accessed at [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

## Architecture

### Structure

Though this is a very small API, this project embraces Flask's [Blueprint](https://flask.palletsprojects.com/en/2.1.x/blueprints/#why-blueprints) system to keep code modular from the beginning.

Directory structure is laid out like so:

```shell script
csv_poc/
├── api
│   └── v1
│       └── __init__.py
├── database
│   └── __init__.py
└── utils
    └── exc.py
├── app.py
├── extensions.py
├── settings.py

```

UPDATE THIS WITH PER-DIRECTORY DESCRIPTIONS

### Database

This project uses SQLite for the lightweight needs of the API. 
