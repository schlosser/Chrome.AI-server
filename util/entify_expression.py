from fuzzywuzzy import process

def entify_expression(expression, entities):
    """

    Expression is a string expression like:
       "Buy me a ticket from San Fran to New Ork for 1pm on Thurs"

    Entities are a mapping of keys to string matches:
       {'from_city': 'San Francicso',
        'to_city': 'New York',
        'time': '1pm on Thursday'}

    returns a cleaner expression that perfectly matches the entities:
       "Buy me a ticket from San Francisco to New York for noon at 1am"
    """

    names = entities.values()
    words = expression.split()
    choices = []
    for i in range(len(words)):
        for j in range(i+1, len(words)+1):
            choices.append(' '.join(words[i:j]))

    for key in entities.keys():
        name = entities[key]
        extracted = process.extract(name, choices, limit=5)
        best = extracted[0]

        for choice in extracted[1:]:
            (choice_name, choice_val) = choice
            if choice_val < best[1] or (choice_val == best[1] and len(choice_name) < len(best[0])):
                break
            best = choice

        expression = expression.replace(best[0], name)
    return expression

if __name__ == '__main__':
    print entify_expression('Buy me a ticket from San Fran to New Ork for 1pm on Thursday', {
        'from_city': 'San Francicso',
         'to_city': 'New York',
         'time': '1pm on Thursday'
     })

