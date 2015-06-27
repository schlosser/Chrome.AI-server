from flask import Blueprint, request
from werkzeug.exceptions import BadRequest
from util.json_response import json_success, json_error_message
from util.wit_helper import get_all_intents, get_all_entities
from util.train import train

api = Blueprint('api', __name__)
NO_JSON = "Found no JSON.  Did you set Content-Type: application/json?"


@api.route('/')
def hello_world():
    return json_success("Hello World!")


@api.route('/train', methods=['POST'])
def new_training_data():
    try:
        training_data = request.get_json()
        if training_data is None:
            raise BadRequest(description=NO_JSON)
        train(training_data)
    except BadRequest as e:
        print e, e.description
        return json_error_message('Failed to parse JSON data',
                                  error_data=e.description)

    return json_success('Training data added successfully')


@api.route('/training_data')
def view_training_data():
    return json_success({
        'intents': get_all_intents(),
        'entities': get_all_entities()
    })
