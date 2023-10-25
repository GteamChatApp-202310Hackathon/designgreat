from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import UserDB

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

#Display login page
@app.route('/login')
def signup():
  return render_template('hoge')

#Process login
@app.route('/login', methods=['POST'])
def userLogin():
  email = request.form.get('email')
  password = request.form.get('password')

  if email == '' or password == '':
    #flash('空のフォームがあるようです')
    print('空のフォームがあるようです')
  else:
    user = UserDB.getUser(email)
    if user is None:
      #flash('このユーザーは存在しません')
      print('このユーザーは存在しません')
    else:
      hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
      if hashPassword != user["password"]:
        #flash('パスワードが間違っています！')
        print('パスワードが間違っています！')
      else:
        session['uid'] = user["uid"]
        return redirect('/')
  return redirect('/login')

#Logout
@app.route('/login')
def logout():
  session.clear()
  return redirect('/login')