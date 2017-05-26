from flask import Flask
app = Flask(__name__)

import app as routes
import db
