import tempfile
import os
import json
from flask import Flask, request, make_response
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

temp_path = os.path.join(tempfile.gettempdir(), 'storage.data')

def get_data():
    if not os.path.exists(temp_path):
        return {}
    with open(temp_path, 'r') as file:
        raw_data = file.read()
        if raw_data:
            text = json.loads(raw_data)
            return text
        return {}
    

# show a main list
class Title(Resource):
    def get(self):
        response = make_response("Хранилище ключ-значение.", 200)
        response.mimetype = "text/plain"
        return response
    
# show a single item
class Storage(Resource):
    def get(self):
        key = request.args.get('key')
        data = get_data()
        return data.get(key)

# show a list of all items
class StorageList(Resource):
    def get(self):
        return get_data()

# write item to file
class StorageWrite(Resource):
    def post(self):
        req = json.loads(request.data)
        data = get_data()
        for key in req.keys():
            value = req[key]
            if key in data:
                data[key].append(value)
            else:
                data[key] = [value]
        with open(temp_path, 'w') as file:
            file.write(json.dumps(data))
        response = make_response("Success add date", 200)
        response.mimetype = "text/plain"
        return response

##
## Actually setup the Api resource routing here
##
api.add_resource(Title, '/')
api.add_resource(StorageList, '/api/v1/storage/json/all')
api.add_resource(Storage, '/api/v1/storage/json/read')
api.add_resource(StorageWrite, '/api/v1/storage/json/write')

if __name__ == '__main__':
    app.run(debug=True)