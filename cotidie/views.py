from cotidie import app
from flask import request, render_template, redirect, url_for, flash, g
from cotidie.database import *
from cotidie.auth import *
from sqlalchemy import desc
from operator import attrgetter
from datetime import datetime, timedelta
import collections

@app.before_request
def before_request():
   g.user = request.authorization['username'] if request.authorization else None

@app.route("/")
def index():
    app.logger.debug(request.authorization)
    return render_template("index.html", is_home=True)

@app.route("/actions")
@app.route("/actions/<int:action_id>")
@requires_auth
def actions(action_id=None):
    if action_id is None:
        actions = Action.query.filter_by(user=request.authorization['username']).all()
        return render_template("actions.html", actions=actions)
    else:
        action = Action.query.filter_by(id = action_id, user=request.authorization['username']).first()
        completion_count = len([a for a in action.completions if a.user == request.authorization['username']])
        return render_template("action.html", action=action, completion_count=completion_count, today=datetime.today())

@app.route("/actions/add", methods=['POST'])
@requires_auth
def add_action():
    f = request.form
    new_action = Action(title=f['title'], description=f['description'], priority=f['priority'], min_amount=f['min_amount'], user=request.authorization['username'])
    db.session.add(new_action)
    db.session.commit()

    flash('Successfully added new action.', 'success')

    return redirect(url_for('actions', action_id=new_action.id))

@app.route("/actions/<int:action_id>/remove", methods=['POST'])
@requires_auth
def remove_action(action_id):
    action = Action.query.filter_by(id=action_id, user=request.authorization['username']).first()
    db.session.delete(action)
    db.session.commit()

    flash('Successfully deleted action.', 'warning')

    return redirect(url_for('actions'))

@app.route("/days")
@app.route("/days/<string:date>")
@requires_auth
def days(date=None):
    if date is None:
        return redirect(url_for('days', date=datetime.today().strftime('%Y-%m-%d')))
    else:
        completions = Completion.query.filter_by(date=date, user=request.authorization['username']).all()

        # Group by action
        actions = sorted(set([c.action for c in completions]), key=attrgetter('priority', 'id'))
        groups = {}
        for a in actions:
            groups[a] = [c for c in completions if c.action == a]

        unused_actions = [a for a in Action.query.filter_by(user=request.authorization['username']).order_by(desc(Action.priority)).all() if a not in actions]
        date=datetime.strptime(date, '%Y-%m-%d')
        return render_template('day.html', date=date, prev_date=date-timedelta(1), next_date=date+timedelta(1), actions=actions, groups=groups, unused_actions=unused_actions)

@app.route("/days/<string:date>/completion", methods=["POST"])
@requires_auth
def add_completion(date):
    f = request.form
    new_completion = Completion(action_id=f['action_id'], date=datetime.strptime(date, "%Y-%m-%d"), comment=f["comment"], user=request.authorization['username'])
    db.session.add(new_completion)
    db.session.commit()

    return redirect(url_for("days", date=date))

@app.route("/days/<string:date>/remove", methods=["POST"])
@requires_auth
def remove_completion(date):
    f = request.form
    c = Completion.query.filter_by(id=f['completion_id'], user=request.authorization['username']).first()
    db.session.delete(c)
    db.session.commit()

    return redirect(url_for("days", date=date))
