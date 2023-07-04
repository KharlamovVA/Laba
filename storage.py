import tempfile
import os
import json
import argparse

temp_path = os.path.join(tempfile.gettempdir(), 'storage.data')

def get_data():
    if not os.path.exists(temp_path):
        return {}

    with open(temp_path, 'r') as file:
        raw_data = file.read()
        if raw_data:
            return json.loads(raw_data)
        return {}

def put(key, value):
    data = get_data()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]

    with open(temp_path, 'w') as file:
        file.write(json.dumps(data))

def get(key):
    data = get_data()
    return data.get(key)

def clear():
    os.remove(temp_path)

parser = argparse.ArgumentParser()
parser.add_argument('--key')
parser.add_argument('--val')
parser.add_argument('--clear', action='store_true', help='Clear')

args = parser.parse_args()

try:
    if args.key and args.val:
        put(args.key, args.val)
    elif args.key:
        print(get(args.key))
    elif args.clear:
        clear()    
    else:
        print('Wrong command')
except FileNotFoundError:
    print('No data')