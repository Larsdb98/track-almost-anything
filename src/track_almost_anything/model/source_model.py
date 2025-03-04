from track_almost_anything._logging import (
    log_info,
    log_debug,
    log_error,
    TrackAlmostAnythingException,
)

from PySide6.QtCore import QObject


# All handling of camera inputs and video source to feed into detections shall reside here
class SourceModel(QObject):
    def __init__(self):
        super().__init__()
        pass
