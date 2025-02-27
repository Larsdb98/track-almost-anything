from ..view import View
from track_almost_anything._logging import log_info, log_debug, log_error
from .utils import image2pixmap

from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtGui import QPixmap
import numpy as np
import cv2
from typing import Tuple, Dict

# TODO: Implement logic for roi control


class LiveViewController(QObject):
    def __init__(self, view: View):
        super().__init__()
        self.view = view

        self.view.installEventFilter(self)
        self.view.ui.label_video_feed.installEventFilter(self)

        self.detection_current_image = None
        self.detection_current_pixmap = None

        self.last_resize_params = None

        self.roi_point_1 = None  # TODO: By default make ROI the same size as image
        self.roi_point_2 = None

    def eventFilter(self, watched, event):
        if watched == self.view and event.type() == QEvent.Resize:
            # log_debug("Controller :: Detection Controller :: Resize event received.")
            self.update_pixmap()

        if (
            watched == self.view.ui.label_video_feed
            and event.type() == QEvent.MouseButtonPress
        ):
            if event.button() == Qt.LeftButton:
                x, y = event.position().toPoint().x(), event.position().toPoint().y()
                self.roi_point_1 = self.clamp_marker_to_image_bounds(
                    marker=(x, y), resize_params=self.last_resize_params
                )
                log_debug(
                    f"Controller :: LiveViewController: Left click event occured at {self.roi_point_1}"
                )
                self.update_pixmap()
                return True
            if event.button() == Qt.RightButton:
                x, y = event.position().toPoint().x(), event.position().toPoint().y()
                self.roi_point_2 = self.clamp_marker_to_image_bounds(
                    marker=(x, y), resize_params=self.last_resize_params
                )
                log_debug(
                    f"Controller :: LiveViewController: Left click event occured at {self.roi_point_2}"
                )
                self.update_pixmap()
                return True

        return super().eventFilter(watched, event)

    def resize_image_for_live_view(self, image: np.ndarray) -> np.ndarray:
        live_width = self.view.ui.label_video_feed.size().width()
        live_height = self.view.ui.label_video_feed.size().height()
        img_height, img_width = image.shape[:2]

        live_aspect = live_width / live_height
        img_aspect = img_width / img_height

        if img_aspect > live_aspect:
            new_width = live_width
            new_height = int(live_width / img_aspect)
        else:
            new_height = live_height
            new_width = int(live_height * img_aspect)

        resized_image = cv2.resize(
            image, (new_width, new_height), interpolation=cv2.INTER_AREA
        )
        # Dark gray frame rgb(15, 15, 15) around live view image
        live_view_image = 15 * np.ones((live_height, live_width, 3), dtype=np.uint8)

        x_offset = (live_width - new_width) // 2
        y_offset = (live_height - new_height) // 2

        live_view_image[
            y_offset : y_offset + new_height, x_offset : x_offset + new_width
        ] = resized_image

        live_view_image = self.add_markers(
            live_view_image, marker1=self.roi_point_1, marker2=self.roi_point_2
        )

        # Save last resize parameters to avoid recomputing for roi
        self.last_resize_params = {
            "new_width": new_width,
            "new_height": new_height,
            "x_offset": x_offset,
            "y_offset": y_offset,
            "orig_width": img_width,
            "orig_height": img_height,
        }

        return live_view_image

    def clamp_marker_to_image_bounds(
        self,
        marker: Tuple[int, int],
        resize_params: Dict[str, int],
    ) -> Tuple[int, int]:
        if marker is None or self.detection_current_image is None:
            return None
        if resize_params is None:
            return marker

        x, y = marker
        clamped_x = max(
            resize_params["x_offset"],
            min(x, resize_params["x_offset"] + resize_params["new_width"] - 1),
        )
        clamped_y = max(
            resize_params["y_offset"],
            min(y, resize_params["y_offset"] + resize_params["new_height"] - 1),
        )
        return (clamped_x, clamped_y)

    def add_markers(
        self,
        image: np.ndarray,
        marker1: Tuple[int, int],
        marker2: Tuple[int, int],
    ) -> np.ndarray:
        cnt = 0
        if marker1 is not None:
            image = cv2.circle(
                image, marker1, radius=3, color=(255, 0, 0), thickness=-1
            )
            cnt += 1
        if marker2 is not None:
            image = cv2.circle(
                image, marker2, radius=3, color=(0, 255, 0), thickness=-1
            )
            cnt += 1
        if cnt >= 2:
            image = cv2.rectangle(
                image, marker1, marker2, color=(0, 255, 0), thickness=1
            )

        return image

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

    def reset_roi_points(self) -> None:
        self.roi_point_1 = None
        self.roi_point_2 = None
