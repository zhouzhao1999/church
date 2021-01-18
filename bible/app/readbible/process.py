# coding=UTF-8

from bible.db import SqlPool


class Process:

    def getbible(self, time1):
        sqlpool = SqlPool()
        rows = sqlpool.getresultset("select NChapter,FullName,SN from Daily "
                                    "left join BibleID on rtrim(ltrim(Daily.NEnglishName)) = BibleID.EnglishName"
                                    " where NDate='" + time1 + "' order by NOrder")
        list = []
        for row in rows:
            list.append({"NChapter": row["NChapter"], "FullName": row["FullName"],
                         "Text": getbiblebychapter(str(row["SN"]), row["NChapter"])})
        ColorCode = ""
        jingkename = ""
        if len(list) != 0:
            jingkename = "每日经课"
            ColorCode = "white"
        else:
            rows = sqlpool.getresultset(f'''
                        select NChapter,FullName,SN,
                            ReadType.NChineseName as ReadTypeName,
                            Liturgical.NChineseName as LiturgicalName,
                            Colors1.NCode as ColorCode,
                            Colors1.NName as ColorName,
                            Colors2.NCode as ColorOrCode,
                            Colors2.NName as ColorOrName
                        from Lectionary
                            left join BibleID on rtrim(ltrim(Lectionary.NEnglishName)) = BibleID.EnglishName
                            left join Liturgical on Liturgical.id = Lectionary.LiturgicalId
                            left join ReadType on ReadType.id = Lectionary.NReadTypeId
                            left join Colors Colors1 on Colors1.NCode = Liturgical.NColor
                            left join Colors Colors2 on Colors2.NCode = Liturgical.NColorOr
                        where NDate='{time1}' order by NOr
            ''')
            for row in rows:
                list.append({"NChapter": row["NChapter"], "FullName": row["FullName"],
                             "Text": getbiblebychapter(str(row["SN"]), row["NChapter"])})
                ColorCode = row["ColorCode"]
                jingkename = row["LiturgicalName"]

        return {"time": time1,
                "list": list,
                "ColorCode": ColorCode.lower(),
                "jingkename": jingkename
                }


# 根据章节信用获得经文的条件，再根据条件获取经文的内容
# 如：7:1-8,15-18  7:54-8:1a
def getbiblebychapter(sn, chapterlist):
    lection = ""
    startzhang = ""
    endzhang = ""
    startjie = ""
    endtjie = ""

    a = 0
    chapterlist = chapterlist.replace(
        "a", "").replace("b", "").replace("c", "")
    chapterlist = chapterlist.split(",")  # 所一段一段分开

    for chapter in chapterlist:
        aaa = chapter.split("-")
        if (len(aaa) == 1 and a == 0):  # 处理只有章没有节 如 39章，只有第一次处理
            # 处理开始的章与节
            bbb1 = aaa[0].split(":")
            if len(bbb1) > 1:
                startzhang = bbb1[0]
                startjie = bbb1[1]
                lection += seekbibleonejie(sn, startzhang, startjie)
            else:
                startzhang = aaa[0]
                lection += seekbibleonezhang(sn, startzhang)
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
            elif len(endtjie) == 0:
                lection += seekbibleonejie(sn, startzhang, startjie)
            else:
                lection += seekbible(sn, startzhang, startjie, endtjie)

        a = a + 1
    return lection


# 根据条件查找经文
def seekbible(volumeSN, chapterSN, verseSNStart, verseSNEnd):
    sql = "select VerseSN,ChapterSN,Lection from Bible where VolumeSN = " + \
        volumeSN + " and ChapterSN = " + chapterSN
    sql += " and VerseSN >= " + verseSNStart + " and VerseSN <= " + verseSNEnd
    sqlpool = SqlPool()
    bible = sqlpool.getresultset(sql)
    text = ""
    for a in bible:
        text += str(a["ChapterSN"]) + ":" + \
            str(a["VerseSN"]) + "." + a["Lection"]
    return text


# 根据条件查找某一章经文
def seekbibleonezhang(volumeSN, chapterSN):
    sql = "select VerseSN,ChapterSN,Lection from Bible where VolumeSN = " + \
        volumeSN + " and ChapterSN = " + chapterSN
    sqlpool = SqlPool()
    bible = sqlpool.getresultset(sql)
    text = ""
    for a in bible:
        text += str(a["ChapterSN"]) + ":" + \
            str(a["VerseSN"]) + "." + a["Lection"]
    return text


# 根据条件查找某一节经文
def seekbibleonejie(volumeSN, chapterSN, verseSN):
    sql = "select VerseSN,ChapterSN,Lection from Bible where VolumeSN = " + \
        volumeSN + " and ChapterSN = " + chapterSN + " and VerseSN >= " + verseSN
    sqlpool = SqlPool()
    bible = sqlpool.getresultset(sql)
    text = ""
    for a in bible:
        text += str(a["ChapterSN"]) + ":" + \
            str(a["VerseSN"]) + "." + a["Lection"]
    return text
