from flask import Flask, render_template, url_for, request
import sqlite3
import datetime

app = Flask(__name__)


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr) VALUES (?,?)", (nm, addr))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


@app.route('/bible')
def bible():
    time1 = datetime.datetime.now().strftime('%Y-%m-%d')
    print(time1)
    time1 = "2021-01-09"
    con = sqlite3.connect("bible.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select NChapter,FullName,SN from Daily "
                "left join BibleID on Daily.NEnglishName = BibleID.EnglishName"
                " where NDate='" + time1 + "' order by NOrder")

    rows = cur.fetchall()
    lists = []
    for row in rows:
        list = {}
        lection = ""
        list["NChapter"] = row["NChapter"]  # 章节
        list["FullName"] = row["FullName"]  # 中文名称
        SN = str(row["SN"])  # 哪一篇圣经

        nChapter = row["NChapter"].split(":")
        if len(nChapter) == 1:
            list["Text"] = seekBible(SN, nChapter[0])
        else:
            verse = nChapter[1].replace("a", "").replace("b", "").split(",")
            for v in verse:
                lection += seekBible(SN, nChapter[0], v.split("-")[0], v.split("-")[1])
            list["Text"] = lection
        lists.append(list)

    return render_template("bible.html", rows=lists)


def seekBible(volumeSN, chapterSN, verseSNStart="", verseSNEnd=""):
    con = sqlite3.connect("bible.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql = "select VerseSN,Lection from Bible where VolumeSN = " + volumeSN + " and ChapterSN = " + chapterSN
    if (len(verseSNStart) != 0 and len(verseSNEnd) != 0):
        sql += " and VerseSN >= " + verseSNStart + " and VerseSN <= " + verseSNEnd
    cur.execute(sql)
    bible = cur.fetchall()
    text = ""
    for a in bible:
        text += str(a["VerseSN"]) + "." + a["Lection"]
    return text


if __name__ == '__main__':
    app.run()
