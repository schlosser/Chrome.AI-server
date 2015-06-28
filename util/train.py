import wit_helper as wh
from werkzeug.exceptions import BadRequest
import serialize


def train(training_dict):

    expression = training_dict.get('expression')
    intents = training_dict.get('intents')
    state = training_dict.get('state')

    if expression is None:
        raise BadRequest(description='bad expression')

    if intents is None:
        raise BadRequest(description='bad intent')

    intent = serialize.to_string(intents)

    if wh.check_if_intent_exists(intent):
        wh.add_expressions_to_existing_intent(intent, [expression])
    else:
        wh.add_new_intent_with_expressions(intent, [expression])

    wh.add_states_to_intent(intent, state)

if __name__ == '__main__':

    data = {
        'expression': 'click the login button',
        'intents': [
            {
                'intentType': 'click',
                'data': {
                    'selector': 'div#foo',
                    'innerText': 'Login'
                }
            }
        ]
    }

    train(data)
