from flask import Flask
from .blueprints.user_api import *

app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(user_api, url_prefix='/user_api')
