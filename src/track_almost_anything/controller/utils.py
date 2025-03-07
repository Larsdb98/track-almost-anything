from track_almost_anything._logging import TrackAlmostAnythingException, log_error
from PySide6.QtGui import QImage
from typing import Tuple
import numpy as np


def image2pixmap(image: np.ndarray) -> QImage:
    height, width, _ = image.shape
    bytes_per_line = 3 * width
    q_image = QImage(
        image.data, width, height, bytes_per_line, QImage.Format_RGB888
    ).rgbSwapped()
    return q_image


def map_live_view_to_image(
    pixel_coords_in_live_view: Tuple[int, int], last_resize_params: dict
) -> Tuple[int, int]:
    if last_resize_params is None:
        log_error(
            "Controller :: RoiController: Last resizing parameters are not available !"
        )
        raise TrackAlmostAnythingException(
            "Last resizing parameters are not available !"
        )
    x_live, y_live = pixel_coords_in_live_view
    new_width = last_resize_params["new_width"]
    new_height = last_resize_params["new_height"]
    x_offset = last_resize_params["x_offset"]
    y_offset = last_resize_params["y_offset"]
    orig_width = last_resize_params["orig_width"]
    orig_height = last_resize_params["orig_height"]

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


def map_image_to_live_view(
    image_coordinates: Tuple[int, int], last_resize_params: dict
) -> Tuple[int, int]:
    if last_resize_params is None:
        log_error(
            "Controller :: RoiController: Last resizing parameters are not available !"
        )
        raise TrackAlmostAnythingException(
            "Last resizing parameters are not available !"
        )
    orig_width = last_resize_params["orig_width"]
    orig_height = last_resize_params["orig_height"]
    new_width = last_resize_params["new_width"]
    new_height = last_resize_params["new_height"]
    x_offset = last_resize_params["x_offset"]
    y_offset = last_resize_params["y_offset"]

    img_x, img_y = image_coordinates

    # Scale image coordinates to resized image dimensions
    live_x = int((img_x / orig_width) * new_width) + x_offset
    live_y = int((img_y / orig_height) * new_height) + y_offset

    return live_x, live_y
