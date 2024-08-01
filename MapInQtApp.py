import sys
import math
import gpxpy
import folium
from PyQt5.QtCore import QSize, Qt,  QUrl
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QTextEdit,QHBoxLayout,
                             QPushButton, QVBoxLayout, QMessageBox, QFileDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont, QImage, QPainter
import gpxAnalyser
import sys

def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        coordinates = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coordinates.append((point.latitude, point.longitude))
    return coordinates

def CreateMapFromFile(gpxFileName):
    return create_map(parse_gpx(gpxFileName))

# Function to create a Folium map with the GPX track
def create_map(coordinates):
    if coordinates:
        start_coords = coordinates[0]

        #folium_map = folium.Map(location=start_coords, zoom_start=14, tiles='OpenStreetMap')
        folium_map = folium.Map(location=gpxAnalyser.getCenterCoordinate(coordinates), zoom_start=14, tiles='OpenStreetMap')

        # add track to map...
        folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(folium_map)
        return folium_map
    else:
        return None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def save_to_png(self):
        # Define the size of the image
        size = self.web_view.size()
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.white)  # Optional: Fill with white background

        # Create a QPainter to render the web content to the image
        painter = QPainter(image)

        # Render the web content to the image
        #self.web_view.render(painter)

        # End painting
        painter.end()

        # Save the image as PNG
        image.save("c:\\temp\\map.png", "PNG")
        print("Saved webpage to webpage.png")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Coordinate File", "", "GPX Files (*.gpx);;All Files (*)", options=options)
        if file_name:
            #self.load_coordinates_from_file(file_name)
            self.gpxFile_input.setText(file_name)
            total_distance, total_time, points = gpxAnalyser.calculate_total_distance(file_name)
            self.text_edit.setText(points)
            self.distance_result.setText(str(total_distance))
            map = CreateMapFromFile(file_name)
            if map:
                map.save("c:\\temp\\map.html")
                self.web_view.setUrl(QUrl.fromLocalFile("c:\\temp\\map.html"))


    def initUI(self):
        self.setWindowTitle('Distance Calculator')
        self.setFixedSize(QSize(1200, 1000))

        layout = QVBoxLayout()

        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(1100, 700)

        # add map...
        #self.web_view.setUrl(QUrl.fromLocalFile("C:\\Users\\gradtje\\source\\repos\\GpxAnalyser-1\\map.html"))
        layout.addWidget(self.web_view)


        self.gpxFile_label = QLabel('Filename:')
        self.gpxFile_input = QLineEdit()
        layout.addWidget(self.gpxFile_label)
        layout.addWidget(self.gpxFile_input)

        self.file_button = QPushButton('Load from File')
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        self.saveMap_button = QPushButton('save map to file')
        self.saveMap_button.clicked.connect(self.save_to_png)
        layout.addWidget(self.saveMap_button)


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

        self.setWindowTitle("GPX Track on Real Map")
        self.resize(1200, 800)
        self.show()

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
    mainWindow = MainWindow()
    #mainWindow.show()
    sys.exit(app.exec_())