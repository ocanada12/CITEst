# app/model.py
import cv2
import numpy as np


class CameraModel:
    """카메라에서 프레임을 읽어오는 순수 모델 (OpenCV 의존)"""

    def __init__(self, device_index: int = 0):
        self.device_index = device_index
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("CameraModel: 카메라를 열 수 없습니다.")

    def read_frame(self) -> np.ndarray | None:
        if self.cap is None:
            return None
        ok, frame = self.cap.read()
        if not ok:
            return None
        return frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None


class MotorModel:
    """
    모터 이동을 담당하는 모델.
    나중에 시리얼/STM32 코드만 여기 안에 넣으면 됨.
    """

    def __init__(self):
        self.state = "stopped"

    def move_start(self):
        # TODO: 실제 모터 제어 코드로 교체
        print("[Motor] move_start() 호출")
        self.state = "moving"

    def move_stop(self):
        # TODO: 실제 모터 제어 코드로 교체
        print("[Motor] move_stop() 호출")
        self.state = "stopped"
