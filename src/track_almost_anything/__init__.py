from track_almost_anything._logging import log_info, log_error

import os
import json
from pathlib import Path

ROOT_PATH = Path(os.path.abspath(__file__)).parents[2]
PATH_TO_DETECTION_MODELS = ROOT_PATH / "resources/detection_models/"

try:
    config_file_path = ROOT_PATH / "src/track_almost_anything/config.json"
    with open(config_file_path) as f:
        APP_CONFIG = json.load(f)

except Exception as e:
    log_error(
        f"An Exception occured while opening the Tracker's configuration file ! {e}"
    )
    log_info("Using default settings...")
    APP_CONFIG = {}
