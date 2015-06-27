import requests
import urllib
import json

app_id = '558ee6bf-0b74-450c-858c-08dad79ff974'
server_access_token = 'AM6WLX35JI3LRSB74VTQEUTYKHJPEXFP'

headers = {'Authorization': 'Bearer ' + server_access_token}


def get_all_intents():

    response = requests.get('https://api.wit.ai/intents?v=20150627', headers = headers)
    return json.dumps(response.text)


def get_all_entities():

    response = requests.get('https://api.wit.ai/entities?v=20150627', headers = headers)
    return json.dumps(response.text)


def get_intent_from_text(text):

    encoded_text = urllib.quote(text)
    response = requests.get('https://api.wit.ai/message?v=20150627&q=' + encoded_text, headers = headers)

    return response.text


def add_new_intent_with_expressions(intent, expression):
    "Expressions is a list of strings to add to the given intent"
    payload = {
        'name': intent,
        'expressions': [
            {'body' : expression}
        ]
    }

    response = requests.post('https://api.wit.ai/intents?v=20150627', headers=headers, data=json.dumps(payload))

    return response.text


def add_expressions_to_existing_intent(intent, expressions):
    "Expressions is a list of strings to add to the given intent"
    payload = []

    for expression in expressions:
        payload.append({'body': expression})

    post_url = 'https://api.wit.ai/intents/' + intent + '/expressions' + '?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(payload))

    return response.text


def check_if_intent_exists(intent):

    response = requests.get('https://api.wit.ai/intents?v=20150627', headers = headers)
    response_json = json.loads(response.text)

    for existing_intent in response_json:
        if existing_intent.get('name') == intent:
            return True

    return False


def create_entity(entity_id, values=None):
    """Values is an array of dictionaries with values that map to expressions.
    Example:

    [
        { "value":"Paris",
         "expressions":["Paris", "City of Light", "Capital of France"]
        },
        { "value":"New York",
         "expressions":["New York", "Big Apple", "Best city"]
        }
    ]

    """
    payload = {
        'id': entity_id,
    }

    if values:
        payload['values'] = values


    print payload
    post_url = 'https://api.wit.ai/entities?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(payload))

    return response.text

def add_value_to_existing_entity(entity_id, value):
    """Value is a dictionary:

    {
        'value':'Paris',
        'expressions':['Paris','City of Light','Capital of France']
    }
    """
    print json.dumps(value)

    post_url = 'https://api.wit.ai/entities/' + entity_id + '/values?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(value))

    return response.text


def add_values_to_existing_entity(entity_id, values):
    """Value is a dictionary:

    {
        'value':'Paris',
        'expressions':['Paris','City of Light','Capital of France']
    }
    """

    payload = {
        'values': values #a list of value objects
    }

    post_url = 'https://api.wit.ai/entities/' + entity_id + '?v=20150627'
    response = requests.put(post_url, headers=headers, data=json.dumps(payload))

    return response.text




if __name__ == '__main__':
    pass
    #add_new_intent_expression_mapping('click_logout_button', 'log me out')
    #get_intent_from_text('log me out')
    # add_expressions_to_existing_intent('clean_the_hog', ['wash the hog'])
    # create_entity('hog_taste', [{ "value":"Delicious",
         #"expressions":["Delicious", "Tasty", "Bacony"]}])
    # values = [
    #     {"value":"Paris",
    #      "expressions":["Paris","City of Light","Capital of France"]
    #     },
    #     { "value":"Delicious",
    #      "expressions":["Delicious", "Tasty", "Bacony"]
    #     }
    # ]
    #print add_values_to_existing_entity('hog_taste', values)

    print get_all_entities()
