import json

REPLACEMENTS = [
    ('\'', '_9470'),
    ('\"', '_9471'),
    (' ', '_9472'),
    ('-', '_9473'),
    ('#', '_9474'),
    ('.', '_9475'),
    (',', '_9476'),
    (':', '_9477'),
    ('{', '_9478'),
    ('}', '_9479'),
    ('[', '_9480'),
    (']', '_9481'),
    ('(', '_9482'),
    (')', '_9483'),
    ('<', '_9484'),
    ('>', '_9485'),
    ('/', '_9486'),
    ('\\', '_9487'),
    ('$', '_9488'),
    ('@', '_9489'),
    ('!', '_9490'),
    ('=', '_9491'),
    ('+', '_9492'),
    ('*', '_9493'),
    ('?', '_9494'),
    ('~', '_9495')
]


def to_string(data):
    json_string = json.dumps({'data': data}, sort_keys=True)
    for char, encoding in REPLACEMENTS:
        json_string = json_string.replace(char, encoding)
    return 'ENC' + json_string


def from_string(json_string):
    for char, encoding in REPLACEMENTS:
        json_string = json_string.replace(encoding, char)
    return json.loads(json_string[3:])['data']
