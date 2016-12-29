import json
import sys
import time

from flask import render_template, request

from . import app
from .utils import find_games

@app.route('/')
def index():
    keywords = request.args.get('keywords', '')
    return render_template('index.html', games=find_games(keywords))
