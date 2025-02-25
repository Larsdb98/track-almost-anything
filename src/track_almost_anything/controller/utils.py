from PySide6.QtGui import QImage
import numpy as np


def image2pixmap(image: np.ndarray) -> QImage:
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_image = QImage(
        image.data, width, height, bytes_per_line, QImage.Format_RGB888
    ).rgbSwapped()
    return q_image
