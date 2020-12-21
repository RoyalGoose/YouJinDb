from flask import Flask, request, render_template
from flask_cors import CORS
import json
from pymongo import MongoClient

MongoUrl = 'mongodb://YouJin:YouJinPwd@82.148.31.138:27017/ps?authSource=YouJin'
MongoDb = 'YouJin'
MongoColl = 'YouJinColl'
client = MongoClient(MongoUrl)
db = client[MongoDb]
coll = db[MongoColl]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def dbread(key):
    try:
        if key:
            cursor = coll.find({'id': key})
        else:
            cursor = coll.find({})
        elements = []
        for element in cursor:
            elements.append(element)
        return elements
    except Exception as ex:
        print(ex)
        return 'Failed'


def dbwrite(data):
    try:
        print(data)
        coll.insert_many([data])
        return True
    except Exception as ex:
        print(ex)
        return False


@app.route('/', methods=['POST'])
def mainpost():
    req = request.args.to_dict()
    if dbwrite(req):
        return 'Success'
    else:
        return 'Failed'


@app.route('/', methods=['GET'])
def main():
    req = request.args.to_dict()
    print(req)
    try:
        if 'id' in req.keys():
            data = dbread(req['id'])
        else:
            data = dbread(None)
        result = {}
        for element in data:
            element = dict(element)
            ID = str(element['_id'])
            element.pop('_id')
            result[ID] = element
        return result
    except Exception as ex:
        print(ex)
        return 'Failed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
