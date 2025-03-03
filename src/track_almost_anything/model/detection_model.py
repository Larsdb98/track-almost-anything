from track_almost_anything.api.processing.detection import (
    YoloObjectDetection,
    ObjectDetectionConfig,
)
from ..api.processing.utils import (
    YOLO_DETECTION_MODELS_CHECKPOINTS,
    TorchBackend,
)
from ..api.processing.detection import DETECTION_FAMILIES, YOLO_CLASS_LABEL_DICT

from track_almost_anything._logging import log_info, log_debug, log_error

import numpy as np
import queue


class DetectionModel:
    def __init__(self):
        self.detection_model = ""
        self.model_size = ""
        self.max_number_items = 1

        self.detection_confidence = 0.8

        self.items_to_detect = YOLO_CLASS_LABEL_DICT.keys()
        self.active_items = []

        self.detection_thread = None
        self.image_queue = queue.Queue()

        self._detector = None
        self._detection_backend = TorchBackend()

    def setup_yolo(self, detection_submodel: str, model_size: str = "n"):
        self._detector = YoloObjectDetection(
            detection_family=detection_submodel,
            model_size=model_size,
            device=self._detection_backend.get(),
        )
        log_info(f"YOLO object detection was set up: {self.detection_model_type}")

    def update_detection_config(self, detection_config: ObjectDetectionConfig):
        self.detection_model = detection_config.model
        self.model_size = detection_config.model_size
        self.detection_confidence = detection_config.confidence

    def detect(self, image: np.ndarray):
        results = self._detector.predict(image=image)
        return results

    def destroy(self):
        if self._detector is not None:
            self._detector.destroy()
