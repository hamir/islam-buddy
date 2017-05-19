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
  params = request.get_json(silent=True, force=True)

  print '============================'
  print 'params = ', params
  location = params.get('location')
  print 'location = ', location
  print 'lat = ', params.get('location').get('latitude')
  print 'lng = ', params.get('location').get('longitude')

  if not params.has_key('lat') or not request.args.has_key('lng'):
    return 'Please provide a lat and lng.'

  prayer_times = \
      daily_prayer.GetPrayerTimes(request.args.get('lat'), request.args.get('lng'))
  r = make_response(json.dumps(prayer_times, indent=4))
  r.headers['Content-Type'] = 'application/json'
  return r
