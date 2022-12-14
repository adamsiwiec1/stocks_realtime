import json
from pymongo import MongoClient
import logging
import os
import time
from twelvedata import TDClient

logging.basicConfig(filename='/var/log/pyparser.log', level=logging.INFO)

mg = MongoClient(os.environ['MONGO_PUBLIC_IP'], int(os.environ['MONGO_PORT']),
                 username=os.environ['MONGO_USER'],
                 password=os.environ['MONGO_PASSWORD'])
collection = mg['stockdb']['price_changes']
logging.info(collection)


def on_event(e):
    if e.get('event') != 'heartbeat':
        logging.info(collection.insert_one(e))
    logging.info(str(e))


td = TDClient(apikey=os.environ["API_KEY"])
ws = td.websocket(symbols=json.loads(os.environ['SYMBOLS']), on_event=on_event)
ws.connect()
while True:
    try:
        ws.heartbeat()
    except:
        ws = td.websocket(symbols=json.loads(os.environ['SYMBOLS']), on_event=on_event)
        ws.connect()
    time.sleep(5)