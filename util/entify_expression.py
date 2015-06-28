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
    mapping = {
    '1st': '01',
    '2nd': '02',
    '3rd': '03',
    '4th': '04',
    '5th': '05',
    '6th': '06',
    '7th': '07',
    '8th': '08',
    '9th': '09',
    '10th': '10',
    '11th': '11',
    '12th': '12',
    '13th': '13',
    '14th': '14',
    '15th': '15',
    '16th': '16',
    '17th': '17',
    '18th': '18',
    '19th': '19',
    '20th': '20',
    '21st': '21',
    '22nd': '22',
    '23rd': '23',
    '24th': '24',
    '25th': '25',
    '26th': '26',
    '27th': '27',
    '28th': '28',
    '29th': '29',
    '30th': '30',
    '31th': '31'
    };

    for key in mapping.keys():
        expression = expression.replace(key, mapping[key])

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
    # print entify_expression('Buy me a ticket from San Fran to New Ork for 1pm on Thursday', {
    #     'from_city': 'San Francicso',
    #      'to_city': 'New York',
    #      'time': '1pm on Thursday'
    #  })

    print entify_expression("I'm booking a flight from Boston to San Francisco on July 3rd to July 5th for one person and coach", {
        'from': 'San Francisco, CA',
        'to': 'Boston, MA',
        'on': 'Jul 03',
        'then': 'Jul 05'
    })