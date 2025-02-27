# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from ..model import DetectionModel
from ..view import View
from .table_view_controller import TableViewController

from ..api.processing.detection import DETECTION_FAMILIES, YOLO_CLASS_LABEL_DICT
from track_almost_anything._logging import log_info, log_debug, log_error

import multiprocessing
from PySide6.QtCore import QTimer, QObject, Signal, Qt, QEvent
from PySide6.QtGui import QPixmap
from PySide6 import QtWidgets
import numpy as np
import cv2


class DetectionController(QObject):
    def __init__(self, detection_model: DetectionModel, view: View):
        super().__init__()
        self.detection_model = detection_model
        self.view = view

        self.detection_current_pixmap = None
        self.detection_current_image = None
        self.live_view_size = None

        # All items table view
        self.all_items_table_view_controller = TableViewController(
            table_view=self.view.ui.table_view_all_detectables
        )
        self.all_items_table_view_controller.populate_table(
            items=YOLO_CLASS_LABEL_DICT.keys()
        )

        # Active items table view
        self.active_items_table_view_controller = TableViewController(
            table_view=self.view.ui.table_view_active_detections
        )

        self.view.ui.label_video_feed.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored,  # Width can shrink/grow
            QtWidgets.QSizePolicy.Ignored,  # Height can shrink/grow
        )
        self.view.ui.label_video_feed.setScaledContents(True)

        self._bind()
        self.view.installEventFilter(self)

        # TODO: Set up detection loop in separate Qt Process to run in parallel from main UI thread

        log_debug("Controller :: Detection Controller initialized successfully.")

    def _bind(self):
        detection_families = DETECTION_FAMILIES.keys()
        self.view.ui.combo_detection_algo.addItems(detection_families)
        self.view.ui.combo_detection_algo.currentTextChanged.connect(
            self.update_detection_model_type
        )
        self.view.ui.combo_model_type.currentTextChanged.connect(
            self.update_detectable_items
        )
        # Set initial value for display purposes upon launch
        self.view.ui.combo_model_type.addItems(DETECTION_FAMILIES["yolo"])

        self.view.ui.button_all.clicked.connect(
            self.all_items_table_view_controller.select_all
        )
        self.view.ui.button_none.clicked.connect(
            self.all_items_table_view_controller.deselect_all
        )
        self.view.ui.button_move_to_active.clicked.connect(
            self.update_selected_detectable_items
        )
        self.view.ui.button_remove_active.clicked.connect(
            self.active_items_table_view_controller.remove_selected_items
        )

        # Test
        self.view.ui.button_save_roi.clicked.connect(self.test_load_image_to_cam_view)

    def eventFilter(self, watched, event):
        if watched == self.view and event.type() == QEvent.Resize:
            log_debug("Controller :: Detection Controller :: Resize event received.")
            self.update_pixmap()
        return super().eventFilter(watched, event)

    def update_live_view_pixmap(self, image: np.ndarray) -> None:
        if self.detection_current_image:
            live_view_image = self.image_to_live_view_pixmap(
                image=self.detection_current_image
            )

    def image_to_live_view_pixmap(self, image: np.ndarray) -> np.ndarray:
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
        # Update video feed QLabel weith a resized pixmap
        if self.detection_current_pixmap:
            label_size = self.view.ui.label_video_feed.size()
            log_debug(
                f"Controller :: Detection Controller :: Live view size: {label_size.height()} & {label_size.width()}"
            )
            scaled_pixmap = self.detection_current_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            self.view.ui.label_video_feed.setPixmap(scaled_pixmap)
            self.view.ui.label_video_feed.setAlignment(Qt.AlignCenter)

    def update_selected_detectable_items(self):
        selected_detectable_items = self.all_items_table_view_controller.get_selection()
        # self.active_items_table_view_controller.remove_selected_items()
        all_active_detectable_items = (
            self.active_items_table_view_controller.get_all_items()
        )
        all_active_detectable_items.extend(selected_detectable_items)
        log_info(
            f"Detection :: New active detectable items: {all_active_detectable_items}"
        )
        # remove duplicates
        new_active_detectable_items = list(dict.fromkeys(all_active_detectable_items))
        self.active_items_table_view_controller.clear_table()
        self.active_items_table_view_controller.populate_table(
            items=new_active_detectable_items
        )
        self.detection_model.active_items = new_active_detectable_items

    def update_detection_model_type(self):
        self.view.ui.combo_model_type.clear()

        detection_algorithm = self.view.ui.combo_detection_algo.currentText()
        model_types = DETECTION_FAMILIES[detection_algorithm]
        self.view.ui.combo_model_type.addItems(model_types)

        self.update_detectable_items()

    def update_detectable_items(self):
        detection_algorithm = self.view.ui.combo_detection_algo.currentText()
        if detection_algorithm == "yolo":
            self.all_items_table_view_controller.clear_table()
            self.active_items_table_view_controller.clear_table()
            self.all_items_table_view_controller.populate_table(
                items=YOLO_CLASS_LABEL_DICT.keys()
            )
        elif detection_algorithm == "mediapipe":
            self.all_items_table_view_controller.clear_table()
            self.active_items_table_view_controller.clear_table()

    def test_load_image_to_cam_view(self):
        image_loc = r"/Users/larsdelbubba/Desktop/Coding Projects/track-almost-anything/tests_and_extras_taa/taa_ai_gui_1.png"
        self.detection_current_pixmap = QPixmap(image_loc)
        self.view.ui.label_video_feed.setPixmap(
            self.detection_current_pixmap.scaled(
                self.view.ui.label_video_feed.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )
        self.update_pixmap()
