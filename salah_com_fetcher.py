"""Fetches prayer times from 'www.salah.com'."""

import requests
import json


_SALAH_API_URL = 'http://www.salah.com/times/get'
'''
The 'salah.com' API provides a response in the following format:
"Prayers": { 
  "2017": { "5": { 17": {
    # actual prayer times yere
    "Fajr": "5 AM"
    ...
  }}}
}
The depth of the useful information (prayer times) is at level 4
'''
_PRAYER_TIMES_RESPONSE_DEPTH = 4


def GetDailyPrayerTimes(lat, lng):
  """Gets the daily prayer times from 'salah.com'.

  Performs a POST request on the salah.com prayer times API
  to get today's prayer times (local to timezone of provided
  location).

  Args:
    lat: a double representing the latitude
    lng: a double representing the longitude

  Returns: a dict containing of daily prayer times
  """
  # set up the parameters in the format expected by 'salah.com'
  print 'a'
  post_data = {
    'lt': lat,
    'lg': lng,
  }
  print 'b'
  request = requests.post(_SALAH_API_URL, data=post_data)
  print 'c'
  response = json.loads(request.text)
  print 'd'
  # dig into the response until we find the prayer times
  for i in range(_PRAYER_TIMES_RESPONSE_DEPTH):
    response = response.itervalues().next()
  print 'e'
  return response
