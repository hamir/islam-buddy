#!/usr/bin/env python
import os
import pprint
import json

from flask import Flask
from flask import request
from flask import make_response
from daily_prayer import DailyPrayer
import util


app = Flask(__name__)
daily_prayer = DailyPrayer()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'


@app.route('/salah', methods=['POST', 'GET'])
def get_salah():
  if request.method == 'GET':
    print 'received GET request'
    params = {
      'lat': request.args.get('lat'),
      'lng': request.args.get('lng'),
      'prayer': request.args.get('prayer'),
    }
    print 'params = ', params
  elif request.method == 'POST':
    print 'received POST request'
    params = request.get_json(silent=True, force=True)
    print params
    print '============================'
    print 'params = ', params
    prayer = params.get("result").get("parameters").get("prayer-name")

    #location = params.get('location')
    #print 'location = ', location
    #print 'lat = ', params.get('location').get('latitude')
    #print 'lng = ', params.get('location').get('longitude')

  #if not params.get('lat') or not params.get('lng'):
  #  return util.json_error('Please provide a lat and lng.')

  #prayer_times = \
  #  daily_prayer.GetPrayerTimes(params.get('lat'), params.get('lng'))

  prayer_times = daily_prayer.GetPrayerTimes(37.3541079,-121.9552355)
  prayer_time = {"speech": "The time for " + prayer  + " is  " + prayer_times.get(prayer)}
  return util.json_response(prayer_time)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

