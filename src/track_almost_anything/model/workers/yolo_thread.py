from track_almost_anything.api.processing.detection import YoloObjectDetection

from track_almost_anything._logging import log_info, log_debug
from .abstract_detection_thread import AbstractDetectionThread

import cv2
import time


class YoloThread(AbstractDetectionThread):
    def __init__(self, image_queue, model_type: str):
        super().__init__(image_queue=image_queue)
        self.model_type = model_type

    def run(self):
        log_info("Model :: Workers :: MediaPipePoseThread: Detection started...")
        img_width = 1280
        img_height = 720
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, img_width)
        self.capture.set(4, img_height)

        detector = YoloObjectDetection()
        detector.setup_yolo_detector()
        log_info("Model :: Workers :: MediaPipePoseThread: Starting loop...")
        while self.running:
            # TODO: Replace with actual detection logic
            success, image = self.capture.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            raw_results = detector.predict(image_rgb=image)
            detection_results = detector.yolo_results_to_cpu(raw_results)
            debug_image = detector.draw_yolo_detections(
                image, results=detection_results
            )
            detection_result = {"debug_image": debug_image}

            self.detection_result.emit(detection_result)

            while self.paused:
                time.sleep(0.1)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.capture.release()
        log_info("Model :: Workers :: MediaPipePoseThread: Killing detection worker.")
