from cotidie import app
from flask import request, render_template
from cotidie.database import *

@app.route("/")
def index():
    return render_template("index.html", is_home=True)

@app.route("/actions")
def actions():
    actions = Action.query.all()
    return render_template("actions.html", actions=actions)
