from cotidie import app
from flask_sqlalchemy import SQLAlchemy

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
