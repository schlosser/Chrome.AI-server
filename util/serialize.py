import json

REPLACEMENTS = [
    ('\'', '_70'),
    ('\"', '_71'),
    (' ', '_72'),
    ('-', '_73'),
    ('#', '_74'),
    ('.', '_75'),
    (',', '_76'),
    (':', '_77'),
    ('{', '_78'),
    ('}', '_79'),
    ('[', '_80'),
    (']', '_81'),
    ('(', '_82'),
    (')', '_83'),
    ('<', '_84'),
    ('>', '_85'),
    ('/', '_86'),
    ('\\', '_87'),
    ('$', '_88'),
    ('@', '_89'),
    ('!', '_90'),
    ('=', '_91'),
    ('+', '_92'),
    ('*', '_93'),
    ('?', '_94'),
    ('~', '_95')
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
