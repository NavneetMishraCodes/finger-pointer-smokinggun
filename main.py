import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
cap = cv2.VideoCapture(0)
hand_detector = HandDetector(maxHands=1, detectionCon=0.5, minTrackCon=0.5)
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    hands, frame = hand_detector.findHands(frame)
    if hands:
        for hand in hands:
            landmarks = hand["lmList"]
            index_x, index_y = landmarks[8][0], screen_height/frame_height*landmarks[8][1]
            thumb_x, thumb_y = landmarks[4][0], screen_height/frame_height*landmarks[4][1]
            cv2.circle(frame, (index_x, landmarks[8][1]), 10, (0, 255, 255), -1)
            cv2.circle(frame, (thumb_x, landmarks[4][1]), 10, (0, 255, 255), -1)
            print('outside', abs(index_y - thumb_y))
            if abs(index_y - thumb_y) < 20:
                pyautogui.click()
                pyautogui.sleep(1)
            elif abs(index_y - thumb_y) < 100:
                pyautogui.moveTo(screen_width/frame_width*index_x, index_y)
    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()