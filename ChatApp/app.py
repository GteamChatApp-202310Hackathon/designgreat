from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

#Constant definition
EMAIL_PATTERN = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
TEACHER_PASSWORD = "secret_teacher_password"  # Temporary teacher password

#Display login page
@app.route('/login')
def signup():
  return render_template('hoge')

#Hashing passwords whith SHA-256
def hash_password(password):
  return hashlib.sha256(password.encode('utf-8')).hexdigest()

#Process login
@app.route('/login', methods=['POST'])
def user_login():
  email = request.form.get('email')
  password = request.form.get('password')

  if not email or not password:
    flash('空のフォームがあるようです')
    return redirect('/login')
  
  user = dbConnect.getUser(email)
  hashed_password = hash_password(password)

  if user is None or hashed_password != user["password"]:
    flash('メールアドレスまたはパスワードが間違っています')
    return redirect('/login')
  
  session['user_id'] = user["user_id"]
  return redirect('/')

#Logout
@app.route('/login')
def logout():
  session.clear()
  return redirect('/login')

#Display Signup Page
@app.route('/signup')
def signup():
  return render_template('registration/signup.html')

#Validating signup input
def validate_signup_input(name, email, password1, password2, teacher_password, is_teacher):
  errors = {}
  if not all([name, email, password1, password2]):
    errors['empty'] = '入力されていない項目があります'
  if password1 != password2:
    errors['password_missmatch'] = 'パスワードが一致しません'
  if re.match(EMAIL_PATTERN, email) is None:
    errors['email_injustice'] = '正しいメールアドレスの形式ではありません'
  if dbConnect.getUser(email) is not None:
    errors['email_exist'] = '既に登録されたメールアドレスです'
  if is_teacher and teacher_password != TEACHER_PASSWORD:
    errors['teacher_injustice'] = ('不正な教員パスワードです')
  return errors

#Process signup
@app.route('/signup', methods=['POST'])
def user_signup():
  name = request.form.get('name')
  email = request.form.get('email')
  password1 = request.form.get('password1')
  password2 = request.form.get('password2')
  teacher_password = request.form.get('teacher_password')
  is_teacher = 'teacher' in request.form #教員チェックボックスがチャックされているか

  error_messages = validate_signup_input(name, email, password1, password2, teacher_password, is_teacher)
  if error_messages:
    return render_template('signup.html', error_messages=error_messages)
  
  user_id = str(uuid.uuid4())
  hashed_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
  dbConnect.createUser(user_id, name, email, hashed_password)
  session['user_id'] = user_id
  return redirect('/')

# チャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll()
        channels.reverse()
        user_role = dbConnect.getUserRole(uid)  # ユーザーの役割を取得
    return render_template('index.html', channels=channels, uid=uid, role=user_role)


#Display 404 error page
@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'),404

#Display 500 error page
@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=False)