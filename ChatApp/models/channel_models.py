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
    def getUserRole(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT role_name FROM users INNER JOIN roles ON users.role_id = roles.id WHERE users.id = %s;"
            cur.execute(sql, (uid,))
            result = cur.fetchone()
            return result['role_name']
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()
            
