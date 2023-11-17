import json
import urllib.request
import urllib.parse
import math
import func


def run():
    center = func.center_split(input())
    radius = func.nums_split(input())
    threshold = func.nums_split(input())
    num_of_places = func.nums_split(input())
    aqi_type = func.aqi_split(input())
    reverse = func.reverse_split(input())

    center_cords = func.center_direct(center)

    data = func.aqi_direct(aqi_type)
    
    if reverse == 'REVERSE NOMINATIM':
        locations = func.Reverse_Nominatim(center_cords, radius, threshold, num_of_places, data)
        locations.display()
    else:
        locations = func.Reverse_Files(center_cords, reverse, radius, threshold, num_of_places, data)
        locations.display()



if __name__ == '__main__':
    run()
