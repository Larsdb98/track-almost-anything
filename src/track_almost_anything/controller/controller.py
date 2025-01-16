from ..model import Model
from ..view import View
from track_almost_anything._logging import log_info, log_debug, log_error


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        log_debug("Controller class called successfully.")
