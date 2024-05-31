# from win10toast import ToastNotifier
from cptools.notify import mac_notify # 맥북용 알림
import math
import cv2

sleep_count = 0
init_ratio_1 = 0.01
init_ratio_2 = 0.01

def sleepiness_detection(detector, img, log=False, notification=True):

    global sleep_count
    global init_ratio_1
    global init_ratio_2
    # toast 알림을 주는 객체 생성
    # sleep_detection_toaster = ToastNotifier()
    
    face_lmList = detector.findFaceLandmark(img, draw=False)
    if cv2.waitKey(5) & 0xFF == ord('s'):
        x1, y1 = face_lmList[33][1:3]
        x2, y2 = face_lmList[159][1:3]
        x3, y3 = face_lmList[145][1:3] 
        init_ratio_1 = math.sqrt(abs(y2-y3)**2 + abs(x2-x3)**2) / math.sqrt(abs(y2-y1)**2 + abs(x2-x1)**2)

        x4, y4 = face_lmList[263][1:3]
        x5, y5 = face_lmList[386][1:3]
        x6, y6 = face_lmList[374][1:3] 
        
        init_ratio_2 = math.sqrt(abs(y5-y6)**2 + abs(x5-x6)**2) / math.sqrt(abs(y5-y4)**2 + abs(x5-x4)**2)

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
        
        
    if dist_1/dist_2 < init_ratio_1*0.9 or dist_3/dist_4 < init_ratio_2*0.9:
        sleep_count += 1
    else:
        sleep_count = 0

    
    if sleep_count > 30:
        if notification:
            # sleep_detection_toaster.show_toast("Sleepiness WARNING", f" \nPlease Stretch your body.\n")
            mac_notify(title='당신은 졸고 있습니다', text='스트레칭을 진행해주세요!!')

        print("[ Sleepiness WARNING ] - Please Stretch your body")
        sleep_count = 0

    print("ratio :", (dist_1/dist_2,dist_3/dist_4),"init_ratio :", (init_ratio_1, init_ratio_2), "  sleep_count :", sleep_count)
