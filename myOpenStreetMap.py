import gpxpy
import folium
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

# Function to parse GPX file and return coordinates
def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        coordinates = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coordinates.append((point.latitude, point.longitude))
    return coordinates


def getCenterCoordinate(coordinates):
    
    latMin = 90
    latMax = 0
    longMin = 360
    longMax = 0
    
    for (lat, long) in coordinates:
        long = (long + 360) % 360
        if latMin > lat: latMin = lat
        if latMax < lat: latMax = lat
        if longMin > long: longMin = long
        if longMax < long: longMax = long

    latCenter = latMin + (latMax - latMin)/2
    longCenter = longMin + (longMax - longMin)/2

    if longCenter > 180: longCenter -= 360

    return (latCenter, longCenter)



# Function to create a Folium map with the GPX track
def create_map(coordinates):
    if coordinates:
        start_coords = coordinates[0]

        #folium_map = folium.Map(location=start_coords, zoom_start=14, tiles='OpenStreetMap')
        folium_map = folium.Map(location=getCenterCoordinate(coordinates), zoom_start=14, tiles='OpenStreetMap')

        # add track to map...
        folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(folium_map)
        return folium_map
    else:
        return None

# Main function to integrate everything
def main(gpx_file):
    coordinates = parse_gpx(gpx_file)
    folium_map = create_map(coordinates)

    if folium_map:
        # Save the map to an HTML file
        folium_map.save("map.html")

        # Create the PyQt5 application
        app = QApplication(sys.argv)
        window = QWidget()
        layout = QVBoxLayout()
        web_view = QWebEngineView()

        # Load the map.html file
        web_view.setUrl(QUrl.fromLocalFile("C:\\Users\\gradtje\\source\\repos\\GpxAnalyser-1\\map.html"))
        layout.addWidget(web_view)
        window.setLayout(layout)
        window.setWindowTitle("GPX Track on Real Map")
        window.resize(1200, 800)
        window.show()

        sys.exit(app.exec_())

if __name__ == "__main__":
    gpx_file = "C:\\Users\\gradtje\\source\\repos\\GpxAnalyser\\osm-upload7453061963705800278.gpx"  # Replace with the path to your GPX file
    #gpx_file = "C:\\Users\\gradtje\\source\\repos\\GpxAnalyser-1\\osm-upload3749191287725211725.gpx"
    main(gpx_file)
