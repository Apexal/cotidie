from cotidie import app
from flask import request, render_template
from cotidie.database import *
from cotidie.auth import *

@app.route("/")
def index():
    return render_template("index.html", is_home=True)

@app.route("/actions")
@app.route("/actions/<int:action_id>")
@requires_auth
def actions(action_id=None):
    if action_id is None:
        actions = Action.query.all()
        return render_template("actions.html", actions=actions)
    else:
        action = Action.query.filter_by(id = action_id).first()
        return render_template("action.html", action=action)
