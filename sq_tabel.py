import sqlite3

def add_sessions():
    con = sqlite3.connect(".sqlite")
    cur = con.cursor()