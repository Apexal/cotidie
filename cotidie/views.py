from cotidie import app
from flask import request, render_template, redirect, url_for, flash
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

@app.route("/actions/add", methods=['POST'])
def add_action():
    f = request.form
    new_action = Action(title=f['title'], description=f['description'], priority=f['priority'], min_amount=f['min_amount'])
    db.session.add(new_action)
    db.session.commit()

    return redirect(url_for('actions', action_id=new_action.id))
    