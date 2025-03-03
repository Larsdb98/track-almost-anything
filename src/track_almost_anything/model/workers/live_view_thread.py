from track_almost_anything.api.processing.detection import MPHandsDetection
from track_almost_anything._logging import log_info, log_debug

from PySide6.QtCore import Signal, QThread
import cv2
import time


class DetectionThread(QThread):
    detection_result = Signal(dict)

    def __init__(self):
        super().__init__()
        # self.image_queue = image_queue
        self.running = True
        self.capture = None

    def run(self):
        log_info("Model :: Workers :: DetectionThread: Detection started...")
        img_width = 1280
        img_height = 720
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, img_width)
        self.capture.set(4, img_height)

        detector = MPHandsDetection()
        log_info("Model :: Workers :: DetectionThread: Starting loop...")
        while self.running:
            # TODO: Replace with actual detection logic
            success, image = self.capture.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = detector.predict(image_rgb=image)

            debug_image = detector.debug_draw_hands(
                image_rgb=image, mp_detection_results_raw=results
            )
            debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)

            detection_result = {"debug_image": debug_image}

            self.detection_result.emit(detection_result)
            log_debug("Model :: Workers :: DetectionThread: Emitted signal.")
            time.sleep(0.05)  # Prevents excessive CPU usage

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.capture.release()
        log_info("Model :: Workers :: DetectionThread: Killing detection worker.")
