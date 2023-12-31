from flask import Flask, request, redirect, render_template, session, flash
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
TEACHER_PASSWORD = "teacher"  # Temporary teacher password.　Plans to move to environment variables.

#Display login page
@app.route('/login')
def login():
  return render_template('registration/login.html')

#Hashing passwords whith SHA-256
def hash_password(password):
  return hashlib.sha256(password.encode('utf-8')).hexdigest()

#Process login
@app.route('/login', methods=['POST'])
def user_login():
  name = request.form.get('name')
  password = request.form.get('password1')

  if not name or not password:
    flash('空のフォームがあるようです')
    return redirect('/login')
  
  user = dbConnect.getUser(name)
  hashed_password = hash_password(password)

  if user is None or hashed_password != user["password"]:
    flash('ユーザー名またはパスワードが間違っています')
    return redirect('/login')
  
  session['user_id'] = user["id"]
  return redirect('/')

#Logout
@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')

#Display Signup Page
@app.route('/signup')
def signup():
  return render_template('registration/signup.html')

#Validating signup input
def validate_signup_input(name, email, password1, password2, teacher_password, not_teacher):
  errors = {}
  if not all([name, email, password1, password2]):
    errors['empty'] = '入力されていない項目があります'
  if len(password1) < 10:
    errors['password_length'] = 'パスワードは10文字以上で入力してください'
  if password1 != password2:
    errors['password_missmatch'] = 'パスワードが一致しません'
  if re.match(EMAIL_PATTERN, email) is None:
    errors['email_injustice'] = '正しいメールアドレスの形式ではありません'
  if dbConnect.getUser(email=email) is not None:
    errors['email_exist'] = '既に登録されたメールアドレスです'
  if dbConnect.getUser(name=name) is not None:
    errors['name_exist'] = '既に登録されたユーザー名です'
  if not not_teacher and teacher_password != TEACHER_PASSWORD:
    errors['teacher_injustice'] = ('不正な教員パスワードです')
  return errors

#Process signup
@app.route('/signup', methods=['POST'])
def user_signup():
  name = request.form.get('name')
  email = request.form.get('email')
  password1 = request.form.get('password1')
  password2 = request.form.get('password2')
  teacher_password = request.form.get('teacherspassword')
  not_teacher = not teacher_password
  if request.form.get('teacherspassword') == 'teacher':
    role = True
  else:
    role = False

  error_messages = validate_signup_input(name, email, password1, password2, teacher_password, not_teacher)
  if error_messages:
    return render_template('registration/signup.html', error_messages=error_messages)
  
  user_id = str(uuid.uuid4())
  hashed_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
  dbConnect.createUser(user_id, name, email, hashed_password, role, teacher_password)
  session['user_id'] = user_id
  return redirect('/')

# チャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("user_id")
    if uid is None:
        return redirect('/login')
    
    channels = dbConnect.getChannelAll()
    channels.reverse()
    user_role = dbConnect.getUserRoleById(uid)
    print(user_role)  # ユーザーの役割を取得

    # ユーザーの役割に基づいてテンプレートに渡す変数を設定
    return render_template('index.html', channels=channels, uid=uid, user_role=user_role)

# チャンネルの追加
@app.route('/', methods=['POST'])
def add_channel():
    uid = session.get("user_id")
    if uid is None or dbConnect.getUserRoleById(uid) != True:
        return redirect('/login')
    channel_name = request.form.get('channelTitle')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        dbConnect.addChannel(uid, channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

# チャンネルの更新
@app.route('/update_channel', methods=['POST'])
def update_channel():
    uid = session.get("user_id")
    if uid is None or dbConnect.getUserRoleById(uid) != True:
        return redirect('/login')

    cid = request.form.get('cid')
    channel_name = request.form.get('channelTitle')
    channel_description = request.form.get('channelDescription')

    # チャンネル名が既に存在するかどうかを確認
    existing_channel = dbConnect.getChannelByName(channel_name)
    # existing_channelが辞書を返すため、idを取得するにはキーを使用する
    if existing_channel and str(existing_channel['id']) != cid:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

    dbConnect.updateChannel(uid, channel_name, channel_description, cid)
    return redirect('/detail/{cid}'.format(cid = cid))

# チャンネル詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session['user_id']
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    user_role = dbConnect.getUserRoleById(uid)

    return render_template('detail.html', messages=messages, channel=channel, uid=uid, user_role=user_role)

# チャンネルの削除
@app.route('/delete/<int:cid>')
def delete_channel(cid):
    uid = session.get("user_id")
    if uid is None:
        return redirect('/login') 
    role = dbConnect.getUserRoleById(uid)
    if not role:
        flash('チャンネルは教員のみ削除可能です')
        return redirect('/')
    
    dbConnect.deleteChannel(cid)
    return redirect('/')
  
#Create Message
@app.route('/message', methods=["POST"])
def add_message():
    user_id = session['user_id']
    if user_id is None:
      return redirect('/login')
    
    message = request.form.get('message')
    channel_id = request.form.get('cid')

    if message:
      dbConnect.createMessage(user_id, channel_id, message)
    
    return redirect('/detail/{channel_id}'.format(channel_id = channel_id ))

#Delete Message
@app.route('/delete_message', methods=['POST'])
def delete_message():
  user_id = session.get("user_id")
  if user_id is None:
    return redirect('/login')
  
  message_id = request.form.get('message_id')
  channel_id = request.form.get('cid')

  if message_id:
    dbConnect.deleteMessage(message_id)
  
  return redirect('/detail/{channel_id}'.format(channel_id = channel_id))

#Update message for pin
@app.route('/pin_message', methods=['POST'])
def pin_message():
  user_id = session["user_id"]
  if user_id is None:
    return redirect('/login')
  
  message_id = request.form.get('message_id')
  channel_id = request.form.get('cid')

  if message_id:
    print(dbConnect.getPinMessages(channel_id))
    if dbConnect.getPinMessages(channel_id):
      flash('ピン留めされたメッセージが存在します。', 'pin_error')
    else:
      print("notsuc")
      dbConnect.updateMessageForPin(message_id)

  return redirect('/detail/{channel_id}'.format(channel_id = channel_id))


#Delete pin message
@app.route('/delete_pin_message', methods=['POST'])
def delete_pin_message():
  user_id = session["user_id"]
  if user_id is None:
    return redirect('/login')
  
  message_id = request.form.get('message_id')
  channel_id = request.form.get('cid')

  if message_id:
    dbConnect.deleteMessageForPin(message_id)
  
  return redirect('/detail/{channel_id}'.format(channel_id = channel_id))

#リアクションの追加または削除
@app.route('/reaction_message', methods=['POST'])
def reaction_message():
    user_id = session["user_id"]
    if user_id is None:
        return redirect('/login')
    
    message_id = request.form.get('message_id')
    channel_id = request.form.get('cid')

    # ユーザーが既にリアクションしているかどうかを確認
    if dbConnect.hasReaction(user_id, message_id):
        # リアクションが存在する場合、それを削除
        dbConnect.removeReaction(user_id, message_id)
    else:
        # リアクションが存在しない場合、新しいリアクションを追加
        dbConnect.addReaction(user_id, message_id)
    
    return redirect('/detail/{channel_id}'.format(channel_id = channel_id))

#Display 404 error page
@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'),404

#Display 500 error page
@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)