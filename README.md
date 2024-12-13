# Hand Gesture Recognition using MediaPipe

![Hand Gesture Recognition](https://github.com/hardikm121/hand-gesture)

This Python project utilizes the [MediaPipe](https://mediapipe.dev/) library and [OpenCV](https://opencv.org/) to perform real-time hand gesture recognition. With this code, you can control your computer's cursor and keyboard using hand gestures.

## Features

* Detects and tracks hand landmarks in real time.
* Recognizes left and right-hand gestures for mouse and keyboard control.
* Control the mouse cursor and perform keyboard actions (e.g., move, click, swipe) using hand gestures.
* Easily customizable for different hand gestures and actions.
* **New Feature**: Includes a web interface for starting and stopping the project. The project now starts using `python app.py`.

## Prerequisites

Before running the code, make sure you have the following dependencies installed:

- Python 3.x
- OpenCV (`pip install opencv-python`)
- MediaPipe (`pip install mediapipe`)
- PyAutoGUI (`pip install pyautogui`)
- Flask (pip install flask) (for the web interface)

## Hand Gestures and Actions

- > **Left Hand (Mouse Control):**
  >
- Move your left hand to control the mouse cursor.
- When the index finger tip is above the index finger middle, it simulates a left mouse click.
- **Right Hand (Keyboard Control):**
  - Move your right hand to control the keyboard.
  - Swipe right or left to simulate arrow key presses ('right' or 'left').
  - Swipe up or down to simulate arrow key presses ('up' or 'down').

## Web Interface

The project now includes a simple webpage for starting and stopping the hand gesture recognition system:

* Start the application by running `python app.py`.
* Use the web interface to control when the gesture recognition system starts or stops.

## How to Use the Web Interface:

* Run the project with python app.py.
* Open your web browser and navigate to the provided URL (e.g., [http://127.0.0.1:5000](http://127.0.0.1:5000/)).

* Click the Start button to begin the gesture recognition system.
* Click the Stop button to terminate the gesture recognition system.

## Author

* Hardik Malviya
* GitHub:https://github.com/hardikm121
* https://www.linkedin.com/in/hardik288/

Enjoy controlling your computer with hand gestures! 🖐️🖥️
