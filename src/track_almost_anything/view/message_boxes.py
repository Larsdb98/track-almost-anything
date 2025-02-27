from PySide6.QtWidgets import QMessageBox, QWidget


class MessageBoxView(QWidget):
    def __init__(self):
        super().__init__()

    def warning_ok_cancel(self, title: str, message: str) -> str:
        ret = QMessageBox.warning(
            self, title, message, QMessageBox.Ok | QMessageBox.Cancel
        )
        if ret == QMessageBox.Ok:
            return "Ok"
        else:
            return "Cancel"

    def warning_ok(self, title: str, message: str) -> None:
        ret = QMessageBox.warning(self, title, message, QMessageBox.Ok)
