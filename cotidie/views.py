from cotidie import app
from flask import request, render_template, redirect, url_for, flash
from cotidie.database import *
from cotidie.auth import *
from sqlalchemy import desc
from operator import attrgetter
from datetime import datetime, timedelta

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
@requires_auth
def add_action():
    f = request.form
    new_action = Action(title=f['title'], description=f['description'], priority=f['priority'], min_amount=f['min_amount'])
    db.session.add(new_action)
    db.session.commit()

    flash('Successfully added new action.', 'success')

    return redirect(url_for('actions', action_id=new_action.id))

@app.route("/actions/<int:action_id>/remove", methods=['POST'])
@requires_auth
def remove_action(action_id):
    action = Action.query.get(action_id)
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
        completions = Completion.query.filter_by(date=date).all()

        # Group by action
        actions = sorted(set([c.action for c in completions]), key=attrgetter('priority', 'id'))
        groups = {}
        for a in actions:
            groups[a] = [c for c in completions if c.action == a]
        
        unused_actions = [a for a in Action.query.order_by(desc(Action.priority)).all() if a not in actions]
        date=datetime.strptime(date, '%Y-%m-%d')
        return render_template('day.html', date=date, prev_date=date-timedelta(1), next_date=date+timedelta(1), groups=groups, unused_actions=unused_actions)

@app.route("/days/<string:date>/completion", methods=["POST"])
@requires_auth
def add_completion(date):
    f = request.form
    new_completion = Completion(action_id=f['action_id'], date=datetime.strptime(date, "%Y-%m-%d"), comment=f["comment"])
    db.session.add(new_completion)
    db.session.commit()

    return redirect(url_for("days", date=date))

@app.route("/days/<string:date>/remove", methods=["POST"])
@requires_auth
def remove_completion(date):
    f = request.form
    c = Completion.query.get(f['completion_id'])
    db.session.delete(c)
    db.session.commit()

    return redirect(url_for("days", date=date))
