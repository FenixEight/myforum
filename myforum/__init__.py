from flask import Flask
from flask.ext.mako import MakoTemplates

app = Flask(__name__)

mako = MakoTemplates(app)
app.config.setdefault('MAKO_TRANSLATE_EXCEPTIONS', False)
app.config['MAKO_TRANSLATE_EXCEPTIONS'] = False

from myforum.controllers import main

