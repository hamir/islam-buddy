import sqlite3
import json
from contextlib import closing
from flask import g
import click
from main import app

_DATABASE = 'database.db'

def connect_db():
  return sqlite3.connect(_DATABASE)

@app.before_request
def before_request():
  g.db = connect_db()

@app.after_request
def after_request(response):
  g.db.close()
  return response

def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = [dict((cur.description[idx][0], value)
             for idx, value in enumerate(row)) for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv

def insert(table, fields=(), values=()):
  cur = g.db.cursor()
  query = 'INSERT OR REPLACE INTO %s (%s) VALUES (%s)' % (
      table,
      ', '.join(fields),
      ', '.join(['?'] * len(values))
  )
  cur.execute(query, values)
  g.db.commit()
  id = cur.lastrowid
  cur.close()
  return id

@app.cli.command()
def initdb():
  with closing(connect_db()) as db:
    with app.open_resource('db_schema.sql') as f:
      db.cursor().executescript(f.read())
    db.commit()
  click.echo('database created')

def GetUserInfo(user_id):
  user = query_db('select * from user_infos where user_id = ?',
                [user_id], one=True)
  if user is None:
    return {}
  else:
    return json.loads(user['data'])

def AddOrUpdateUser(user_id, user_info):
  insert('user_infos', ('user_id', 'data'), (user_id, json.dumps(user_info)))

def DeleteUser(user_id):
  query_db('delete from user_infos where user_id = ?', [user_id])
