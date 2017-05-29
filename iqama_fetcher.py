import re
import util
import requests
import json

_SCRAPER_URL = 'https://islam-buddy-staging.herokuapp.com/iqama'

def GetIqamaTime(desired_prayer, masjid):
  """Gets the iqama time from the heruko scraper service by peforming a POST.

  Args:
    desired_prayer: DailyPrayer enum representing desired salah
    masjid: a string representing the masjid of intereset

  Returns: a dict containing the prayers and iqama times
  """

  # set up the parameters in the format expected by the scraper service
  post_params = {
    'masjid': masjid,
  }
  print 'scraper get_params = ', post_params
  request = requests.post(_SCRAPER_URL, params=post_params, timeout=15)
  
  # checks if request isn't bad
  if(request.status_code == requests.codes.ok):
    response = json.loads(request.text)
    print 'response from scraper service = ', response

    # translate the dict keys to enums
    iqama_times = {}
    for key in response:
      prayer = util.StringToDailyPrayer(key)
      if prayer:
        iqama_times[prayer] = response[key]

    return iqama_times[desired_prayer]
  else:
    print 'bad response from scraper service = ', request.status_code
    return None
