from ultralytics import YOLO

# Load the YOLOv8 pretrained model
model = YOLO("yolov8n.pt")  # nano model (fastest, smallest)

# Image source from COCO dataset
source = 'http://images.cocodataset.org/val2017/000000039769.jpg'

# Run predictions and save results
results = model.predict(source=source, save=True)
print("Prediction complete! Results saved.")
