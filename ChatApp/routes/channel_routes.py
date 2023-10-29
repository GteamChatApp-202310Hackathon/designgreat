from flask import Flask, redirect, render_template, session
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
        user_role = ChannelDB.getUserRole(uid)  # ユーザーの役割を取得
    return render_template('index.html', channels=channels, uid=uid, role=user_role)
