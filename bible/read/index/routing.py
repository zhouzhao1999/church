import datetime
from flask import render_template, request
from bible.read.index import Process
from bible import app


@app.route('/index', methods=['GET'])
def index():

    return render_template("index.html")
