from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import threading
import time

app = Flask(__name__)

# Global variables
camera = None
detection_active = False
model = YOLO("yolov8n.pt")
lock = threading.Lock()

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.prev_time = 0
    
    def get_frame(self, detect=False):
        ret, frame = self.video.read()
        
        if not ret:
            return None
        
        if detect:
            # Run YOLOv8 inference
            results = model(frame, verbose=False)
            frame = results[0].plot()
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - self.prev_time) if (current_time - self.prev_time) > 0 else 0
            self.prev_time = current_time
            
            # Add FPS display
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()
    
    def release(self):
        self.video.release()

def gen_frames(detect=False):
    global camera
    while True:
        with lock:
            if camera is None:
                break
            
            frame = camera.get_frame(detect=detect)
            if frame is None:
                break
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(0.01)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global camera, detection_active
    
    with lock:
        if camera is None:
            camera = VideoCamera()
    
    return Response(gen_frames(detect=detection_active),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection')
def start_detection():
    global detection_active
    detection_active = True
    return jsonify({'status': 'Detection started'})

@app.route('/stop_detection')
def stop_detection():
    global detection_active
    detection_active = False
    return jsonify({'status': 'Detection stopped'})

@app.route('/close_camera')
def close_camera():
    global camera, detection_active
    detection_active = False
    if camera:
        camera.release()
        camera = None
    return jsonify({'status': 'Camera closed'})

if __name__ == '__main__':
    try:
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        if camera:
            camera.release()
        print("Application closed")
