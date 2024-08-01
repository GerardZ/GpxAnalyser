import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic

from datetime import datetime
import pytz

local_timezone_str = 'Europe/Amsterdam'    # Target local timezone

def convert_gmt_to_local(gmt_datetime, local_timezone_str):

    local_timezone = pytz.timezone(local_timezone_str)
    local_datetime = gmt_datetime.astimezone(local_timezone)
    
    return local_datetime

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


def calculate_total_distance(gpx_file_path):
    # Parse the GPX file
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    total_distance = 0.0
    start_time = None
    points = ""

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
                deltaSeconds = int((time2-time1).total_seconds())
                deltaTime = f"{deltaSeconds//3600}:{deltaSeconds % 3600 // 60:02}:{deltaSeconds%60:02}"
                speed = calculate_average_speed(distance, deltaSeconds)
                local_datetime = convert_gmt_to_local(time2, local_timezone_str)

                points += f"distance: {int(distance):3}m, speed: {speed:5.1f}kmH, Dtime: {deltaTime} time:{local_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
                #print(f"distance: {int(distance):3}m, speed: {speed:3.1f}kmH, time: {deltaTime}")

                if start_time is None:
                    start_time = point1.time

                end_time = point2.time

    
    # Calculate total time in seconds
    total_time = (end_time - start_time).total_seconds() if start_time and end_time else 0

    return total_distance, total_time, points

def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return int(hours), int(minutes), int(remaining_seconds)

def calculate_average_speed(total_distance, total_time):
    # Convert total distance to kilometers and total time to hours
    total_distance_km = total_distance / 1000
    total_time_hours = total_time / 3600
    average_speed = total_distance_km / total_time_hours if total_time_hours > 0 else 0
    return average_speed

if __name__ == '__main__':
    # Example usage
    gpx_file_path = 'osm-upload7453061963705800278.gpx'
    total_distance, total_time, points = calculate_total_distance(gpx_file_path)
    average_speed = calculate_average_speed(total_distance, total_time)
    print (points)
    print(f"Total distance: {total_distance/1000:2.2} Km")
    print(f"Average speed: {average_speed:5.2} km/h")
    hours, minutes, seconds = convert_seconds(total_time)
    print(f"over: {hours} hours, {minutes} minutes and {seconds} seconds")


