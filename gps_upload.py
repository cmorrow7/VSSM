import requests
from gps import *
from datetime import datetime
import sys
import os
import pytz
from dateutil.parser import parse
import time
from time import sleep
import signal
import json
import usb.core

def findUSB():
	found = False
	ident = ''
	dev = usb.core.find(find_all = True)
	for cfg in dev:
		ident = str(cfg.idVendor) + str(cfg.idProduct)
		if(ident == '5446423'):
			found = True
	if(found == False):
		print('GPS device not connected')
	return found
	
	
	
def terminateProcess(signalNumber,frame):
    print('Exit received, stopping GPS')
    global running
    running = False

# Used to change position timestamp from UCT to PST
def changeTimezone(timestamp):
	pst = parse(timestamp)
	pst = pst.astimezone(pytz.timezone('US/Pacific'))
	return pst

# Retrieve latitude, longitude, and time from GPS module
def getPositionData(gps):
	nx = gpsd.next()
	if nx['class'] == 'TPV':
		latitude = getattr(nx,'lat', "Unknown")
		longitude = getattr(nx,'lon', "Unknown")
		now = getattr(nx,'time', "Unknown")
		now = changeTimezone(now)
		now = str(now).partition(' ')
		time = now[2]
		day = now[0]
		if(latitude < -90 or latitude > 90):
			return ""
		else :
			return {"lat" : str(latitude) , "long" : str(longitude) , 
		"time" : str(time) , "day" : str(day)}
	else:
		return ""

def sendPositionData():
	pos = ""
	# Waits for valid data from the GPS module
	# Need to catch inf loop and test with unresponsive module
	while pos == "":
		pos = getPositionData(gpsd)
	return pos


# register the signals to be caught
signal.signal(signal.SIGINT, signal.SIG_IGN) #ignores keyboard interrupt
signal.signal(signal.SIGTERM, terminateProcess) #exits upon termination signal

print('GPS PID is: ' + str(os.getpid()))

if(os.path.exists('pids.json')):
    with open('pids.json','r') as pid_list:
        try:
            pids = json.loads(pid_list.read())
            pids['gps'] = os.getpid()
            pid_list.close()
            with open('pids.json','w') as pid_list:
                pid_list.write(json.dumps(pids))
                pid_list.close()

            running = True
        except:
            pid_list.close()
            running = False
          
else:
    running = False

# GPSD functions referenced from
# https://gpsd.gitlab.io/gpsd/gpsd_json.html
# https://gpsd.gitlab.io/gpsd/libgps.html

# Enables reporting mode
gpsd = gps(mode=WATCH_ENABLE)

if(running):
	running = findUSB()

while running:
	sleep(100)
	old_pos = ""
	new_pos = sendPositionData()
	if(new_pos != old_pos):
		requests.post('http://vssm.ddns.net/gps.php', data = new_pos)
		old_pos = new_pos
	else:
		print("Same location")
		
