import csv
from ultralytics import YOLO

# Load the model
model = YOLO("../models/2best.pt")

# Path to the video file
video_path = "../test_vids/recorded_video_0.avi"

# Path to the CSV file
csv_path = "../data_points/data_cords.csv"

# Open the CSV file in write mode initially to write the header
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x', 'y', 'w', 'h'])  # write the header

# Predict with the model and write data after each loop
results = model(video_path)  # predict on a video

for result in results:
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        boxes = result.boxes.xywh  # get boxes with xywh format
        for box in boxes:
            writer.writerow(box.tolist())  # convert tensor to list and write

print(f"Data coordinates have been written to {csv_path}")