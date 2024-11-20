from track_almost_anything._logging import (
    TrackerFileNotFoundError,
    TrackerIncompatibleFileError,
)

from pydantic import BaseModel, field_validator
from pathlib import Path
from typing import List
import os


class ImageSequenceConfig(BaseModel):
    sequence_name: str
    img_filenames: list[str]
    img_paths: list[str]
    frame_count: int

    @field_validator("frame_count")
    def check_frame_count(cls, frame_count, values):
        img_filenames = values.get("img_filenames")
        img_paths = values.get("img_paths")

        if frame_count != len(img_filenames) or frame_count != len(img_paths):
            raise ValueError(
                f"frame count ({frame_count}) does not match the number of image filenames: "
                f"({len(img_filenames)}) or image paths: ({len(img_paths)})."
            )

        return frame_count


def get_image_sequence_config_from_dir(
    img_dir_path: Path, accepted_formats: List[str] = [".png", ".jpg"]
) -> ImageSequenceConfig:
    img_dir_path = Path(img_dir_path)

    if not img_dir_path.is_dir():
        raise TrackerFileNotFoundError(f"The directory {img_dir_path} does not exist.")

    sequence_name = img_dir_path.name
    img_files = sorted(
        [
            f.name
            for f in img_dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in accepted_formats
        ]
    )

    if not img_files:
        raise TrackerIncompatibleFileError(
            f"No compatible files found in {img_dir_path}. "
            f"Accepted formats: {', '.join(accepted_formats)}"
        )

    img_paths = [str(img_dir_path / filename) for filename in img_files]
    image_seq_config = ImageSequenceConfig(
        sequence_name=sequence_name, img_filenames=img_files, img_paths=img_paths
    )

    return image_seq_config
