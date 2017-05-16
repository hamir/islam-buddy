# Islam Buddy

Islam Buddy allows you to quickly and conveniently find local Prayer Times and masjid Iqama times.

### Setup

Load the virtual environment
```
$ . venv/bin/activate
```

Run the server (inside /server)
```
$ export FLASK_APP=main.py
$ flask run
```

## Directories ##

/server - Flask server that serves prayer and iqama times

/venv - this will be the shared virtual environment that the server will run on (this allows us to all have the same environment when testing locally and for deployments)