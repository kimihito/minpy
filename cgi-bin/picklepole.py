#!/usr/bin/env python
# coding: utf-8

import pickle
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()

form_body = u"""
  <form method="POST" action="/cgi-bin/picklepole.py">
    好きな軽量言語は？<br />
    %s
    <input type="submit" />
  </form>"""

radio_parts=u"""
<input type="radio" name="language" value=""%s />%s
<div style="border-left: solid %sem red; ">%s</div>
"""
#1
lang_dic=()
try:
  f=open('./favorite_language.dat')
  lang_dic=pickle.load(f)
  #1
except IOError:
  pass

content=""
req=Request()
if req.form.has_key('language'):
  lang=req.form['language'].value
  lang_dic[lang]=lang_dic.get(lang, 0)+1
#2
f=open('./favorite_language.dat','w')
pickle.dump(lang_dic, f)
#2
#3
for lang in ['Perl', 'PHP', 'Python', 'Ruby']:
  num=lang_dic.get(lang,0)
  content+=radio_parts%(lang,lang,num,num)
#3
res = Response()
body=form_body%content
res.set_body(get_htmltemplate()%body)
print res
