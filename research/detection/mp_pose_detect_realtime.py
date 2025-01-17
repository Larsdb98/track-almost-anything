from track_almost_anything.api.processing.detection import MPPoseDetection
from track_almost_anything.api.io import (
    get_image_sequence_config_from_dir,
    load_image_rgb,
)

import cv2
from pathlib import Path


def main():
    sequence_dir = Path(
        "/Users/larsdelbubba/Desktop/Coding Projects/track-almost-anything_resources/Video/MOT17/test/MOT17-08-DPM/img1/"
    )
    sequence_config = get_image_sequence_config_from_dir(img_dir_path=sequence_dir)

    detector = MPPoseDetection()

    for i, img_path in enumerate(sequence_config.img_paths):
        image = load_image_rgb(img_path)

        results = detector.predict(image_rgb=image)
        debug_image = detector.debug_draw_poses(
            image_rgb=image, mp_detection_results_raw=results
        )
        debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)

        cv2.imshow("Pose Detections", debug_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
