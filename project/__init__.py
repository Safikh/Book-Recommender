from flask import Flask
from project.core.views import core

app = Flask(__name__)
app.register_blueprint(core)
