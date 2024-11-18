from flask import Flask, render_template, jsonify, send_file
import subprocess
import os

app = Flask(__name__)
process = None  # To store the subprocess

@app.route("/")
def index():  
    return render_template("index.html")  # Render the front page

@app.route("/start", methods=["GET"])
def start_gesture_control():
    global process
    if process is None or process.poll() is not None:
        # Start the gesture control script
        try:
            process = subprocess.Popen(["python", "main.py"])
            app.logger.info("Gesture control started successfully.")
            return jsonify({"status": "success", "message": "Gesture control started!"})
        except Exception as e:
            app.logger.error(f"Error starting gesture control: {e}")
            return jsonify({"status": "error", "message": f"Error starting gesture control: {e}"})
    else:
        app.logger.warning("Gesture control is already running.")
        return jsonify({"status": "error", "message": "Gesture control is already running!"})

@app.route("/stop", methods=["GET"])
def stop_gesture_control():
    global process
    if process is not None and process.poll() is None:
        try:
            process.terminate()
            process = None
            app.logger.info("Gesture control stopped successfully.")
            return jsonify({"status": "success", "message": "Gesture control stopped successfully!"})
        except Exception as e:
            app.logger.error(f"Error stopping gesture control: {e}")
            return jsonify({"status": "error", "message": f"Error stopping gesture control: {e}"})
    else:
        app.logger.warning("No gesture control process is running.")
        return jsonify({"status": "error", "message": "No gesture control process is running!"})

@app.route("/open-file", methods=["GET"])
def open_file():
    try:
        file_path = os.path.join(os.getcwd(), "main.py")  # Get absolute path of main.py
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False)  # Open file in browser
        else:
            return jsonify({"status": "error", "message": "File not found!"})
    except Exception as e:
        app.logger.error(f"Error opening file: {e}")
        return jsonify({"status": "error", "message": f"Error opening file: {e}"})

if __name__ == "__main__":
    # Ensure that the app runs on the specified port when deployed
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
