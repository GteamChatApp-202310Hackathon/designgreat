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
    def createUser(user_id, name, email, password, teacher_password="None"):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users(id, user_name, password, teacher_password, email) VALUES(%s, %s, %s, %s, %s);"
            cur.execute(sql, (user_id, name, password, teacher_password, email))
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
            sql = "SELECT role_name FROM roles INNER JOIN users ON roles.id = users.role_id WHERE users.id = %s;"
            cur.execute(sql, (uid,))
            result = cur.fetchone()
            return result['role_name']
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
            sql = "DELETE FROM messages WHERE message_id = %s"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    #
    def updateMessageForPin(message_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE messages SET role=true WHERE message_id = %s"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()