import cv2
import mediapipe as mp
import numpy as np


class MPHandsDetection:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_hands: int = 2,
        detection_confidence: float = 0.5,
        tracking_confidence: float = 0.5,
    ):
        self.static_image_mode = static_image_mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.detector = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )

        # Temporary draw of hands onto image
        self.mp_draw = mp.solutions.drawing_utils

    def predict(self, image_rgb: np.ndarray):
        results = self.detector.process(image_rgb)
        return results

    def debug_draw_hands(
        self, image_rgb: np.ndarray, mp_detection_results_raw
    ) -> np.ndarray:
        if mp_detection_results_raw.multi_hand_landmarks:
            for handLms in mp_detection_results_raw.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    image_rgb, handLms, self.mp_hands.HAND_CONNECTIONS
                )
        return image_rgb
