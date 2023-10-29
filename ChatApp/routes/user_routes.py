from flask import request, redirect, render_template, session, flash, Blueprint
import hashlib

from models import UserDB

user_routes = Blueprint('user_routes', __name__)


#Display login page
@user_routes.route('/login')
def signup():
  return render_template('hoge')

#Process login
@user_routes.route('/login', methods=['POST'])
def userLogin():
  email = request.form.get('email')
  password = request.form.get('password')

  if not email or not password:
    flash('空のフォームがあるようです')
    return redirect('/login')
  
  user = UserDB.getUser(email)
  hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

  if user is None or hashed_password != user["password"]:
    flash('メールアドレスまたはパスワードが間違っています')
    return redirect('/login')
  
  session['user_id'] = user["user_id"]
  return redirect('/')

#Logout
@user_routes.route('/login')
def logout():
  session.clear()
  return redirect('/login')
