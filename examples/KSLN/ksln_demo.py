import cv2
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import modules.HolisticModule as hm



# video input 
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Holistic 객체 생성
detector = hm.HolisticDetector()



while True:

    number = 0
    # defalut BGR img
    success, img = cap.read()
    # mediapipe를 거친 이미지 생성 -> img
    img = detector.findHolistic(img, draw=True)
    
    
    # left_hand_lmList = detector.findLefthandLandmark(img, draw=False)
    right_hand_lmList = detector.findRighthandLandmark(img, draw=True)

    # 인체가 감지가 되었는지 확인하는 구문
    # if len(left_hand_lmList) != 0 and len(right_hand_lmList) != 0:
    if len(right_hand_lmList) != 0:
        right_hand_fingersUp_list_a0 = detector.right_hand_fingersUp(axis=False)
        right_hand_fingersUp_list_a1 = detector.right_hand_fingersUp(axis=True)
        thumb_index_length = detector.findLength_rh_rh(4, 8)
        print(right_hand_fingersUp_list_a0, right_hand_fingersUp_list_a1)

        

        if right_hand_lmList[5][1] > right_hand_lmList[17][1] and right_hand_lmList[4][2] > right_hand_lmList[8][2]:
            if right_hand_fingersUp_list_a0 == [0, 1, 0, 0, 0] and right_hand_lmList[8][2] < right_hand_lmList[7][2]:
                number = 1
            elif right_hand_fingersUp_list_a0 == [0, 1, 1, 0, 0]:
                number = 2
            elif right_hand_fingersUp_list_a0 == [0, 1, 1, 1, 0]:
                number = 3
            elif right_hand_fingersUp_list_a0 == [0, 1, 1, 1, 1]:
                number = 4
            
            elif right_hand_fingersUp_list_a0 == [1, 0, 1, 1, 1] and thumb_index_length < 30:
                number = 10

        if right_hand_lmList[5][1] > right_hand_lmList[17][1]:
            if right_hand_fingersUp_list_a0 == [1, 0, 0, 0, 0]:
                number = 5

        if right_hand_fingersUp_list_a0[0] == 0 and right_hand_fingersUp_list_a0[2:] == [0, 0, 0] and right_hand_lmList[8][2] + 20 >= right_hand_lmList[7][2]:
            number = 10

        if right_hand_lmList[5][2] < right_hand_lmList[17][2] and right_hand_lmList[4][2] < right_hand_lmList[8][2]:
            if right_hand_fingersUp_list_a1 == [1, 1, 0, 0, 0]:
                number = 6
            elif right_hand_fingersUp_list_a1 == [1, 1, 1, 0, 0]:
                number = 7
            elif right_hand_fingersUp_list_a1 == [1, 1, 1, 1, 0]:
                number = 8
            elif right_hand_fingersUp_list_a1 == [1, 1, 1, 1, 1]:
                number = 9

        



    # Get status box
    cv2.rectangle(img, (0,0), (100, 60), (245, 117, 16), -1)

    # Display Probability
    cv2.putText(img, 'NUMBER'
                , (15,18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(number)
                , (25,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # img를 우리에게 보여주는 부분
    cv2.imshow("Image", img)

    # ESC 키를 눌렀을 때 창을 모두 종료하는 부분
    if cv2.waitKey(1) & 0xFF == 27:
        break 

cap.release()
cv2.destroyAllWindows()
    