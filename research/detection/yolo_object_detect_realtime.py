from track_almost_anything.api.processing.detection import YoloObjectDetection
from track_almost_anything.api.processing.utils import TorchBackend
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

    t_backend = TorchBackend()
    detector = YoloObjectDetection(model_type="yolov5n", device=t_backend.get())
    detector.setup_yolo_detector()

    for i, img_path in enumerate(sequence_config.img_paths):
        img = load_image_rgb(img_path)

        raw_results = detector.predict(image_rgb=img)
        detection_results = detector.yolo_results_to_cpu(raw_results)
        res_image = detector.draw_yolo_detections(img, results=detection_results)

        cv2.imshow("YOLO Object Detections", res_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
