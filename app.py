from flask import Flask, Response, render_template
import cv2
import threading
from main import camera_feed_process  # Import from main.py

app = Flask(__name__)
cameras = {}
exit_signals = {}

def start_cameras():
    """Detect and initialize all available cameras."""
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            cap.release()
            break
        cameras[index] = cap
        exit_signals[index] = threading.Event()
        index += 1

def stop_cameras():
    """Release all cameras and set exit signals."""
    for index, cap in cameras.items():
        cap.release()
        exit_signals[index].set()

def generate_frames(camera_index):
    """Yield frames from camera_feed_process, managed by main.py."""
    cap = cameras[camera_index]
    exit_signal = exit_signals[camera_index]
    if cap is None or not cap.isOpened():
        return  # Early exit if the camera is not available

    for frame in camera_feed_process(camera_index, exit_signal):
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    """Video feed route for each camera."""
    return Response(generate_frames(camera_index), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Render the main page with links to all camera feeds."""
    start_cameras()  # Start or detect cameras at this point
    return render_template('index.html', cameras=cameras.keys())

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    finally:
        stop_cameras()


# from flask import Flask, Response, render_template
# import cv2
# import threading

# app = Flask(__name__)
# camera = None

# def start_camera(camera_index=0):
#     global camera
#     camera = cv2.VideoCapture(camera_index)  # Default to index 0 for the laptop camera

# def stop_camera():
#     global camera
#     if camera is not None:
#         camera.release()
#         camera = None

# def generate_frames():
#     """Yield frames from the camera to the Flask response."""
#     global camera
#     if camera is None or not camera.isOpened():
#         start_camera()

#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         ret, buffer = cv2.imencode('.jpg', frame)
#         if ret:
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         else:
#             break

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     try:
#         start_camera()
#         app.run(debug=True)
#     finally:
#         stop_camera()
# ==============================================================================

# from flask import Flask, Response, render_template
# import cv2
# from main import camera_feed_process
# app = Flask(__name__)

# def get_frame(camera_index):
#     cap = cv2.VideoCapture(camera_index)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         yield frame
#     cap.release()
    
# def generate_frames(camera_index):
#     cap = cv2.VideoCapture(camera_index)
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     cap.release()

# @app.route('/video_feed/<int:camera_index>')
# def video_feed(camera_index):
#     return Response(generate_frames(camera_index),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     # Assuming cameras are indexed at 0, 1, 2, etc.
#     num_cameras = 4  # Adjust based on your setup
#     return render_template('index.html', num_cameras=num_cameras)

# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, render_template, Response
# import threading
# import camera_system  # This assumes your camera logic is callable

# app = Flask(__name__)

# @app.route('/start_feed')
# def start_feed():
#     """Endpoint to start the camera feed."""
#     # Start the camera feed process in a new thread to avoid blocking Flask's main thread
#     thread = threading.Thread(target=camera_system.camera_feed_process, args=(0,))  # Adjust args as necessary
#     thread.daemon = True
#     thread.start()
#     return "Camera feed started!"

# @app.route('/')
# def index():
#     """Home page to control the camera."""
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

