import util
import re
import requests
import json
from masjid_util import GetIqamaID
from xml.etree import ElementTree

_IQAMAH_NET_URL = 'http://feed.iqamah.net/IQ'

def GetIqamaTime(desired_prayer, masjid):
  """Gets the iqama time from the iqamah.net service by peforming a POST.

  Args:
    desired_prayer: DailyPrayer enum representing desired salah
    masjid: a string representing the masjid of intereset

  Returns: a dict containing the prayers and iqama times
  """

  masjid_encoded = util._EncodeParameter(masjid,0)
  masjid_ID = GetIqamaID(masjid_encoded)
  
  desired_prayer = util.GetPrayerKeyName(desired_prayer)
  
  print 'Masjid ID ', masjid_ID

  if not masjid_ID:
    return None

  request = requests.get(_IQAMAH_NET_URL + str(masjid_ID) + ".xml", timeout=15)
  
  # checks if request isn't bad
  if(request.status_code == requests.codes.ok):
    tree = ElementTree.fromstring(request.content)
    
    for index in range(0,len(tree[1])):
      if(desired_prayer.lower() == (tree[1][index].tag).lower()):
        iqama_time = tree[1][index].text
        break

    if not (re.match(r'(M$)|(m$)', iqama_time, flags=0)):
      iqama_time = AddAMPM(desired_prayer, str(iqama_time)) 
    return iqama_time
  else:
    print 'bad response from iqamah service = ', request.status_code
    return None

def AddAMPM(prayer, time):
  if(re.match(r'(\d+:\d+)', time, flags=0)):
    if(re.match(r'(^f)', prayer.lower(), flags=0)):
      return time + ' AM'
    return time + ' PM'
  else:
    return time 
