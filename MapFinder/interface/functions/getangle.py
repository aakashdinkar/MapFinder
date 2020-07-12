import numpy as np

def get_angle(p1, p2):
    
    
    longitude_diff = np.radians(p2.lon - p1.lon)
    
    latitude1 = np.radians(p1.lat)
    latitude2 = np.radians(p2.lat)
    
    x_vector = np.sin(longitude_diff) * np.cos(latitude2)
    y_vector = (np.cos(latitude1) * np.sin(latitude2) 
        - (np.sin(latitude1) * np.cos(latitude2) 
        * np.cos(longitude_diff)))
    angle = np.degrees(np.arctan2(x_vector, y_vector))
    
    # Checking and adjustring angle value on the scale of 360
    if angle < 0:
        return angle + 360
    return angle