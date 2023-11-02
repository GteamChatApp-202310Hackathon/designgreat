import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
  #Get user info at login.
  def getUser(email):
    try:
      dbconn = DB.getConnection()
      cur = dbconn.cursor()
      sql = "SELECT * FROM users WHERE email=%s"
      cur.execute(sql, (email))
      user = cur.fetchone()
      return user
    except Exception as e:
      print(e + 'が発生しています')
      abort(500)
    finally:
      cur.close()

  #Create user at signin
  def createUser(user_id, name, email, password, teacher_password):
    try:
      conn = DB.getConnection()
      cur = conn.cursor()
      sql = "INSERT INTO users(id, user_name, password, teacher_password, email, role_id) VALUES(%s, %s, %s, %s, %s);"
      cur.execute(sql, (user_id, name, email, password, teacher_password))
      conn.commit()
    except Exception as e:
      print(e + 'が発生しています')
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