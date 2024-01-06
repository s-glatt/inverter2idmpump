#!/usr/bin/env python

import pymodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import time

#-----------------------------------------
# Routine to read a float    
def readint(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,slave=unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Big)
    result_IntRegister = IntRegister.decode_32bit_int()
    return(result_IntRegister)   


def read(sma_ip, sma_port):  
    try:
        
        # connection SMA
        client = ModbusTcpClient(sma_ip,port=sma_port)     
        client.connect()  
        # solar power stored in 30775, see:
        # https://files.sma.de/downloads/EDMx-Modbus-TI-de-16.pdf
        time.sleep(1)
        solarpower = readint(client,30775,3)
        # energymeterpower_drawn stored in 30865
        # energymeterpower_feedin stored in 30867, see:
        # https://files.sma.de/downloads/HM-20-Modbus-NSD-TI-en-12.pdf
        time.sleep(1)
        energymeterpower_drawn = readint(client,30865,3)
        time.sleep(1)
        energymeterpower_feedin = readint(client,30867,3)
        return (solarpower, energymeterpower_drawn, energymeterpower_feedin)
  
    except Exception as ex:
        print ("ERROR SMA: ", ex)
    finally:
        client.close() 
