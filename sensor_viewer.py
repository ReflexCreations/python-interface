from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path


class SensorViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.settings = SensorSettings()
        self.layout.addWidget(self.settings)
        self.setLayout(self.layout)

class SensorSettings(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.sensitivity = 10
        
        self.label = QtWidgets.QLabel("Sensor Settings")
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        
        sensitivity_label = QtWidgets.QLabel("Panel Sensitivity:")
        self.sensitivity_selector = QtWidgets.QSpinBox()
        self.sensitivity_selector.setRange(10, 1000)
        self.sensitivity_selector.valueChanged.connect(self.update_sensitivity)

        self.layout.addWidget(sensitivity_label)
        self.layout.addWidget(self.sensitivity_selector)

        self.setLayout(self.layout)

    def update_sensitivity(self):
        self.sensitivity = self.sensitivity_selector.value()