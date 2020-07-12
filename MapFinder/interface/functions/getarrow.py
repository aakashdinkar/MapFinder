from collections import namedtuple
import numpy as np
from . import getangle
import folium

def getArrows(locations, color='blue', size=6, n_arrows=3):
    
    Point = namedtuple('Point', field_names=['lat', 'lon'])
    # creating point from Point named tuple
    point1 = Point(locations[0][0], locations[0][1])
    point2 = Point(locations[1][0], locations[1][1])
    angle = getangle.get_angle(point1, point2) - 90
    

    arrow_latitude = np.linspace(point1.lat, point2.lat, n_arrows + 2)[1:n_arrows+1]
    arrow_longitude = np.linspace(point1.lon, point2.lon, n_arrows + 2)[1:n_arrows+1]
    
    final_arrows = []
    
    for points in zip(arrow_latitude, arrow_longitude):
        final_arrows.append(folium.RegularPolygonMarker(location=points, 
                      fill_color=color, number_of_sides=3, 
                      radius=size, rotation=angle))
    return final_arrows