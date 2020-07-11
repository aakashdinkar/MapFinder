import requests
import json
import folium


api_key = False
if api_key is False:
	api_key = 42
	baseurl = "http://py4e-data.dr-chuck.net/json"
else:
	baseurl = "https://maps.googleapis.com/maps/api/geocode/json"

while True:
	address = input("Enter address: ")
	if len(address) < 1: break

	params = dict()
	params['address'] = address
	if api_key is not False:
		params['key'] = api_key
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
	print("lat {}, lng {}".format(lat,lng))
	m = folium.Map(
		location=[lat, lng],
		zoom_start = 12
	)
	tooltip = 'Click me!'

	folium.Marker([lat, lng], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)
	m.save("index.html")
	break
