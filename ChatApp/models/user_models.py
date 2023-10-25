import pymysql
from util.DB import DB
from flask import abort

class UserDB:
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