from ..model import Model
from ..view import View
from .detection_controller import DetectionController
from track_almost_anything._logging import log_info, log_debug, log_error


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.detection_controller = DetectionController(
            detection_model=model.detection_model, view=view
        )

        log_debug("Controller initialized successfully.")
