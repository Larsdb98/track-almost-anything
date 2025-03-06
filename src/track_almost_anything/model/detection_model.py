from track_almost_anything.api.processing.detection import ObjectDetectionConfig
from ..api.processing.utils import TorchBackend
from ..api.processing.detection import YOLO_CLASS_LABEL_DICT
from .workers import MediaPipeHandsThread, MediaPipePoseThread, YoloThread
from .source_model import SourceModel

from track_almost_anything._logging import log_info, log_debug, log_error

from PySide6.QtCore import QObject
import queue


class DetectionModel(QObject):
    def __init__(self, source_model: SourceModel):
        self.source_model = source_model

        self.detection_model = ""
        self.model_type = ""

        self.detection_confidence = 0.8

        self.items_to_detect = YOLO_CLASS_LABEL_DICT.keys()
        self.active_items = []

        self.detection_thread = None
        self.image_queue = queue.Queue()

        # self._detector = None
        self._detection_backend = TorchBackend()

    def set_detection_model(self, detection_model: str, model_type: str):
        self.detection_model = detection_model
        self.model_type = model_type
        # TODO: implement logic in case model types change. Only if necessary

    def update_detection_config(self, detection_config: ObjectDetectionConfig):
        self.detection_model = detection_config.model
        self.model_type = detection_config.model_size
        self.detection_confidence = detection_config.confidence

    def setup_detection_process(self) -> None:
        if self.detection_model == "mediapipe":
            match self.model_type:
                case "hands":
                    self.detection_thread = MediaPipeHandsThread(
                        image_queue=self.image_queue
                    )
                case "pose":
                    self.detection_thread = MediaPipePoseThread(
                        image_queue=self.image_queue
                    )
                # Default
                case _:
                    log_error(
                        f"Model :: DetectionModel: Unknown model type: {self.model_type}"
                    )
        elif self.detection_model == "yolo":
            self.detection_thread = YoloThread(
                image_queue=self.image_queue, model_type=self.model_type
            )
        else:
            log_error(
                f"Model :: DetectionModel: Unknown detection model: {self.detection_model}"
            )

    def start_detection_process(self):
        self.detection_thread.start()

    def stop_detection_process(self) -> bool:
        if self.detection_thread:
            self.detection_thread.stop()
            self.detection_thread = None
            return True
        else:
            return False
