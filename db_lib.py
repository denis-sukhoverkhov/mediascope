from flask import g
import sqlite3


def get_db(path_to_db):
    db = g._database = sqlite3.connect(path_to_db)
    return db


def query_db(cursor, query, args=(), one=False):
    cur = cursor.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv