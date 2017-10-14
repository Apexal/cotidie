#! /usr/bin/env python3

from flask import Flask, render_template, session, redirect, url_for, request
app = Flask(__name__)

@app.route("/")
def index():
    app.logger.debug('A value for debugging')
    return "Hello World!"