#!/usr/bin/env python
import os
import pprint

from flask import Flask
from flask import request
#from daily_prayer import DailyPrayer
import util


app = Flask(__name__)
#daily_prayer = DailyPrayer()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'

"""
@app.route('/salah', methods=['POST', 'GET'])
def get_salah():
  if request.method == 'GET':
    print 'received GET request'
    params = {
      'lat': request.args.get('lat'),
      'lng': request.args.get('lng'),
    }
    print 'params = ', params
  elif request.method == 'POST':
    params = request.get_json()
    print params
    print '============================'
    print 'params = ', params
    location = params.get('location')
    print 'location = ', location
    print 'lat = ', params.get('location').get('latitude')
    print 'lng = ', params.get('location').get('longitude')

  if not params.get('lat') or not params.get('lng'):
    return util.json_error('Please provide a lat and lng.')

  prayer_times = \
    daily_prayer.GetPrayerTimes(params.get('lat'), params.get('lng'))

  print 'prayer times = ', prayer_times

  return util.json_response(prayer_times)
"""


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
