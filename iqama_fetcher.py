"""Fetches iqamah times from the Iqamah.net service."""

import re
from xml.etree import ElementTree
import util
import requests
from masjid_util import GetIqamaID

_IQAMAH_NET_URL = 'http://feed.iqamah.net/IQ'

def GetIqamaTime(desired_prayer, masjid):
  """Gets the iqama time from the iqamah.net service by peforming a GET.

  Args:
    desired_prayer: DailyPrayer enum representing desired salah
    masjid: a string representing the masjid of intereset

  Returns: a string containing the iqama time along with AM/PM
  """

  # making sure the masjid input is in UTF-8 format
  masjid_encoded = util.EncodeParameter(masjid, 0)
  # getting the id from the _MASJID_METADATA
  masjid_id = GetIqamaID(masjid_encoded)

  desired_prayer = util.GetPrayerKeyName(desired_prayer)

  print 'Iqamah.net Masjid ID ', masjid_id

  # if masjid_id doesn't exist then return None
  if not masjid_id:
    return None

  request = requests.get(_IQAMAH_NET_URL + str(masjid_id) + ".xml", timeout=15)

  # checks if request isn't bad
  # pylint: disable=no-member
  if request.status_code == requests.codes.ok:
    # setting a tree node to the beginning of request xml content
    tree = ElementTree.fromstring(request.content)
    # setting an element node to element 'IqDay' which contains the
    # prayer names and timings
    # <IqDay><Fajr>##:##</Fajr>.....</IqDay>
    iqamah_element = tree.findall('IqDay')[0]

    # looping through the IqDay tags (prayer names)
    for index in range(0, len(iqamah_element)):
      # convert the prayer names in the IqDay element to a known format
      iqamah_name = GetEquivalentPrayer(str(iqamah_element[index].tag))
      if desired_prayer.lower() == (iqamah_name).lower():
        iqama_time = iqamah_element[index].text
        break

    print 'Iqama Time ', iqama_time

    # if iqama time was found then add AM or PM to the time
    if iqama_time:
      return AddAMPM(desired_prayer, str(iqama_time))
    return None
  print 'bad response from iqamah service = ', request.status_code
  return None

def AddAMPM(prayer, time):
  """Returns the time variable back with AM/PM added

  Args:
    prayer: a string representing desired salah
    time: a string representing the iqamah time

  Returns: a string containing the iqamah time along with AM/PM
  """

  # if the time input is in a format where it contains ##:##
  # then proceed forward otherwise return None
  if re.match(r'(\d+:\d+)', time, flags=0):
    # strip the time variable from anything added to it
    # example: 10:00 PM becomes 10:00
    time = re.findall(r'(\d+:\d+)', time)
    # add PM by default except if the prayer is Fajr
    if re.match(r'((^f)(.+)(r$))', prayer.lower(), flags=0):
      return time[0] + ' AM'
    return time[0] + ' PM'
  return time

def GetEquivalentPrayer(prayer):
  """Returns the prayer equivalent to the defined prayer-name entity

  Args:
    prayer: a string representing desired salah

  Returns: a string containing prayer-name entity equivalent to the desired
  input prayer
  """
  eq_prayer = None

  # if prayer matches an 'f' at the beginning and an 'r' at the end
  if re.match(r'((^f)(.+)(r$))', prayer.lower(), flags=0):
    eq_prayer = 'Fajr'
  # if prayer matches an 'd' or 'z' at the beginning and an 'r' at the end
  elif re.match(r'((^d)(.+)(r$))|((^z)(.+)(r$))', prayer.lower(), flags=0):
    eq_prayer = 'Dhuhr'
  # if prayer matches an 'a' at the beginning and an 'r' at the end
  elif re.match(r'((^a)(.+)(r$))', prayer.lower(), flags=0):
    eq_prayer = 'Asr'
  # if prayer matches an 'm' at the beginning and an 'b' at the end
  elif re.match(r'((^m)(.+)(b$))', prayer.lower(), flags=0):
    eq_prayer = 'Maghrib'
  # if prayer matches an 'i' at the beginning and an 'a' at the end
  elif re.match(r'((^i)(.+)(a$))', prayer.lower(), flags=0):
    eq_prayer = 'Isha'
  # if prayer matches an 'g' or 'j' at the beginning
  elif re.match(r'((^g))|((^j))', prayer.lower(), flags=0):
    eq_prayer = 'Jumma'
  return eq_prayer
