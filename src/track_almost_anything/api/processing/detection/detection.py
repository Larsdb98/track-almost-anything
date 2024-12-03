from track_almost_anything import PATH_TO_DETECTION_MODELS
from track_almost_anything.api.processing.utils import (
    TorchBackend,
    DETECTION_MODELS,
    DETECTION_FAMILIES,
)
from track_almost_anything._logging import log_info, log_debug

import numpy as np
from ultralytics import YOLO
from pydantic import BaseModel
from typing import Tuple, List, Dict


class ObjectDetectionInferenceConfig(BaseModel):
    image_dimensions: Tuple[int, int]
    boxes: List[Tuple[float, float, float, float]]  # xyxy
    classes: List[int]
    names: Dict[int, str]


class ObjectDetection:
    def __init__(
        self, detection_family: str = "yolov8", model_size: str = "n", device=None
    ):
        self._detection_family = detection_family
        if device is None:
            backend = TorchBackend()
            self.device = backend.get()
        else:
            self.device = device
        log_debug(f"Detection :: init - Using detection backend: {self.device}")

        if detection_family in DETECTION_FAMILIES["yolo"]:
            self.detector = self.set_yolo_detector(
                detection_family=detection_family, model_size=model_size
            )

    def set_yolo_detector(self, detection_family: str, model_size: str):
        detection_model = DETECTION_MODELS[detection_family][model_size]
        detection_model_path = PATH_TO_DETECTION_MODELS / detection_model

        detector = YOLO(detection_model_path)
        detector.model.to(self.device)
        log_info(f"Detection Model from YOLO: {detection_model}")
        return detector

    def predict(
        self, image: np.ndarray, inference_config: ObjectDetectionInferenceConfig = None
    ):
        results = self.detector(image)
        return results

    def unpack_yolo_results(self, results):
        boxes = results[0].boxes.xywh.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        print(f"Boxes: {boxes}. Type: {type(boxes)}")
        print(f"Classes: {clss}. Type: {type(clss)}")
        print(f"Names of Classes: {names}. Type: {type(names)}")

    def destroy(self) -> None:  # TODO: properly free up gpu
        del self.detector
