from track_almost_anything._logging import (
    log_info,
    log_debug,
    log_error,
    log_warm,
    TrackAlmostAnythingException,
)
from track_almost_anything.api.io import (
    get_image_sequence_config_from_dir,
    load_image_rgb,
    load_image_bgr,
    ImageSequenceConfig,
)

from PySide6.QtCore import QObject, Signal
import cv2
import queue
from pathlib import Path
from typing import Dict


# All handling of camera inputs and video source to feed into detections shall reside here.
class SourceModel(QObject):
    new_image_requested = Signal()

    def __init__(self):
        super().__init__()
        self.image_queue = queue.Queue()

        self.image_sequence_mode = False
        self.live_camera_mode = False

        self.image_current_frame_id = 0
        self.image_sequence_count = None
        self.image_sequence_config = None
        self.video_config = None

        self.capture = None

    def is_image_sequence_set(self) -> bool:
        if self.image_sequence_count is not None:
            return True
        return False

    def is_video_config_set(self) -> bool:
        if self.video_config is not None:
            return True
        return False

    def setup_opencv_video(self) -> None:
        self.capture = cv2.VideoCapture(self.video_config)

    def setup_opencv_camera(
        self, source: int, img_width: int = 1280, img_height: int = 720
    ) -> None:
        self.capture = cv2.VideoCapture(source)
        self.capture.set(3, img_width)
        self.capture.set(4, img_height)

        self.image_sequence_mode = False
        self.live_camera_mode = True

    def setup_image_sequence(self, image_sequence_config: ImageSequenceConfig) -> None:
        self.image_sequence_mode = True
        self.live_camera_mode = False
        self.image_sequence_config = image_sequence_config
        self.image_sequence_count = self.image_sequence_config.frame_count
        self.image_current_frame_id = 0

    def release_source(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None

        self.image_sequence_mode = False
        self.live_camera_mode = False

        self.image_current_frame_id = 0
        self.image_sequence_count = None
        self.image_sequence_config = None
        self.video_config = None

    def request_new_image(self) -> None:
        if self.image_sequence_mode:
            if (
                self.image_current_frame_id
                <= self.image_sequence_config.frame_count - 1
            ):
                image = load_image_bgr(
                    image_path=self.image_sequence_config.img_paths[
                        self.image_current_frame_id
                    ]
                )
            else:
                image = None

            self.image_queue.queue.clear()
            self.image_queue.put(image)
            self.new_image_requested.emit()
            self.image_current_frame_id += 1

        else:
            try:
                success, image = self.capture.read()
                if success:
                    self.image_queue.queue.clear()
                    self.image_queue.put(image)
                    self.new_image_requested.emit()
            except Exception as e:
                log_warm(
                    "Model :: SourceModel :: Request new image: An error occured. Likely due to STOP button being pressed. This can be ignored."
                )

    def get_file_or_directory(self, selected_path: Path) -> None:
        log_debug(f"Model :: SourceModel: Selected path: {selected_path}")

        if selected_path.is_dir():
            try:
                image_sequence_config = get_image_sequence_config_from_dir(
                    img_dir_path=selected_path,
                    accepted_formats=[".png", ".jpg", ".jpeg"],
                )
                self.setup_image_sequence(image_sequence_config=image_sequence_config)
                self.image_sequence_mode = True
            except Exception as e:
                log_error(
                    f"Model :: SourceModel: An error occured loading images from directory: {e}"
                )

        if selected_path.suffix.lower() in {".mp4", ".mov"}:
            self.image_sequence_mode = False
            self.video_config = selected_path
            self.setup_opencv_video()

    def get_available_cameras_opencv(self, max_cameras: int = 10) -> Dict[str, int]:
        log_debug(f"Using OpenCV version: {cv2.__version__}")
        available = {}

        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)  # , cv2.CAP_DSHOW) may be necessary for Windows

            if not cap.read()[0]:
                log_debug(f"Model :: SourceModel: Camera index {i:02d} not found...")
                continue

            available[f"Camera {len(available) + 1}"] = i
            cap.release()

        log_debug(f"Model :: SourceModel: Cameras found: {available}")

        if len(available):
            return available
        else:
            return None
