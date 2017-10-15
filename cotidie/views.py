from cotidie import app
from flask import request, render_template, redirect, url_for, flash
from cotidie.database import *
from cotidie.auth import *

from datetime import datetime

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

    flash('Successfully added new action.', 'success')

    return redirect(url_for('actions', action_id=new_action.id))

@app.route("/days")
@app.route("/days/<string:date>")
def days(date=None):
    if date is None:
        return redirect(url_for('days', date=datetime.today().strftime('%Y-%m-%d')))
    else:
        completions = Completion.query.filter_by(date=date).all()

        # Group by action
        actions = set([c.action for c in completions])
        groups = {}
        for a in actions:
            groups[a] = [c for c in completions if c.action == a]
        
        unused_actions = [a for a in Action.query.all() if a not in actions]

        return render_template('day.html', date=datetime.strptime(date, '%Y-%m-%d'), groups=groups, unused_actions=unused_actions)

@app.route("/days/<string:date>/completion", methods=["POST"])
def add_completion(date):
    f = request.form
    new_completion = Completion(action_id=f['action_id'], date=datetime.strptime(date, "%Y-%m-%d"), comment=f["comment"])
    db.session.add(new_completion)
    db.session.commit()

    return redirect(url_for("days", date=date))