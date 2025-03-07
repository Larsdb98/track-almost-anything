from .detection_model import DetectionModel
from .roi_model import RoiModel
from .source_model import SourceModel

from track_almost_anything._logging import log_info, log_debug, log_error


class Model:
    def __init__(self):
        self.roi_model = RoiModel()
        self.source_model = SourceModel()
        self.detection_model = DetectionModel(source_model=self.source_model)

        log_debug("Model initialized successfully.")

    def destroy(self):
        pass
