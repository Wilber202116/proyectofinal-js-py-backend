import sqlite3
from flask import g
from config import Config

DATABASE = Config.SQLITE_DB

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#metodo para consultar si existe base de datos o agregar algo
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#metodo para modificar datos existentes en la db
def modify_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    new_id = cur.lastrowid
    db.commit()
    cur.close()
    return new_id
'''
def new_id(cur):
    new_id = cur.lastrowid
    return new_id
'''
#metodo obtener los datos
def get_data_from_database(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()