# -*- coding: utf-8 -*-

from prayer_info import PrayerInfo
from intent_handler import IntentHandler

_prayer_info = PrayerInfo()
_intent_handler = IntentHandler(_prayer_info, None, None)

desired_prayer = 'fajr'
lat = 37
lng = -121
city = 'Santa Clara'
date_str = None
prayer_time_prop = None

print 'default'
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-01'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-02'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-03'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-05'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'maghrib'

print desired_prayer
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'fajr'
prayer_time_prop = 'fasting times'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'next prayer'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'time until'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'time until'
desired_prayer = 'dhuhr'

print prayer_time_prop + ' ' + desired_prayer 
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'invalid prayer time prop'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'invalid desired prayer'

print desired_prayer
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'fajr'
lat = 30
lng = 30
city = 'Markaz El-Hamam'
date_str = None
prayer_time_prop = None

print city
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-01'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-02'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-03'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '2018-06-05'

print date_str
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'maghrib'

print desired_prayer
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'fajr'
prayer_time_prop = 'fasting times'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'next prayer'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'time until'

print prayer_time_prop
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

prayer_time_prop = 'time until'
desired_prayer = 'dhuhr'

print prayer_time_prop + ' ' + desired_prayer 
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

desired_prayer = 'fajr'
lat = 45.5
lng = -75.5
city = 'Montréal'
date_str = None
prayer_time_prop = None

print city
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = '06-02/2018'

print 'invalid date string'
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

date_str = 'invalid'

print 'invalid date string'
output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']
