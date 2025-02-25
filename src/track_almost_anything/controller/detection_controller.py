from ..model import DetectionModel
from ..view import View
from .table_view_controller import TableViewController
from .live_view_controller import LiveViewController
from .utils import image2pixmap

from ..api.processing.detection import DETECTION_FAMILIES, YOLO_CLASS_LABEL_DICT
from ..api.processing.detection import MPHandsDetection
from track_almost_anything._logging import log_info, log_debug, log_error

import queue
from PySide6.QtCore import QTimer, QObject, Signal, QThread  # , Qt, QEvent

from PySide6 import QtWidgets
import numpy as np
import cv2
import time


# For now I'm just using the basic built-in camera of my machine.
# TODO: change that
# TODO: Implement thread stop request for safer thread exit


class DetectionThread(QThread):
    detection_result = Signal(dict)

    def __init__(self, image_queue):
        super().__init__()
        self.image_queue = image_queue
        self.running = True
        self.capture = None

    def run(self):
        log_debug(
            "Controller :: DetectionController :: DetectionThread: Detection started..."
        )
        img_width = 1280
        img_height = 720
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, img_width)
        self.capture.set(4, img_height)

        detector = MPHandsDetection()
        log_debug(
            "Controller :: DetectionController :: DetectionThread: Starting loop..."
        )
        while self.running:
            # if not self.image_queue.empty():
            # image = self.image_queue.get()
            # if image is None:
            #     break

            # TODO: Replace with actual detection logic
            success, image = self.capture.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = detector.predict(image_rgb=image)

            debug_image = detector.debug_draw_hands(
                image_rgb=image, mp_detection_results_raw=results
            )
            debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)

            detection_result = {"debug_image": debug_image}

            self.detection_result.emit(detection_result)
            log_debug(
                "Controller :: DetectionController :: DetectionThread: Emitted signal."
            )
            time.sleep(0.05)  # Prevents excessive CPU usage

    def stop(self):
        self.running = False

        self.quit()
        # self.wait()
        self.capture.release()
        log_debug(
            "Controller :: DetectionController :: DetectionThread: Detection terminated."
        )


class DetectionController(QObject):
    def __init__(
        self,
        live_view_controller: LiveViewController,
        detection_model: DetectionModel,
        view: View,
    ):
        super().__init__()
        self.live_view_controller = live_view_controller
        self.detection_model = detection_model
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
        # self.view.installEventFilter(self)

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

    def start_detection_process(self):
        self.view.ui.button_start.setEnabled(False)
        self.view.ui.button_stop.setEnabled(True)
        self.detection_thread = DetectionThread(self.image_queue)
        self.detection_thread.detection_result.connect(self.handle_detection_result)
        self.detection_thread.start()

    def stop_detection_process(self):
        if self.detection_thread:
            self.detection_thread.stop()
            self.detection_thread = None
        self.view.ui.button_start.setEnabled(True)

        self.view.ui.button_start.setEnabled(True)
        self.view.ui.button_stop.setEnabled(False)

    def send_image(self, image: np.ndarray) -> None:
        self.image_queue.put(image)

    def handle_detection_result(self, result) -> None:
        log_debug("Controller :: DetectionController :: Received detection result.")
        debug_image = result["debug_image"]
        self.live_view_controller.load_image(image=debug_image)

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


# class DetectionController_legacy(QObject):
#     def __init__(
#         self,
#         live_view_controller: LiveViewController,
#         detection_model: DetectionModel,
#         view: View,
#     ):
#         super().__init__()
#         self.live_view_controller = live_view_controller
#         self.detection_model = detection_model
#         self.view = view

#         self.detection_current_pixmap = None
#         self.detection_current_image = None

#         self.image_queue = multiprocessing.Queue()
#         self.detection_queue = multiprocessing.Queue()
#         self.detection_signal = Signal(list)
#         self.process = None
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.poll_detections)

#         # All items table view
#         self.all_items_table_view_controller = TableViewController(
#             table_view=self.view.ui.table_view_all_detectables
#         )
#         self.all_items_table_view_controller.populate_table(
#             items=YOLO_CLASS_LABEL_DICT.keys()
#         )

#         # Active items table view
#         self.active_items_table_view_controller = TableViewController(
#             table_view=self.view.ui.table_view_active_detections
#         )

#         self.view.ui.label_video_feed.setSizePolicy(  # Enable shrink/grow
#             QtWidgets.QSizePolicy.Ignored,
#             QtWidgets.QSizePolicy.Ignored,
#         )
#         self.view.ui.label_video_feed.setScaledContents(True)

#         self._bind()
#         # self.view.installEventFilter(self)

