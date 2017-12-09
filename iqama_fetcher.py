"""Fetches iqamah times from the Iqamah.net service."""

import re
from xml.etree import ElementTree
import util
import requests
from masjid_util import GetMasjidID

_IQAMAH_NET_URL = 'http://feed.iqamah.net/IQ'

_NUMERIC_STRINGS = {
    'First' : 0,
    'Second' : 1,
    'Third' : 2,
    'Fourth' : 3,
    'Fifth': 4,
}

# Fajr prayer matches an 'f' at the beginning and an 'r' at the end
_FAJR = re.compile(r'((^f)(.+)(r$))')
# Dhuhr prayer matches an 'd' or 'z' at the beginning and an 'r' at the end
_DHUHR = re.compile(r'((^d)(.+)(r$))|((^z)(.+)(r$))')
# Asr prayer matches an 'a' at the beginning and an 'r' at the end
_ASR = re.compile(r'((^a)(.+)(r$))')
# Maghrib prayer matches an 'm' at the beginning and an 'b' at the end
_MAGHRIB = re.compile(r'((^m)(.+)(b$))')
# Isha prayer matches an 'i' at the beginning and an 'a' at the end
_ISHA = re.compile(r'((^i)(.+)(a$))')
# Jumma prayer matches an 'g' or 'j' at the beginning
_JUMMA = re.compile(r'((^g))|((^j))')

def GetIqamaTime(desired_prayer, masjid):
  """Gets the iqama time from the iqamah.net service by peforming a GET.

  Args:
    desired_prayer: DailyPrayer enum representing desired salah
    masjid: a string representing the masjid of intereset

  Returns: a string containing the iqamah time along with AM/PM
  """

  # making sure the masjid input is in UTF-8 format and
  # getting the id from the _MASJID_METADATA
  masjid_id = GetMasjidID(util.EncodeParameter(masjid))

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
    for iqamah in iqamah_element:
      # convert the prayer names in the IqDay element to a known format
      iqamah_name = GetEquivalentPrayer(str(iqamah.tag))
      if iqamah_name.lower() in desired_prayer.lower():
        # for the Jumma case, the timings is in the following format
        # <Juma><JumaAdhan>##:##,##:##</JumaAdhan></Juma>
        if 'Jumma' in desired_prayer:
          # get the index based on the entity name
          # example: First Jumma will return 0, Second Jumma will return 1
          jumma_index = _NUMERIC_STRINGS[desired_prayer.split(' ')[0]]
          if (iqamah[0].text).split(',')[jumma_index]:
            iqamah_time = (iqamah[0].text).split(',')[jumma_index]
        else:
          iqamah_time = iqamah.text
        break

    print 'Iqamah Time ', iqamah_time

    # if iqama time was found then format time to ##:##
    if iqamah_time:
      return FormatTime(str(iqamah_time))
    return None
  print 'bad response from iqamah service = ', request.status_code
  return None

def FormatTime(time):
  """Returns the time variable back in ##:## format

  Args:
    time: a string representing the iqamah time

  Returns: a string containing the iqamah time in ##:## format
  """

  # if the time input is in a format where it contains integers
  # then proceed forward otherwise return None
  if re.match(r'(\d+)', time):
    # strip the time variable from anything added to it
    # example: 10:00 PM becomes 1000 and 5 AM becomes 5
    time = ''.join(re.findall(r'(\d+)', time))
    # if time length is more than 2 characters then add a : after
    # the second character from the right
    # example: 1000 becomes 10:00 and 5 stays 5
    if len(time) > 2:
      return time[:-2] + ':' + time[-2:]
    return time + ':00'

def GetEquivalentPrayer(prayer):
  """Returns the prayer equivalent to the defined prayer-name entity

  Args:
    prayer: a string representing desired salah

  Returns: a string containing prayer-name entity equivalent to the desired
  input prayer
  """
  prayer = prayer.lower()
  eq_prayer = None

  if _FAJR.match(prayer):
    eq_prayer = 'Fajr'
  elif _DHUHR.match(prayer):
    eq_prayer = 'Dhuhr'
  elif _ASR.match(prayer):
    eq_prayer = 'Asr'
  elif _MAGHRIB.match(prayer):
    eq_prayer = 'Maghrib'
  elif _ISHA.match(prayer):
    eq_prayer = 'Isha'
  elif _JUMMA.match(prayer):
    eq_prayer = 'Jumma'
  return eq_prayer
