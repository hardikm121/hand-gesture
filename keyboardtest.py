import cv2  # Computer vision library
import mediapipe as mp  # Hand detection ke liye
import pyautogui  # Screen cursor control aur keyboard press ke liye

# Hand tracking initialize kara
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Frames pe draw karne ke liye
mp_drawing = mp.solutions.drawing_utils

# Screen ki size li
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)  # Camera access karo

prev_x = None  # Previous x-coordinate ke liye
prev_y = None  # Previous y-coordinate ke liye

while cap.isOpened():  # Jab tak camera open hai
    ret, frame = cap.read()  # Frame capture kari

    frame = cv2.flip(frame, 1)  # Frame ko horizontal flip kara

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # RGB me convert karo mediapipe ke lia
    results = hands.process(rgb_frame)  # Frame mein hand landmarks detect karo

    if results.multi_hand_landmarks:  # Agar hand landmarks detect hue
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)  # Landmarks draw kara

            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Index finger ka tip
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # Thumb ka tip
            pinky_mcp = landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]  # Pinky MCP

            # Swipe gesture detect karo index finger ke tip se
            x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)  # Index tip coordinates calculate kare

            if prev_x is not None and prev_y is not None:  # Agar pehle ka position hai
                dx = x - prev_x  # X-axis ka difference
                dy = y - prev_y  # Y-axis ka difference

                if abs(dx) > abs(dy):  # Agar horizontal swipe hai
                    if dx > 50:  # Right swipe threshold
                        pyautogui.press('right')
                    elif dx < -50:  # Left swipe threshold
                        pyautogui.press('left')
                else:  # Agar vertical swipe hai
                    if dy > 50:  # Down swipe threshold
                        pyautogui.press('down')
                    elif dy < -50:  # Up swipe threshold
                        pyautogui.press('up')

            prev_x = x  # Current x ko prev_x banaya
            prev_y = y  # Current y ko prev_y banaya

            # Rock gesture detect (thumb tip close to pinky MCP)
            distance_thumb_pinky = ((thumb_tip.x - pinky_mcp.x) ** 2 + (thumb_tip.y - pinky_mcp.y) ** 2) ** 0.5  # Thumb aur pinky ke beech ka distance

            if distance_thumb_pinky < 0.1:  # Rock gesture ka threshold
                pyautogui.press('space')

    cv2.imshow("Gesture Recognition", frame)  # Frame ko window mein show kara

    if cv2.waitKey(10) & 0xFF == ord('q'):  
        break

cap.release() 
cv2.destroyAllWindows()  
