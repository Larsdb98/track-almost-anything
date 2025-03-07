from ..model import Model
from ..view import View
from .live_view_controller import LiveViewController
from .utils import image2pixmap, map_live_view_to_image, map_image_to_live_view
from track_almost_anything._logging import (
    TrackAlmostAnythingException,
    log_error,
    log_info,
    log_debug,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from typing import Tuple
import numpy as np


class RoiController:
    def __init__(
        self, live_view_controller: LiveViewController, model: Model, view: View
    ):
        self.live_view_controller = live_view_controller
        self.model = model
        self.view = view

        self.roi_x = None
        self.roi_y = None

        self._bind()

        log_debug("Controller :: Roi Controller initialized successfully.")

    def _bind(self) -> None:
        self.view.ui.button_save_roi.clicked.connect(self.get_roi)
        self.view.ui.button_clear_roi.clicked.connect(self.clear_roi)

    def get_roi(self) -> None:
        roi_live_view_1 = self.live_view_controller.roi_point_1_image_frame
        roi_live_view_2 = self.live_view_controller.roi_point_2_image_frame
        if roi_live_view_1 is None or roi_live_view_2 is None:
            # TODO: add Qt error prompt
            log_error(
                "Controller :: RioController: ROI point(s) have not all been defined !"
            )
            self.view.message_boxes.warning_ok(
                title="Warning",
                message="ROI points have not all been set! Set them first by left and right clicking on the live view then try again.",
            )

        self.roi_x, self.roi_y = self.process_roi(
            point_1_image_view=roi_live_view_1, point_2_image_view=roi_live_view_2
        )

        current_image = self.live_view_controller.detection_current_image
        if current_image is not None:
            self.create_and_set_roi_preview()

        self.view.ui.button_clear_roi.setEnabled(True)
        log_info(f"Controller :: RoiController: ROI was added")

    def process_roi(
        self, point_1_image_view: Tuple[int, int], point_2_image_view: Tuple[int, int]
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        roi_x = None
        roi_y = None

        point_1_image_x, point_1_image_y = point_1_image_view
        point_2_image_x, point_2_image_y = point_2_image_view

        if point_1_image_x < point_2_image_x:
            roi_x = (point_1_image_x, point_2_image_x)
        else:
            roi_x = (point_2_image_x, point_1_image_x)

        if point_1_image_y < point_2_image_y:
            roi_y = (point_1_image_y, point_2_image_y)
        else:
            roi_y = (point_2_image_y, point_1_image_y)

        return roi_x, roi_y

    def create_and_set_roi_preview(self) -> None:
        roi_preview_image = self.model.roi_model.create_roi_preview(
            roi_x=self.roi_x,
            roi_y=self.roi_y,
            roi_preview_width=self.view.ui.label_roi_preview.size().width(),
            roi_preview_height=self.view.ui.label_roi_preview.size().height(),
            image=self.live_view_controller.get_current_image(),
        )

        roi_preview_pixmap = QPixmap.fromImage(image2pixmap(image=roi_preview_image))
        self.view.ui.label_roi_preview.setPixmap(roi_preview_pixmap)
        self.view.ui.label_roi_preview.setAlignment(Qt.AlignCenter)

    def clear_roi(self) -> None:
        # TODO: trigger update for detection to no longer use ROI
        label_roi_preview_width = self.view.ui.label_roi_preview.size().width()
        label_roi_preview_height = self.view.ui.label_roi_preview.size().height()

        self.model.roi_model.clear_roi()

        roi_preview_image = 15 * np.ones(
            (label_roi_preview_height, label_roi_preview_width, 3), dtype=np.uint8
        )
        roi_preview_pixmap = QPixmap.fromImage(image2pixmap(image=roi_preview_image))
        self.view.ui.label_roi_preview.setPixmap(roi_preview_pixmap)
        self.view.ui.label_roi_preview.setAlignment(Qt.AlignCenter)

        self.view.ui.button_clear_roi.setEnabled(False)

        log_info("Controller :: RoiController: ROI was deleted")
