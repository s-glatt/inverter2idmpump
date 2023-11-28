#!/usr/bin/env python

import os
import psycopg2
import math

conn = "unknown"

# write watts to TimescaleDB
def writeW(key, value):
    write('watts',key,value)

# write voltages to TimescaleDB
def writeV(key, value):
    write('voltages',key,value)

# write temps to TimescaleDB
def writeT(key, value):
    write('temps',key,value)

# write percentages to TimescaleDB
def writeP(key, value):
    write('percentages',key,value)

# write kilowatthours to TimescaleDB
def writeK(key, value):
    write('kilowatthours',key,value)

# write data to TimescaleDB
def write(table, key, value):
    try:
        global conn  
        # create a cursor      
        cur = conn.cursor()   
        # execute a statement
        sql = 'insert into '+table+' (time, key, value) values (now(), %s, %s)'
        cur.execute(sql, (key,value,))   
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except Exception as ex:
        print ("ERROR: ", ex) 
        cur.execute("rollback")

# exec in db
def exec(sql):
    try:
        global conn
        # create a cursor
        cur = conn.cursor()   
        # execute a statement
        cur.execute(sql)  
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except Exception as ex:
        print ("ERROR: ", ex) 
        cur.execute("rollback")

def connect(timescaledb_ip, timescaledb_username, timescaledb_password):
    try:       
        
        #init Timescaledb
        global conn
        conn = psycopg2.connect(
            host=timescaledb_ip,
            database="postgres",
            user=timescaledb_username,
            password=timescaledb_password)
        
    except Exception as ex:
        print ("ERROR: ", ex)         

def close():
    global conn
    conn.close()
