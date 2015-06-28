import requests
import urllib
import json

app_id = '558ee6bf-0b74-450c-858c-08dad79ff974'
server_access_token = 'AM6WLX35JI3LRSB74VTQEUTYKHJPEXFP'

headers = {'Authorization': 'Bearer ' + server_access_token}


def get_all_intents():

    response = requests.get('https://api.wit.ai/intents?v=20150627', headers = headers)
    return response.json()


def get_all_entities():

    response = requests.get('https://api.wit.ai/entities?v=20150627', headers = headers)
    return response.json()


def get_intent_from_text(text):

    encoded_text = urllib.quote(text)
    response = requests.get('https://api.wit.ai/message?v=20150627&q=' + encoded_text, headers = headers)

    return response.text


def add_new_intent_with_expressions(intent, expressions):
    "Expressions is a list of strings to add to the given intent"

    expressions_list = []

    for expression in expressions:
        to_append = {'body': expression}
        expressions_list.append(to_append)

    payload = {
        'name': intent,
        'expressions': expressions_list
    }

    response = requests.post('https://api.wit.ai/intents?v=20150627', headers=headers, data=json.dumps(payload))

    return response.json()


def add_expressions_to_existing_intent(intent, expressions):
    "Expressions is a list of strings to add to the given intent"
    payload = []

    for expression in expressions:
        payload.append({'body': expression})

    post_url = 'https://api.wit.ai/intents/' + intent + '/expressions?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(payload))

    return response.json()


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


    post_url = 'https://api.wit.ai/entities?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(payload))

    if not response.ok:
        print response.text
    return response.json()

def get_entity_by_id(entity_id):
    """Gets an entity by id."""
    response = requests.get('https://api.wit.ai/entities/' + entity_id +'?v=20150627', headers=headers)
    if not response.ok:
        print 'text: ', response.text
    return response.json()


def add_value_to_existing_entity(entity_id, value):
    """Value is a dictionary:

    {
        'value':'Paris',
        'expressions':['Paris','City of Light','Capital of France']
    }
    """

    post_url = 'https://api.wit.ai/entities/' + entity_id + '/values?v=20150627'
    response = requests.post(post_url, headers=headers, data=json.dumps(value))

    return response.json()


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

    return response.json()


def wipe_intent(name):

    delete_url = 'https://api.wit.ai/intents/' + name + '?v=20150627'
    requests.delete(delete_url, headers=headers)


def wipe_entity(name):

    delete_url = 'https://api.wit.ai/entities/' + name + '?v=20150627'
    requests.delete(delete_url, headers=headers)


def wipe_data():
    """Wipe all data in wit.ai
    """

    intents = get_all_intents()
    entities = get_all_entities()

    for intent in intents:
        wipe_intent(intent.get('name'))

    for entity in entities:
        if not entity.startswith('wit$'):
            wipe_entity(entity)

def get_states_from_intent(intent):

    request_url = 'https://api.wit.ai/intents/' + intent + '?v=20150627'
    response = requests.get(request_url, headers = headers)

    meta = response.json().get('meta')
    if meta:
        return meta.get('states', [])

    return []

def add_states_to_intent(intent, states):
    """States is an array"""

    states += get_states_from_intent(intent)
    states = list(set(states))

    payload = {
        'meta': {
            'states': states
        }
    }

    post_url = 'https://api.wit.ai/intents/' + intent + '?v=20150627'
    response = requests.put(post_url, headers=headers, data=json.dumps(payload))

    return response.text


def show_expressions_for_intent(intent):

    request_url = 'https://api.wit.ai/intents/' + intent + '?v=20150627'
    response = requests.get(request_url, headers=headers)
    if not response.ok:
        print response.text

    return response.json()


def add_entities_to_intent(intent, expressions):

    post_url = 'https://api.wit.ai/intents/' + intent + '?v=20150627'
    response = requests.put(post_url, headers=headers, data=json.dumps(expressions))

    return response.text