#         # TODO: Set up detection loop in separate Qt Process to run in parallel from main UI thread

#         log_debug("Controller :: Detection Controller initialized successfully.")

#     def _bind(self):
#         detection_families = DETECTION_FAMILIES.keys()
#         self.view.ui.combo_detection_algo.addItems(detection_families)
#         self.view.ui.combo_detection_algo.currentTextChanged.connect(
#             self.update_detection_model_type
#         )
#         self.view.ui.combo_model_type.currentTextChanged.connect(
#             self.update_detectable_items
#         )
#         # Set initial value for display purposes upon launch
#         self.view.ui.combo_model_type.addItems(DETECTION_FAMILIES["yolo"])

#         self.view.ui.button_all.clicked.connect(
#             self.all_items_table_view_controller.select_all
#         )
#         self.view.ui.button_none.clicked.connect(
#             self.all_items_table_view_controller.deselect_all
#         )
#         self.view.ui.button_move_to_active.clicked.connect(
#             self.update_selected_detectable_items
#         )
#         self.view.ui.button_remove_active.clicked.connect(
#             self.active_items_table_view_controller.remove_selected_items
#         )

#         # Detection loop
#         self.view.ui.button_start.clicked.connect(self.start_detection_process)
#         self.view.ui.button_stop.clicked.connect(self.stop_detection_process)
#         # Signals

#         # Test
#         self.view.ui.button_save_roi.clicked.connect(
#             self.live_view_controller.test_load_image_to_cam_view
#         )

#     def start_detection_process(self):
#         self.view.ui.button_start.setEnabled(False)
#         self.process = multiprocessing.Process(
#             target=self.detection_loop, args=(self.image_queue, self.detection_queue)
#         )
#         self.process.start()
#         self.timer.start(50)  # poll every 50ms

#     def stop_detection_process(self):
#         self.timer.stop()
#         if self.process and self.process.is_alive():
#             log_debug(
#                 "Controller :: DetectionController :: Detection process is still alive..."
#             )
#             self.image_queue.put(None)  # stop signal previously defined
#             self.process.join()

#         log_debug(
#             "Controller :: DetectionController :: Detection process was killed successfully. "
#         )

#         self.view.ui.button_start.setEnabled(True)
#         self.view.ui.button_stop.setEnabled(False)

#     def send_image(self, image: np.ndarray) -> None:
#         self.image_queue.put(image)

#     def poll_detections(self):
#         detections = []
#         while not self.detection_queue.empty():
#             detections.append(self.detection_queue.get())
#         if detections:
#             self.detection_signal.emit(detections)

#     def detection_loop(
#         self, image_queue: multiprocessing.Queue, detection_queue: multiprocessing.Queue
#     ) -> None:
#         # TODO: Detection model selection & init
#         log_debug(
#             "Controller :: DetectionController:: Subprocess started in parallel..."
#         )
#         while True:
#             try:
#                 image = image_queue.get(timeout=1)
#                 if image is None:
#                     break
#                 # TODO: add detection block here

#             except multiprocessing.queues.Empty:
#                 continue

#     def update_selected_detectable_items(self):
#         selected_detectable_items = self.all_items_table_view_controller.get_selection()
#         # self.active_items_table_view_controller.remove_selected_items()
#         all_active_detectable_items = (
#             self.active_items_table_view_controller.get_all_items()
#         )
#         all_active_detectable_items.extend(selected_detectable_items)
#         log_info(
#             f"Detection :: New active detectable items: {all_active_detectable_items}"
#         )
#         # remove duplicates
#         new_active_detectable_items = list(dict.fromkeys(all_active_detectable_items))
#         self.active_items_table_view_controller.clear_table()
#         self.active_items_table_view_controller.populate_table(
#             items=new_active_detectable_items
#         )
#         self.detection_model.active_items = new_active_detectable_items

#     def update_detection_model_type(self):
#         self.view.ui.combo_model_type.clear()

#         detection_algorithm = self.view.ui.combo_detection_algo.currentText()
#         model_types = DETECTION_FAMILIES[detection_algorithm]
#         self.view.ui.combo_model_type.addItems(model_types)

#         self.update_detectable_items()

#     def update_detectable_items(self):
#         detection_algorithm = self.view.ui.combo_detection_algo.currentText()
#         if detection_algorithm == "yolo":
#             self.all_items_table_view_controller.clear_table()
#             self.active_items_table_view_controller.clear_table()
#             self.all_items_table_view_controller.populate_table(
#                 items=YOLO_CLASS_LABEL_DICT.keys()
#             )
#         elif detection_algorithm == "mediapipe":
#             self.all_items_table_view_controller.clear_table()
#             self.active_items_table_view_controller.clear_table()
