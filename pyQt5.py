import sys
import math
from PyQt5.QtCore import QSize, Qt
#from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QTextEdit,QHBoxLayout,
                             QPushButton, QVBoxLayout, QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont
import gpxAnalyser

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

class DistanceCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Coordinate File", "", "GPX Files (*.gpx);;All Files (*)", options=options)
        if file_name:
            #self.load_coordinates_from_file(file_name)
            self.gpxFile_input.setText(file_name)
            total_distance, total_time, points = gpxAnalyser.calculate_total_distance(file_name)
            self.text_edit.setText(points)
            self.distance_result.setText(str(total_distance))

    def initUI(self):
        self.setWindowTitle('Distance Calculator')
        self.setFixedSize(QSize(1000, 300))

        layout = QVBoxLayout()

        self.gpxFile_label = QLabel('Filename:')
        self.gpxFile_input = QLineEdit()
        layout.addWidget(self.gpxFile_label)
        layout.addWidget(self.gpxFile_input)

        self.file_button = QPushButton('Load from File')
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        # Create a QTextEdit widget
        self.text_edit = QTextEdit(self)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)  # Disable line wrap
        # Set the preferred height to 10 lines
        font_metrics = self.text_edit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.text_edit.setFixedHeight(line_height * 10)
        # Set a monospaced font for the QTextEdit
        font = QFont("Courier New", 10)
        self.text_edit.setFont(font)


        layout.addWidget(self.text_edit)

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate_distance)
        layout.addWidget(self.calculate_button)

        h_layout1 = QHBoxLayout()
        self.distance_label = QLabel('Distance: ')
        h_layout1.addWidget(self.distance_label)
        self.distance_result = QLabel('0')
        h_layout1.addWidget(self.distance_result)
        layout.addLayout(h_layout1)

        self.setLayout(layout)

    def calculate_distance(self):
        try:
            lon1 = float(self.lon1_input.text())
            lat1 = float(self.lat1_input.text())
            lon2 = float(self.lon2_input.text())
            lat2 = float(self.lat2_input.text())
            distance = haversine(lon1, lat1, lon2, lat2)
            self.result_label.setText(f"Distance: {distance:.2f} km")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers for all coordinates.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = DistanceCalculator()
    calculator.show()
    sys.exit(app.exec_())