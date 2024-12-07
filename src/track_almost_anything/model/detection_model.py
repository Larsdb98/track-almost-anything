from track_almost_anything.api.processing.detection import YoloObjectDetection
from track_almost_anything.api.processing.utils import (
    DETECTION_MODELS,
    DETECTION_FAMILIES,
    TorchBackend,
)

from track_almost_anything._logging import log_info, log_debug, log_error


class DetectionModel():
    def __init__(self, detection_model_type: str, detection_model_confidence: float):
        self.detection_model_type = detection_model_type
        self.detection_family = "yolo"
        self.detection_confidence = detection_model_confidence
        
        self._detector = None
        self._detection_backend = TorchBackend()

    def setup_yolo(self):
        self._detector = YoloObjectDetection(
            detection_family=self.detection_model_type,
            model_size="n",
            device=self._detection_backend.get(),
        )
        log_info(f"Following YOLO object detection was set up: {self.detection_model_type}")

    def detect(self):
        self.detector.predict

    def destroy(self):
        if self._detector is not None:
            self._detector.destroy()
