from track_almost_anything.api.processing.detection import MPHandsDetection
from track_almost_anything.api.io import (
    load_image_rgb,
)

import cv2


def main():
    img_width = 1280
    img_height = 720
    capture = cv2.VideoCapture(0)
    capture.set(3, img_width)
    capture.set(4, img_height)

    detector = MPHandsDetection()

    try:
        while True:
            success, image = capture.read()
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = detector.predict(image_rgb=image)

            debug_image = detector.debug_draw_hands(
                image_rgb=image, mp_detection_results_raw=results
            )
            debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)

            cv2.imshow("Hand Detections", debug_image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        capture.release()


if __name__ == "__main__":
    main()
