from track_almost_anything._logging import log_info

from PySide6.QtCore import Signal, QThread
import queue


class AbstractDetectionThread(QThread):
    detection_result = Signal(dict)
    request_new_image = Signal()

    def __init__(self, image_queue: queue.Queue):
        super().__init__()
        self.image_queue = image_queue
        self.running = True
        self.paused = False

    def toggle_pause(self):
        self.paused ^= True
        log_info(
            "Detection thread paused." if self.paused else "Detection thread resumed."
        )

    def emit_new_image_request(self):
        self.request_new_image.emit()

    def get_pause_status(self) -> bool:
        return self.paused

    def set_pause_status(self, paused: bool) -> None:
        self.paused = paused

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
