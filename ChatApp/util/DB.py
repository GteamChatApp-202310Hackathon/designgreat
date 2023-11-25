import pymysql

class DB:
  def getConnection():
    try:
      conn = pymysql.connect(
        host="db-designgreat.c8aw7zh7sgmb.ap-northeast-1.rds.amazonaws.com",
        db="designgreat",
        user="designgreat",
        password="saturday21",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
      )
      return conn
    except (ConnectionError):
        print("コネクションエラーです")
        conn.close()
