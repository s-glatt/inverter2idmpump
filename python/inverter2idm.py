#!/usr/bin/env python

from datetime import datetime
import math

import Config
import Mqtt
import IdmPump 
import Sma 
import TimescaleDb


# metrics from Mqtt-broker
def mqtt(opendtu_power, opendtu_yieldday):
    try:
        result = Mqtt.get(opendtu_power+'/#')
        fvalue = float(result[opendtu_power])
        if not math.isnan(fvalue):
            TimescaleDb.writeW('mqtt', fvalue)

        #result = Mqtt.get(opendtu_yieldday)
        #print(result['opendtu_470576571/ac/yieldday'])
        return fvalue
       
    except Exception as ex:
        print ("ERROR mqtt: ", ex)



# metrics from SMA
def sma(sma_ip, sma_port):
    try:
        result = Sma.read(sma_ip, sma_port)
        fvalue = float(result)
        if not math.isnan(fvalue):
            TimescaleDb.writeW('sma', fvalue)
        return fvalue

    except Exception as ex:
        print ("ERROR sma: ", ex)



# metrics from IDM
def idm(idm_ip, idm_port, feed_in):
    try:
        return IdmPump.writeandread(idm_ip, idm_port, feed_in)
        
    except Exception as ex:
        print ("ERROR idm: ", ex)




if __name__ == "__main__":  
    print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()

        # connect interfaces
        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])
        Mqtt.connect(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"])

        # metrics
        mqtt_feed_in = round(mqtt(conf["opendtu_power"], conf["opendtu_yieldday"]))
        sma_feed_in = round(sma(conf["sma_ip"], conf["sma_port"]))
        print (f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} OpenDtu: {mqtt_feed_in}W, SMA: {sma_feed_in}W, feed_in_limit: {conf['feed_in_limit']}W")

        # add invert power
        feed_in = mqtt_feed_in + sma_feed_in


        # feed in must be above our limit
        # idm feed_in in kW, negativ numbers for power from grid, 0 to reset
        if feed_in > conf['feed_in_limit']:
            idm(conf["idm_ip"], conf["idm_port"], feed_in/1000)
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM feed-in reached: ", feed_in, "W")               
            TimescaleDb.writeW('to_idm', feed_in)
        else:
            idm(conf["idm_ip"], conf["idm_port"], 0)
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM send ZERO: ", 0)  
            TimescaleDb.writeW('to_idm', 0)


        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR: ", ex) 
