YOLO_DETECTION_MODELS = [
    "yolov5s",
    "yolov5n",
    "yolov5l",
    "yolov5x",
    "yolov8s",
    "yolov8n",
    "yolov8l",
    "yolov8x",
]
MEDIAPIPE_DETECTION_MODELS = ["hands", "pose"]

DETECTION_FAMILIES = {
    "yolo": YOLO_DETECTION_MODELS,
    "mediapipe": MEDIAPIPE_DETECTION_MODELS,
}

YOLO_DETECTION_MODELS_CHECKPOINTS = {
    "yolov5": {
        "s": "yolov5su.pt",
        "n": "yolov5nu.pt",
        "l": "yolov5lu.pt",
        "x": "yolov5xu.pt",
    },
    "yolov8": {
        "s": "yolov8s.pt",
        "n": "yolov8n.pt",
        "l": "yolov8l.pt",
        "x": "yolov8x.pt",
    },
}
