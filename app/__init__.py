from flask import Flask
from flask.ext.cors import CORS, cross_origin
from routes import api

app = None

def create_app():
    """Setup code to create flask app."""

    global app
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)

    return app