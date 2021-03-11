import datetime
from flask import render_template, request
from bible.app.admin import Process
from bible import flaskapp
import os
import uuid
import sys
from werkzeug.utils import secure_filename


flaskapp.config['UPLOAD_FOLDER'] = os.getcwd() + "/bible/static/upload"


@flaskapp.route('/admin', methods=['GET'])
def admin():
    process = Process()
    result = process.getList()
    return render_template("admin.html", result=result)


@flaskapp.route('/admin/upload', methods=['POST'])
def admin_upload():
    try:
        f = request.files['file']
        print(os.getcwd())
        uuidstr = str(uuid.uuid1()).replace("-", "")
        f.save(os.path.join(flaskapp.config['UPLOAD_FOLDER'], secure_filename(uuidstr+".jpg")))
    except Exception as re:
        return {"success": False, "msg": re.args}
    return {"success": True, "filename": f.filename}