# coding=UTF-8

from bible.db import SqlPool
import datetime


class Process:
    def getList(self):
        sql = '''
            select * from (
                select 
                    1 as NType,
                    '每日经课'as NName, 
                    Daily.NDate as NDate, 
                    group_concat(FullName || NChapter) as Chapter,
                    'Gray' as ColorCode,
                    NPerson_W,
                    NPerson_P
                from Daily 
                left join BibleID on rtrim(ltrim(Daily.NEnglishName)) = BibleID.EnglishName
                left join ReadPerson on ReadPerson.NDate = Daily.NDate
                group by Daily.NDate
                
                union all
                
                select 
                    2 as NType,
                    Liturgical.NChineseName as LiturgicalName,
                    NDate,
                    group_concat(FullName || NChapter) as Chapter,
                    Colors1.NCode as ColorCode,'',''
                from Lectionary
                    left join BibleID on rtrim(ltrim(Lectionary.NEnglishName)) = BibleID.EnglishName
                    left join Liturgical on Liturgical.id = Lectionary.LiturgicalId
                    left join ReadType on ReadType.id = Lectionary.NReadTypeId
                    left join Colors Colors1 on Colors1.NCode = Liturgical.NColor
                    left join Colors Colors2 on Colors2.NCode = Liturgical.NColorOr
                group by Liturgical.NChineseName
            )
            where NDate<= DATE('now','14 days')
            order by NDate desc
            limit 21
        '''

        sqlpool = SqlPool()
        rows = sqlpool.getresultset(sql)
        list = []
        for row in rows:
            list.append({
                "NName": row["NName"], 
                "NDate": row["NDate"],
                "Chapter": row["Chapter"],
                "ColorCode": row["ColorCode"],
                "WeekName" : getWeekName(row["NDate"]),
                "NType":  row["NType"],
                "NPerson_W":  row["NPerson_W"],
                "NPerson_P":  row["NPerson_P"]
                })

        return {"list":list}

def getWeekName(NDate):
    time1 = datetime.datetime.strptime(NDate, '%Y-%m-%d')
    weekname = ""
    week = time1.weekday()
    if week == 0:
        weekname = "星期一"
    elif week == 1:
        weekname = "星期二"
    elif week == 2:
        weekname = "星期三"
    elif week == 3:
        weekname = "星期四"
    elif week == 4:
        weekname = "星期五"
    elif week == 5:
        weekname = "星期六"
    elif week == 6:
        weekname = "主日"
    return weekname