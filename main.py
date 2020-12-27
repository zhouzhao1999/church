from flask import Flask, render_template, url_for, request
import sqlite3
import datetime

app = Flask(__name__)


@app.route('/bible', methods=['GET'])
def bible():
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
            print(time1)
        elif way == "2":
            time1 = selectTime

    con = sqlite3.connect("bible.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select NChapter,FullName,SN from Daily "
                "left join BibleID on rtrim(ltrim(Daily.NEnglishName)) = BibleID.EnglishName"
                " where NDate='" + time1 + "' order by NOrder")
    rows = cur.fetchall()
    lists = []
    for row in rows:
        lists.append({"NChapter": row["NChapter"], "FullName": row["FullName"],
                      "Text": getbiblebychapter(str(row["SN"]), row["NChapter"])})
    return render_template("bible.html", rows=lists, time=time1)


# 根据条件查找经文
def seekbible(volumeSN, chapterSN, verseSNStart="", verseSNEnd=""):
    con = sqlite3.connect("bible.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql = "select VerseSN,ChapterSN,Lection from Bible where VolumeSN = " + volumeSN + " and ChapterSN = " + chapterSN
    if len(verseSNStart) != 0 and len(verseSNEnd) != 0:
        sql += " and VerseSN >= " + verseSNStart + " and VerseSN <= " + verseSNEnd
    print(sql)
    cur.execute(sql)
    bible = cur.fetchall()
    text = ""
    for a in bible:
        text += str(a["ChapterSN"]) + ":" + str(a["VerseSN"]) + "." + a["Lection"]
    return text


# 根据条件查找某一节经文
def seekbibleone(volumeSN, chapterSN, verseSN):
    con = sqlite3.connect("bible.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql = "select VerseSN,ChapterSN,Lection from Bible where VolumeSN = " + volumeSN + " and ChapterSN = " + chapterSN + " and VerseSN >= " + verseSN
    print(sql)
    cur.execute(sql)
    bible = cur.fetchall()
    text = ""
    for a in bible:
        text += str(a["ChapterSN"]) + ":" + str(a["VerseSN"]) + "." + a["Lection"]
    return text


# 根据章节信用获得经文
# 如：7:1-8,15-18  7:54-8:1a
def getbiblebychapter(sn, chapterlist):
    lection = ""
    startzhang = ""
    endzhang = ""
    startjie = ""
    endtjie = ""

    a = 0
    chapterlist = chapterlist.replace("a", "").replace("b", "").replace("c", "")
    chapterlist = chapterlist.split(",")  # 所一段一段分开

    for chapter in chapterlist:
        aaa = chapter.split("-")
        if (len(aaa) == 1 and a == 0):  # 处理只有章没有节 如 39章，只有第一次处理
            lection += seekbible(sn, aaa[0])
        else:
            # 处理开始的章与节
            bbb1 = aaa[0].split(":")
            if len(bbb1) > 1:
                startzhang = bbb1[0]
                startjie = bbb1[1]
            else:
                startjie = aaa[0]

            # 处理结束的章与节
            if len(aaa) == 1:
                endtjie = ""
            else:
                bbb2 = aaa[1].split(":")
                if len(bbb2) > 1:
                    endzhang = bbb2[0]
                    endtjie = bbb2[1]
                else:
                    endtjie = aaa[1]

            if len(endzhang) != 0:
                lection += seekbible(sn, startzhang, startjie, "200")
                lection += seekbible(sn, endzhang, "0", endtjie)
                print(lection)
            elif len(endtjie) == 0:
                lection += seekbibleone(sn, startzhang, startjie)
            else:
                lection += seekbible(sn, startzhang, startjie, endtjie)
                print(lection)

        a = a + 1
    return lection


if __name__ == '__main__':
    app.run()

# @app.route('/addrec', methods=['POST', 'GET'])
# def addrec():
#     if request.method == 'POST':
#         try:
#             nm = request.form['nm']
#             addr = request.form['add']
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO students (name,addr) VALUES (?,?)", (nm, addr))
#                 con.commit()
#                 msg = "Record successfully added"
#         except:
#             con.rollback()
#             msg = "error in insert operation"
#         finally:
#             return render_template("result1.html", msg=msg)
#             con.close()
