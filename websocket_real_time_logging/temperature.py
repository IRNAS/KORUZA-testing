#!/usr/bin/python

import threading
import time
import json
import sys
from pprint import pprint
from websocket import create_connection

exitFlag = 0

values = [0,0,0,0,0,0]

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
                    file.write(' %f' % obj['sfp'][sfp_id]['rx_power_db'])
                    file.write(' %f\n' % obj['sfp'][sfp_id]['temperature_c'])
                    values[threadID]=obj['sfp'][sfp_id]['rx_power_db']
                #print threadName, time.time(), obj['sfp']['150918']['rx_power_db']
                #file.write('%f ' % time.time())
                #file.write(' %f\n' % obj['sfp'][koruzaID]['rx_power_db'])
                #values[threadID]=obj['sfp'][koruzaID]['rx_power_db']
                #pprint(obj['sfp']['150918']['rx_power_db'])
        else:
            pass




# You need to enter IP addresses of all KORUZA units you wish to log from for all links

# Create new threads
# Unit 1 - kaust 1-1
thread1 = myThread(0, "Thread-1", "ws://10.254.82.126/ws", 1)
# Unit 2 - kaust-1-2
thread2 = myThread(1, "Thread-2", "ws://10.254.82.101/ws", 1)

# Unit 1 - kaust 3-1
thread3 = myThread(2, "Thread-3", "ws://10.254.82.122/ws", 1)
# Unit 2 - kaust-3-2
thread4 = myThread(3, "Thread-4", "ws://10.254.82.116/ws", 1)


# Additional units
# Unit 1 - monkeybrains-1-1
thread5 = myThread(4, "Thread-5", "ws://10.254.82.117/ws", 1)
# Unit 2 - monkeybrains-1-2
thread6 = myThread(5, "Thread-6", "ws://10.254.82.125/ws", 1)





# Add threads to main thread
thread1.daemon = True
thread2.daemon = True
thread3.daemon = True
thread4.daemon = True
thread5.daemon = True
thread6.daemon = True

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()


# Keep main thread alive
while True:
    time.sleep(1)
    print values[0],values[1],values[2], values[3],values[4], values[5]
