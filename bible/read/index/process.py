# coding=UTF-8

from bible.db import SqlPool


class Process:
    def getList(self):
        sql = '''
            with a as (
                select '每日经课'as NName, 
                    NDate, 
                    group_concat(FullName || NChapter) as Chapter,'white' as ColorCode  
                from Daily 
                left join BibleID on rtrim(ltrim(Daily.NEnglishName)) = BibleID.EnglishName
                group by NDate
                
                union all
                
                select 
                    Liturgical.NChineseName as LiturgicalName,
                    NDate,
                    group_concat(FullName || NChapter) as Chapter,
                    Colors1.NCode as ColorCode
                from Lectionary
                    left join BibleID on rtrim(ltrim(Lectionary.NEnglishName)) = BibleID.EnglishName
                    left join Liturgical on Liturgical.id = Lectionary.LiturgicalId
                    left join ReadType on ReadType.id = Lectionary.NReadTypeId
                    left join Colors Colors1 on Colors1.NCode = Liturgical.NColor
                    left join Colors Colors2 on Colors2.NCode = Liturgical.NColorOr
            group by Liturgical.NChineseName
            )
            select * from a
            where NDate<= DATE()
            order by NDate desc
            limit 20
        '''

        sqlpool = SqlPool()
        rows = sqlpool.getresultset(sql)
        for row in rows:
            list.append({"NName": row["NName"], "NDate": row["NDate"],
                            "Chapter": row["Chapter"]})

        return {"list":list}
