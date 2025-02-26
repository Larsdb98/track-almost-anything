from ..model import Model
from ..view import View
from .live_view_controller import LiveViewController
from track_almost_anything._logging import TrackAlmostAnythingException, log_error

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

    def _bind(self) -> None:
        pass

    def get_roi(self) -> None:
        pass

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
