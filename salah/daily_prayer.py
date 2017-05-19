"""Computes daily salah times based on location."""

import salah_com_fetcher


class DailyPrayer(object):

  def GetPrayerTimes(self, lat, lng):
    """Gets the daily prayer times for a given lat/lng.

    Args:
      lat: a double representing the latitude
      lng: a double representing the longitude

    Returns: a dict containing of daily prayer times
    """
    return salah_com_fetcher.GetDailyPrayerTimes(lat, lng)
