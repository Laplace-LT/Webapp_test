import sqlite3
import re
import requests

DATABASE = 'database.db'

def create_kishi_table():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS data (name, rating)")
    url = 'https://shogidata.info/list/rateranking.html'

    r = requests.get(url)

    index = -1

    while True:
        index = r.text.find("</a></td><td>", index + 1)
        name_start = r.text.rfind('html">', 0, index) + 6
        if index == -1:
            break
        name = r.text[name_start:index].split()[0]
        rating = r.text[index+13:index+19]
        check = con.execute("SELECT * FROM data WHERE name = ?", [name])
        # print(check.fetchone())
        if check.fetchone() is None:
            # print(f"insert {name}")
            con.execute("INSERT INTO data VALUES (?, ?)", [name, rating])
        else:
            # print(f"update {name}")
            con.execute("UPDATE data SET rating = ? WHERE name == ?", [rating, name])
    con.commit()
    con.close()