import pymysql
from util.DB import DB
from flask import abort

class ChannelDB:

    # すべてのチャンネル情報を取得する関数
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
            
