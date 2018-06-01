"""Computes daily salah times based on location."""

import salah_com_fetcher
import util


# pylint: disable-msg=r0903
class PrayerInfo(object):
    """Gets and packages prayer information."""

    @classmethod
    def GetPrayerTimes(cls, lat, lng):
        """Gets the daily prayer times for a given lat/lng.

        Args:
          lat: a double representing the latitude
          lng: a double representing the longitude

        Returns: a dict containing (DailyPrayer -> string) of daily
            prayer times
        """
        #print "[enter][GetPrayerTimes]"

        prayer_times = salah_com_fetcher.GetDailyPrayerTimes(lat, lng)
        if prayer_times == {}:
            return {}
        #print '[GetPrayerTimes] salah.com scrape result = ', prayer_times
        result = {}

        for key in prayer_times:
            prayer = util.StringToDailyPrayer(key)
            if prayer:
                result[prayer] = prayer_times[key]

        #print '[GetPrayerTimes] prayer times = ', result

        #print "[exit][GetPrayerTimes]"
        return result
