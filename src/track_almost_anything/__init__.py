from track_almost_anything._logging import (
    log_info,
    log_error,
    TrackerFileNotFoundError,
    TrackerAlmostAnythingException,
)


import os
import json
from pathlib import Path
from typing import Dict

ROOT_PATH = Path(os.path.abspath(__file__)).parents[2]
PATH_TO_DETECTION_MODELS = ROOT_PATH / "resources/detection_models/"


def config_check(app_config: Dict) -> bool:
    # TODO: implement this function
    return True


def load_default_config() -> Dict:
    app_config = {}
    return app_config


try:
    config_file_path = ROOT_PATH / "src/track_almost_anything/config.json"
    try:
        with open(config_file_path) as f:
            APP_CONFIG = json.load(f)
    except FileNotFoundError:
        raise TrackerFileNotFoundError(
            f"Settings file {config_file_path} doesn't exist !"
        )

    status = config_check(app_config=APP_CONFIG)
    if not status:
        raise TrackerAlmostAnythingException("Invalid settings file !")
    log_info(f"Loaded settings file from {config_file_path} successfully.")


except Exception as e:
    log_error(
        f"An Exception occured while opening the Tracker's configuration file ! {e}"
    )
    log_info("Using default settings...")
    APP_CONFIG = load_default_config()
