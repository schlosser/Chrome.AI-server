from flask import Blueprint, request
from util.json_response import json_success, json_error_message
from util.wit_helper import get_all_intents, get_all_entities
from util.train import train

api = Blueprint('api', __name__)


class APIException(Exception):

    def __init__(self, message="Invalid parameters"):
        self.message = message


@api.route('/')
def hello_world():
    return json_success("Hello World!")


@api.route('/train', methods=['POST'])
def new_training_data():
    # parse expression
    expression = request.form.get('expression')
    if not expression:
        return json_error_message('Missing expression',
                                  error_data=request.form)

    # parse confience
    confidence = request.form.get('confidence')
    if not confidence:
        return json_error_message('Missing confidence',
                                  error_data=request.form)
    confidence = int(confidence)

    # parse intents
    intents = request.form.getlist('intents')
    intents = [intent for intent in intents if intent]
    if not intents:
        return json_error_message('Missing intents',
                                  error_data=request.form)

    # train
    train(expression, confidence, intents)
    return json_success('Training data added successfully')


def _validate(fieldname, type):
    field = request.form[fieldname]

    return field


@api.route('/train', methods=['GET'])
def test_train_route():
    return '''
<form method="POST" action="/train">
Expression: <input type="text" name="expression"><br>
Confidence: <input type="number" name="confidence"><br>
Intents[0]: <input type="text" name="intents"><br>
Intents[1]: <input type="text" name="intents"><br>
Intents[2]: <input type="text" name="intents"><br>
<button type="submit">Submit</button></form>
    '''


@api.route('/training_data')
def view_training_data():
    return json_success({
        'intents': get_all_intents(),
        'entities': get_all_entities()
    })
