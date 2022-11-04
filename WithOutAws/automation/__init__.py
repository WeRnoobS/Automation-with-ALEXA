import logging
from flask.app import Flask
from flask_ask import Ask
from os import getenv

if getenv('FLASK_DEBUG') == 'development':
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)
    logging.getLogger(__name__).setLevel(logging.DEBUG)

app=Flask(__name__)
ask=Ask(app,'/')


logger = app.logger

from . import intents
