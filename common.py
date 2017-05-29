class DailyPrayer(object):
  UNSPECIFIED = 0;
  FAJR = 1;
  DHUHR = 2;
  ASR = 3;
  MAGHRIB = 4;
  ISHA = 5;
  QIYAM = 6;

class Intent(object):
  UNSPECIFIED = 0
  WHEN_IS_PRAYER = 1
  WHEN_IS_PRAYER_NAME = 2

class Locality(object):
  UNSPECIFIED = 0
  CITY = 1
  MASJID = 2
