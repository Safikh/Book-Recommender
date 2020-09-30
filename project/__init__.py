from flask import Flask
from project.core.views import core

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

app.register_blueprint(core)
