from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ComputationScreen:
    def __init__(self, steps):
        label_computation_info = QtWidgets.QLabel(
            "Computation in progress... Please wait.\n" + str(steps) + " steps total.")
        label_computation_info.setAlignment(Qt.AlignCenter)
        label_computation_info.setFont(QFont("MS Shell Dlg 2", 9))
        label_computation_info.setMaximumHeight(50)

        self.pbar = QtWidgets.QProgressBar()
        self.pbar.setMaximum(steps)
        self.pbar.setMaximumWidth(500)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label_computation_info)
        layout.addWidget(self.pbar)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(70)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(layout)
        # container.setAutoFillBackground(True)
        # container.setStyleSheet("background-color: blue;")

    def get_screen(self):
        return self.container

    def update_progress_bar(self, new_value):
        self.pbar.setValue(int(new_value))


class LoadingScreen:
    def __init__(self):
        self.label_loading_info = QtWidgets.QLabel("Loading results... Please wait.")
        self.label_loading_info.setAlignment(Qt.AlignCenter)

    def get_screen(self):
        return self.label_loading_info
