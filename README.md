# Islam Buddy #

Islam Buddy allows you to quickly and conveniently find local Prayer Times and masjid Iqama times.

## Amer's Plan ##

- rename the class daily_prayer to prayer_info
- gracefully handle the lat/lng invalid error case (i.e. print error message)
note: salahcomfetcher return empty dictionary on fail
daily prayer print got an empty or couldn’t get

## Setup ##

Install the required packages.
```
$ pip install -r requirements.txt
```

Run the server (inside /server)
```
$ ./run_server
```

To make a sample request, try:
```
$ ./run_query
```
