import cv2
from ultralytics import YOLO
import time

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Set webcam resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# FPS counter variables
prev_time = 0

print("Starting live object detection. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Run YOLOv8 inference
    results = model(frame, verbose=False)
    
    # Visualize results
    annotated_frame = results[0].plot()
    
    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
    prev_time = current_time
    
    # Add FPS to frame
    cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow("Live YOLOv8 Object Detection", annotated_frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Detection stopped.")