def tag_expression_with_entities(expression_body, entities, intent_id):

    for entity_id, value in entities.iteritems():

        if not entity_id in get_all_entities():
            create_entity(entity_id, [{'value': value, 'expressions': [value]}])

        expression = [exp for exp in show_expressions_for_intent(intent_id)['expressions'] if exp['body'] == expression_body][0]

        entity = get_entity_by_id(entity_id)

        tag_expression_with_entity(expression, entity, value, intent_id)


def tag_expression_with_entity(expression, entity, value, intent_id):
    sync_headers = {
        'Authorization': 'Bearer U3HCPMX47IB7QHFAYR7EK7LGOCY3ESVE',
        'Origin': 'https://wit.ai',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.wit.20150405+json',
        # 'Referer': 'https://wit.ai/benthehenten/speakeasy/intents/walk_the_hog',
        'Connection': 'keep-alive',
        'X-Wit-Instance': '558ee6bf-0b74-450c-858c-08dad79ff974'
    }
    data = [{
        'data': {
            'semantic':{
                'entities': [{
                    'start': expression['body'].find(value),
                    'end': expression['body'].find(value) + len(value),
                    'value': value,
                    'wisp': entity['name']  #'558f9714-538e-4f98-aec0-2400e80bcafc' # wisp of the entity
                }],
                'intent': intent_id  # '87b45c4b-daf0-4b0e-a57a-c74160aa4291' # intent to associate with
            },
            'text': {
                'id': expression['id'],  # '558f93fd-a2d7-451d-af81-72367e672bee', #
                'text': expression['body']
            }
        },
        'type': 'added-semantic'
    }]

    response = requests.put('https://api.wit.ai/sync', headers=sync_headers, data=json.dumps(data))


if __name__ == '__main__':
    #add_new_intent_with_expressions('walk_the_hog', ['walk my cool hog'])
    pass
    # print create_entity('animal')
    # print show_expressions_for_intent('walk_the_hog')


    # expressions = [
    #     {
    #         'body': 'go walk my hog',
    #         'entities': [{
    #             'body': 'hog',
    #             'wisp': '558f9714-538e-4f98-aec0-2400e80bcafc',
    #             'value': 'hog',
    #             'start': 11,
    #             'end': 14,
    #             'name': 'animal',
    #             'lang': 'en',
    #             'subentities': []
    #         }]
    #     }
    # ]
    # print add_entities_to_intent('walk_the_hog', expressions)



    # print show_expressions_for_intent('walk_the_hog')

    #wipe_data()
    #print get_intent_from_text('google search for dogs')
    # print add_new_intent_with_expressions('walk_the_hog', ['walk my hog, son!'])
    # add_states_to_intent('walk_the_hog', ['new.ycombinator.com'])
    # add_states_to_intent('walk_the_hog', ['maj.com'])
    # add_states_to_intent('walk_the_hog', ['maj.com'])
    # print get_states_from_intent('walk_the_hog')
    # print show_expressions_for_intent('walk_the_hog')
    #print add_state_to_intent('walk_the_hog')
    #add_new_intent_expression_mapping('click_logout_button', 'log me out')
    #get_intent_from_text('log me out')
    # print add_expressions_to_existing_intent('walk_the_hog', ['wash the hog'])

    # values = [
    #     {"value":"Paris",
    #      "expressions":["Paris","City of Light","Capital of France"]
    #     },
    #     { "value":"Delicious",
    #      "expressions":["Delicious", "Tasty", "Bacony"]
    #     }
    # ]
    #print add_values_to_existing_entity('hog_taste', values)

    # print get_all_entities()

    #print add_new_intent_with_expressions('walk_the_snake', ['walk my snake'])

    #print check_if_intent_exists('{"data": {"innerText": "Login", "selector": "div#foo"}, "intentType": "click"}')

    #create_entity("<#$(#COOL")
    #print add_expressions_to_existing_intent('walk_the_zeebra', ['walk my animal safari'])
    #print wipe_data()
