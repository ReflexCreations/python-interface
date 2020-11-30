from PyQt5 import QtCore, QtGui, QtWidgets
from platform_interface import PlatformInterface
import pyqtgraph
import sys
import time
import threading


class Viewer():
    def __init__(self):
        super().__init__()
        self.update_frame = 0
        self.color_wheel = ['r', 'g', 'c', 'y']
        pyqtgraph.setConfigOption('background', QtGui.QColor(42, 42, 42))
        pyqtgraph.setConfigOption('foreground', 'w')
        self.graph_widget = pyqtgraph.PlotWidget(enableMenu=False)
        self.graph_widget.getPlotItem().hideAxis('bottom')

        self.graph_widget.setMouseEnabled(x=False, y=False)
        self.x = list(range(4))
        self.y = list(range(4))
        self.data_line = list(range(4))
        for i in range(0, 4):
            self.x[i] = list(range(250))
            self.y[i] = list(range(250))
            self.data_line[i] = pyqtgraph.PlotCurveItem(self.x[i], self.y[i], pen=pyqtgraph.mkPen(self.color_wheel[i % 4], width=2))
            self.graph_widget.addItem(self.data_line[i])
        

    def start_plot(self, platform_interface, panel):
        self.offset = panel * 4
        self.platform_interface = platform_interface
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        if self.platform_interface is not None:
            for i in range(0, 4):
                self.x[i] = self.x[i][1:]
                self.x[i].append(time.time())
                self.y[i] = self.y[i][1:]
                self.y[i].append(self.platform_interface.panel_data[i + self.offset])

            self.update_frame += 1
            if (self.update_frame % 4) == 0:
                for i in range(0, 4):
                    self.data_line[i].setData(self.x[i], self.y[i])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    viewer = Viewer()
    sys.exit(app.exec_())