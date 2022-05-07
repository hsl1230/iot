import paho.mqtt.client as mqtt
import time
import requests
import json

def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print("received message: ", payload)
    sensor_data = json.loads(payload)
    # sensor_data["sensorName"] = "0x00124b00251f6ccc"
    # response = requests.post("http://localhost:59986/api/v2/resource/sample-json/json", json = sensor_data)
    response = requests.post("http://localhost:59986/api/v2/resource/SNZB-02-Sensor/sensorData", json = sensor_data)
    print("set sensorData status: ", response.status_code)
    response = requests.post("http://localhost:59986/api/v2/resource/SNZB-02-Sensor/temperature", json = sensor_data["temperature"])
    print("set temperature status: ", response.status_code)
    response = requests.post("http://localhost:59986/api/v2/resource/SNZB-02-Sensor/humidity", json = sensor_data["humidity"])
    print("set humidity status: ", response.status_code)

mqttBroker = "localhost"

client = mqtt.Client("zigbee2mqtt")
client.connect(mqttBroker)

client.subscribe("zigbee2mqtt/0x00124b00251f6ccc")
client.on_message = on_message

client.loop_forever()