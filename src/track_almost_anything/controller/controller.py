from ..model import Model
from ..view import View
from .detection_controller import DetectionController
from .live_view_controller import LiveViewController
from .roi_controller import RoiController
from track_almost_anything._logging import log_info, log_debug, log_error


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.live_view_controller = LiveViewController(view=view)

        self.roi_controller = RoiController(
            live_view_controller=self.live_view_controller,
            model=self.model,
            view=self.view,
        )

        self.detection_controller = DetectionController(
            live_view_controller=self.live_view_controller,
            detection_model=model.detection_model,
            view=view,
        )

        log_debug("Controller initialized successfully.")
