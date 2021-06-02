# Management program, watches subprocesses to verify correct operation
# Che Morrow

import signal
import os
import time
from subprocess import call
import json

error = 0

# All process functions can be called when a signal is received from a
# subprocess. Currently not implemented.
def processGPS(signalNumber,frame):
    print('Received GPS Error')
    with open('pids.json','r') as pid_list:
        pids = json.loads(pid_list.read())
        pids['gps'] = 0
        pid_list.close()
    with open('pids.json','w') as pid_list:
        pid_list.write(json.dumps(pids))
        pid_list.close()
    #increment error counter
    global error
    error = error + 1
    return

def processVoice(signalNumber,frame):
    print('Received Voice Error')
    with open('pids.json','r') as pid_list:
        pids = json.loads(pid_list.read())
        pids['voice'] = 0
        pid_list.close()
    with open('pids.json','w') as pid_list:
        pid_list.write(json.dumps(pids))
        pid_list.close()
    #increment error counter
    global error
    error = error + 1
    return

def processOBD(signalNumber,frame):
    print('Received OBD Error')
    with open('pids.json','r') as pid_list:
        pids = json.loads(pid_list.read())
        pids['obd'] = 0
        pid_list.close()
    with open('pids.json','w') as pid_list:
        pid_list.write(json.dumps(pids))
        pid_list.close()
    #increment error counter
    global error
    error = error + 1
    return

# Finds and returns the program ID belonging to the passed subprocess
def read_pids(process):
    with open('pids.json','r') as pid_list:
        pids = json.loads(pid_list.read())
        pid_list.close()
    return pids[process]

# Sets all program IDs in the list to zero.
def reset_pids():
    with open('pids.json','w') as pid_list:
        pids = {'vssm':0,'gps':0,'voice':0,'obd':0}
        pid_list.write(json.dumps(pids))
        pid_list.close()

# Sets the program ID for the management process
def set_pid():
    print('VSSM PID is:',os.getpid())
    with open('pids.json','r') as pid_list:
        pids = json.loads(pid_list.read())
        pids['vssm'] = os.getpid()
        pid_list.close()
    with open('pids.json','w') as pid_list:
        pid_list.write(json.dumps(pids))
        pid_list.close()

# Process exits upon receiving SIGTERM signal
def exit(signalNumber,frame):
    print('Exit received, stopping subprocesses')
    global running
    running = False

# All check functions use the stored program IDs to poll the subprocesses
# If the process is not running, it is launched using call()
def checkGPS():
    their_pid = read_pids('gps')
    if(their_pid != 0):
        try:
            os.kill(int(their_pid), signal.SIGINT)
        except OSError:
            print('GPS stopped, restarting')
            term = 'python /home/pi/gps_upload.py &'
            call([term], shell=True)
            global error
            error = error + 1
    else:
        print('GPS PID not found')
        term = 'python /home/pi/gps_upload.py &'
        call([term], shell=True)
    return

def checkVoice():
    their_pid = read_pids('voice')
    if(their_pid != 0):
        try:
            os.kill(int(their_pid), signal.SIGINT)
        except OSError:
            print('Voice stopped, restarting')
            term = 'python3 /home/pi/voice.py &'
            call([term], shell=True)
            global error
            error = error + 1
    else:
        print('Voice PID not found')
        term = 'python3 /home/pi/voice.py &'
        call([term], shell=True)
    return

def checkOBD():
    their_pid = read_pids('obd')
    if(their_pid != 0):
        try:
            os.kill(int(their_pid), signal.SIGINT)
        except OSError:
            print('OBD stopped, restarting')
            term = 'python /home/pi/obd_upload.py &'
            call([term], shell=True)
            global error
            error = error + 1
    else:
        print('OBD PID not found')
        term = 'python /home/pi/obd_upload.py &'
        call([term], shell=True)
    return

# register the signals to be caught
signal.signal(signal.SIGINT, processVoice) #voice error, change pid to 0
signal.signal(signal.SIGUSR1, processGPS) #gps error, change pid to 0
signal.signal(signal.SIGUSR2, processOBD) #obd error, change pid to 0
signal.signal(signal.SIGTERM, exit) #kill -15 VSSM.pid

reset_pids()
set_pid()

# Flashes the status LED to show startup process has begun
cmd = "/home/pi/mopower/mpcmd MORSE=E"
call([cmd], shell=True)
time.sleep(1)
cmd = "/home/pi/mopower/mpcmd MORSE="
call([cmd], shell=True)

# Makes sure the UPS has the correct startup and shutdown voltage ranges
cmd = "/home/pi/mopower/mpcmd INPUT_CONTROL[0]=2,1,1,12.10,3,1,0,1,1"
call([cmd], shell=True)
time.sleep(1)
cmd = "/home/pi/mopower/mpcmd INPUT_CONTROL[1]=3,3,1,10.10,10,0,0,0,1"
call([cmd], shell=True)

# Main loop, continues to check subprocesses until error limit is reached
# When the error count gets to ten hardware issues are assumed and the Pi restarts
running = True
while running:
    if(error >= 10):
        cmd = "sudo reboot"
        call([cmd], shell=True)
    checkVoice()
    checkOBD()
    checkGPS()
    time.sleep(30)

# When main loop is left exit signals are sent to all subprocesses
# If the subprocess is not running on close (due to crash) this is logged
their_pid = read_pids('gps')
if(their_pid != 0):
    try:
        os.kill(int(their_pid), signal.SIGTERM)
    except:
        print('GPS not running on close')

their_pid = read_pids('voice')
if(their_pid != 0):
    try:
        os.kill(int(their_pid), signal.SIGTERM)
    except:
        print('Voice not running on close')

their_pid = read_pids('obd')
if(their_pid != 0):
    try:
        os.kill(int(their_pid), signal.SIGTERM)
    except:
        print('OBD not running on close')

term = 'rm pids.json'
call([term], shell=True)
