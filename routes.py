from flask import Blueprint, request, redirect, url_for
from werkzeug.exceptions import BadRequest
from util.json_response import json_success, json_error_message
from util.wit_helper import get_all_intents, get_all_entities, wipe_data, show_expressions_for_intent
from util.train import train
import json
from util import serialize

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


@api.route('/_/fire')
def kill_it_with_fire():
    wipe_data()
    return redirect(url_for('.view_training_data'))


@api.route('/training_data')
def view_training_data():
    intents = get_all_intents()
    entities = get_all_entities()

    return json_success({
        'intents': intents,
        'entities': entities
    })

@api.route('/intent/<intent>/expressions')
def show_expressions(intent):
    return json_success({
        'data': show_expressions_for_intent(intent)
    })

@api.route('/troy')
def show_human_data():
    intents = get_all_intents()

    for intent in intents:
      intent['expressions'] = show_expressions_for_intent(intent.get('name'))
      intent['name'] = serialize.from_string(intent.get('name'))

    return json_success({
        'intents': intents
    })
