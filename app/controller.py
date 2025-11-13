# app/controller.py
import numpy as np
from PyQt5.QtCore import QObject, QTimer

from .model import CameraModel, MotorModel
from .view import MainWindowView


class MainController(QObject):
    """
    View와 Model 사이를 중재하는 Controller.
    - Start 버튼 클릭 → 카메라 시작 + 모터 이동 시작 + 타이머 시작
    - Stop 버튼 클릭  → 타이머 정지 + 카메라 정지 + 모터 이동 정지
    """

    def __init__(self, view: MainWindowView,
                 camera_model: CameraModel,
                 motor_model: MotorModel,
                 parent=None):
        super().__init__(parent)
        self.view = view
        self.camera_model = camera_model
        self.motor_model = motor_model

        self.timer = QTimer(self)
        self.timer.setInterval(33)  # 약 30fps
        self.timer.timeout.connect(self._on_timer)

        # View의 버튼을 Controller 메소드와 연결
        self.view.btnStart.clicked.connect(self.start)
        self.view.btnStop.clicked.connect(self.stop)

    # ---------- 이벤트 핸들러 ----------
    def start(self):
        """Start 버튼 눌렀을 때"""
        try:
            self.camera_model.start()
        except RuntimeError as e:
            # 실제에선 메시지 박스 등을 띄워도 됨
            print(e)
            return

        self.motor_model.move_start()
        self.timer.start()

    def stop(self):
        """Stop 버튼 눌렀을 때"""
        self.timer.stop()
        self.camera_model.stop()
        self.motor_model.move_stop()

    # ---------- 내부 메소드 ----------
    def _on_timer(self):
        """주기적으로 카메라 프레임 읽어서 View 업데이트"""
        frame = self.camera_model.read_frame()
        if frame is None:
            return

        # 픽셀 총합 계산 (uint64로 한 번 캐스팅해서 overflow 방지)
        pixel_sum = int(np.asarray(frame, dtype=np.uint64).sum())

        # View 업데이트
        self.view.update_frame(frame)
        self.view.update_sum(pixel_sum)
