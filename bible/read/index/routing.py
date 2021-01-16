import datetime
from flask import render_template
from bible.read.index import Process
from bible import app


@app.route('/index.html', methods=['GET'])
def index():
    
    process = Process()
    result = process.getList()
    
    return render_template("index.html",result=result)
