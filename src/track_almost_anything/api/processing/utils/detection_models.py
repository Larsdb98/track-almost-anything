YOLO_DETECTION_MODELS = ["yolov5", "yolov8"]

DETECTION_FAMILIES = {"yolo": YOLO_DETECTION_MODELS, "mediapipe": ["hands", "pose"]}

DETECTION_MODELS_CHECKPOINTS = {
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
