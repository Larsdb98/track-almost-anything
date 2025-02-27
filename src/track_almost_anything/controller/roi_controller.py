from ..model import Model
from ..view import View
from .live_view_controller import LiveViewController
from track_almost_anything._logging import (
    TrackAlmostAnythingException,
    log_error,
    log_info,
    log_debug,
)

from typing import Tuple


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

    def get_roi(self) -> None:
        roi_live_view_1 = self.live_view_controller.roi_point_1
        roi_live_view_2 = self.live_view_controller.roi_point_2
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
            point_1_live_view=roi_live_view_1, point_2_live_view=roi_live_view_2
        )

        current_image = self.live_view_controller.detection_current_image
        if current_image is not None:
            pass
            # TODO: implement this: add region of interest highlight with alpha channel ideally

        log_info(f"Controller :: RoiController: ROI was added")

    def process_roi(
        self, point_1_live_view: Tuple[int, int], point_2_live_view: Tuple[int, int]
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        roi_x = None
        roi_y = None
        point_1_image_x, point_1_image_y = self.map_live_view_to_image(
            point_1_live_view
        )
        point_2_image_x, point_2_image_y = self.map_live_view_to_image(
            point_2_live_view
        )
        if point_1_image_x < point_2_image_x:
            roi_x = (point_1_image_x, point_2_image_x)
        else:
            roi_x = (point_2_image_x, point_1_image_x)

        if point_1_image_y < point_2_image_y:
            roi_y = (point_1_image_y, point_2_image_y)
        else:
            roi_y = (point_2_image_y, point_1_image_y)

        return roi_x, roi_y

    def map_live_view_to_image(
        self, pixel_coords_in_live_view: Tuple[int, int]
    ) -> Tuple[int, int]:
        if self.live_view_controller.last_resize_params is None:
            log_error(
                "Controller :: RoiController: Last resizing parameters are not available !"
            )
            raise TrackAlmostAnythingException(
                "Last resizing parameters are not available !"
            )
        x_live, y_live = pixel_coords_in_live_view
        new_width = self.live_view_controller.last_resize_params["new_width"]
        new_height = self.live_view_controller.last_resize_params["new_height"]
        x_offset = self.live_view_controller.last_resize_params["x_offset"]
        y_offset = self.live_view_controller.last_resize_params["y_offset"]
        orig_width = self.live_view_controller.last_resize_params["orig_width"]
        orig_height = self.live_view_controller.last_resize_params["orig_height"]

        if not (
            x_offset <= x_live < x_offset + new_width
            and y_offset <= y_live < y_offset + new_height
        ):
            log_error(
                "Controller :: RoiController: Invalid X or Y offsets on live view widget!"
            )
            return None
        x_img = (x_live - x_offset) * (orig_width / new_width)
        y_img = (y_live - y_offset) * (orig_height / new_height)
        return int(round(x_img)), int(round(y_img))
