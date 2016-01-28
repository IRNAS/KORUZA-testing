#!/usr/bin/python

import threading
import time
import json
import sys
from pprint import pprint
from websocket import create_connection

exitFlag = 0

values = [0,0,0,0,0,0,0,0,0,0,0]

class myThread (threading.Thread):
    def __init__(self, threadID, name, ip, index):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip = ip
        self.index = index
    def run(self):
        print "Starting " + self.name
        if (self.index == 1):
            print_unit(self.threadID,self.name, self.ip)
        elif (self.index == 2):
            print_sensor(self.threadID,self.name, self.ip)
        else:
            print_sensor2(self.threadID,self.name, self.ip)
        print "Exiting " + self.name

def print_unit(threadID, threadName, ip):
    ws = create_connection(ip)
    waitflag = 1
    sfpname ='none'
    while waitflag:
        result =  ws.recv()
        if (result[0] == 's'):
            result = result[7:]
            obj = json.loads(result)
            if (obj['type'] == 'sfp'):
                sfpname = obj['metadata'][0]['model']
                print ("Received '%s'" % result)
                waitflag=0
    filename=threadName+'-'+sfpname
    # Open file for writing
    file = open(filename, "w")
    while True:
        if exitFlag:
            threadName.exit()
        result =  ws.recv()
        if (result[0] == 's'):
            result = result[7:]
            obj = json.loads(result)
            if (obj['type'] == 'sfp'):
                for sfp_id in obj['sfp']:
                    file.write('%f ' % time.time())
                    file.write(' %f\n' % obj['sfp'][sfp_id]['rx_power_db'])
                    values[threadID]=obj['sfp'][sfp_id]['rx_power_db']
        else:
            pass

def print_sensor(threadID,threadName, ip):
    filename=threadName+'-'+'tsl2561'
    # Open file for writing
    file = open(filename, "w")
    ws = None
    while True:
        try:
            if exitFlag:
                return
            
            if ws is None:
                ws = create_connection(ip, timeout=2)
                ws.recv()

            result =  ws.recv()
            #print result
            if (result != 0):
                obj = json.loads(result)
                #print result
                file.write('%f ' % time.time())
                file.write(' %d' % obj['sensors.generic']['light_1']['value'])
                file.write(' %d' % obj['sensors.generic']['light_2']['value'])
                file.write(' %d\n' % obj['sensors.generic']['light_3']['value'])
                values[threadID]=obj['sensors.generic']['light_3']['value']
            else:
                print "Error A\n"
                values[threadID]=0
        except:
            if ws is not None:
                ws.close()
            ws = None
            values[threadID]=0
            
def print_sensor2(threadID,threadName, ip):
    filename=threadName+'-'+'tsl2561'
    # Open file for writing
    file = open(filename, "w")
    ws = None
    while True:
        try:
            if exitFlag:
                return
            
            if ws is None:
                ws = create_connection(ip, timeout=10)
                ws.recv()

            result =  ws.recv()
            #print result
            if (result != 0):
                obj = json.loads(result)
                #print result
                file.write('%f ' % time.time())
                file.write(' %d' % obj['sensors.generic']['light_1']['value'])
                file.write(' %d' % obj['sensors.generic']['light_2']['value'])
                file.write(' %d' % obj['sensors.generic']['light_3']['value'])
                file.write(' %d' % obj['sensors.generic']['light_4']['value'])
                file.write(' %d' % obj['sensors.generic']['light_5']['value'])
                file.write(' %d\n' % obj['sensors.generic']['light_6']['value'])
                values[threadID]=obj['sensors.generic']['light_3']['value']
                values[threadID+1]=obj['sensors.generic']['light_6']['value']
            else:
                print "Error A\n"
                values[threadID]=0
        except:
            if ws is not None:
                ws.close()
            ws = None
            values[threadID]=0

# For every KORUZA unit you need to create a thread and define an IP by replacing <unit IP>

# Koruza 1
thread1 = myThread(0, "Thread-1", "ws://<unit IP>/ws", 1)
thread1.daemon = True
thread1.start()

# Koruza 2
thread2 = myThread(1, "Thread-2", "ws://<unit IP>/ws", 1)
thread2.daemon = True
thread2.start()

# create threads for sensors if you have any

# Sensor - single
thread3 = myThread(3, "Thread-9", "ws://<unit IP>:81", 2)
thread3.daemon = True
thread3.start()
# Sensor - double
thread4 = myThread(4, "Thread-10", "ws://<unit IP>:81", 3)
thread4.daemon = True
thread4.start()

# Keep main thread alive
while True:
    time.sleep(1)
    print values[0],values[1],values[2], values[3],values[4], values[5],values[6],values[7], values[8],values[9], values[10]
