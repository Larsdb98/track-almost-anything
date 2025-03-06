from track_almost_anything._logging import log_info, log_debug, log_error
from track_almost_anything.model import Model
from track_almost_anything.view import View

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Qt

from pathlib import Path


class SourceController(QObject):
    def __init__(self, model: Model, view: View):
        super().__init__()
        self.model = model
        self.view = view

        self.available_cameras_opencv = (
            self.model.source_model.get_available_cameras_opencv(max_cameras=5)
        )

        self._bind()

    def _bind(self) -> None:
        self.view.ui.button_load_video.clicked.connect(self.load_from_file_or_dir)

        self.update_camera_devices()

    def update_camera_devices(self):
        self.view.ui.comboBox_image_source.clear()
        self.view.ui.comboBox_image_source.addItems(
            list(self.available_cameras_opencv.keys())
        )
        self.view.ui.comboBox_image_source.addItem("From File...")

    def load_from_file_or_dir(self, path: str):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter(
            "Videos (*.mp4 *.mov);; Images Folder (Select a folder)"
        )

        if file_dialog.exec():  # False if "cancel" is pressed
            selected_files = file_dialog.selectedFiles()
            self.model.source_model.get_file_or_directory(
                selected_path=Path(selected_files[0])
            )
            index = self.view.ui.comboBox_image_source.findText(
                "From File...", Qt.MatchFixedString
            )
            if index >= 0:
                self.view.ui.comboBox_image_source.setCurrentIndex(index)
