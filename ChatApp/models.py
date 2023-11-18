import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    #Get user info at login.
    def getUser(name=None, email=None):
        try:
            dbconn = DB.getConnection()
            cur = dbconn.cursor()
            user = None
            if name:
                sql = "SELECT * FROM users WHERE user_name=%s"
                cur.execute(sql, (name,))
                user = cur.fetchone()
            elif email:
                sql = "SELECT * FROM users WHERE email=%s"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #Create user at signin
    def createUser(user_id, name, email, password, role, teacher_password="None"):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users(id, user_name, password, teacher_password, email,role) VALUES(%s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (user_id, name, password, teacher_password, email, role))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #Get all Channel info.
    def getChannelAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # ユーザーの役割を取得する関数
    def getUserRoleById(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT role FROM users WHERE id = %s;"
            cur.execute(sql, (uid,))
            result = cur.fetchone()
            return result['role']
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # cidからチャンネルの情報を取得する関数            
    def getChannelById(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid,))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # channel_nameからチャンネルの情報を取得する関数        
    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE channel_name=%s;"
            cur.execute(sql, (channel_name,))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # 新しいチャンネルを追加する関数
    def addChannel(uid, newChannelName, newChannelDescription):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (user_id, channel_name, description) VALUES (%s, %s, %s);"
            cur.execute(sql, (uid, newChannelName, newChannelDescription))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # cidを持つチャンネルの情報を更新する関数        
    def updateChannel(uid, newChannelName, newChannelDescription, cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels SET channel_name=%s, description=%s WHERE id=%s;"
            cur.execute(sql, (newChannelName, newChannelDescription, cid))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #チャンネルを削除する関数
    def deleteChannel(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()            

    #Get all posted messages in the channel.
    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            #sql = "SELECT m.id, u.id, m.message FROM messages as m INNER JOIN users AS u ON m.user_id = u.id WHERE channel_id = %s"
            sql = "SELECT * FROM messages WHERE channel_id = %s"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return messages

    #Create Message
    def createMessage(user_id, channel_id, message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(user_id, channel_id, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (user_id, channel_id, message))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #Delete Message
    def deleteMessage(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE id = %s"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #Create pin messages
    def updateMessageForPin(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE messages SET pin_message=true WHERE id = %s"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #Delete pin messages
    def deleteMessageForPin(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE messages SET pin_message=false WHERE id = %s"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            
    # メッセージにリアクションを追加する関数
    def addReaction(user_id, message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            # すでにリアクションがあるかチェック
            cur.execute("SELECT id FROM reactions WHERE user_id = %s AND message_id = %s", (user_id, message_id))
            if cur.fetchone():
                return False  # 既にリアクションがあれば追加しない
            cur.execute("INSERT INTO reactions (user_id, message_id) VALUES (%s, %s)", (user_id, message_id))
            conn.commit()
            return True
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # メッセージのリアクションを削除する関数
    def removeReaction(user_id, message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            cur.execute("DELETE FROM reactions WHERE user_id = %s AND message_id = %s", (user_id, message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # 特定のユーザーが特定のメッセージにリアクションしているかを確認するメソッド
    def hasReaction(user_id, message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM reactions WHERE user_id = %s AND message_id = %s", (user_id, message_id))
            return cur.fetchone() is not None
        except Exception as e:
            print(str(e))
            abort(500)
        finally:
            cur.close()
            
    # メッセージのリアクション数をカウントする関数
    def countReactions(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as count FROM reactions WHERE message_id = %s", (message_id,))
            result = cur.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()