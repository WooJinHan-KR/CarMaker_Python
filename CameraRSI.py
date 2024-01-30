import sys
import os
import logging
from types import *
import time, socket
import cv2
import numpy as np

class VDS:
    def __init__(self, ip="localhost", port=2210, log_level=logging.INFO):
        self.logger = logging.getLogger("Autonomous.py")
        self.logger.setLevel(log_level)
        self.ip = ip
        self.port = port
        self.socket = None
        self.cameras = []
        self.connected = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        data = self.socket.recv(64)
        if(data.decode().find("*IPGMovie") != -1):
            self.logger.info("IPG Movie is Connected...")
            self.connected = True

    def check_port(self):
        try:
            sock = socket.create_connection((self.ip, self.port), timeout=1)
            sock.close()
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False        

    def read(self):

        if not self.connected:
            self.logger.error("Connect first by calling .connect()")
            return None
        
        self.socket.setblocking(False)

        # Get Image header and fill data
        data = self.socket.recv(64)
        splitdata = data.decode().split(" ")
        imgtype = splitdata[2]
        img_size = splitdata[4]
        data_len = int(splitdata[5])
        imag_h = int(img_size.split('x')[1])
        image_w = int(img_size.split('x')[0])
        lastdata = b''
        size = 0

        while(size != data_len):
            data = self.socket.recv(1024)
            try:
                strdata = data.decode()
                if strdata[0] == '*' and strdata[1] == 'V':
                    splitdata = data.decode().split(" ")
                    imgtype = splitdata[2]
                    img_size = splitdata[4]
                    data_len = int(splitdata[5])
                    imag_h = int(img_size.split('x')[1])
                    image_w = int(img_size.split('x')[0])
                    lastdata = b''
                    size = 0
                    continue
            except socket.error as e:
                # Handle non-blocking socket error (no data available)
                if e.errno == socket.errno.EWOULDBLOCK:
                    continue
                else:
                    # Handle other socket errors
                    self.logger.error(f"Socket error: {e}")
                    return None
                #pass

            lastdata += data
            size = np.frombuffer(lastdata, dtype=np.uint8).size
            
        datalist = np.frombuffer(lastdata, dtype=np.uint8)
        if(imgtype == "rgb"):
            img = datalist.reshape((imag_h, image_w, 3))
        elif(imgtype == "grey"):
            img = datalist.reshape((imag_h, image_w))
        else:
            self.logger.error("rgb and gray are supported for now")

        return img
