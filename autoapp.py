"""Main entrypoint for the application.

This file is meant to be used in conjunction with the Flask CLI in order to run
the Flask development server.

  Typical usage (in a shell environment):

  $ . ./venv/bin/activate
  $ export FLASK_APP=autoapp.py
  $ export FLASK_ENV=development
  $ flask run

"""
from csv_poc.app import create_app

app = create_app()
