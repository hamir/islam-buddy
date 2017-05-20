#!/usr/bin/env python
import os
import pprint
import json

from flask import Flask, request, make_response
from daily_prayer import PrayerInfo 
import util
from common import DailyPrayer


app = Flask(__name__)
prayer_info = PrayerInfo()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'


@app.route('/salah', methods=['POST', 'GET'])
def GetSalah():
  if request.method == 'GET':
    print 'received GET request'
    params = {
      'lat': request.args.get('lat'),
      'lng': request.args.get('lng'),
      'prayer': request.args.get('prayer'),
    }
    print 'params = ', params

    if not params.get('lat') or not params.get('lng'):
      return util.JsonError('Please provide a lat and lng.')

    prayer_times = \
      prayer_info.GetPrayerTimes(params.get('lat'), params.get('lng'))

    # convert from map<PrayerTime, string> to map<string, string>
    output_prayer_times = {}
    for key in prayer_times:
      output_prayer_times[util.GetPrayerKeyName(key)] = prayer_times[key]

    return util.JsonResponse(output_prayer_times)
  elif request.method == 'POST':
    print 'received POST request'
    params = request.get_json(silent=True, force=True)

    # this needs to be less hacky - @hamdy maybe a request extractor class?
    prayer = params.get("result").get("parameters").get("PrayerName")
    print 'prayer = ', prayer

    #location = params.get('location')
    #print 'location = ', location
    #print 'lat = ', params.get('location').get('latitude')
    #print 'lng = ', params.get('location').get('longitude')

    prayer_times = prayer_info.GetPrayerTimes(37.3541079,-121.9552355)
    prayer_time = prayer_times.get(util.StringToDailyPrayer(prayer))
    print 'prayer_times[', prayer, "] = ", prayer_time 

    speech = "The time for %s is %s." % (prayer, prayer_time)
    return util.JsonResponse({"speech": speech})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

