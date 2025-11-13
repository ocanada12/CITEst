# app/main.py
import os
import sys

from PyQt5.QtWidgets import QApplication

from .model import CameraModel, MotorModel
from .view import MainWindowView
from .controller import MainController


def main():
    # CI 환경에서도 돌아가게 하기 위해 옵션 설정 (로컬에선 무시됨)
    os.environ.setdefault("QT_QPA_PLATFORM", "windows" if os.name == "nt" else "xcb")

    app = QApplication.instance() or QApplication(sys.argv)

    view = MainWindowView()
    camera_model = CameraModel(device_index=0)
    motor_model = MotorModel()

    controller = MainController(view, camera_model, motor_model)

    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
