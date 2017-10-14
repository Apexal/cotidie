#! /usr/bin/env python3

from flask import Flask, session, redirect, url_for, request
app = Flask(__name__)

from cotidie.database import db
import cotidie.auth
import cotidie.views

db.create_all()
