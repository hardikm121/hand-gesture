import cv2  # Computer vision library
import mediapipe as mp  # Hand detection
import pyautogui  # Screen cursor control
import time  # Time module for gesture timing

mp_hands = mp.solutions.hands  # MediaPipe hands module
hands = mp_hands.Hands()  # Initialize hand detection
mp_drawing = mp.solutions.drawing_utils  # To draw hand landmarks

screen_width, screen_height = pyautogui.size()  # Get screen size

# Variables for double-click detection
last_gesture_time = None  # Initialize as None
gesture_timeout = 1.0  # Time to recognize a double-click (in seconds)
double_click_threshold = 0.5  # Time within which the second click should happen

def main():
    global last_gesture_time  # Make sure the global variable is used
    cap = cv2.VideoCapture(0)  # Start video capture
    prev_x = None  # For swipe detection (previous x-coordinate)
    prev_y = None  # For swipe detection (previous y-coordinate)

    while cap.isOpened():  # While camera is open
        ret, frame = cap.read()  # Read frame from camera
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally (mirror effect)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB for MediaPipe
        results = hands.process(rgb_frame)  # Process the frame for hand landmarks

        if results.multi_hand_landmarks:  # If hands are detected
            for landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Index finger tip
                thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # Thumb tip

                # Detecting a pinch gesture for double-click
                pinch_distance = abs(index_tip.x - thumb_tip.x) + abs(index_tip.y - thumb_tip.y)

                # If pinch gesture is detected, check if it's a double-click
                if pinch_distance < 0.1:  # Adjust threshold for pinch distance
                    current_time = time.time()  # Get current time when pinch is detected
                    if last_gesture_time is not None and current_time - last_gesture_time < gesture_timeout:  # If it's within double-click time window
                        pyautogui.doubleClick()  # Perform double click
                        last_gesture_time = None  # Reset after double click
                    else:
                        last_gesture_time = current_time  # Update last gesture time

                # Hand detection and actions based on hand (left or right)
                handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label
                if handedness == "Left":  # If left hand
                    mcp_x = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x  # X coordinate of middle finger base
                    mcp_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y  # Y coordinate of middle finger base

                    # Calculate cursor position based on hand landmarks
                    scaling_factor = 1  # Sensitivity for cursor movement
                    cursor_x = int(mcp_x * screen_width * scaling_factor)
                    cursor_y = int(mcp_y * screen_height * scaling_factor)
                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)  # Move the cursor

                    # Left-click when index tip is below middle finger
                    if index_tip.y >= landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                        pyautogui.click()

                elif handedness == "Right":  # If right hand
                    x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)  # Get screen coordinates for right hand

                    if prev_x is not None and prev_y is not None:
                        dx = x - prev_x  # X-axis change
                        dy = y - prev_y  # Y-axis change

                        # Swipe detection based on horizontal or vertical movement
                        if abs(dx) > abs(dy):
                            if dx > 50:
                                pyautogui.press('right')  # Right swipe
                            elif dx < -50:
                                pyautogui.press('left')  # Left swipe
                        else:
                            if dy > 50:
                                pyautogui.press('down')  # Down swipe
                            elif dy < -50:
                                pyautogui.press('up')  # Up swipe

                    prev_x = x  # Update previous coordinates
                    prev_y = y

        cv2.imshow("Gesture Recognition", frame)  # Display the frame with hand landmarks

        if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()  # Release camera
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()  # Run the main function  AT http://127.0.0.1:5000/
