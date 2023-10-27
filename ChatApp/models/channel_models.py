import pymysql
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from flask import abort
from util.DB import DB

class dbConnect:

    # すべてのチャンネル情報を取得する関数
    @staticmethod
    def getChannelAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor(pymysql.cursors.DictCursor)  # 結果を辞書形式で取得
            sql = "SELECT * FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # ユーザーの役割を取得する関数
    @staticmethod
    def getUserRoleById(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT role_name FROM roles INNER JOIN users ON users.role_id = roles.id WHERE users.id = %s;"
            cur.execute(sql, (uid,))
            result = cur.fetchone()

            # 追加: 結果がNoneかどうかの確認
            if result is None:
                print(f"ユーザーID {uid} に関連する役割が見つかりませんでした。")
                return None
            
            return result['role_name']
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


if __name__ == "__main__":
    # テスト用コード
    channels = dbConnect.getChannelAll()
    print("Channels:", channels)

    # ユーザーIDを元に役割を取得（例：ユーザーID=970af84c-dd40-47ff-af23-282b72b7cca8）
    user_role = dbConnect.getUserRoleById("970af84c-dd40-47ff-af23-282b72b7cca8")
    if user_role is not None:
        print("User Role:", user_role)
    else:
        print("User Role not found for the given ID.")