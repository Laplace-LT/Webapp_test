from flask import Flask
app = Flask(__name__)
import sample.main

from sample import db
db.create_kishi_table()