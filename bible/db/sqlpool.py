import sqlite3


class SqlPool():
    def getresultset(self, sql):
        con = sqlite3.connect("bible/db/bible.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        resultset = cur.fetchall()
        return resultset

