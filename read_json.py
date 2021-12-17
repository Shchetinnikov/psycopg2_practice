import json

def get_json(name):
    data = {}
    with open(f'{name}.json', 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


if __name__ == '__main__':
    print("Empty program 'read_json'")