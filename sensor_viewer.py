from PyQt5 import QtWidgets, QtGui, QtCore


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
        self.keymap = 30
        self.scan_code_dict = {
            "A": 30,
            "B": 48,
            "C": 46,
            "D": 32,
            "E": 18,
            "F": 33,
            "G": 34,
            "H": 35,
            "I": 23,
            "J": 36,
            "K": 37,
            "L": 38,
            "M": 50,
            "N": 49,
            "O": 24,
            "P": 25,
            "Q": 16,
            "R": 19,
            "S": 31,
            "T": 20,
            "U": 22,
            "V": 47,
            "W": 17,
            "X": 45,
            "Y": 21,
            "Z": 44
        }

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

        key_label = QtWidgets.QLabel("Key mapped:")
        self.key_selector = QtWidgets.QComboBox()
        for key, value in self.scan_code_dict.items():
            self.key_selector.addItem(key, value)
        self.key_selector.currentIndexChanged.connect(self.update_keymap)

        self.layout.addWidget(sensitivity_label)
        self.layout.addWidget(self.sensitivity_selector)
        self.layout.addWidget(key_label)
        self.layout.addWidget(self.key_selector)

        self.setLayout(self.layout)

    def update_sensitivity(self):
        self.sensitivity = self.sensitivity_selector.value()

    def update_keymap(self):
        self.keymap = self.key_selector.currentData()
