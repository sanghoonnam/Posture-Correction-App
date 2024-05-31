import cv2
# from win10toast import ToastNotifier # 윈도우용 알림
from cptools.notify import mac_notify # 맥북용 알림

import modules.HolisticModule as hm
from modules.turtle_neck import turtlenect_detection
from modules.eye_blink import eyeblink_detection


# video input 
cap = cv2.VideoCapture(0)

# Holistic 객체(어떠한 행위를 하는 친구) 생성
detector = hm.HolisticDetector()

while True:
    # defalut BGR img
    success, img = cap.read()
    # mediapipe를 거친 이미지 생성 -> img
    img = detector.findHolistic(img, draw=False)
    # output -> list ( id, x, y, z) 32 개 좌표인데 예를 들면, (11, x, y, z)
    pose_lmList = detector.findPoseLandmark(img, draw=False)
    # 468개의 얼굴 점 리스트
    face_lmList = detector.findFaceLandmark(img, draw=False)
    
    # 인체가 감지가 되었는지 확인하는 구문
    if len(pose_lmList) != 0 and len(face_lmList) != 0:

        turtlenect_detection(detector, img, sensitivity = 8, log=False, notification=True)

        eyeblink_detection(detector, img, sensitivity = 10, log=True, notification=True)

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break 

cap.release()
cv2.destroyAllWindows()
    