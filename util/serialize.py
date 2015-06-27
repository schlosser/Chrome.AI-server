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
    (')', '_9483')
]


def to_string(dict):
    json_string = json.dumps(dict, sort_keys=True)
    for char, encoding in REPLACEMENTS:
        json_string = json_string.replace(char, encoding)
    return 'ENC' + json_string
