from ultralytics import YOLO
import cv2
import time
import os
import csv
from datetime import datetime

MODEL_NAME = "yolov8s.pt"      # faster than yolov8m
CONFIDENCE_THRESHOLD = 0.65
IOU_THRESHOLD = 0.40
IMAGE_SIZE = 416              # faster than 640
CAMERA_INDEX = 0

SAVE_FOLDER = "project_outputs"
SCREENSHOT_FOLDER = os.path.join(SAVE_FOLDER, "screenshots")
VIDEO_FOLDER = os.path.join(SAVE_FOLDER, "videos")
LOG_FILE = os.path.join(SAVE_FOLDER, "detection_log.csv")

os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Object", "Confidence", "X1", "Y1", "X2", "Y2"])

print("Loading YOLO model...")
model = YOLO(MODEL_NAME)
print("Model loaded successfully.")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Error: Camera not found.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

recording = False
video_writer = None
previous_time = 0
total_frames = 0
total_detections = 0


def save_detection_to_csv(object_name, confidence, x1, y1, x2, y2):
    now = datetime.now()

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            object_name,
            round(confidence, 2),
            x1, y1, x2, y2
        ])


def save_screenshot(frame):
    filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(SCREENSHOT_FOLDER, filename)
    cv2.imwrite(filepath, frame)
    print(f"Screenshot saved: {filepath}")


def start_video_recording():
    global video_writer, recording

    filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
    filepath = os.path.join(VIDEO_FOLDER, filename)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(filepath, fourcc, 10.0, (frame_width, frame_height))

    recording = True
    print(f"Recording started: {filepath}")


def stop_video_recording():
    global video_writer, recording

    if video_writer is not None:
        video_writer.release()

    video_writer = None
    recording = False
    print("Recording stopped.")


def correct_common_mistakes(object_name, confidence, x1, y1, x2, y2):
    width = x2 - x1
    height = y2 - y1
    area = width * height

    wrong_book_labels = [
        "tie",
       
        "traffic light",
        "tv"
    ]

    if object_name in wrong_book_labels and area > 35000:
        return "book / notebook"

    return object_name


def get_box_color(object_name):
    if object_name == "person":
        return (0, 255, 0)
    elif object_name == "book / notebook":
        return (255, 0, 255)
    elif object_name == "cell phone":
        return (255, 0, 0)
    elif object_name in ["knife", "scissors"]:
        return (0, 0, 255)
    else:
        return (255, 255, 0)


def draw_detection_box(frame, object_name, confidence, x1, y1, x2, y2):
    color = get_box_color(object_name)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    label = f"{object_name} {confidence:.2f}"

    text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
    text_width, text_height = text_size

    cv2.rectangle(
        frame,
        (x1, y1 - text_height - 10),
        (x1 + text_width + 10, y1),
        color,
        -1
    )

    cv2.putText(
        frame,
        label,
        (x1 + 5, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 0),   # black text
        2
    )


def draw_small_text(frame, fps, object_count, confidence_value, recording_status):
    color = (0, 0, 0)   # black text
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 25), font, 0.60, color, 2)
    cv2.putText(frame, f"Objects: {object_count}", (10, 50), font, 0.60, color, 2)
    cv2.putText(frame, f"Conf: {confidence_value:.2f}", (10, 75), font, 0.60, color, 2)

    if recording_status:
        cv2.putText(frame, "REC ON", (10, 100), font, 0.60, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "REC OFF", (10, 100), font, 0.60, color, 2)

    cv2.putText(
        frame,
        "Q Quit | S Screenshot | R Record | +/- Confidence",
        (10, frame_height - 15),
        font,
        0.55,
        color,
        2
    )


def draw_warning(frame, detected_objects):
    if "knife" in detected_objects or "scissors" in detected_objects:
        cv2.putText(
            frame,
            "WARNING: Dangerous Object!",
            (10, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255),
            2
        )


while True:
    success, frame = cap.read()

    if not success:
        print("Error: Could not read camera frame.")
        break

    total_frames += 1

    current_time = time.time()
    fps = 1 / (current_time - previous_time) if previous_time != 0 else 0
    previous_time = current_time

    results = model(
        frame,
        conf=CONFIDENCE_THRESHOLD,
        iou=IOU_THRESHOLD,
        imgsz=IMAGE_SIZE,
        verbose=False
    )

    object_count = 0
    detected_objects = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            object_name = model.names[class_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            object_name = correct_common_mistakes(
                object_name, confidence, x1, y1, x2, y2
            )

            object_count += 1
            total_detections += 1
            detected_objects.append(object_name)

            draw_detection_box(frame, object_name, confidence, x1, y1, x2, y2)
            save_detection_to_csv(object_name, confidence, x1, y1, x2, y2)

    draw_warning(frame, detected_objects)
    draw_small_text(frame, fps, object_count, CONFIDENCE_THRESHOLD, recording)

    if recording and video_writer is not None:
        video_writer.write(frame)

    cv2.imshow("Advanced Object Detection System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord("s"):
        save_screenshot(frame)

    elif key == ord("r"):
        if recording:
            stop_video_recording()
        else:
            start_video_recording()

    elif key == ord("+") or key == ord("="):
        CONFIDENCE_THRESHOLD += 0.05
        if CONFIDENCE_THRESHOLD > 0.95:
            CONFIDENCE_THRESHOLD = 0.95
        print(f"Confidence increased to {CONFIDENCE_THRESHOLD:.2f}")

    elif key == ord("-"):
        CONFIDENCE_THRESHOLD -= 0.05
        if CONFIDENCE_THRESHOLD < 0.30:
            CONFIDENCE_THRESHOLD = 0.30
        print(f"Confidence decreased to {CONFIDENCE_THRESHOLD:.2f}")


cap.release()

if recording:
    stop_video_recording()

cv2.destroyAllWindows()

print("Program closed successfully.")
print(f"Total frames processed: {total_frames}")
print(f"Total detections made: {total_detections}")
print(f"Detection log saved at: {LOG_FILE}")