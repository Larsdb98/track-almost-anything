from track_almost_anything.cli import app_parser
from track_almost_anything._logging import configure_logger, log_info, log_error
from track_almost_anything.model import Model
from track_almost_anything.view import View
from track_almost_anything.controller import Controller

from PySide6 import QtWidgets
import sys


def main() -> int:
    args = app_parser()
    log_level = args.log_level
    log_dir = args.log_dir

    configure_logger(log_level=log_level, log_dir=log_dir)
    log_info("_______________ Track Almost Anything _______________")

    # App Singleton
    app = QtWidgets.QApplication(sys.argv)

    model = Model()
    view = View(model=model)
    controller = Controller(model=model, view=view)

    # Launch UI
    view.show()
    sys.exit(app.exec_())

    return 0


if __name__ == "__main__":
    main()
