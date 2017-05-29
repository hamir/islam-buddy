import requests
import json

_GMAPS_API_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

# Use for Staging GAE
_GMAPS_API_GEOCODE_KEY = 'AIzaSyBC9cKscPGfI0Ge0uPJxO29ru0qLvxfcdA'

# Use for Production GAE
#_GMAPS_API_GEOCODE_KEY = 'AIzaSyBTm8Tq2_27EHG9sylGxpcwZk2B4ynjiJU'

def GetGeocode(city, state, country):
  """Gets the longitude and latitude from the Google Maps API.

  Performs a POST request on the Google Maps API
  to get the longitude and latitude from the provided city/state/country

  Args:
    city: a string representing the city
    state: a string representing the state (US only)
    country: a string representing the country

  Returns: a dict containing the longitude and latitude
  """

  address_params = ''
  if city:
    address_params += city + " "
  if state:
    address_params += state + " "
  if country:
    address_params += country + " "

  # set up the parameters in the format expected by the Google Maps Geocode API
  post_params = {
    'address': address_params,
    'key': _GMAPS_API_GEOCODE_KEY,
  }
  print 'GMAPS Geocode post_params = ', post_params
  request = requests.post(_GMAPS_API_GEOCODE_URL, params=post_params, timeout=15)
  print 'here = ', request.text
  response = json.loads(request.text).get("results")[0].get("geometry").get("location")
  print 'response from GMAPS Geocode', response
  return response

def ReverseGeocodeCity(lat, lng):
  """Returns city from the Google Maps API based on Lat and Lng.

  Performs a POST request on the Google Maps API
  to get the city from the provided latitude and longitude

  Args:
    lat: a double representing the latitude
    lng: a double representing the longitude

  Returns: a string containing the city
  """

  address_params = ('%.16f' % lat) + ',' + ('%.16f' % lng)

  # set up the parameters in the format expected by the Google Maps Geocode API
  post_params = {
    'latlng': address_params,
    'key': _GMAPS_API_GEOCODE_KEY,
  }
  print 'GMAPS Reverse Geocode post_params = ', post_params
  request = requests.post(_GMAPS_API_GEOCODE_URL, params=post_params, timeout=15)
  print 'GMAPS Reverse Geocode response = ', request.text
  response = json.loads(request.text).get("results")[0].get("address_components")
  
  for address in response:
    if address.get("types")[0] == "locality":
      print 'response from GMAPS Reverse Geocode', address
      return address.get("long_name")
  # if no address returned, return None
  return None
