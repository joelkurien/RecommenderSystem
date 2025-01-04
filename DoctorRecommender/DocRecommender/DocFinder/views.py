from django.shortcuts import render
from django.http import JsonResponse
from geopy.geocoders import Nominatim
import requests
from .constants import *
# Create your views here.

def getCurrentLocation(request):
    publicIPAddress = getPublicIPAddress(request)
    if publicIPAddress!=IP_FAILURE:
        try:
            response = requests.get(f"http://ip-api.com/json/{publicIPAddress}?fields={LOCATION_INFO_CODE}")
            if response.status_code == 200:
                location_data = response.json()
                lat = location_data["lat"]
                lon = location_data["lon"]
                geolocator = Nominatim(user_agent="DocFinder")
                location = geolocator.reverse((lat, lon), exactly_one=True)
                if location:
                    address = location.raw['address']
                    city = address.get('city', '')
                    suburb = address.get('suburb', '')
                    print(address)
                    return JsonResponse({
                        "city": city,
                        "suburb": suburb,
                        "full_address": location.address
                    }, status=200)
        except Exception as e:
            return f"Error: {e}"
            

def getPublicIPAddress(request):
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json().get('ip')
        else:
            return IP_FAILURE
    except Exception as e:
        return f"Error: {e}"