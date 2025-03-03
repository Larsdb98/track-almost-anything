from track_almost_anything._logging import log_info, log_debug, log_error

from PySide6.QtCore import Signal, QThread
import time


class AbstractDetectionThread(QThread):
    detection_result = Signal(dict)

    def __init__(self, image_queue):
        super().__init__()
        self.image_queue = image_queue
        self.running = True
        self.paused = False

    def run(self):
        while self.running:

            # Pausing loop
            while self.paused:
                time.sleep(0.1)

    def toggle_pause(self):
        self.paused ^= True
        if self.paused:
            log_info("Model :: DetectionModel :: Worker: Image stream has been paused.")
        else:
            log_info("Model :: DetectionModel :: Worker: Image stream has resumed.")

    def get_pause_status(self) -> bool:
        return self.paused

    def set_pause_status(self, paused: bool) -> None:
        self.paused = paused

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
