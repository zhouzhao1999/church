import os
import sqlite3


class SqlPool():
    def getresultset(self, sql):
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        con = sqlite3.connect(father_path + "/bible.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        resultset = cur.fetchall()
        return resultset
