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
    flash('空のフォームがあるようです')
  else:
    user = UserDB.getUser(email)
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if (user is None) or (hashPassword != user["password"]):
      flash('ユーザー名もしくはパスワードが間違っています')
    else:
      session['user_id'] = user["user_id"]
      return redirect('/')
  return redirect('/login')

#Logout
@app.route('/login')
def logout():
  session.clear()
  return redirect('/login')
