import mediapipe as mp
import numpy as np


class MPPoseDetection:
    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        enable_segmentation: bool = False,
        smooth_landmarks: bool = True,
        detection_confidence: float = 0.5,
        tracking_confidence: float = 0.5,
    ):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.enable_segmentation = enable_segmentation
        self.smooth_landmarks = smooth_landmarks
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_pose = mp.solutions.pose
        self.detector = self.mp_pose.Pose(
            static_image_mode=self.static_image_mode,
            model_complexity=self.model_complexity,
            enable_segmentation=self.enable_segmentation,
            smooth_landmarks=self.smooth_landmarks,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        # Temporary draw of pose onto image
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def predict(self, image_rgb: np.ndarray):
        results = self.detector.process(image_rgb)
        return results

    def debug_draw_poses(
        self, image_rgb: np.ndarray, mp_detection_results_raw
    ) -> np.ndarray:
        if mp_detection_results_raw.pose_landmarks:
            self.mp_draw.draw_landmarks(
                image_rgb,
                mp_detection_results_raw.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style(),
            )

        return image_rgb

    def destroy(self):
        del self.detector
