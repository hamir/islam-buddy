#!/usr/bin/env python
import json
from flask import Flask
from flask import request
from flask import make_response
from salah.daily_prayer import DailyPrayer


app = Flask(__name__)
daily_prayer = DailyPrayer()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'


@app.route('/salah', methods=['POST', 'GET'])
def get_salah():
  if request.method == 'GET':
    params = {
      'lat': request.args.get('lat'),
      'lng': request.args.get('lng'),
    }
  elif request.method == 'POST':
    params = request.get_json()
    print params
    print '============================'
    print 'params = ', params
    location = params.get('location')
    print 'location = ', location
    print 'lat = ', params.get('location').get('latitude')
    print 'lng = ', params.get('location').get('longitude')

  if not params.has_key('lat') or not params.has_key('lng'):
    return 'Please provide a lat and lng.'

  prayer_times = \
    daily_prayer.GetPrayerTimes(params.get('lat'), params.get('lng'))


  r = make_response(json.dumps(prayer_times, indent=4))
  r.headers['Content-Type'] = 'application/json'
  return r

if __name__ == "__main__":
  port = int(os.getenv('PORT', 5000))

  print("Starting app on port %d" % port)

  app.run(debug=False, port=port, host='0.0.0.0')
