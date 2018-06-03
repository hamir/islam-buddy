"""Fetches prayer times from 'www.salah.com'."""

import json
import requests

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
_PRAYER_TIMES_RESPONSE_DEPTH = 3


def GetCalcMethod(lat, lng):
  """Returns the Calculation method based on given region

  MWL: Europe and Far East
  ISNA: North America
  Egypt: Africa, Syria, Lebanon
  Umm Al Qura: Arabian Peninsula
  U. of Islamic Sciences: Pakistan, Afganistan, India, Bangladesh

  Args:
    lat: a double representing the latitude
    lng: a double representing the longitude

  Returns: calculation method"""
  
  if lng >= -180 and lng < -30:
    return 'ISN'
  elif lng >= -30 and lng < 35 and lat >= -35 and lat <= 35:
    return 'EGO'
  elif lng >= 35 and lng < 60 and lat >= 10 and lat <= 30:
    return 'UAQ'
  elif lng >= 60 and lng < 95 and lat >= 5 and lat <= 40:
    return 'KAR'
  else:
    return 'MWL'


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
  post_data = {
      'lt': lat,
      'lg': lng,
      'm' : GetCalcMethod(lat, lng),
  }
  #print 'post_data = ', post_data
  for request_try in range(2):
    try:
      request = requests.post(_SALAH_API_URL, data=post_data, timeout=15)
      if request.status_code == requests.codes.ok:
        break
      elif request_try == 2:
        return (None, None)
    except BaseException:
      if request_try == 2:
        return (None, None)
      continue

  try:
    #print 'here = ', request.text
    response = json.loads(request.text).get("Prayers")
    #print 'response from salah.com API', response
    # dig into the response until we find the prayer times
    for _ in range(_PRAYER_TIMES_RESPONSE_DEPTH):
      response = response.itervalues().next()
    return (response, 0)
  except BaseException:
    return (None, None)

