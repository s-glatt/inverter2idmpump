#!/usr/bin/env python

import time
import json
import FlatJson
import socket
from paho.mqtt import client as mqtt_client

client = "unknown"
searchattributes = []
valueattributes = {}


def on_message(client, userdata, message):
    content = str(message.payload.decode("utf-8"))
    #print("received message =",str(message.payload.decode("utf-8")))
    if content:
        global valueattributes
        valueattributes = {str(message.topic):str(message.payload.decode("utf-8"))}
        

def get(topic):
    try:
        #print(topic)
        global client
        global valueattributes
        valueattributes = {}
        client.on_message=on_message
        client.subscribe(topic)
        client.loop_start()
        counter = 0
        #wait max 10 sec
        while len(valueattributes) == 0 and counter < 100:
            counter = counter + 1
            time.sleep(0.1)
        client.loop_stop()
        client.unsubscribe(topic)
        return valueattributes
    except Exception as ex:
        print ("ERROR Mqtt: ", ex) 


def connect(mqtt_broker, mqtt_port, mqtt_user, mqtt_password):
    try:
        
        client_id = 'solarmonitor-mqtt-'+socket.gethostname()

        # Set Connecting Client ID
        global client
        client = mqtt_client.Client(client_id)
        client.username_pw_set(mqtt_user, mqtt_password)
        client.connect(mqtt_broker, mqtt_port)
 
    except Exception as ex:
        print ("ERROR Mqtt: ", ex)    
