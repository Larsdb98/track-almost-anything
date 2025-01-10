from ..view.view import View
from .detection_model import DetectionModel

from track_almost_anything._logging import log_info, log_debug, log_error


class Model:
    def __init__(self):
        self.detection_model = DetectionModel()

    def destroy(self):
        self.detection_model.destroy()
