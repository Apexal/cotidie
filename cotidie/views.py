from cotidie import app
from flask import render_template
from cotidie.database import *

@app.route("/")
def index():
    return render_template('index.html')
