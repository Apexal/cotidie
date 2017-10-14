#! /usr/bin/env python3

from flask import Flask, render_template, session, redirect, url_for, request
app = Flask(__name__)

import cotidie.auth

@app.route("/")
def index():
    return render_template('index.html')
