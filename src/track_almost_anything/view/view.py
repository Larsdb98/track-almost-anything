from .ui_main_window import Ui_MainWindow
from .aspect_ratio_label_widget import AspectRatioLabel
from track_almost_anything._logging import log_debug, log_error
from track_almost_anything.model import Model

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class View(QtWidgets.QMainWindow):
    def __init__(self, model: Model, parent=None):
        super(View, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Replace live video feed with custom widget
        # that maintains aspect ratio

        # self.ui.label_video_feed = AspectRatioLabel(self.ui.widget_view_video_feed)
        # self.ui.label_video_feed.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        # self.ui.label_video_feed.setStyleSheet("background-color: rgb(15, 15, 15);")

        log_debug("View initialized successfully.")
