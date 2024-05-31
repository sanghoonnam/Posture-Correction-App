import cv2
import time
import modules.HolisticModule as hm
# from win10toast import ToastNotifier # 윈도우용 알림
from cptools.notify import mac_notify # 맥북용 알림
import math
import numpy as np

###################################################
sensitivity = 8
###################################################

# privious time for fps
pTime = 0
# cerrent time for fps
cTime = 0

# video input 
# cap = cv2.VideoCapture(-1, cv2.CAP_ANY)
cap = cv2.VideoCapture(0)

# Holistic 객체(어떠한 행위를 하는 친구) 생성
detector = hm.HolisticDetector()

# toast 알림을 주는 객체 생성
# toaster = ToastNotifier()

# turtle_neck_count 변수 초기 세팅
turtle_neck_count = 0

# 목 길이 저장하는 array
len_arr=np.array([])
init_len=0
init_eye_len=0
init_neck_len=0

import tkinter as tk
from tkinter import messagebox

def create_alert():
    # 메인 윈도우 생성
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨김

    # 화면 크기와 메인 윈도우 크기를 구하여 화면 중앙에 위치시킴
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'+{screen_width // 2}+{screen_height // 2}')

    # 알림창 표시
    messagebox.showinfo("알림", "가장 올바른 자세에서 s키를 눌러주세요!!")

    # 이벤트 루프 종료
    root.destroy()
create_alert()

while True:
    # defalut BGR img
    success, img = cap.read()

    # mediapipe를 거친 이미지 생성 -> img
    img = detector.findHolistic(img, draw=True)

    # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
    pose_lmList = detector.findPoseLandmark(img, draw=True)
    # 468개의 얼굴 점 리스트
    face_lmList = detector.findFaceLandmark(img, draw=True)

    # 인체가 감지가 되었는지 확인하는 구문
    if len(pose_lmList) != 0 and len(face_lmList) != 0:
        # print("pose[11]", pose_lmList[11])
        # print("pose[12]", pose_lmList[12])
        # print("face[152]",face_lmList[152])

        # 양 어깨 좌표 11번과 12번의 중심 좌표를 찾아 낸다.
        center_shoulder = detector.findCenter(11,12)

        # 양쪽 눈 중심 좌표 찾아 낸다.
        eye_1 = detector.findFaceCenter(159,145)
        eye_2 = detector.findFaceCenter(386,374)

        # 목 길이 center_shoulder 좌표와 얼굴 152번(턱) 좌표를 사용하여 길이 구하는 부분
        # 목 길이가 표시된 이미지로 변경
        length, img = detector.findDistance(152, center_shoulder, img, draw=True)

        # 양쪽 눈 사이의 길이 측정 및 이미지 표시
        length_1, img = detector.findFaceDistance(eye_1, eye_2, img, draw=True)

        len_arr = np.append(len_arr,length)
        if len_arr.shape[0]>10:
            init_len = len_arr[-10:].mean()
        
        # 웹캠이 켜진 화면에 내가 생각하는 이상적인 포즈인 순간에 s키를 누르면 길이가 측정되어 앞으로의 거북목 판단 근거가 된다.     
        if cv2.waitKey(5) & 0xFF == ord('s'):
            init_eye_len = detector.findFaceDistance(eye_1, eye_2, img, draw=True)[0]
            init_neck_len = detector.findDistance(152, center_shoulder, img, draw=True)[0]
        # print(f"neck:{length}, eyes:{length_1}, ratio:{length/length_1}")        
        # 핵심 로직 목 길이가 임계치보다 작을 때, 거북목으로 생각한다.
        if length < init_len*0.9:
            turtle_neck_count += 1
        # 목길이, 임계치, 노트북과의 거리
        print("Length : {:.3f},   Mean of length : {:.3f}, Turtle neck count : {:.3f}".format(length, init_len, turtle_neck_count))

        # 10번 거북목으로 인식되면 알림을 제공한다. 
        # if length < turtleneck_detect_threshold and turtle_neck_count > 10:
        if length < init_len*0.9 and turtle_neck_count > 10:
            # 얼마나 거북목인지 계산해주는 부분 (0~ 100 점) 
            # tutleneck_score = int((turtleneck_detect_threshold - int(length))/turtleneck_detect_threshold*100)
            turtleneck_score = int((init_len - int(length))/init_len*100)
            print("WARNING - Keep your posture straight.")
            print(f"TurtleNeck Score = {turtleneck_score}",)
            # win10toast 알림 제공
            print("TurtleNect WARNING", f"Keep your posture straight.\n\nDegree Of TurtleNeck = {turtleneck_score}")
            mac_notify(title='당신은 거북목입니다', text='자세를 고쳐주세요!!!')
            # toaster.show_toast("TurtleNect WARNING", f"Keep your posture straight.\n\nDegree Of TurtleNeck = {tutleneck_score}")
            # 알림 제공 후 카운트를 다시 0으로 만든다.
            turtle_neck_count = 0

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break 

cap.release()
cv2.destroyAllWindows()
    