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

        # Handling of table views are a bit different for the time being
        self.all_items_table_view_controller = TableViewController(
            table_view=self.view.ui.table_view_all_detectables
        )
        self.all_items_table_view_controller.populate_table(
            items=YOLO_CLASS_LABEL_DICT.keys()
        )

        self._bind()

    def _bind(self):
        detection_families = DETECTION_FAMILIES.keys()
        self.view.ui.combo_detection_algo.addItems(detection_families)
        self.view.ui.combo_detection_algo.currentTextChanged.connect(
            self.update_detection_model_type
        )
        # Set initial value for display purposes upon launch
        self.view.ui.combo_model_type.addItems(DETECTION_FAMILIES["yolo"])

        self.view.ui.button_all.clicked.connect(
            self.all_items_table_view_controller.select_all
        )
        self.view.ui.button_none.clicked.connect(
            self.all_items_table_view_controller.deselect_all
        )

    def update_detection_model_type(self):
        self.view.ui.combo_model_type.clear()

        detection_algorithm = self.view.ui.combo_detection_algo.currentText()
        model_types = DETECTION_FAMILIES[detection_algorithm]
        self.view.ui.combo_model_type.addItems(model_types)

        self.view.ui.table_view_all_detectables
