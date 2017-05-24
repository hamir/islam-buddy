import requests
import json


_GMAPS_API_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
_GMAPS_API_GEOCODE_KEY = 'AIzaSyBC9cKscPGfI0Ge0uPJxO29ru0qLvxfcdA'

def GetGeocode(city, state, country):
  """Gets the longitude and latitude from the Google Maps Geocode API.

  Performs a POST request on the Google Maps Geocode API
  to get the longitude and latitude from the provided city/state/country

  Args:
    city: a string representing the city
    state: a string representing the state (US only)
    country: a string representing the country

  Returns: a dict containing the longitude and latitude
  """
  
  address_params = city + " " + state + " " + country
  
  # set up the parameters in the format expected by the Google Maps Geocode API
  post_params = {
    'address': address_params,
    'key': _GMAPS_API_GEOCODE_KEY,
  }
  print 'GMAPS Geocode post_params = ', post_params
  request = requests.post(_GMAPS_API_GEOCODE_URL, params=post_params)
  print 'here = ', request.text
  response = json.loads(request.text).get("results")[0].get("geometry").get("location")
  print 'response from GMAPS Geocode API', response
  return response

