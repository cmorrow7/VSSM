from subprocess import call
from datetime import date
import obd
from obd import OBDStatus
import requests
import sys
import signal
import os
import time
import json
from time import sleep

def terminateProcess(signalNumber,frame):
    print('Exit received, stopping OBD')
    global running
    running = False

# register the signals to be caught
signal.signal(signal.SIGINT, signal.SIG_IGN) #ignores keyboard interrupt
signal.signal(signal.SIGTERM, terminateProcess) #exits upon termination signal

print('OBD PID is: ' + str(os.getpid()))

if(os.path.exists('pids.json')):
    with open('pids.json','r') as pid_list:
        try:
            pids = json.loads(pid_list.read())
            pids['obd'] = os.getpid()
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

#day = date.today()
#payl = {"day" : day, "code" : "Test Codes Follow, Disregard"}

if(running):
	day = ""
	wait = 100

	connection = obd.OBD()
	cmd = obd.commands.RPM
	response = connection.query(cmd)
	rpm = response.value

	while(rpm == None and wait > 0):
		connection = obd.OBD()
		cmd = obd.commands.RPM
		response = connection.query(cmd)
		rpm = response.value
		wait = wait - 1;
		print(wait)

	if(rpm == None):
		sys.exit()

	day = date.today()

	new_code = "RPM at start: " + str(rpm)
	payl = {"day" : day, "code" : new_code}
	requests.post('http://vssm.ddns.net/obd.php', data = payl)

	# cmd = obd.commands.GET_DTC
	# response = connection.query(cmd, force=True)
	# dtcs = response.value

	# if dtcs != None:
		# for code in dtcs:
			# if(code[1] == ""):
				# new_code = code[0] + ", Unknown Error Code"
				# dtc_log.write(new_code)
				# dtc_log.write("\n")
			# else:
				# new_code = code[0] + ", " + code[1]
				# dtc_log.write(new_code)
				# dtc_log.write("\n")

			# payl = {"day" : day, "code" : new_code}
			# requests.post('http://vssm.ddns.net/obd.php', data = payl)
	# else:
		# payl = {"day" : day, "code" : "No Trouble Codes Detected"}
		# requests.post('http://vssm.ddns.net/obd.php', data = payl)
		# dtc_log.write("Nothing found using GET_DTC\n")


while running:
	cmd = obd.commands.GET_CURRENT_DTC
	response = connection.query(cmd, force=True)
	dtcs = response.value

	if dtcs != None:
		for code in dtcs:
			if(code[1] == ""):
				new_code = code[0] + ", Unknown Error Code"
			else:
				new_code = code[0] + ", " + code[1]
			day = date.today()
			payl = {"day" : day, "code" : new_code}
			requests.post('http://vssm.ddns.net/obd.php', data = payl)
	else:
		payl = {"day" : day, "code" : "No Trouble Codes Detected"}
		requests.post('http://vssm.ddns.net/obd.php', data = payl)
	time.sleep(500)
