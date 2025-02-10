# Thanks stack overflow
# https://stackoverflow.com/questions/452333/how-to-maintain-widgets-aspect-ratio-in-qt

from PySide6.QtWidgets import QWidget, QSizePolicy, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class AspectRatioWidget(QWidget):
    """
    A widget that maintains its aspect ratio.
    """

    def __init__(self, *args, ratio=4 / 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.ratio = ratio
        self.adjusted_to_size = (-1, -1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))

    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjusted_to_size:
            # Avoid infinite recursion. I suspect Qt does this for you,
            # but it's best to be safe.
            return
        self.adjusted_to_size = size

        full_width = size.width()
        full_height = size.height()
        width = min(full_width, full_height * self.ratio)
        height = min(full_height, full_width / self.ratio)

        h_margin = round((full_width - width) / 2)
        v_margin = round((full_height - height) / 2)

        self.setContentsMargins(h_margin, v_margin, h_margin, v_margin)


class AspectRatioLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_aspect_ratio = None  # To store the aspect ratio of the first image

    def setPixmap(self, pixmap: QPixmap):
        """Override setPixmap to store the aspect ratio of the first image."""
        super().setPixmap(pixmap)

        # Store the aspect ratio of the first image loaded
        if self.pixmap_aspect_ratio is None:
            self.pixmap_aspect_ratio = pixmap.width() / pixmap.height()

    def heightForWidth(self, width: int) -> int:
        """Override heightForWidth to preserve aspect ratio based on the first image."""
        if self.pixmap_aspect_ratio is not None:
            return int(
                width / self.pixmap_aspect_ratio
            )  # Calculate height based on width and aspect ratio
        return super().heightForWidth(
            width
        )  # Default behavior if aspect ratio is not set
