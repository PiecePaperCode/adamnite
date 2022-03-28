def json(to_serialize) -> dict:
    dictionary = {}
    for name, value in vars(to_serialize).items():
        if name.startswith('__'):
            continue
        if isinstance(value, (str, int, float, list, dict)):
            dictionary.update({name: value})
    return dictionary
