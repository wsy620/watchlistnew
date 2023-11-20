from flask import Flask
app = Flask(__name__)
import json

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'