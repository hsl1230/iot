##############################################################################################################
#     ______    __          _  __        __          _                                   __            
#    / ____/___/ /___ ____ | |/ /   ____/ /__ _   __(_)_______     _____________  ____ _/ /_____  _____
#   / __/ / __  / __ `/ _ \|   /   / __  / _ \ | / / / ___/ _ \   / ___/ ___/ _ \/ __ `/ __/ __ \/ ___/
#  / /___/ /_/ / /_/ /  __/   |   / /_/ /  __/ |/ / / /__/  __/  / /__/ /  /  __/ /_/ / /_/ /_/ / /    
# /_____/\__,_/\__, /\___/_/|_|   \__,_/\___/|___/_/\___/\___/   \___/_/   \___/\__,_/\__/\____/_/     
#             /____/                                                                                   
##############################################################################################################
# Name;         createRESTDevice.py
# Description:  Script with all REST calls required to create a new device in EdgeX Foundry - Geneva release
#               The device in this use case exposes a REST API which EdgeX Foundry can interact with. 
#               The device does not support sending sensor values (separate script is avilable for that use case)
# Version:      0.1
# Author:       Jonas Werner
##############################################################################################################


import requests, json, sys, re, time, os, warnings, argparse, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime

warnings.filterwarnings("ignore")

# Gather information from arguments
parser=argparse.ArgumentParser(description="Python script for creating a new device from scratch in EdgeX Foundry")
parser.add_argument('-ip',help='EdgeX Foundry IP address', required=True)
parser.add_argument('-devip',help='Target device IP address', required=True)

args=vars(parser.parse_args())

edgex_ip    = args["ip"]
device_ip   = args["devip"]

# To create a device we need a device profile in YAML format. This function uploads and registers
# the device profile with EdgeX Foundry. Based on the content of the device profile, EdgeX Foundry
# may create entries for the device in the command module as well as meta data.
def uploadDeviceProfile():
    multipart_data = MultipartEncoder(
        fields={
                'file': ('smart-plug-device-profile.yaml', open('smart-plug-device-profile.yaml', 'rb'), 'text/plain')
               }
        )

    url = 'http://%s:59881/api/v2/deviceprofile/uploadfile' % edgex_ip
    response = requests.post(url, data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})

    print("Result of uploading device profile: %s with message %s" % (response, response.text))




# This is a dummy device service since the existing REST device service doesn't yet support sending commands
def createDeviceService():
    url = 'http://%s:59881/api/v2/deviceservice' % edgex_ip

    payload = [{
        "requestId": str(uuid.uuid1()),
        "apiVersion": "v2",
        "service": {
            "name":"rest2mqtt-device-service",
            "description":"Gateway for sending commands to external mqtt devices",
            "adminState":"UNLOCKED",
            "labels":["color","mqtt", "gateway"],
            "baseAddress": f"http://{device_ip}:5000"
        }
    }]
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print("Result for createDeviceService: %s - Message: %s" % (response, response.text))



# Finally we can create the actual device. It will be named and will also reference both the 
# device service it supports as well as the device profile it corresponds to
# The device creation requires a protocols section. Perhaps it can be expanded to include
# information about the device, like IP, port, etc. but isn't actively used for these tutorials
def addNewDevice():
    url = 'http://%s:59881/api/v2/device' % edgex_ip

    payload = [{
        "apiVersion": "v2",
        "device": {
            "name": "0x00124b0025139c1e",
            "description": "smart plug",
            "adminState": "UNLOCKED",
            "operatingState": "UP",
            "protocols": {
                "example": {
                    "host": "localhost",
                    "port": "0",
                    "unitID": "1"
                }
            },
            "labels": [
                "state",
                "smart plug"
            ],
            "location": "calgary",
            "serviceName": "rest2mqtt-device-service",
            "profileName": "smart-plug-profle"
        }
    }]
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print("Result for addNewDevice: %s - Message: %s" % (response, response.text))


if __name__ == "__main__":
    uploadDeviceProfile()
    createDeviceService()
    addNewDevice()
