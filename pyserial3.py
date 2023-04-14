import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import QTimer

# Create a custom MainWindow class
class RealTimePlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Plotter")
        self.setGeometry(100, 100, 800, 400)
        self.layout = QVBoxLayout()
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.layout.addWidget(self.chart_view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.axisX().setTitleText("Time")
        self.x_axis = QValueAxis()
        self.x_axis.setRange(0, 100)
        self.chart.setAxisX(self.x_axis, self.series)
        self.chart.axisY().setTitleText("Y Label")
        self.chart.axisY().setRange(1, 1024)
        self.ser = serial.Serial('COM4', 9600)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10)  

    def update_plot(self):
        try:
            data = self.ser.readline().decode().rstrip() 
            y = float(data) 
            print(data) 
            x = self.series.count() 
            self.series.append(x, y)
            self.x_axis.setRange(x - 100, x)

        except Exception as e:
            print("Error updating plot:", e)

    def closeEvent(self, event):
        self.ser.close()
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimePlotter()
    window.show()
    sys.exit(app.exec_())