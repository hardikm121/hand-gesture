import cv2  # Computer vision library
import mediapipe as mp  # Hand detection ke liye
import pyautogui  # Screen cursor control ke liye
import time  # Time module for gesture timing

mp_hands = mp.solutions.hands  # MediaPipe hands module
hands = mp_hands.Hands()  # Hand detection initialize kar
mp_drawing = mp.solutions.drawing_utils  # Hand landmarks draw karne ke liye

screen_width, screen_height = pyautogui.size()  # Screen ki size li

# Variables for double click detection
last_gesture_time = 0
gesture_timeout = 1.0  # Time to recognize a double click (in seconds)
double_click_threshold = 0.5  # Time within which the second click should happen for double-click to be valid

def main():
    cap = cv2.VideoCapture(0)  # Video capture start kari
    prev_x = None  # Swipe detection ke liye pehle ka x-coordinate
    prev_y = None  # Swipe detection ke liye pehle ka y-coordinate
    last_click_time = 0  # Variable to track last click time

    while cap.isOpened():  # Jab tak camera open hai
        ret, frame = cap.read()  # Camera se frame liya
        frame = cv2.flip(frame, 1)  # Image ko mirror karo 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # RGB mein convert kara for mediapipe
        results = hands.process(rgb_frame)  # Frame mein hand detect karo

        if results.multi_hand_landmarks:  # Agar hands detect hue
            for landmarks in results.multi_hand_landmarks:
                # Check karo ki hand left hai ya right
                handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)  # Frame par hand landmarks draw karo

                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Index finger tip
                index_mid = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]  # Index finger middle
                thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # Thumb tip
                thumb_mid = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]  # Thumb middle

                # Detecting a pinch gesture for double-click
                # Check if the index finger and thumb are close to each other (pinching gesture)
                pinch_distance = abs(index_tip.x - thumb_tip.x) + abs(index_tip.y - thumb_tip.y)
                
                if pinch_distance < 0.05:  # Threshold for pinch gesture (can be adjusted)
                    current_time = time.time()
                    if current_time - last_gesture_time < gesture_timeout:  # If double-click gesture is detected within the time frame
                        pyautogui.doubleClick()  # Perform double click
                        last_gesture_time = 0  # Reset after double click
                    else:
                        last_gesture_time = current_time  # Update last gesture time

                if handedness == "Left":  # Agar left hand hai
                    mcp_x = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x  # Middle finger ka x-coordinate
                    mcp_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y  # Middle finger ka y-coordinate

                    scaling_factor = 1  # Sensitivity adjust karne ke liye
                    cursor_x = int(mcp_x * screen_width * scaling_factor)  # Cursor ka x-position calculate kara
                    cursor_y = int(mcp_y * screen_height * scaling_factor)  # Cursor ka y-position calculate kara
                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)  # Cursor ko move karne ke lia

                    if index_tip.y >= index_mid.y:  # Agar index tip middle se neeche hai to click kara
                        pyautogui.click()

                elif handedness == "Right":  # Agar right hand hai
                    x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)  # Finger tip ke coordinates

                    if prev_x is not None and prev_y is not None:  # Agar pehle ka position hai
                        dx = x - prev_x  # X ka change calculate karo
                        dy = y - prev_y  # Y ka change calculate karo

                        if abs(dx) > abs(dy):  # Agar horizontal swipe hai
                            if dx > 50:
                                pyautogui.press('right')  # Right swipe
                            elif dx < -50:
                                pyautogui.press('left')  # Left swipe
                        else:  # Agar vertical swipe hai
                            if dy > 50:
                                pyautogui.press('down')  # Down swipe
                            elif dy < -50:
                                pyautogui.press('up')  # Up swipe

                    prev_x = x  # Pehle ka x update karo
                    prev_y = y  # Pehle ka y update karo

        cv2.imshow("Gesture Recognition", frame)  # Frame dikhaye

        if cv2.waitKey(10) & 0xFF == ord('q'):  # 'q' press karne par exit
            break

    cap.release()  # Camera release karo
    cv2.destroyAllWindows()  # Window close karo

if __name__ == "__main__":
    main()  # Main function start
