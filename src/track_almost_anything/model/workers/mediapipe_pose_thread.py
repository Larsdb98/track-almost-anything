from track_almost_anything.api.processing.detection import (
    MPPoseDetection,
)
from track_almost_anything._logging import log_info, log_debug
from .abstract_detection_thread import (
    AbstractDetectionThread,
)

import cv2
import time
import queue


class MediaPipePoseThread(AbstractDetectionThread):
    def __init__(self, image_queue: queue.Queue):
        super().__init__(image_queue=image_queue)

    def run(self):
        log_info("Model :: Workers :: MediaPipePoseThread: Detection started...")
        detector = MPPoseDetection()

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
            results = detector.predict(image_rgb=image)

            debug_image = detector.debug_draw_poses(
                image_rgb=image, mp_detection_results_raw=results
            )
            debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)
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
