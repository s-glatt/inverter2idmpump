#!/usr/bin/env python

import sys
import os
import psutil
from datetime import datetime
import math

import Config
import Mqtt
import IdmPump 
import Sma 
import TimescaleDb


# check if programm was startet in a privious instance
def is_process_running(python_progname):
    for process in psutil.process_iter():
         if python_progname in process.cmdline() and process.pid != os.getpid():
             return True 
    return False


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
def sma(sma_ip, sma_port, read_allvalues):
    try:
        if read_allvalues==1:
            solarpower, energymeterpower_drawn, energymeterpower_feedin = Sma.readWE(sma_ip, sma_port)
            if not solarpower == None and not math.isnan(solarpower) and solarpower >= 0:
                solarpower = float(solarpower)
                TimescaleDb.writeW('sma_'+str(sma_ip), solarpower)
            else:
                solarpower = 0

            if not energymeterpower_drawn == None and not math.isnan(energymeterpower_drawn) and energymeterpower_drawn >= 0:
                energymeterpower_drawn = float(energymeterpower_drawn)
                TimescaleDb.writeW('energymeter_drawn_'+str(sma_ip), energymeterpower_drawn)
            else:
               energymeterpower_drawn = 0

            if not energymeterpower_feedin == None and not math.isnan(energymeterpower_feedin) and energymeterpower_feedin >= 0:
                energymeterpower_feedin = float(energymeterpower_feedin)
                TimescaleDb.writeW('energymeter_feedin_'+str(sma_ip), energymeterpower_feedin)
            else:
               energymeterpower_feedin = 0

            return (solarpower, energymeterpower_drawn, energymeterpower_feedin)
        else:
            solarpower = Sma.readW(sma_ip, sma_port)
            if not solarpower == None and not math.isnan(solarpower) and solarpower >= 0:
                solarpower = float(solarpower)
                TimescaleDb.writeW('sma_'+str(sma_ip), solarpower)
            else:
                solarpower = 0

            return (solarpower, None, None)

    except Exception as ex:
        print ("ERROR sma: ", ex)



# write metrics to IDM
def idmwrite(idm_ip, idm_port, feed_in):
    try:
        return IdmPump.write(idm_ip, idm_port, feed_in)
        
    except Exception as ex:
        print ("ERROR idm: ", ex)


# read metrics from IDM
def idmread(idm_ip, idm_port):
    try:
        return IdmPump.read(idm_ip, idm_port)
        
    except Exception as ex:
        print ("ERROR idm: ", ex)



if __name__ == "__main__":  
    if is_process_running(sys.argv[0]):
       print('The script is still running.')
       sys.exit()

    print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()

        # connect interfaces
        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])
        Mqtt.connect(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"])

        # get solar power and energymeter metrics
        mqtt_feed_in = mqtt(conf["opendtu_power"], conf["opendtu_yieldday"])
        sma_feed_in, energymeter_drawn, energymeter_feedin = sma(conf["sma_ip"], conf["sma_port"], conf["sma_read_allvalues"])
        sma_feed_in2, energymeter_drawn2,engerymeter_feedin2 = sma(conf["sma_ip2"], conf["sma_port2"], conf["sma_read_allvalues2"])

        # round the values
        mqtt_feed_in = round(mqtt_feed_in)
        sma_feed_in = round(sma_feed_in)
        sma_feed_in2 = round(sma_feed_in2)
        energymeter_drawn = round(energymeter_drawn)
        energymeter_feedin = round(energymeter_feedin)

        print (f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} OpenDtu: {mqtt_feed_in}W, SMA: {sma_feed_in}W, SMA2: {sma_feed_in2}W, IDM feed_in_limit_on: {conf['feed_in_limit_on']}W, IDM feed_in_limit_off: {conf['feed_in_limit_off']}W")
        print (f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Energymeter Drawn: {energymeter_drawn}W, Energymeter Feed: {energymeter_feedin}W")

        # add invert power
        feed_in = mqtt_feed_in + sma_feed_in + sma_feed_in2


        # idm feed in must be above our feed_in_limit_on to switch on
        # if idm feed in between feed_in_limit_on and feed_in_limit_off, test if it was on (state)
        # idm feed_in in kW, negativ numbers for power from grid, 0 to reset

        if feed_in > conf['feed_in_limit_on']:
            # limit to feed_in_limit_on to avoid to high values
            feed_in = conf['feed_in_limit_on']
            idmwrite(conf["idm_ip"], conf["idm_port"], feed_in/1000)
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM PV-feed-in write: ", feed_in, "W", sep="")               
            TimescaleDb.writeW('to_idm', feed_in)

        elif (feed_in > conf['feed_in_limit_off']) and (feed_in < conf['feed_in_limit_on']):
            # read the actual idm pv-state
            idm = round(idmread(conf["idm_ip"], conf["idm_port"])*1000)
            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} IDM read: {idm}W")
            if idm > conf['feed_in_limit_off']:
                idmwrite(conf["idm_ip"], conf["idm_port"], feed_in/1000)
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM PV-feed-in write: ", feed_in, "W", sep="")               
                TimescaleDb.writeW('to_idm', feed_in)
            else:
                idmwrite(conf["idm_ip"], conf["idm_port"], 0)
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM PV-feed-in write: ", 0, "W", sep="")  
                TimescaleDb.writeW('to_idm', 0)

        else:
            idmwrite(conf["idm_ip"], conf["idm_port"], 0)
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " IDM PV-feed-in write: ", 0, "W", sep="")  
            TimescaleDb.writeW('to_idm', 0)


        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR: ", ex) 
