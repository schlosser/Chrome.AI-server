import wit_helper as wh
from werkzeug.exceptions import BadRequest
import serialize


def train(training_dict):

    expression = training_dict.get('expression')
    intents = training_dict.get('intents')
    print expression

    if expression is None:
        raise BadRequest(description='bad expression')

    if intents is None:
        raise BadRequest(description='bad intent')

    intent = serialize.to_string(intents)

    print intent

    print wh.check_if_intent_exists(intent)
    if wh.check_if_intent_exists(intent):
        print "adding 0ld"
        wh.add_expressions_to_existing_intent(intent, [expression])
    else:
        print "adding new"
        wh.add_new_intent_with_expressions(intent, [expression])


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
