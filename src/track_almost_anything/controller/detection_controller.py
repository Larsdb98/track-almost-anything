from ..model import Model
from ..view import View
from .table_view_controller import TableViewController
from .live_view_controller import LiveViewController
from .source_controller import SourceController

from ..api.processing.detection import DETECTION_FAMILIES, YOLO_CLASS_LABEL_DICT
from track_almost_anything._logging import log_info, log_debug, log_error, log_warm

import queue
from PySide6.QtCore import QObject

from PySide6 import QtWidgets

# For now I'm just using the basic built-in camera of my machine.


class DetectionController(QObject):
    def __init__(
        self,
        live_view_controller: LiveViewController,
        source_controller: SourceController,
        model: Model,
        view: View,
    ):
        super().__init__()
        self.live_view_controller = live_view_controller
        self.source_controller = source_controller
        self.model = model
        self.view = view

        self.detection_thread = None
        self.image_queue = queue.Queue()

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

        self.view.ui.label_video_feed.setSizePolicy(  # Enable shrink/grow
            QtWidgets.QSizePolicy.Ignored,
            QtWidgets.QSizePolicy.Ignored,
        )
        self.view.ui.label_video_feed.setScaledContents(True)

        self._bind()

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

        # Detection loop
        self.view.ui.button_start.clicked.connect(self.start_detection_process)
        self.view.ui.button_stop.setEnabled(False)  # TODO: refactor this in UI file
        self.view.ui.button_stop.clicked.connect(self.stop_detection_process)

    def set_detection_model(self) -> None:
        detection_model = self.view.ui.combo_detection_algo.currentText()
        model_type = self.view.ui.combo_model_type.currentText()
        self.model.detection_model.set_detection_model(
            detection_model=detection_model, model_type=model_type
        )

    def start_detection_process(self):
        self.view.ui.button_start.setEnabled(False)
        self.view.ui.button_stop.setEnabled(True)
        self.set_detection_model()
        self.model.detection_model.setup_detection_process()
        self.model.detection_model.detection_thread.detection_result.connect(
            self.handle_detection_result
        )
        # Connect source to detection pipeline
        source = self.view.ui.comboBox_image_source.currentText()
        if source == "From File...":
            if self.model.source_model.is_image_sequence_set():
                log_info("Controller :: DetectionController: Image sequence is ready.")
            elif self.model.source_model.is_video_config_set():
                log_info("Controller :: DetectionController: Video file is ready.")

            else:
                log_warm("No image sequence or video has been selected yet")
                self.source_controller.load_from_file_or_dir()
        else:
            available_cameras = self.source_controller.get_available_cameras_opencv()

            # TODO: We should be able to choose the resolution.
            self.model.source_model.setup_opencv_camera(
                source=available_cameras[source], img_width=1280, img_height=720
            )
            log_info(f"Controller :: DetectionController: Using {source}.")

        self.model.detection_model.detection_thread.request_new_image.connect(
            self.model.source_model.request_new_image
        )
        self.view.ui.button_pause.clicked.connect(
            self.model.detection_model.detection_thread.toggle_pause
        )
        self.model.detection_model.start_detection_process()

    def stop_detection_process(self):
        # Unpause before stopping detection thread
        if self.model.detection_model.detection_thread.get_pause_status():
            self.model.detection_model.detection_thread.set_pause_status(paused=False)

        success = self.model.detection_model.stop_detection_process()
        self.model.source_model.release_source()
        if success:
            self.view.ui.button_start.setEnabled(True)
            self.view.ui.button_stop.setEnabled(False)
        else:
            log_error(
                "Controller :: DetectionController: Unable to stop current detection process."
            )

    # TODO: needs to be modified once detection outputs have been "uniformized"
    def handle_detection_result(self, result) -> None:
        # log_debug("Controller :: DetectionController :: Received detection result.")
        debug_image = result["debug_image"]
        self.live_view_controller.load_image(image=debug_image)

    def update_selected_detectable_items(self):
        selected_detectable_items = self.all_items_table_view_controller.get_selection()
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
        self.model.detection_model.active_items = new_active_detectable_items

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
