from track_almost_anything import PATH_TO_DETECTION_MODELS
from track_almost_anything.api.processing.utils import (
    TorchBackend,
    YOLO_DETECTION_MODELS_DICT,
)
from track_almost_anything._logging import log_info, log_debug

import numpy as np
from ultralytics import YOLO
from pydantic import BaseModel, Field, ConfigDict
from typing import Tuple, List, Dict
import torch
import cv2


class ObjectDetectionInferenceConfig(BaseModel):
    image_dimensions: Tuple[int, int]
    boxes: List[Tuple[float, float, float, float]]  # xyxy
    classes: List[int]
    names: Dict[int, str]


class ObjectDetectionResults(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    boxes: torch.Tensor
    classes: List[int]
    names: Dict[int, str]


class ObjectDetectionConfig(BaseModel):
    model: str
    model_size: str = Field(type=str, default="n")
    confidence: float = Field(type=float, default=0.8)


class YoloObjectDetection:
    def __init__(self, model_type: str = "yolov5n", device=None, yolo_verbose=False):
        self.model_type = model_type
        self.yolo_verbose = yolo_verbose
        if device is None:
            log_debug(
                f"API :: YOLO Detection: No device was given. Detecting devices..."
            )
            backend = TorchBackend()
            self.device = backend.get()
        else:
            self.device = device
        log_debug(f"API :: YOLO Detection: Using detection backend: {self.device}")

        self.detector = None

    def set_model_type(self, model_type: str) -> None:
        self.model_type = model_type

    def setup_yolo_detector(self) -> None:
        detection_model = YOLO_DETECTION_MODELS_DICT[self.model_type]
        detection_model_path = PATH_TO_DETECTION_MODELS / detection_model

        self.detector = YOLO(detection_model_path)
        self.detector.model.to(self.device)
        log_info(f"API :: YOLO: Using detection model {detection_model}")

    def predict(
        self,
        image_rgb: np.ndarray,
        inference_config: ObjectDetectionInferenceConfig = None,
    ):
        results = self.detector(image_rgb, verbose=self.yolo_verbose)
        return results

    def unpack_yolo_results(self, results):
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        clss_int = [int(clss_item) for clss_item in clss]
        names = results[0].names
        print(f"Boxes: {boxes}. Type: {type(boxes)}")
        print(f"Classes: {clss_int}. Type: {type(clss)}")
        print(f"Names of Classes: {names}. Type: {type(names)}")

    def yolo_results_to_cpu(self, results) -> ObjectDetectionResults:
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        clss_int = [int(clss_item) for clss_item in clss]
        names = results[0].names

        object_detection_results = ObjectDetectionResults(
            boxes=boxes, classes=clss_int, names=names
        )
        return object_detection_results

    def draw_yolo_detections(
        self, image_rgb: np.ndarray, results: ObjectDetectionResults
    ):
        for box, cls in zip(results.boxes, results.classes):
            # Extract box coordinates in xyxy format
            x1, y1, x2, y2 = map(int, box)

            class_name = results.names.get(cls, "Unknown")

            color = (0, 255, 0)

            cv2.rectangle(image_rgb, (x1, y1), (x2, y2), color, 2)

            label = f"{class_name}"

            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = x1
            text_y = y1 - 10 if y1 - 10 > 10 else y1 + 10

            # Draw the text background rectangle for better visibility
            cv2.rectangle(
                image_rgb,
                (text_x, text_y - text_size[1]),
                (text_x + text_size[0], text_y),
                color,
                -1,
            )

            cv2.putText(
                image_rgb,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
        image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
        return image_rgb

    def destroy(self) -> None:  # TODO: properly free up gpu
        del self.detector
