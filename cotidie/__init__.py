#! /usr/bin/env python3

import os
from flask import Flask, session, redirect, url_for, request
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

from cotidie.database import db
import cotidie.views

db.create_all()
