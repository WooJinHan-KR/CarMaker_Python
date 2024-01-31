import sys, string, os, subprocess
from pathlib import Path
from CameraRSI import VDS
import cv2
import sys
from types import *
import numpy as np

class LaneDetector:

    def detect_lanes(self, frame):
        # 이미지를 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 엣지 검출 (Canny 사용)
        edges = cv2.Canny(gray, 50, 150)
        # Hough 변환을 사용하여 직선 검출
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=100, maxLineGap=50)
        # 검출된 직선들을 원본 이미지에 그리기
        line_image = np.zeros_like(frame)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
        # 원본 이미지와 그려진 직선들을 합성
        result = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
        return result

    def load_img(self):
        while True:
            # Capture frame-by-frame
            frame = VDS.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # 차선 검출 수행
            result = self.detect_lanes(frame)

            # 결과 이미지를 표시
            cv2.imshow('Lane Detection', result)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break