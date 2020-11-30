import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from platform_interface import PlatformInterface
from graph_viewer import Viewer
from led_viewer import LedViewer
from sensor_viewer import SensorViewer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RE:Flex Configuration")
        self.setPalette(self.dark_palette())
        icon = QtGui.QIcon()
        icon.addFile('assets/icon-16x16.png', QtCore.QSize(16, 16))
        icon.addFile('assets/icon-48x48.png', QtCore.QSize(48, 48))
        self.setWindowIcon(icon)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        scroll_area = QtWidgets.QScrollArea()
        layout = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        toolbar = self.toolbar()
        self.panel_interfaces = []
        left_panel = PanelInterface("Left")
        self.panel_interfaces.append(left_panel)
        down_panel = PanelInterface("Down")
        self.panel_interfaces.append(down_panel)
        up_panel = PanelInterface("Up")
        self.panel_interfaces.append(up_panel)
        right_panel = PanelInterface("Right")
        self.panel_interfaces.append(right_panel)
        layout.addWidget(toolbar)
        layout.addWidget(left_panel.widget)
        layout.addWidget(down_panel.widget)
        layout.addWidget(up_panel.widget)
        layout.addWidget(right_panel.widget)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.setCentralWidget(scroll_area)
        
    def dark_palette(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, QtGui.QColor(49, 49, 49))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(42, 42, 42))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(90, 90, 90))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtGui.QColor(49, 49, 49))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(90, 90, 90))
        return palette

    def toolbar(self):
        self.available_pads = QtWidgets.QComboBox()
        self.available_pads.setPlaceholderText("Pad Enumeration Unimplemented.")
        self.available_pads.setDisabled(True)
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.setFixedWidth(80)
        self.connect_button.clicked.connect(self.connect_clicked)
        self.disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.setFixedWidth(80)
        self.disconnect_button.setDisabled(True)
        self.disconnect_button.clicked.connect(self.disconnect_clicked)
        self.enumerate_button = QtWidgets.QPushButton("Refresh")
        self.enumerate_button.setFixedWidth(80)
        self.enumerate_button.clicked.connect(self.enumerate_clicked)

        toolbar_layout = QtWidgets.QHBoxLayout()
        toolbar_layout.addWidget(self.available_pads)
        toolbar_layout.addWidget(self.connect_button)
        toolbar_layout.addWidget(self.disconnect_button)
        toolbar_layout.addWidget(self.enumerate_button)
        toolbar_widget = QtWidgets.QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setFixedHeight(40)
        return toolbar_widget

    def connect_clicked(self):
        self.platform = PlatformInterface()
        if self.platform.is_running:
            self.connect_button.setDisabled(True)
            self.enumerate_button.setDisabled(True)
            self.disconnect_button.setEnabled(True)
            panel_index = 0
            for panel_interface in self.panel_interfaces:
                panel_interface.viewer.start_plot(self.platform, panel_index)
                panel_index += 1

    def disconnect_clicked(self):
        self.platform.disconnect()

        self.connect_button.setEnabled(True)
        self.enumerate_button.setEnabled(True)
        self.disconnect_button.setDisabled(True)

    def enumerate_clicked(self):
        pass

class PanelInterface():
    def __init__(self, name):
        panel_layout = QtWidgets.QHBoxLayout()
        self.viewer = Viewer()
        panel_layout.addWidget(self.viewer.graph_widget)
        self.led_panel = QtWidgets.QWidget()
        led_viewer = LedViewer()
        panel_layout.addWidget(led_viewer)

        self.widget = QtWidgets.QGroupBox(name)
        self.widget.setLayout(panel_layout)
        #self.widget.setMinimumHeight(led_viewer.viewer.AREA + 40)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec_()