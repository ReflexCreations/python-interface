from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path

class SensorViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.viewer = SensorPanel()
        self.settings = SensorSettings()

        self.layout.addWidget(self.settings)
        self.layout.addWidget(self.viewer)
        self.setLayout(self.layout)

class SensorSettings(QtWidgets.QWidget):
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
        self.style_select.addItem("Cyclic")
        self.layout.addWidget(self.style_select)

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
        self.dialog.setNameFilters(["Animation File(*.gif)","Image Files(*.png *.bmp)"])
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            f = open(file_name[0], 'r')
            with f:
                #data = f.read()
                self.file_name_label.setText(Path(file_name[0]).stem)

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
