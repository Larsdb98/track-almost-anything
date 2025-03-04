from track_almost_anything._logging import log_info, log_debug, log_error

from PySide6.QtCore import QObject
from typing import Tuple
import numpy as np
import cv2


class RoiModel(QObject):
    def __init__(self):
        self.roi_x = None
        self.roi_y = None

        self.roi_image_preview = None

    def create_roi_preview(
        self,
        roi_x: Tuple[int, int],
        roi_y: Tuple[int, int],
        roi_preview_width: int,
        roi_preview_height: int,
        image: np.ndarray,
    ) -> np.ndarray:
        self.roi_x = roi_x
        self.roi_y = roi_y
        self.roi_image = image

        overlay = image.copy()
        img_height, img_width = image.shape[:2]

        live_aspect = roi_preview_width / roi_preview_height
        img_aspect = img_width / img_height

        if img_aspect > live_aspect:
            new_width = roi_preview_width
            new_height = int(roi_preview_width / img_aspect)
        else:
            new_height = roi_preview_height
            new_width = int(roi_preview_height * img_aspect)

        cv2.rectangle(
            overlay,
            (self.roi_x[0], self.roi_y[0]),
            (self.roi_x[1], self.roi_y[1]),
            color=(43, 156, 255),
            thickness=-1,
        )
        alpha = 0.4
        sub_image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

        new_image = cv2.resize(
            sub_image, (new_width, new_height), interpolation=cv2.INTER_AREA
        )

        roi_view_image = 15 * np.ones(
            (roi_preview_height, roi_preview_width, 3), dtype=np.uint8
        )

        x_offset = (roi_preview_width - new_width) // 2
        y_offset = (roi_preview_height - new_height) // 2

        roi_view_image[
            y_offset : y_offset + new_height, x_offset : x_offset + new_width
        ] = new_image

        return roi_view_image
