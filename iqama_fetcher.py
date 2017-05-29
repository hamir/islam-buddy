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

    iqama_time = response[desired_prayer]
    
    return iqama_time
  else:
    print 'bad response from scraper service = ', request.status_code
    return None
