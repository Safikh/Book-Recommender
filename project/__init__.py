from flask import Flask
from project.core.views import core
from project.error_pages.handlers import error_pages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

app.register_blueprint(core)
app.register_blueprint(error_pages)
