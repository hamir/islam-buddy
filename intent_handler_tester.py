# -*- coding: utf-8 -*-

from prayer_info import PrayerInfo
from intent_handler import IntentHandler

_prayer_info = PrayerInfo()
_intent_handler = IntentHandler(_prayer_info, None, None)

desired_prayer = 'fajr'
lat = 40.715856
lng = -73.8300517
city = 'Queens County'
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

desired_prayer = 'isha'
lat = 30.375321
lng = 69.34511599999999
city = None
date_str = None
prayer_time_prop = None

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 33.93911
lng = 67.7

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 20.593684
lng = 78.96288

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 23.684994
lng = 90.356331

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 34.8020745
lng = 38.996815

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 33.854721
lng = 35.862285

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 4.210484
lng = 101.975766

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 32.427908
lng = 53.688046

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 32.427908
lng = 53.688046

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 26.0667
lng = 50.5577

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 33.223191
lng = 43.679291

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 21.4735329
lng = 55.975413

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 15.552727
lng = 48.516388

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 23.424076
lng = 53.847818

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 29.31166
lng = 47.481766

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 25.354826
lng = 51.183884

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 1.352083
lng = 103.819836

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 1.352083
lng = 103.819836

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 46.227638
lng = 2.213749

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']

lat = 38.963745
lng = 35.243322

output_str = _intent_handler._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, date_str, prayer_time_prop)
print output_str['displayText']
