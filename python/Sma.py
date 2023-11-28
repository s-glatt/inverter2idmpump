#!/usr/bin/env python

import pymodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

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
        return readint(client,30775,3)
  
    except Exception as ex:
        print ("ERROR SMA: ", ex)
    finally:
        client.close() 
