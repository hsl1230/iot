import paho.mqtt.client as mqtt
import time
import requests
import json
import argparse

parser = argparse.ArgumentParser(description = 'turn the power on/off of a smart plug')

parser.add_argument("-d", "--device", help = "specify the specific plug", required = True)
parser.add_argument("-s", "--state", help = "set the state of the plug.", default = "TOGGLE")
args = parser.parse_args()

state = args.state
device = args.device

mqttBroker = "localhost"

client = mqtt.Client("zigbee2mqtt")
client.connect(mqttBroker)

client.publish(f"zigbee2mqtt/{device}/set", json.dumps({"state": state}))
