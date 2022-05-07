import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))
    
mqttBroker = "localhost"

client = mqtt.Client("zigbee2mqtt-json-1")
client.connect(mqttBroker)

client.subscribe("zigbee2mqtt/0x00124b00251f6ccc/json")
client.on_message = on_message

client.loop_forever()
