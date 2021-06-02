# Adapted from the test_microphone example provided by the Vosk API team
# https://github.com/alphacep/vosk-api
# Che Morrow
#!/usr/bin/env python3

import os
import queue
import sounddevice as sd
from subprocess import call
import vosk
import sys
import json
from picamera import PiCamera
from time import sleep
from datetime import datetime
import requests
import signal
import time
import subprocess as sp
import shutil

def terminateProcess(signalNumber,frame):
    print('Exit received, stopping Voice')
    global running
    running = False

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def record():
    cmd = "/home/pi/mopower/mpcmd MORSE=E"
    call([cmd], shell=True)

    path = '/home/pi/recordings'
    stat = shutil.disk_usage(path)
    print(stat[2])
    if (stat[2] <= 100000000):
        while(stat[2] <= 100000000):
            list_dir = os.listdir('/home/pi/recordings/')
            list_dir.sort()
            oldest_video = "/home/pi/recordings/" + list_dir[0]
            cmd = "rm " + oldest_video
            call([cmd], shell=True)
            print('Removed ',oldest_video)
            stat = shutil.disk_usage(path)

    stamp = datetime.now()
    time = int(stamp.strftime("%H"))
    stamp = stamp.strftime("%m-%d-%y_%H,%M,%S")
    with PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 30
        if(time >= 20 or time <= 6):
            camera.iso = 800
        camera.annotate_text = stamp
        camera.annotate_text_size = 18
        camera.start_recording('%s.h264' % stamp)
        sleep(60)
        camera.stop_recording()
        camera.close()

    cmd = "MP4Box -add " + stamp + ".h264 " + stamp + ".mp4"
    call([cmd], shell=True)
    cmd = "rm " + stamp + ".h264"
    call([cmd], shell=True)
    cmd = "mv " + stamp + ".mp4 /home/pi/recordings"
    call([cmd], shell=True)
    cmd = "/home/pi/mopower/mpcmd MORSE="
    call([cmd], shell=True)
    return

def upload():
    url = "http://vssm.ddns.net/upload.php"

    list_dir = os.listdir('/home/pi/recordings/')
    list_dir.sort(reverse=True)

    video = "/home/pi/recordings/" + list_dir[0]

    with open(video,"rb") as vid:
        result = requests.post(url,data={"submit":"submit"},files={"vid":vid})
        print (result.text)
    return

def sms():
    cmd = "/home/pi/mopower/mpcmd MORSE=SOS"
    call([cmd], shell=True)
    sleep(5)
    cmd = "/home/pi/mopower/mpcmd MORSE="
    call([cmd], shell=True)
    return

# register the signals to be caught
signal.signal(signal.SIGINT, signal.SIG_IGN) #ignores keyboard interrupt
signal.signal(signal.SIGTERM, terminateProcess) #exits upon termination signal

print('Voice PID is:',os.getpid())

if(os.path.exists('pids.json')):
    with open('pids.json','r') as pid_list:
        try:
            pids = json.loads(pid_list.read())
            pids['voice'] = os.getpid()
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

stdoutdata = sp.getoutput('hcitool con')

if('54:B7:E5:6E:A2:51' in stdoutdata.split()):
    print('Microphone connected')
else:
    print('Cannot communicate with microphone')
    running = False

while running:
    print('Voice Running')
    log = open("voice_log.txt","a")
    stamp = datetime.now()
    stamp = stamp.strftime("%m-%d-%y_%H,%M,%S")
    log.write("Starting @ " + stamp)

    q = queue.Queue()

    # print(sd.query_devices())
    # Device set to the Pi's default input, determined using the above cmd
    # Default is the Bluetooth lavalier at 11
    dev = 11

    device_info = sd.query_devices(dev, 'input')
    model = vosk.Model("model")
    dev_sr = int(device_info['default_samplerate'])

    record_cmd = 'vehicle begin recording'
    upload_cmd = 'vehicle transmit video'
    sms_cmd = 'vehicle emergency contact'

    with sd.RawInputStream(samplerate=dev_sr, blocksize = 8000, device=dev, dtype='int16',
                            channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, dev_sr)
        log.write('Entering main loop\n')
        while running:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                command = result['text']
                if(command.find(sms_cmd) >= 0):
                    print('Contacting EMS')
                    #no implementation
                    sms()
                elif(command.find(record_cmd) >= 0):
                    print('Recording Video')
                    record()
                elif(command.find(upload_cmd) >= 0):
                    print('Uploading Video')
                    upload()
                elif(command.find('secret exit command') >= 0):
                    sys.exit()
