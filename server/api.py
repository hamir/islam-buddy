from flask import Flask
from salah.daily_prayer import DailyPrayer
import json


app = Flask(__name__)
daily_prayer = DailyPrayer()


@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'


@app.route('/salah')
def get_salah():
  prayer_times = \
      daily_prayer.GetPrayerTimes(37.3541079, -121.9552355)
  return json.dumps(prayer_times, indent=4)