from flask import Flask, redirect, render_template, session, request
from datetime import timedelta
import uuid

from models import ChannelDB

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# チャンネル一覧ページの表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = ChannelDB.getChannelAll()
        channels.reverse()
        user_role = ChannelDB.getUserRoleById(uid)  # ユーザーの役割を取得
    return render_template('index.html', channels=channels, uid=uid, role=user_role)


# チャンネルの追加
@app.route('/', methods=['POST'])
def add_channel():
    uid = session.get("uid")
    if uid is None or ChannelDB.getUserRoleById(uid) != 'teacher':
        return redirect('/login')
    channel_name = request.form.get('channelTitle')
    channel = ChannelDB.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        ChannelDB.addChannel(uid, channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)


# チャンネルの更新
@app.route('/update_channel', methods=['POST'])
def update_channel():
    uid = session.get("uid")
    if uid is None or ChannelDB.getUserRoleById(uid) != 'teacher':
        return redirect('/login')

    cid = request.form.get('cid')
    channel_name = request.form.get('channelTitle')
    channel_description = request.form.get('channelDescription')

    ChannelDB.updateChannel(uid, channel_name, channel_description, cid)
    return redirect('/detail/{cid}'.format(cid = cid))


# チャンネル詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = ChannelDB.getChannelById(cid)
  # messages = ChannelDB.getMessageAll(cid)

    return render_template('detail.html', channel=channel, uid=uid)
  # return render_template('detail.html', messages=messages, channel=channel, uid=uid)
  
  
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
