#!/usr/bin/env python
#coding:utf-8

import sqlite3
from string import Template
from os import path
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()

con=sqlite3.connect('./bookmark.dat')
cur=con.cursor()
try:
  cur.execute("""CREATE TABLE bookmark(
                  title text, url text);""")
except:
  pass

req=Request()
f=req.form
value_dic={'message':'', 'title':'', 'url':'', 'bookmarks':''}


if f.has_key('post'):
  if not f.getvalue('title','') or not f.getvalue('url',''):
    value_dic['message']=u'タイトルとURLは必須項目です'
    value_dic['title']=unicode(f.getvalue(
                        'title', ''), 'utf-8', 'ignore')
    value_dic['url']=f.getvalue('url','')
  else:
    cur.execute(
        """INSERT INTO bookmark(title, url) VALUES(?,?)""",
        (f.getvalue('title',''), f.getvalue('url','')))
    con.commit()
cur.execute("SELECT title, url FROM bookmark")
value_dic['bookmarks']=tuple(cur.fetchall())

res=Response()
p=path.join(path,dirname(__file__), 'stbookmarkform.html')
t=SimpleTemplate(file_path=p)
body=t.render(value_dic)

res.set_body(body)
print res
