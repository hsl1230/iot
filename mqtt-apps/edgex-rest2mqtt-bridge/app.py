import logging
import json
import time
import os
from flask import Flask, render_template, redirect, request, url_for, make_response, jsonify
from flask_restful import Resource, Api, reqparse
import paho.mqtt.client as mqtt

def on_disconnect(client, userdata, rc = 0):
    logging.info(f"DisConnected result code {rc}")
    client.loop_stop()

mqttBroker = "localhost"
pubClient = mqtt.Client("zigbee2mqtt-pub")
pubClient.connect(mqttBroker)
pubClient.on_disconnect = on_disconnect
pubClient.loop_start()

subClient = mqtt.Client("zigbee2mqtt-sub")
subClient.connect(mqttBroker)
subClient.loop_start()
subClient.on_disconnect = on_disconnect

def changeSmartPlugState(device, state):
    logging.info(f"changing smart plug {device} state to {state} ...")
    pubClient.publish(f"zigbee2mqtt/{device}/set", json.dumps({"state": state}))
    logging.info(f"topic: zigbee2mqtt/{device}/set")

def wait_for(client, period = 0.25):
    print("waiting...")
    if client.suback_flag:
        print("waiting out...")
        while not client.suback_flag:
            print("waiting in...")
            client.loop()
            time.sleep(period)
            


def querySmartPlugState(device):
    sensor_data = {}
    message_processed = False;
    def on_message(client, userdata, message):
        print("#######on message ")
        payload = str(message.payload.decode("utf-8"))
        print("received message: ", payload)
            
        nonlocal sensor_data
        sensor_data = json.loads(payload)
        nonlocal message_processed
        message_processed = True

    print(f"subscribe from zigbee2mqtt/{device}...")
    subClient.subscribe(f"zigbee2mqtt/{device}")
    subClient.on_message = on_message

    print(f"publishing to zigbee2mqtt/{device}/get")
    pubClient.publish(f"zigbee2mqtt/{device}/get", json.dumps({"state": ""}))

    while not message_processed:
        subClient.loop()
        pubClient.loop()
        time.sleep(0.1)
    
    #wait_for(subClient, 0.25)
    subClient.unsubscribe(f"zigbee2mqtt/{device}")
    
    return sensor_data


app = Flask(__name__)
color = "green"

@app.route('/')
def index():
    content = make_response(render_template('index.html'))
    return content


@app.route('/_ajaxAutoRefresh', methods= ['GET'])
def stuff():
    return jsonify(color=color)


@app.route('/api/v2/device/register',methods=['POST'])
def register():
    request.get_json(force=True)

    parser = reqparse.RequestParser()
    parser.add_argument('id', required=True)
    args = parser.parse_args()

    id = args['id']

    print("registering device: ", id)

    returnData = {
        "apiVersion": "v2",
        "statusCode": 200
    }

    return json.dumps(returnData), 200

@app.route('/api/v2/device/name/<id>/state',methods=['GET'])
def getState(id):
    sensor_data = querySmartPlugState(id)
    resultData = { "apiVersion": "v2", "status_code": 200, "event": {"apiVerson": "v2", "deviceName": id, "profileName": "",
                                                                 "readings": { "deviceName": id, "profileName": "", "resourceName": "state", "value": sensor_data["state"] }  }}
    print("result data: ", resultData)
    return json.dumps(resultData), 200


@app.route('/api/v2/device/name/<id>/changeState',methods=['PUT'])
def changeStateByCommand(id):
    return changeState(id)
    
@app.route('/api/v2/device/name/<id>/state',methods=['PUT'])
def changeStateByAttribute(id):
    return changeState(id)


def changeState(id):
    request.get_json(force=True)

    parser = reqparse.RequestParser()
    parser.add_argument('state', required=True)
    args = parser.parse_args()

    state = (args['state'])

    print("requesting device: ", id)
    changeSmartPlugState(id, state)

    returnData = {
        "apiVersion": "v2",
        "statusCode": 200
    }

    return json.dumps(returnData), 200


if __name__ == "__main__":
	app.run(    debug=False, \
                host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
