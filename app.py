from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

MongoUrl = 'mongodb://YouJin:YouJinPwd@82.148.31.138:27017/ps?authSource=YouJin'
MongoDb = 'YouJin'
MongoColl = 'YouJinColl'
client = MongoClient(MongoUrl)
db = client[MongoDb]
coll = db[MongoColl]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def slog(type='info', txt=''):
    txt = type + datetime.now().strftime(" %d.%m.%Y %H:%M:%S.%f ") + str(txt) + '\n'
    # print(txt.replace('\n', ''))
    f = open('server.log', 'a', encoding='utf-8')
    f.write(txt)
    f.close()


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
        slog('exep', '| dbread | %s' % ex)
        return 'Failed'


def dbwrite(data):
    try:
        print(data)
        coll.insert_many([data])
        return True
    except Exception as ex:
        slog('exep', '| dbwrite | %s' % ex)
        return False


def dbdelete(data):
    try:
        coll.remove({'id': data})
        return True
    except Exception as ex:
        slog('exep', '| dbdelete | %s' % ex)
        return False


@app.route('/', methods=['POST'])
def mainpost():
    slog('info', '| post | Request from %s' % request.remote_addr)
    req = request.args.to_dict()
    if 'action' in req.keys() and req.get('action') == 'delete':
        if dbdelete(req['id']):
            return 'Success'
        else:
            return 'Failed'
    else:
        if dbwrite(req):
            return 'Success'
        else:
            return 'Failed'


@app.route('/', methods=['GET'])
def main():
    slog('info', '| main | Request from %s' % request.remote_addr)
    req = request.args.to_dict()
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
        slog('exep', '| main | %s' % ex)
        return 'Failed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
