import paho.mqtt.client as mqtt
import time
import requests
import json
import uuid

#Zigbee2MQTT:info  2022-05-11 15:06:52: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc"},"type":"device_announce"}'
#Zigbee2MQTT:warn  2022-05-11 15:07:05: Device '0x00124b00251f6ccc' left the network
#Zigbee2MQTT:info  2022-05-11 15:07:05: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc"},"type":"device_leave"}'
#Zigbee2MQTT:info  2022-05-11 15:07:08: Device '0x00124b00251f6ccc' joined
#Zigbee2MQTT:info  2022-05-11 15:07:08: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc"},"type":"device_joined"}'
#Zigbee2MQTT:info  2022-05-11 15:07:08: Starting interview of '0x00124b00251f6ccc'
#Zigbee2MQTT:info  2022-05-11 15:07:08: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc","status":"started"},"type":"device_interview"}'
#Zigbee2MQTT:info  2022-05-11 15:07:08: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc"},"type":"device_announce"}'
#Zigbee2MQTT:info  2022-05-11 15:07:13: Successfully interviewed '0x00124b00251f6ccc', device has successfully been paired
#Zigbee2MQTT:info  2022-05-11 15:07:13: Device '0x00124b00251f6ccc' is supported, identified as: SONOFF Temperature and humidity sensor (SNZB-02)
#Zigbee2MQTT:info  2022-05-11 15:07:13: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"definition":{"description":"Temperature and humidity sensor",
# "exposes":[{"access":1,"description":"Remaining battery in %","name":"battery","property":"battery","type":"numeric","unit":"%","value_max":100,"value_min":0},{"access":1,"description":"Measured temperature value","name":"temperature","property":"temperature","type":"numeric","unit":"°C"},{"access":1,"description":"Measured relative humidity","name":"humidity","property":"humidity","type":"numeric","unit":"%"},{"access":1,"description":"Voltage of the battery in millivolts","name":"voltage","property":"voltage","type":"numeric","unit":"mV"},{"access":1,"description":"Link quality (signal strength)","name":"linkquality","property":"linkquality","type":"numeric","unit":"lqi","value_max":255,"value_min":0}],
# "model":"SNZB-02",
# "options":[{"access":2,"description":"Number of digits after decimal point for temperature, takes into effect on next report of device.","name":"temperature_precision","property":"temperature_precision","type":"numeric","value_max":3,"value_min":0},{"access":2,"description":"Calibrates the temperature value (absolute offset), takes into effect on next report of device.","name":"temperature_calibration","property":"temperature_calibration","type":"numeric"},{"access":2,"description":"Number of digits after decimal point for humidity, takes into effect on next report of device.","name":"humidity_precision","property":"humidity_precision","type":"numeric","value_max":3,"value_min":0},{"access":2,"description":"Calibrates the humidity value (absolute offset), takes into effect on next report of device.","name":"humidity_calibration","property":"humidity_calibration","type":"numeric"}],"supports_ota":false,"vendor":"SONOFF"},"friendly_name":"0x00124b00251f6ccc","ieee_address":"0x00124b00251f6ccc","status":"successful","supported":true},"type":"device_interview"}'
#Zigbee2MQTT:info  2022-05-11 15:07:13: Configuring '0x00124b00251f6ccc'
#Zigbee2MQTT:info  2022-05-11 15:07:18: MQTT publish: topic 'zigbee2mqtt/0x00124b00251f6ccc', payload '{"linkquality":186,"voltage":2900}'
#Zigbee2MQTT:info  2022-05-11 15:07:19: MQTT publish: topic 'zigbee2mqtt/0x00124b00251f6ccc', payload '{"linkquality":171,"temperature":26.66,"voltage":2900}'
#Zigbee2MQTT:info  2022-05-11 15:07:19: MQTT publish: topic 'zigbee2mqtt/0x00124b00251f6ccc', payload '{"humidity":31.68,"linkquality":171,"temperature":26.66,"voltage":2900}'
#Zigbee2MQTT:info  2022-05-11 15:07:19: MQTT publish: topic 'zigbee2mqtt/0x00124b00251f6ccc', payload '{"battery":76.5,"humidity":31.68,"linkquality":168,"temperature":26.66,"voltage":2900}'
#Zigbee2MQTT:info  2022-05-11 15:07:19: Successfully configured '0x00124b00251f6ccc'
#Zigbee2MQTT:info  2022-05-11 15:07:29: MQTT publish: topic 'zigbee2mqtt/0x00124b00251f6ccc', payload '{"battery":76.5,"humidity":30.28,"linkquality":165,"temperature":26.66,"voltage":2900}'

def device_profile_exists(name):
    response = requests.get("http://localhost:59881/api/v2/deviceprofile/name/{name}")
    return response.status_code == 200
    
def create_profile(profile_name, exposes, options):
    response = requests.post("http://localhost:59881/api/v2/deviceprofile", )
    add_device_request = [
        "requestId": str(uuid.uuid1()),    
    ]
    
def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print("received message: ", payload)
    json_payload = json.loads(payload)
    if json_payload["type"] == "device_interview":
        data = json_payload["data"]
        if data["status"] == "successful":
            definition = data["definition"]
            vendor = definition["vendor"]
            model = definition["model"]
            profile_name = f"mqtt-{vendor}-{model}-profile"
            if not device_profile_exists(profile_name):
                exposes = definition["exposes"]
                options = definition["options"]
                create_profile(profile_name, exposes, options)
            device_name = data["friendly_name"]
            create_device(device_name, profile_name)


mqttBroker = "localhost"

client = mqtt.Client("zigbee2mqtt")
client.connect(mqttBroker)

client.subscribe("zigbee2mqtt/bridge/event")
client.on_message = on_message

client.loop_forever()

