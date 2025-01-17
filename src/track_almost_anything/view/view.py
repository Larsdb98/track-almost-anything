from .ui_main_window import Ui_MainWindow
from track_almost_anything._logging import log_debug, log_error
from track_almost_anything.model import Model

from PySide6 import QtWidgets


class View(QtWidgets.QMainWindow):
    def __init__(self, model: Model, parent=None):
        super(View, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        log_debug("View initialized successfully.")
