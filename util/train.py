import wit_helper as wh
from werkzeug.exceptions import BadRequest
import serialize
from entify_expression import entify_expression


def train(training_dict):

    expression = training_dict.get('expression')
    actions = training_dict.get('intents')
    state = training_dict.get('state')

    if expression is None:
        raise BadRequest(description='bad expression')

    if actions is None:
        raise BadRequest(description='bad intent')

    entities = {}
    for action in actions:
        if action['intentType'] == 'submit':
            entities = dict((serialize.to_string(form_input['selector']), form_input['value']) for \
                form_input in action['data']['inputs'])

    serialized_intent = serialize.to_string(actions)
    expression = entify_expression(expression, entities)

    if wh.check_if_intent_exists(serialized_intent):
        intent_id = wh.add_expressions_to_existing_intent(serialized_intent, [expression])[0]['intent_id']
    else:
        intent_id = wh.add_new_intent_with_expressions(serialized_intent, [expression])['intents'][0]['id']

    wh.add_states_to_intent(serialized_intent, state)

    for action in actions:
        if action['intentType'] == 'submit':
            wh.tag_expression_with_entities(expression, entities, intent_id)


if __name__ == '__main__':

    data = {
        'expression': 'Google Search for cats and dog',
        'intents': [
            {
                'intentType': 'submit',
                'data': {
                    'selector': 'form#foo',
                    'inputs': [
                         {
                            'selector': 'form#foo input[type="text"][name="q"]',
                            'value': 'cats'
                         },

                         {
                            'selector': 'form#foo input[type="text"][name="dogs"]',
                            'value': 'dog'
                         }
                    ]
                }
            }
        ],
        'state': ['google.com']
    }

    train(data)
