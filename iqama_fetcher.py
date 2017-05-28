import re
import requests
import json

_SCRAPER_URL = 'https://islam-buddy-staging.herokuapp.com/iqama'

def GetIqamaTime(desired_prayer,masjid):
  """Gets the iqama time from the heruko scraper service by peforming a GET.

  Args:
    masjid: a string representing the masjid of intereset

  Returns: a dict containing the prayers and iqama times
  """

  # set up the parameters in the format expected by the scraper service
  get_params = {
    'masjid': masjid,
  }
  print 'scraper get_params = ', get_params
  request = requests.post(_SCRAPER_URL, params=get_params, timeout=15)
  
  # checks if request isn't bad
  if(request.status_code == requests.codes.ok):
    response = json.loads(request.text)
    print 'response from scraper service = ', response

    # checks if the size of the prayer and iqama time lists are equivalent
    if len(response[0]['Prayer']) != len(response[0]['IqamaTime']):
      print 'Prayer and IqamaTime lists don\'t match'
      return None

    for idx, prayer in enumerate(response[0]['Prayer']):
      if desired_prayer.lower() in GetEquivalentPrayer(prayer).lower():
        iqama_time = response[0]['IqamaTime'][idx]
        if 'fajr' in desired_prayer.lower():
          iqama_time = iqama_time + " AM"
        else:
          iqama_time = iqama_time + " PM"
        break 

    return iqama_time
  else:
    print 'bad response from scraper service = ', request.status_code
    return None

def GetEquivalentPrayer(prayer):
  """Returns the prayer equivalent to the defined prayer-name entity"""
  if(re.match(r'(^f)', prayer.lower(), flags=0)):
    return 'Fajr'
  elif(re.match(r'(^d)|(^z)', prayer.lower(), flags=0)):
    return 'Dhuhr'
  elif(re.match(r'(^a)', prayer.lower(), flags=0)):
    return 'Asr'
  elif(re.match(r'(^m)', prayer.lower(), flags=0)):
    return 'Maghrib'
  elif(re.match(r'(^i)', prayer.lower(), flags=0)):
    return 'Isha'
  else:
    return None
