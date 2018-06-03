"""Fetches prayer times from 'www.aladhan.com'."""

import json
import requests
import util
from common import CalculationMethod
from datetime import datetime
import time
from gmaps_client import GetTimezone, ReverseGeocodeCountry

_ALADHAN_API_URL = 'http://api.aladhan.com/v1/timings/'


def GetCalcMethod(lat, lng):
  """Returns the Calculation method based on given region

  MWL: Europe and Far East
  ISNA: North America
  Egypt: Africa, Syria, Lebanon, Malaysia
  Umm Al Qura: Arabian Peninsula
  U. of Islamic Sciences: Pakistan, Afganistan, India, Bangladesh
  Institute of Geophysics, University of Tehran: Iran
  Kuwait: Kuwait
  Qatar: Qatar
  Majlis Ugama Islam Singapura, Singapore: Singapore
  Union Organization islamic de France: France
  Diyanet Isleri Baskanligi, Turkey: Turkey

  Args:
    lat: a double representing the latitude
    lng: a double representing the longitude

  Returns: calculation method"""

  country = ReverseGeocodeCountry(lat, lng)
  print country
  if country:
    country_calc_method = util.CountryToCalculationMethod(country)
    if country_calc_method > 0:
      return country_calc_method

  if lng >= -180 and lng < -30:
    #ISNA
    return CalculationMethod.ISNA
  elif lng >= -30 and lng < 35 and lat >= -35 and lat <= 35:
    #EGYPT
    return CalculationMethod.EGYPT
  elif lng >= 35 and lng < 60 and lat >= 10 and lat <= 30:
    #MAKKAH
    return CalculationMethod.MAKKAH
  elif lng >= 60 and lng < 95 and lat >= 5 and lat <= 40:
    #KAR
    return CalculationMethod.KAR
  else:
    #MWL
    return CalculationMethod.MWL


def GetDailyPrayerTimes(lat, lng, date_str):
  """Gets the daily prayer times from 'aladhan.com'.

  Performs a POST request on the aladhan.com prayer times API

  Args:
    lat: a double representing the latitude
    lng: a double representing the longitude
    date_str: a string representing the requested date in YYYY-MM-DD

  Returns: a dict containing of daily prayer times and an day difference integer
  """
  # set up the parameters in the format expected by 'aladhan.com'
  post_data = { 
      'latitude': lat,
      'longitude': lng,
      'method' : GetCalcMethod(lat, lng),
  }

  print post_data['method']

  current_user_timestamp = util.GetCurrentUserTime(lat, lng)
  timestamp = current_user_timestamp
  date_time_format = "%Y-%m-%d %H:%M:%S"
  day_difference = 0
  
  if date_str and date_str != "None":
    user_time_str = current_user_timestamp.strftime("%H:%M:%S")
    user_requested_date_time_str = date_str+' '+user_time_str
    try:
      current_user_date_time = datetime.strptime(current_user_timestamp.strftime(date_time_format), date_time_format)
      user_requested_date_time = datetime.strptime(user_requested_date_time_str, date_time_format)
      day_difference = int((user_requested_date_time - current_user_date_time).days)
      if day_difference > 0:
        timestamp = user_requested_date_time
    except:
      pass
  
  try:
    timestamp_UTC = str(int(time.mktime(timestamp.timetuple())))
  except:
    timestamp_UTC = 0

  #print 'post_data = ', post_data
  for request_try in range(3):
    try:
      request = requests.get(_ALADHAN_API_URL+timestamp_UTC, params=post_data, timeout=15)
      if request.status_code == requests.codes.ok:
        break
      elif request_try == 2:
        return (None, None)
    except:
      if request_try == 2:
        return (None, None)
      continue

  #print 'here = ', request.text
  response = json.loads(request.text).get("data").get("timings")
  return (response, day_difference)

