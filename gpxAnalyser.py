import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic

def calculate_total_distance(gpx_file_path):
    # Parse the GPX file
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    total_distance = 0.0
    start_time = None

    # Iterate through track points and calculate distances
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(len(segment.points) - 1):
                point1 = segment.points[i]
                point2 = segment.points[i + 1]
                
                coords_1 = (point1.latitude, point1.longitude)
                coords_2 = (point2.latitude, point2.longitude)

                time1 = point1.time
                time2 = point2.time

                distance = geodesic(coords_1, coords_2).meters
                total_distance += distance
                speed = calculate_average_speed(distance, (time2-time1).total_seconds())

                print(f"distance: {distance}, speed: {speed}")

                if start_time is None:
                    start_time = point1.time
                

                end_time = point2.time

    
    # Calculate total time in seconds
    total_time = (end_time - start_time).total_seconds() if start_time and end_time else 0

    return total_distance, total_time



def calculate_average_speed(total_distance, total_time):
    # Convert total distance to kilometers and total time to hours
    total_distance_km = total_distance / 1000
    total_time_hours = total_time / 3600
    average_speed = total_distance_km / total_time_hours if total_time_hours > 0 else 0
    return average_speed


# Example usage
gpx_file_path = 'osm-upload7453061963705800278.gpx'
total_distance, total_time = calculate_total_distance(gpx_file_path)
average_speed = calculate_average_speed(total_distance, total_time)
print(f"Total distance: {total_distance} meters")
print(f"Average speed: {average_speed} km/h")


