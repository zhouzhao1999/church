import datetime
from flask import render_template, request
from bible.read.bible import Process
from bible import app


@app.route('/bible', methods=['GET'])
def bible():
    NDate = request.args.get('NDate', '')
    process = Process()
    result = process.getbible(NDate)

    return render_template(f"bible_{result['ColorCode']}.html", result=result)

""" 

    time1 = datetime.datetime.now().strftime('%Y-%m-%d')
    way = request.args.get('way', '')
    selectTime = request.args.get('time', '')
    if len(way) == "0":
        time1 = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        if way == "-1":
            time1 = (datetime.datetime.strptime(selectTime, '%Y-%m-%d') + datetime.timedelta(days=-1)).strftime(
                '%Y-%m-%d')
        elif way == "0":
            time1 = datetime.datetime.now().strftime('%Y-%m-%d')
        elif way == "1":
            time1 = (datetime.datetime.strptime(selectTime, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime(
                '%Y-%m-%d')
        elif way == "2":
            time1 = selectTime """