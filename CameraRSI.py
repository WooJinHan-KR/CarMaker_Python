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
            return

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
            except :
                pass
            
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
    
    def detect_lanes(self, frame):
        # frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define yellow and white color ranges
        yellow_lower = np.array([20, 100, 100], dtype=np.uint8)
        yellow_upper = np.array([30, 255, 255], dtype=np.uint8)
        white_lower = np.array([200, 200, 200], dtype=np.uint8)
        white_upper = np.array([255, 255, 255], dtype=np.uint8)

        # Create masks for yellow and white regions
        yellow_mask = cv2.inRange(frame, yellow_lower, yellow_upper)
        white_mask = cv2.inRange(frame, white_lower, white_upper)

        # Combine the masks
        combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

        # Apply the combined mask to the grayscale image
        masked_gray = cv2.bitwise_and(gray, gray, mask=combined_mask)

        # Define vertices for the region of interest (ROI)
        height, width = frame.shape[:2]
        roi_vertices = np.array([[(0, height * 5 / 6), (0, height / 2), (width, height / 2), (width, height * 5 / 6)]], dtype=np.int32)

        # Apply the ROI mask to the masked grayscale image
        roi_masked_gray = self.region_of_interest(masked_gray, roi_vertices)

        # CannyEdge
        edges = cv2.Canny(roi_masked_gray, 50, 150)

        # HoughTransform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=15, maxLineGap=70)
        # Draw line
        if lines is None:
            return frame
        line_image = np.zeros_like(frame)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
        result = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
        return result
    
    def region_of_interest(self, img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked_img = cv2.bitwise_and(img, mask)
        return masked_img

    def load_img(self) :
        while(True):
            # Capture frame-by-frame
            #MESSAGE = "DVARead DM.Lap.No\r"
            frame = self.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            result = self.detect_lanes(frame)

            cv2.imshow('frame', frame)
            cv2.imshow('Lane Detection', result)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
