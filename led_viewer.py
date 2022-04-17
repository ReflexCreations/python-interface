from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path

"""
This viewer is meant to emulate LED behavior on the pad, however it's currently only partially
implemented for the first release. 
"""

class LedViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        #self.viewer = LedPanel()
        self.settings = LedSettings()

        self.layout.addWidget(self.settings)
        #self.layout.addWidget(self.viewer)
        self.setLayout(self.layout)

pos_by_id = [
    [ 0, 5], [ 0, 6], [ 1, 4], [ 1, 5], [ 1, 6], [ 1, 7], [ 2, 3], [ 2, 4], [ 2, 5], [ 2, 6], [ 2, 7], [ 2, 8],
    [ 3, 2], [ 3, 3], [ 3, 4], [ 3, 5], [ 3, 6], [ 3, 7], [ 3, 8], [ 3, 9], [ 4, 1], [ 4, 2], [ 4, 3], [ 4, 4],
    [ 4, 5], [ 4, 6], [ 4, 7], [ 4, 8], [ 4, 9], [ 4,10], [ 5, 0], [ 5, 1], [ 5, 2], [ 5, 3], [ 5, 4], [ 5, 5],
    [ 5, 6], [ 5, 7], [ 5, 8], [ 5, 9], [ 5,10], [ 5,11], [ 6, 0], [ 6, 1], [ 6, 2], [ 6, 3], [ 6, 4], [ 6, 5],
    [ 6, 6], [ 6, 7], [ 6, 8], [ 6, 9], [ 6,10], [ 6,11], [ 7, 1], [ 7, 2], [ 7, 3], [ 7, 4], [ 7, 5], [ 7, 6],
    [ 7, 7], [ 7, 8], [ 7, 9], [ 7,10], [ 8, 2], [ 8, 3], [ 8, 4], [ 8, 5], [ 8, 6], [ 8, 7], [ 8, 8], [ 8, 9],
    [ 9, 3], [ 9, 4], [ 9, 5], [ 9, 6], [ 9, 7], [ 9, 8], [10, 4], [10, 5], [10, 6], [10, 7], [11, 5], [11, 6]
]

class LedSettings(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel("Light Settings")
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.style_select = QtWidgets.QComboBox()
        self.style_select.addItem("On Press")
        self.style_select.setEnabled(False)
        self.layout.addWidget(self.style_select)
        self.file_path = ""

        self.file_picker = QtWidgets.QPushButton("Open File")
        self.layout.addWidget(self.file_picker)
        self.file_picker.clicked.connect(self.get_led_file)

        self.file_label = QtWidgets.QLabel("Selected:")
        self.file_name_label = QtWidgets.QLabel()
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_name_label)

        self.setLayout(self.layout)

    def get_led_file(self):
        self.dialog = QtWidgets.QFileDialog()
        self.dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.dialog.setNameFilters(["Image Files(*.png *.bmp)"])
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            self.file_path = file_name[0]
            f = open(file_name[0], 'r')
            with f:
                self.file_name_label.setText(Path(file_name[0]).stem)

    def set_led_path(self, path):
        try:
            f = open(path, 'r')
            with f:
                self.file_path = path
                self.file_name_label.setText(Path(path).stem)
        except Exception:
            pass

class LedPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QGridLayout()
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.LED_SIZE = 12
        self.AREA = (self.LED_SIZE + 2) * 10 + 6
        for coord in pos_by_id:
            led = LedEmulator(self.LED_SIZE)
            self.layout.addWidget(led, coord[0], coord[1])
        self.setLayout(self.layout)
        self.setFixedWidth(self.AREA)
        self.setFixedHeight(self.AREA)

class LedEmulator(QtWidgets.QWidget):
    def __init__(self, led_size):
        super().__init__()
        self.LED_SIZE = led_size
    
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_led(qp)
        qp.end()

    def draw_led(self, qp):
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        pen = QtGui.QPen(1)
        pen.setColor(QtGui.QColor(QtGui.QColor(42, 42, 42)))
        qp.setBrush(brush)
        qp.setPen(pen)
        qp.drawRect(0, 0, self.LED_SIZE, self.LED_SIZE)
