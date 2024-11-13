# Hand Gesture Recognition using MediaPipe

![Hand Gesture Recognition](https://github.com/hardikm121/hand-gesture)

This Python project utilizes the [MediaPipe](https://mediapipe.dev/) library and [OpenCV](https://opencv.org/) to perform real-time hand gesture recognition. With this code, you can control your computer's cursor and keyboard using hand gestures.

## Features

- Detects and tracks hand landmarks in real time.
- Recognizes left and right-hand gestures for mouse and keyboard control.
- Control the mouse cursor and perform keyboard actions (e.g., move, click, swipe) using hand gestures.
- Easily customizable for different hand gestures and actions.

## Prerequisites

Before running the code, make sure you have the following dependencies installed:

- Python 3.x
- OpenCV (`pip install opencv-python`)
- MediaPipe (`pip install mediapipe`)
- PyAutoGUI (`pip install pyautogui`)

## Hand Gestures and Actions

-  > **Left Hand (Mouse Control):**
  - Move your left hand to control the mouse cursor.
  - When the index finger tip is above the index finger middle, it simulates a left mouse click.
- **Right Hand (Keyboard Control):**
  - Move your right hand to control the keyboard.
  - Swipe right or left to simulate arrow key presses ('right' or 'left').
  - Swipe up or down to simulate arrow key presses ('up' or 'down').

## Customization

You can customize this code to recognize additional hand gestures and map them to different actions. Modify the code to add your own gestures and actions.

## Acknowledgments

This project uses the [MediaPipe](https://mediapipe.dev/) library for hand landmark detection and tracking.

## Author

- Hardik Malviya
- GitHub:https://github.com/hardikm121

Enjoy controlling your computer with hand gestures! 🖐️🖥️
