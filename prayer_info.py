"""Computes daily salah times based on location."""

import salah_com_fetcher
from common import DailyPrayer


# mapping from salah.com's spelling for a prayer to 
# common.DailyPrayer. This dictionary needs to be kept
# separate from that in util.py
_SALAH_NAME_TO_PRAYER = {
  'fajr': DailyPrayer.FAJR,
  'dhuhr': DailyPrayer.DHUHR,
  'asr': DailyPrayer.ASR,
  'maghrib': DailyPrayer.MAGHRIB,
  'isha': DailyPrayer.ISHA,
  'qiyam': DailyPrayer.QIYAM,
  'unspecified': DailyPrayer.UNSPECIFIED,
}

def _StringToDailyPrayer(prayer_str):
  """Infers a DailyPrayer out of a string."""
  prayer_str = str(prayer_str).lower()
  if prayer_str in _SALAH_NAME_TO_PRAYER:
    return _SALAH_NAME_TO_PRAYER[prayer_str]
  else:
    return ''


class PrayerInfo(object):

  def GetPrayerTimes(self, lat, lng):
    """Gets the daily prayer times for a given lat/lng.

    Args:
      lat: a double representing the latitude
      lng: a double representing the longitude

    Returns: a dict containing (DailyPrayer -> string) of daily 
        prayer times
    """
    print "[enter][GetPrayerTimes]"

    prayer_times = salah_com_fetcher.GetDailyPrayerTimes(lat, lng)
    print '[GetPrayerTimes] salah.com scrape result = ', prayer_times
    result = {}

    for key in prayer_times:
      prayer = _StringToDailyPrayer(key)
      if prayer:
        result[prayer] = prayer_times[key]

    print '[GetPrayerTimes] prayer times = ', result 

    print "[exit][GetPrayerTimes]"
    return result

