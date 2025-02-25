from ..view import View
from track_almost_anything._logging import log_info, log_debug, log_error
from .utils import image2pixmap

from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtGui import QPixmap
import numpy as np
import cv2


class LiveViewController(QObject):
    def __init__(self, view: View):
        super().__init__()
        self.view = view

        self.view.installEventFilter(self)

        self.detection_current_image = None
        self.detection_current_pixmap = None

    def eventFilter(self, watched, event):
        if watched == self.view and event.type() == QEvent.Resize:
            # log_debug("Controller :: Detection Controller :: Resize event received.")
            self.update_pixmap()
        return super().eventFilter(watched, event)

    def resize_image_for_live_view(self, image: np.ndarray) -> np.ndarray:
        live_width = self.view.ui.label_video_feed.size().width()
        live_height = self.view.ui.label_video_feed.size().height()
        img_height, img_width = image.shape[:2]

        live_aspect = live_width / live_height
        img_aspect = img_width / img_height

        if img_aspect > live_aspect:
            # Fit to width
            new_width = live_width
            new_height = int(live_width / img_aspect)
        else:
            # Fit to height
            new_height = live_height
            new_width = int(live_height * img_aspect)

        resized_image = cv2.resize(
            image, (new_width, new_height), interpolation=cv2.INTER_AREA
        )
        live_view_image = np.zeros((live_height, live_width, 3), dtype=np.uint8)

        x_offset = (live_width - new_width) // 2
        y_offset = (live_height - new_height) // 2

        live_view_image[
            y_offset : y_offset + new_height, x_offset : x_offset + new_width
        ] = resized_image

        return live_view_image

    def update_pixmap(self):
        if self.detection_current_image is not None:
            label_size = self.view.ui.label_video_feed.size()

            image_for_live_view = self.resize_image_for_live_view(
                image=self.detection_current_image
            )
            pixmap_for_live_view = QPixmap.fromImage(image2pixmap(image_for_live_view))
            self.view.ui.label_video_feed.setPixmap(pixmap_for_live_view)
            self.view.ui.label_video_feed.setAlignment(Qt.AlignCenter)

    def load_image(self, image: np.ndarray) -> None:
        self.detection_current_image = image
        self.detection_current_pixmap = QPixmap.fromImage(
            image2pixmap(self.detection_current_image)
        )
        self.update_pixmap()
