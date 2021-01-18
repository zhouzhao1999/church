import datetime
from flask import render_template
from bible.app.admin import Process
from bible import flaskapp


@flaskapp.route('/admin', methods=['GET'])
def admin():
    
    process = Process()
    result = process.getList()
    
    return render_template("admin.html",result=result)

