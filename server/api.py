from flask import Flask, request
from salah.daily_prayer import DailyPrayer
import json


app = Flask(__name__)
daily_prayer = DailyPrayer()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'


@app.route('/salah')
def get_salah():
  if not request.args.has_key('lat') or not request.args.has_key('lng'):
    return 'Please provide a lat and lng.'
  prayer_times = \
      daily_prayer.GetPrayerTimes(request.args.get('lat'), request.args.get('lng'))
  return json.dumps(prayer_times, indent=4)