import os
from flask import Flask
from flask_mako import MakoTemplates


app = Flask(__name__)

mako = MakoTemplates(app)
app.config.setdefault('MAKO_TRANSLATE_EXCEPTIONS', False)
app.config['MAKO_TRANSLATE_EXCEPTIONS'] = False
UPLOAD_FOLDER = "static/avatars/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from myforum.lib.db import DataService
from myforum.controllers import main
from myforum.controllers import comment

connection_string = "host='localhost' port=5432 dbname='myforum' user='postgres' password='0932512759'"

app.db = DataService(connection_string)



