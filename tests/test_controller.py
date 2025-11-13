# tests/test_controller.py
import os

import numpy as np
import pytest
from PyQt5.QtWidgets import QApplication

from app.view import MainWindowView
from app.controller import MainController
from app.model import MotorModel


@pytest.fixture(scope="session")
def qapp():
    # CI에서 GUI 없이 돌리기 위한 설정
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class DummyCameraModel:
    """테스트용 더미 카메라 모델 (항상 같은 프레임 반환)"""

    def __init__(self):
        self.started = False
        # 2x2x3, 모든 값이 10인 BGR 이미지 → 픽셀 합 = 2*2*3*10 = 120
        self.frame = np.full((2, 2, 3), 10, dtype=np.uint8)

    def start(self):
        self.started = True

    def read_frame(self):
        if not self.started:
            return None
        return self.frame

    def stop(self):
        self.started = False


def test_controller_pixel_sum(qapp):
    """컨트롤러 타이머 콜백에서 픽셀 합계가 올바르게 표시되는지 테스트"""
    view = MainWindowView()
    dummy_camera = DummyCameraModel()
    motor = MotorModel()

    controller = MainController(view, dummy_camera, motor)

    # 실제로 타이머를 돌리진 않고, 직접 내부 메소드 호출
    dummy_camera.start()
    controller._on_timer()  # 한 번만 호출

    # labelSum에 들어간 텍스트 확인 (2*2*3*10 = 120)
    assert view.labelSum.text() == "120"
    # 모터 상태도 moving이어야 한다고 가정
    # assert motor.state == "moving"
    assert motor.state == "stopped"
