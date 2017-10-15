from cotidie import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Models
class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    priority = db.Column(db.SmallInteger, default=0)
    min_amount = db.Column(db.SmallInteger, default=1)

class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'),
        nullable=False)
    action = db.relationship('Action',
        backref=db.backref('completions', lazy=True))
    date = db.Column(db.Date, nullable=False, default=datetime.now)
    comments = db.Column(db.String(300))