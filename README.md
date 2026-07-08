# 🎯 Advanced Real-Time Object Detection System using YOLOv8

A real-time object detection application built with **Python**, **OpenCV**, and **Ultralytics YOLOv8**. The system detects objects from a webcam feed, displays bounding boxes with confidence scores, logs detections to a CSV file, captures screenshots, records videos, and provides visual warnings for potentially dangerous objects.

---

## 📌 Features

- ✅ Real-time object detection using YOLOv8
- ✅ Webcam live detection
- ✅ Adjustable confidence threshold during runtime
- ✅ Color-coded bounding boxes
- ✅ Detection confidence display
- ✅ FPS monitoring
- ✅ Object counter
- ✅ Automatic CSV logging of every detection
- ✅ Screenshot capture
- ✅ Video recording
- ✅ Dangerous object warning (Knife & Scissors)
- ✅ Automatic folder creation for outputs
- ✅ Lightweight and easy to run

---

## 🛠 Technologies Used

- Python 3.x
- OpenCV
- Ultralytics YOLOv8
- NumPy
- CSV
- Datetime
- OS

---

## 📂 Project Structure

```
Advanced-Object-Detection/
│
├── object_detection.py
├── yolov8s.pt
├── README.md
│
├── project_outputs/
│   ├── screenshots/
│   ├── videos/
│   └── detection_log.csv
│
└── requirements.txt
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Advanced-Object-Detection.git

cd Advanced-Object-Detection
```

### 2. Create a virtual environment (Optional)

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install ultralytics opencv-python
```

---

## ▶️ Running the Project

```bash
python object_detection.py
```

The webcam will open automatically and begin detecting objects.

---

## ⌨️ Keyboard Controls

| Key | Function |
|------|----------|
| **Q** | Quit the application |
| **S** | Save screenshot |
| **R** | Start/Stop video recording |
| **+** | Increase confidence threshold |
| **-** | Decrease confidence threshold |

---

## 📊 Detection Logging

Every detected object is automatically stored in:

```
project_outputs/detection_log.csv
```

Each record contains:

- Date
- Time
- Object Name
- Confidence Score
- Bounding Box Coordinates

---

## 📷 Screenshots

Press:

```
S
```

Screenshots are saved inside:

```
project_outputs/screenshots/
```

---

## 🎥 Video Recording

Press:

```
R
```

Recorded videos are saved inside:

```
project_outputs/videos/
```

---

## ⚠️ Dangerous Object Detection

The application displays a warning whenever one of the following objects is detected:

- Knife
- Scissors

---

## 🎨 Bounding Box Colors

| Object | Color |
|---------|-------|
| Person | Green |
| Book / Notebook | Purple |
| Cell Phone | Blue |
| Knife / Scissors | Red |
| Others | Yellow |

---

## ⚙️ Configurable Parameters

The following values can easily be modified:

```python
MODEL_NAME = "yolov8s.pt"
CONFIDENCE_THRESHOLD = 0.65
IOU_THRESHOLD = 0.40
IMAGE_SIZE = 416
CAMERA_INDEX = 0
```

---

## 📈 Future Improvements

- Multi-camera support
- Object tracking (ByteTrack/DeepSORT)
- Face recognition
- Email/SMS alerts
- Voice notifications
- GUI using PyQt or Tkinter
- GPU optimization
- Cloud storage integration


---

## 👨‍💻 Author

**Muneeba Zahir**

Computer Engineer  
Air University, Islamabad

---

## ⭐ If you found this project helpful, don't forget to star the repository!
