"""Fetches prayer times from 'www.aladhan.com'."""

import util
import praytimes_org
from common import CalculationMethod
from datetime import datetime, timedelta
import time
from gmaps_client import ReverseGeocodeCountry

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
    """Gets the daily prayer times using the praytimes.org codebase.

    Args:
      lat: a double representing the latitude
      lng: a double representing the longitude
      date_str: a string representing the requested date in YYYY-MM-DD

    Returns: a dict containing of daily prayer times and an day difference integer
    """
    
    location = (lat, lng)
    method = GetCalcMethod(lat, lng)
    (current_user_timestamp, dst_UTC_offset, raw_UTC_offset) = util.GetCurrentUserTime(lat, lng)
    try:
        timezone_offset = raw_UTC_offset/(3600 * 1.0)
        dst_flag = 1 if dst_UTC_offset > 0 else 0
    except BaseException:
        return (None, None)

    timestamp = current_user_timestamp
    day_difference = 0
    
    if date_str and date_str != "None":
        try:
            agent_date = (util.GetCurrentUserTime(37.2359, -122.0638))[0].date()
            requested_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_difference = int((requested_date - agent_date).days)

            if day_difference > 0:
                timestamp = current_user_timestamp + timedelta(days=day_difference)
        except BaseException:
            pass

    try:
        timestamp_date = (timestamp.year, timestamp.month, timestamp.day)
        p = praytimes_org.PrayTimes()
        p.setMethod(method)
        prayer_times = p.getTimes(timestamp_date, location, timezone_offset, dst_flag)

        return (prayer_times, day_difference)
    except BaseException:
        return (None, None)

