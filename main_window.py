import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from platform_interface import PlatformInterface
from graph_viewer import Viewer
from led_viewer import LedViewer
from sensor_viewer import SensorViewer
from pathlib import Path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.settings = QtCore.QSettings("RE:Flex", "Dance Pad Settings")
        self.profile = {}
        super(MainWindow, self).__init__()
        self.load_settings()
        title_string = "RE:Flex Configuration"
        self.setWindowTitle(title_string)
        self.setPalette(self.dark_palette())

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

        self.platform = PlatformInterface()
        self.enumerate()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.widget_update)

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
        self.pad_rename = QtWidgets.QPushButton("Rename")
        self.pad_rename.setFixedWidth(80)
        self.pad_rename.clicked.connect(self.rename_pad)
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.setFixedWidth(80)
        self.connect_button.clicked.connect(self.connect_clicked)
        self.disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.setFixedWidth(80)
        self.disconnect_button.setDisabled(True)
        self.disconnect_button.clicked.connect(self.disconnect_clicked)
        self.enumerate_button = QtWidgets.QPushButton("Refresh")
        self.enumerate_button.setFixedWidth(80)
        self.enumerate_button.clicked.connect(self.enumerate)

        connect_toolbar_layout = QtWidgets.QHBoxLayout()
        connect_toolbar_layout.addWidget(self.available_pads)
        connect_toolbar_layout.addWidget(self.pad_rename)
        connect_toolbar_layout.addWidget(self.connect_button)
        connect_toolbar_layout.addWidget(self.disconnect_button)
        connect_toolbar_layout.addWidget(self.enumerate_button)
        connect_toolbar_widget = QtWidgets.QWidget()
        connect_toolbar_widget.setLayout(connect_toolbar_layout)
        connect_toolbar_layout.setContentsMargins(0, 0, 0, 0)

        self.open_profile_button = QtWidgets.QPushButton("Open Profile")
        self.open_profile_button.setFixedWidth(120)
        self.open_profile_button.clicked.connect(self.get_profile)
        self.save_profile_button = QtWidgets.QPushButton("Save Profile")
        self.save_profile_button.setFixedWidth(120)
        self.save_profile_button.clicked.connect(self.set_profile)
        self.show_graph = QtWidgets.QCheckBox("Update Graphs")
        self.show_graph.setFixedWidth(95)
        fps_font = QtGui.QFont()
        fps_font.setBold(True)
        self.sensor_freq = QtWidgets.QLabel("Sensor Freq: 0000 Hz")
        self.sensor_freq.setFont(fps_font)
        self.sensor_freq.setFixedWidth(120)
        self.lights_freq = QtWidgets.QLabel("LED FPS: 00")
        self.lights_freq.setFont(fps_font)
        self.lights_freq.setFixedWidth(90)

        options_toolbar_layout = QtWidgets.QHBoxLayout()
        options_toolbar_layout.addWidget(self.open_profile_button)
        options_toolbar_layout.addWidget(self.save_profile_button)
        options_toolbar_layout.addWidget(self.show_graph)
        options_toolbar_layout.addWidget(self.sensor_freq)
        options_toolbar_layout.addWidget(self.lights_freq)
        options_toolbar_layout.addStretch()
        options_toolbar_widget = QtWidgets.QWidget()
        options_toolbar_widget.setLayout(options_toolbar_layout)
        options_toolbar_layout.setContentsMargins(2, 2, 2, 2)

        toolbar_layout = QtWidgets.QVBoxLayout()
        toolbar_layout.setContentsMargins(2, 2, 2, 2)

        toolbar_layout.addWidget(connect_toolbar_widget)
        toolbar_layout.addWidget(options_toolbar_widget)
        toolbar_widget = QtWidgets.QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        return toolbar_widget

    def rename_pad(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Rename Pad", "Serial " + self.available_pads.currentData() + ": ")
        if ok:
            self.available_pads.setItemText(self.available_pads.currentIndex(), text)

    def load_profile(self):
        self.show_graph.setChecked(self.profile['update_graphs'])
        i = 0
        for interface in self.panel_interfaces:
            interface.sensor_viewer.settings.sensitivity_selector.setValue(self.profile['sensitivities'][i])
            index = interface.sensor_viewer.settings.key_selector.findData(self.profile['keymaps'][i])
            if index is not -1:
                interface.sensor_viewer.settings.key_selector.setCurrentIndex(index)
            interface.led_viewer.settings.set_led_path(self.profile['light_paths'][i])
            i += 1
        self.available_pads.setCurrentIndex(self.available_pads.findData(self.profile['selected_profile']))

    def get_profile(self):
        self.profile_picker = QtWidgets.QFileDialog()
        self.profile_picker.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.profile_picker.setNameFilters(["RE:Flex Profile Files(*.rfx)"])
        if self.profile_picker.exec_():
            file_n = self.profile_picker.selectedFiles()
            f = open(file_n[0], 'r')
            with f:
                file_name = Path(file_n[0]).stem
                title_string = "RE:Flex Configuration - " + file_name
                self.setWindowTitle(title_string)
                self.profile = json.load(f)
        self.load_profile()
        
    def set_profile(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, filter='RE:Flex Profile Files(*.rfx)')
        if path != '':
            with open(path, 'w', encoding='utf-8') as f:
                file_name = Path(path).stem
                self.profile['name'] = file_name
                self.profile['selected_profile'] = self.available_pads.currentData()
                self.profile['update_graphs'] = self.show_graph.isChecked()
                self.profile['sensitivities'] = []
                self.profile['light_paths'] = []
                self.profile['keymaps'] = []
                for interface in self.panel_interfaces:
                    self.profile['sensitivities'].append(interface.sensor_viewer.settings.sensitivity)
                    self.profile['keymaps'].append(interface.sensor_viewer.settings.keymap)
                    self.profile['light_paths'].append(interface.led_viewer.settings.file_path)
                json.dump(self.profile, f, indent=4)
                title_string = "RE:Flex Configuration - " + str(file_name)
                self.setWindowTitle(title_string)

    def connect_clicked(self):
        led_files = []
        for interface in self.panel_interfaces:
            led_files.append(interface.led_viewer.settings.file_path)
        try:
            self.platform.assign_led_files(led_files)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select valid 12*12px PNG files for each panel.")
            return

        sensitivities = []
        keymaps = []
        for interface in self.panel_interfaces:
            sensitivities.append(interface.sensor_viewer.settings.sensitivity)
            keymaps.append(interface.sensor_viewer.settings.keymap)

        if not self.platform.launch(self.available_pads.currentData(), sensitivities, keymaps):
            QtWidgets.QMessageBox.warning(self, "Warning", "Cannot open connection to selected dance pad.")
            self.enumerate()
        elif self.platform.is_running:
            self.update_timer.start(1000)
            self.connect_button.setDisabled(True)
            self.enumerate_button.setDisabled(True)
            self.disconnect_button.setEnabled(True)
            self.pad_rename.setDisabled(True)
            self.open_profile_button.setDisabled(True)
            self.save_profile_button.setDisabled(True)
            self.show_graph.setDisabled(True)
            self.available_pads.setDisabled(True)
            for interface in self.panel_interfaces:
                interface.sensor_viewer.settings.sensitivity_selector.setDisabled(True)
                interface.sensor_viewer.settings.key_selector.setDisabled(True)
                interface.led_viewer.settings.file_picker.setDisabled(True)
            panel_index = 0
            if self.show_graph.isChecked():
                for panel_interface in self.panel_interfaces:
                    panel_interface.viewer.start_plot(self.platform, panel_index)
                    panel_index += 1

    def disconnect_clicked(self):
        self.platform.stop_loop()
        self.update_timer.stop()
        panel_index = 0
        if self.show_graph.isChecked():
            for panel_interface in self.panel_interfaces:
                panel_interface.viewer.stop_plot()
                panel_index += 1
        self.sensor_freq.setText("Sensor Freq: 0000 Hz")
        self.lights_freq.setText("LED FPS: 00")

        self.connect_button.setEnabled(True)
        self.pad_rename.setEnabled(True)
        self.enumerate_button.setEnabled(True)
        self.disconnect_button.setDisabled(True)
        self.open_profile_button.setEnabled(True)
        self.save_profile_button.setEnabled(True)
        self.show_graph.setEnabled(True)
        self.available_pads.setEnabled(True)
        for interface in self.panel_interfaces:
            interface.sensor_viewer.settings.sensitivity_selector.setEnabled(True)
            interface.sensor_viewer.settings.key_selector.setEnabled(True)
            interface.led_viewer.settings.file_picker.setEnabled(True)

    def enumerate(self):
        for i in range(self.available_pads.count()):
            self.settings.setValue(self.available_pads.itemData(i), self.available_pads.itemText(i))
        devs = self.platform.enumerate()
        self.available_pads.clear()
        for d in devs:
            if d['serial_number'] in self.settings.allKeys():
                name = self.settings.value(d['serial_number'])
            else:
                name = d['serial_number']
            self.available_pads.addItem(name, d['serial_number'])
        self.available_pads.setCurrentIndex(0)
        if len(self.available_pads) == 0:
            self.connect_button.setDisabled(True)
            self.pad_rename.setDisabled(True)
        else:
            self.connect_button.setEnabled(True)
            self.pad_rename.setEnabled(True)

    def load_settings(self):
        if not self.settings.value("geometry") is None:
            self.restoreGeometry(self.settings.value("geometry"))
        if not self.settings.value("windowState") is None:
            self.restoreState(self.settings.value("windowState"))

        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        for i in range(self.available_pads.count()):
            self.settings.setValue(self.available_pads.itemData(i), self.available_pads.itemText(i))

    def closeEvent(self, event):
        self.save_settings()

    def widget_update(self):
        self.sensor_freq.setText("Sensor Freq: " + "{:04d}".format(self.platform.sensor_rate()) + "Hz")
        self.lights_freq.setText("LED FPS: " + "{:04d}".format(self.platform.lights_rate()))


class PanelInterface():
    def __init__(self, name):
        panel_layout = QtWidgets.QHBoxLayout()
        self.viewer = Viewer()
        panel_layout.addWidget(self.viewer.graph_widget)
        self.led_panel = QtWidgets.QWidget()
        self.led_viewer = LedViewer()
        self.sensor_viewer = SensorViewer()
        panel_layout.addWidget(self.led_viewer)
        panel_layout.addWidget(self.sensor_viewer)

        self.widget = QtWidgets.QGroupBox(name)
        self.widget.setLayout(panel_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec_()
