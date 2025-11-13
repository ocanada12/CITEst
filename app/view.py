# app/view.py
import os
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class MainWindowView(QtWidgets.QMainWindow):
    """Qt Designer에서 만든 main_window.ui를 loadUi로 불러오는 View"""

    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ui",
            "main_window.ui",
        )
        loadUi(ui_path, self)

        # main_window.ui에서 만든 위젯들이라고 가정
        self.labelVideo: QtWidgets.QLabel
        self.labelSum: QtWidgets.QLabel
        self.btnStart: QtWidgets.QPushButton
        self.btnStop: QtWidgets.QPushButton

    def update_frame(self, frame: np.ndarray):
        """카메라 프레임을 labelVideo에 표시"""
        if frame is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        # 라벨 크기에 맞춰 비율 유지
        pixmap = pixmap.scaled(
            self.labelVideo.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.labelVideo.setPixmap(pixmap)

    def update_sum(self, value: int):
        """픽셀 총합을 labelSum에 표시"""
        self.labelSum.setText(str(value))
