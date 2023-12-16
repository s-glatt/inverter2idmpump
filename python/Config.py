#!/usr/bin/env python

import configparser
import os
from datetime import datetime

#read config
config = configparser.ConfigParser()

def read():
    try:
        #read config
        config.read('inverter2idm.ini')

        values = {}

        values["opendtu_power"] = config['MqttTopicSection']['opendtu_power']
        values["opendtu_yieldday"] = config['MqttTopicSection']['opendtu_yieldday']

        values["timescaledb_ip"] = config['DatabaseSection']['timescaledb_ip']
        values["timescaledb_username"] = config['DatabaseSection']['timescaledb_username']
        values["timescaledb_password"] = config['DatabaseSection']['timescaledb_password']
        if os.getenv('TIMESCALEDB_IP','None') != 'None':
            values["timescaledb_ip"] = os.getenv('TIMESCALEDB_IP')
            #print ("using env: TIMESCALEDB_IP")
        if os.getenv('TIMESCALEDB_USERNAME','None') != 'None':
            values["timescaledb_username"] = os.getenv('TIMESCALEDB_USERNAME')
            #print ("using env: TIMESCALEDB_USERNAME")
        if os.getenv('TIMESCALEDB_PASSWORD','None') != 'None':
            values["timescaledb_password"] = os.getenv('TIMESCALEDB_PASSWORD')
            #print ("using env: TIMESCALEDB_PASSWORD")

        values["idm_ip"] = config['IdmSection']['idm_ip']
        values["idm_port"] = int(config['IdmSection']['idm_port']) 
        values["feed_in_limit_on"] = int(config['IdmSection']['feed_in_limit_on']) 
        values["feed_in_limit_off"] = int(config['IdmSection']['feed_in_limit_off']) 
        if os.getenv('IDM_IP','None') != 'None':
            values["idm_ip"] = os.getenv('IDM_IP')
            #print ("using env: IDM_IP")
        if os.getenv('IDM_PORT','None') != 'None':
            values["idm_port"] = int(os.getenv('IDM_PORT'))
            #print ("using env: IDM_PORT")

        values["sma_ip"] = config['SmaSection']['inverter_ip']
        values["sma_port"] = int(config['SmaSection']['inverter_port'])
        if os.getenv('INVERTER_IP','None') != 'None':
            values["sma_ip"] = os.getenv('INVERTER_IP')
            #print ("using env: INVERTER_IP")
        if os.getenv('INVERTER_PORT','None') != 'None':
            values["sam_port"] = int(os.getenv('INVERTER_PORT'))
            #print ("using env: INVERTER_PORT")

        values["mqtt_broker"] = config['MqttSection']['mqtt_broker']
        values["mqtt_port"] = int(config['MqttSection']['mqtt_port'])
        values["mqtt_user"] = config['MqttSection']['mqtt_user']
        values["mqtt_password"] = config['MqttSection']['mqtt_password']
        if os.getenv('MQTT_BROKER','None') != 'None':
            values["mqtt_broker"] = os.getenv('MQTT_BROKER')
            #print ("using env: MQTT_BROKER")
        if os.getenv('MQTT_PORT','None') != 'None':
            values["mqtt_port"] = int(os.getenv('MQTT_PORT'))
            #print ("using env: MQTT_PORT")
        if os.getenv('MQTT_USER','None') != 'None':
            values["mqtt_user"] = os.getenv('MQTT_USER')
            #print ("using env: MQTT_USER")
        if os.getenv('MQTT_PASSWORD','None') != 'None':
            values["mqtt_password"] = os.getenv('MQTT_PASSWORD')
            #print ("using env: MQTT_PASSWORD")
        
        
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " config: ", values)

        return values
    except Exception as ex:
        print ("ERROR Config: ", ex) 
