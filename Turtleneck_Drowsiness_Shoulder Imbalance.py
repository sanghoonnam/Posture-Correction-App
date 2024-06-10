import cv2
import modules.HolisticModule as hm
# from win10toast import ToastNotifier # 윈도우용 알림
from cptools.notify import mac_notify # 맥북용 알림
import math
import numpy as np


###################################################
sensitivity = 8
###################################################

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
init_ratio=0
init_ratio_1=0
init_ratio_2=0
sleep_count=0
unbalance_count=0
init_arctan=0

import tkinter as tk
from tkinter import messagebox

# 사용자에게 보여주는 초기 알림창
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

        if length_1 != 0:
            curr_ratio = length/length_1

        # 웹캠이 켜진 화면에 내가 생각하는 이상적인 포즈인 순간에 s키를 누르면 길이가 측정되어 앞으로의 거북목 판단 근거가 된다.     
        if cv2.waitKey(1) & 0xFF == ord('s'):
            init_eye_len = detector.findFaceDistance(eye_1, eye_2, img, draw=True)[0]
            init_neck_len = detector.findDistance(152, center_shoulder, img, draw=True)[0]
            init_ratio = init_neck_len / init_eye_len

            x1, y1 = face_lmList[33][1:3]
            x2, y2 = face_lmList[159][1:3]
            x3, y3 = face_lmList[145][1:3] 
            init_ratio_1 = math.sqrt(abs(y2-y3)**2 + abs(x2-x3)**2) / math.sqrt(abs(y2-y1)**2 + abs(x2-x1)**2)

            x4, y4 = face_lmList[263][1:3]
            x5, y5 = face_lmList[386][1:3]
            x6, y6 = face_lmList[374][1:3] 
        
            init_ratio_2 = math.sqrt(abs(y5-y6)**2 + abs(x5-x6)**2) / math.sqrt(abs(y5-y4)**2 + abs(x5-x4)**2)

            x11, y11 = pose_lmList[11][1:3]
            x22, y22 = pose_lmList[12][1:3]
            init_arctan = math.atan((y22-y11)/(x22-x11))
            
        # 핵심 로직 목 길이와 눈 사이의 길이 비율이 정자세에서 측정한 경우 보다 작을 때, 거북목으로 생각한다.
        if init_ratio!=0 and curr_ratio < init_ratio*0.85:
            turtle_neck_count += 1
        
        elif init_ratio!=0 and curr_ratio >= init_ratio*0.85:
            turtle_neck_count = 0

        # 목길이, 임계치, 노트북과의 거리
        print("Current ratio: {:.3f}, Init ratio : {:.3f}, Turtle neck count : {}".format(curr_ratio, init_ratio, turtle_neck_count))

        # 10번 거북목으로 인식되면 알림을 제공한다. 
        if init_ratio!=0 and curr_ratio < init_ratio*0.85 and turtle_neck_count > 20:
            # 얼마나 거북목인지 계산해주는 부분 (0~ 100 점) 
            # tutleneck_score = int((turtleneck_detect_threshold - int(length))/turtleneck_detect_threshold*100)
            turtleneck_score = int((init_ratio - curr_ratio)/init_ratio*100)
            print("WARNING - Keep your posture straight.")
            print(f"TurtleNeck Score = {turtleneck_score}",)
            # win10toast 알림 제공
            print("TurtleNect WARNING", f"Keep your posture straight.\n\nDegree Of TurtleNeck = {turtleneck_score}")
            mac_notify(title='당신은 거북목입니다', text='자세를 고쳐주세요!!!')
            # toaster.show_toast('당신은 거북목입니다', '자세를 고쳐주세요!!!')
            # 알림 제공 후 카운트를 다시 0으로 만든다.
            turtle_neck_count = 0

    # 졸음 탐지 기능 코드
    if len(face_lmList) != 0:
        x1, y1 = face_lmList[33][1:3]
        x2, y2 = face_lmList[159][1:3]
        x3, y3 = face_lmList[145][1:3] 
        
        dist_1 = math.sqrt(abs(y2-y3)**2 + abs(x2-x3)**2) 
        dist_2 = math.sqrt(abs(y2-y1)**2 + abs(x2-x1)**2) 

        x4, y4 = face_lmList[263][1:3]
        x5, y5 = face_lmList[386][1:3]
        x6, y6 = face_lmList[374][1:3] 
        
        dist_3 = math.sqrt(abs(y5-y6)**2 + abs(x5-x6)**2) 
        dist_4 = math.sqrt(abs(y5-y4)**2 + abs(x5-x4)**2) 
        
        
    if dist_1/dist_2 < init_ratio_1*0.85 or dist_3/dist_4 < init_ratio_2*0.85:
        sleep_count += 1
    else:
        sleep_count = 0

    
    if sleep_count > 20:
        # sleep_detection_toaster.show_toast("Sleepiness WARNING", f" \nPlease Stretch your body.\n")
        mac_notify(title='당신은 졸고 있습니다', text='스트레칭을 진행해주세요!!')
        # toaster.show_toast('당신은 졸고 있습니다', '스트레칭을 진행해주세요!!')
        print("[ Sleepiness WARNING ] - Please Stretch your body")
        sleep_count = 0

    print("ratio : ({:.3f},{:.3f}), init_ratio : ({:.3f},{:.3f}),  sleep_count :{}".format(dist_1/dist_2,dist_3/dist_4,init_ratio_1,init_ratio_2, sleep_count))

    # 어깨 불균형 측정 코드
    if len(face_lmList) != 0:
        x11, y11 = pose_lmList[11][1:3]
        x22, y22 = pose_lmList[12][1:3]
        _, img = detector.findFaceDistance((x11,y11), (x22,y22), img, draw=True)
        
        curr_arctan = math.atan((y22-y11)/(x22-x11))
        
    if abs(curr_arctan - init_arctan) > 5 * 2 * math.pi / 360:
        unbalance_count += 1
    else:
        unbalance_count = 0

    
    if unbalance_count > 20:
        mac_notify(title='당신의 자세가 불균형합니다!', text='어깨에 힘을 빼고 편안하게 있어주세요!!')
        # toaster.show_toast('당신의 자세가 불균형합니다!', '어깨에 힘을 빼고 편안하게 있어주세요!!')
        print("[ Unbalanced Posture WARNING ] - Please Relax your body")
        unbalance_count = 0

    print("Current arctan : {:.3f}, init arctan : {:.3f},  unbalance_count :{}".format(curr_arctan,init_arctan,unbalance_count))

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break 

cap.release()
cv2.destroyAllWindows()
