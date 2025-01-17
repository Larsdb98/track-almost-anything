# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from ..model import DetectionModel
from ..view import View
from .table_view_controller import TableViewController

from ..api.processing.detection import DETECTION_FAMILIES, YOLO_CLASS_LABEL_DICT
from track_almost_anything._logging import log_info, log_debug, log_error


class DetectionController:
    def __init__(self, detection_model: DetectionModel, view: View):
        self.detection_model = detection_model
        self.view = view
        log_debug("Controller :: Detection Controller initialized successfully.")

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

        self._bind()

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
