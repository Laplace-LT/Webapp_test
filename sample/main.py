from sample import app
from flask import render_template, request
import sqlite3

DATABASE = "database.db"

@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    db_kishi = con.execute('SELECT * FROM data').fetchall()
    con.close()

    data = []
    for name, rating in db_kishi:
        data.append({'name': name, "rating": rating})

    return render_template(
        'index.html',
        data = data
    )

@app.route('/sub')
def sub():
    return render_template(
        'sub.html'
    )

@app.route('/', methods = ["POST"])
def calculate():
    con = sqlite3.connect(DATABASE)
    db_kishi = con.execute('SELECT * FROM data').fetchall()
    data = []
    for name, rating in db_kishi:
        data.append({'name': name, "rating": rating})
    
    name1, name2 = request.form['name1'], request.form['name2']
    kishi1 = con.execute('SELECT * FROM data WHERE name = ?', [name1]).fetchone()
    kishi2 = con.execute('SELECT * FROM data WHERE name = ?', [name2]).fetchone()
    print(kishi1, kishi2)
    try:
        kishi1_rating = float(kishi1[1])
        kishi2_rating = float(kishi2[1])
        rate = [0, 0, 0, 0]
        rate[0] = 1 / (pow(10, (kishi1_rating - kishi2_rating) / 400))
        rate_opp = 1 - rate[0]
        rate[1] = rate[0] ** 2 * (1 + rate_opp * 2)
        rate[2] = rate[0] ** 3 * (1 + rate_opp * 3 + rate_opp ** 2 * 6)
        rate[3] = rate[0] ** 4 * (1 + rate_opp * 4 + rate_opp ** 2 * 10 + rate_opp ** 3 * 20)
        rate_show = True

    except:
        rate = []
        rate_show = False
        pass

    con.close()
    return render_template(
        'index.html',
        rate = rate,
        kishi1 = kishi1[0],
        kishi2 = kishi2[0],
        rate_show = rate_show,
        data = data
    )