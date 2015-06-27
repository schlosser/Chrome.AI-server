from flask import Flask
import json
from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/')
def hello_world():

  return 'HI!'
