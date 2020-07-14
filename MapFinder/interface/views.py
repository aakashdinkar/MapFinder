from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import folium
from folium.features import *
from collections import namedtuple
import numpy as np
import math
from . import getarrow, distance


latitude = 28.6304
longitude = 77.2177
traffic_map = folium.Map(location=[latitude, longitude], zoom_start=15)
def index(request):
    content = {'map':traffic_map._repr_html_()}
    return render(request,'index.html', content)

def submit(request):
    source = request.POST.get('src')
    destination = request.POST.get('dest')

    baseurl = "http://py4e-data.dr-chuck.net/json"

    i = 0
    loc, place = [], []
    places = []
    places.append(source)
    places.append(destination)
    for item in places:
        address = item
        if len(address) < 1: break

        params = dict()
        params['address'] = address
        params['key'] = 42
        req = requests.get(baseurl, params = params)
        
        data = req.text
        try:
            js = json.loads(data)
        except :
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print("failed to load data!!!")
            continue

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        location = js['results'][0]['formatted_address']
        print("Location: ",location)
        loc.append([lat,lng])
        place.append(location)
        print("lat {}, lng {}".format(lat,lng))


    dist_map = folium.Map(location=loc[0], zoom_start=15)
    folium.Marker(location=loc[0], icon=folium.Icon(color='green') , popup = place[0]).add_to(dist_map)
    folium.Marker(location=loc[1], icon=folium.Icon(color='blue'), popup = place[1]).add_to(dist_map)
    

    folium.PolyLine(locations=[loc[0], loc[1]], color='red').add_to(dist_map)
    arrows = getarrow.getArrows(locations=[loc[0], loc[1]], n_arrows=5)

    for arrow in arrows:
        arrow.add_to(dist_map)

    dist_map.save(r'C:\Users\Aakash\Desktop\MapFinder\MapFinder\templates\map.html')

    dis = distance.find_distance((loc[0][0], loc[0][1]), (loc[1][0], loc[1][1]))
    print("Aerial Distance between %s and %s is %d Km"%(place[0], place[1] ,dis))
    return render(request, 'map.html')