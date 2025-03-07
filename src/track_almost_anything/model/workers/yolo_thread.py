from track_almost_anything.api.processing.detection import YoloObjectDetection

from track_almost_anything._logging import log_info, log_debug
from .abstract_detection_thread import (
    AbstractDetectionThread,
)

import cv2
import time
import queue


class YoloThread(AbstractDetectionThread):
    def __init__(self, image_queue: queue.Queue, model_type: str):
        super().__init__(image_queue=image_queue)
        self.model_type = model_type

    def run(self):
        log_info("Model :: Workers :: MediaPipePoseThread: Detection started...")
        detector = YoloObjectDetection()
        detector.setup_yolo_detector()

        self.request_new_image.emit()  # Request first image
        log_info("Model :: Workers :: MediaPipePoseThread: Starting loop...")

        while self.running:
            try:
                image = self.image_queue.get(timeout=1)  # timeout=1
            except queue.Empty:
                continue

            if image is None:
                log_info(
                    "Model :: Workers :: MediaPipeHandsThread: Sequence Finished Pausing detections..."
                )
                self.paused = True
                continue

            # TODO: modify logic for returning results (image + results or simply results)
            # Need to check what is feasible with Model :: SourceModel
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            raw_results = detector.predict(image_rgb=image)
            detection_results = detector.yolo_results_to_cpu(raw_results)
            debug_image = detector.draw_yolo_detections(
                image, results=detection_results
            )
            detection_result = {"debug_image": debug_image}

            self.detection_result.emit(detection_result)
            self.emit_new_image_request()

            while self.paused:
                time.sleep(0.1)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        log_info("Model :: Workers :: MediaPipePoseThread: Killing detection worker.")
