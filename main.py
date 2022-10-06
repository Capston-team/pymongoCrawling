from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from apscheduler.schedulers.blocking import BlockingScheduler
from skt import skt_title, skt_date, skt_image
from kt import kt_title, kt_date, kt_image
from lg import lg_title, lg_date, lg_image

sched = BlockingScheduler(timezone='Asia/Seoul')

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

    SktResultSet = dict({'title': skt_title(), 'date': skt_date(), 'img': skt_image()})
    KtResultSet = dict({'title': kt_title(), 'date': kt_date(), 'img': kt_image()})
    LgResultSet = dict({'title': lg_title(), 'date': lg_date(), 'img': lg_image()})

    # print(SktResultSet)
    # print('\n\n')
    # print(KtResultSet)
    # print('\n\n')
    # print(LgResultSet)

    skt.update_one({'_id': ObjectId('633007e552ef499751ceb548')}, {"$set": SktResultSet})
    kt.update_one({'_id': ObjectId('6330017d0af9348ced24899f')}, {"$set": KtResultSet})
    lg.update_one({'_id': ObjectId('6336ea180ad3309313d9bfc3')}, {"$set": LgResultSet})

    print("Successful Update eventList")


# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('Test log interval 3MIN')


@app.route('/')
def setEventList():
    UpdateEventList()
    return 'setEventList - Successful update event list'


if __name__ == "__main__":

    sched.start()
    app.run()