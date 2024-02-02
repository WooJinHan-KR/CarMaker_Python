import socket
import time
import os
from pathlib import Path
from CameraRSI import VDS

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
    print("---Please wait for Sensor setting---\n")
    time.sleep(1)
    if vds.check_port():
        print("----------Sensor Connected----------\n")
        print("--Lane Keeping Assist System Start--\n")
        break

# Connect
vds.connect()    
vds.load_img()

MESSAGE = "StopSim\r"

s.send(MESSAGE.encode('utf-8'))
time.sleep(3)
s_string_val = s.recv(BUFFER_SIZE)
print (s_string_val)

s.close()
print ("Driving Done")