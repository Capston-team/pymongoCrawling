from flask import Flask
from flask import make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from apscheduler.schedulers.blocking import BlockingScheduler
from skt import skt_info, skt_date, skt_image
from kt import kt_title, kt_date, kt_image
import json

sched = BlockingScheduler()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_database():
    ca = certifi.where()

    CONNECTION_STRING = "mongodb+srv://YoungWoo:vbn752014&@capstone.qv9bkyx.mongodb.net/?retryWrites=true&w=majority&ssl=true"

    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client['event']


@sched.scheduled_job('interval', hours=24)
def UpdateEventList():
    dbname = get_database()

    skt = dbname['skt']
    kt = dbname['kt']
    lg = dbname['lg']

    SktResultSet = dict({'title': skt_info(), 'date': skt_date(), 'img': skt_image()})
    KtResultSet = dict({'title': kt_title(), 'date': kt_date(), 'img': kt_image()})
    LgResultSet = dict({})

    # items_detail = kt.find({'_id': ObjectId('6330017d0af9348ced24899f')})

    skt.update_one({'_id': ObjectId('633007e552ef499751ceb548')}, {"$set": SktResultSet})
    kt.update_one({'_id': ObjectId('6330017d0af9348ced24899f')}, {"$set": KtResultSet})

    # return make_response(json.dumps(resultSet, ensure_ascii=False).encode('utf-8'))
    print("Successful Update eventList")
    return 'UpdateEventList'


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('Test log interval 3MIN')


@app.route('/')
def hello_world():
    UpdateEventList()
    return 'Hello_world'


if __name__ == "__main__":

    # item_details = skt.find({'_id': ObjectId('633007e552ef499751ceb548')})
    # for item in item_details:
    #     print(item)

    # skt.update_one({'_id': ObjectId('633007e552ef499751ceb548')}, {"$set": skt_json})

    # item_details = skt.find({'_id': ObjectId('633007e552ef499751ceb548')})
    sched.start()
    app.run()