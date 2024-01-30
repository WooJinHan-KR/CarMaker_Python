import socket
import time
import sys, string, os, subprocess
from pathlib import Path
from CameraRSI import VDS
import cv2

CM_PATH = Path("C:/IPG/carmaker/win64-12.0.1/bin/CM.exe")
CM_PROJ = Path("C:/CM_Projects/Python")

TCP_IP = 'localhost'
TCP_PORT = 16660
BUFFER_SIZE = 1024

# initalize VDS
vds = VDS()

os.chdir('C:/IPG/carmaker/win64-12.0.1/bin')
os.system('CM.exe')

# wait CM GUI
time.sleep(2)

# Open TCP/IP Ports in Python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

MESSAGE = "LoadTestRun PythonAutonomous\n"\
        + "QuantSubscribe {Time}\n"\
        + "StartSim\n"\
        + "WaitForCondition {$Qu(Time) > 100}\n"
s.send(MESSAGE.encode('utf-8'))
s_string_val = s.recv(BUFFER_SIZE)

for _ in range(10):
    print("Please wait for Sensor setting.", end=" ")
    time.sleep(1)
    for dot_count in range(1, _ + 2):
        print(".", end="")
        if vds.check_port():
            break
    else :
        print()
    if vds.check_port():
        break

# Connect
vds.connect()    

# Read Images
while(True):
    # Capture frame-by-frame
    frame = vds.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

MESSAGE = "StopSim\r"

s.send(MESSAGE.encode('utf-8'))
time.sleep(3)
s_string_val = s.recv(BUFFER_SIZE)
print (s_string_val)

s.close()
print ("Driving Done")
