import unittest
from unittest.mock import patch
import hashlib
import sys
import io
import contextlib
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from routes import user_routes 
from flask import session

class LoginRouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = user_routes.app.test_client()
        self.app.testing = True

    @patch("routes.user_routes.UserDB.getUser")
    def test_login_empty_form(self, mock_get_user):
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            response = self.app.post('/login', data={"email": "", "password": ""})
            print("Response data:", response.data.decode())
            output = buf.getvalue()
        #self.assertIn('空のフォームがあるようです', response.data.decode())
        self.assertIn('空のフォームがあるようです', output)

    @patch("routes.user_routes.UserDB.getUser")
    def test_login_nonexistent_user(self, mock_get_user):
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            mock_get_user.return_value = None
            response = self.app.post('/login', data={"email": "test@example.com", "password": "password123"})
            output = buf.getvalue()
        #self.assertIn('このユーザーは存在しません', response.data.decode())
        self.assertIn('このユーザーは存在しません', output)

    @patch("routes.user_routes.UserDB.getUser")
    def test_login_wrong_password(self, mock_get_user):
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            mock_user = {
                "email": "test@example.com",
                "password": "wrong_hashed_password"
            }
            mock_get_user.return_value = mock_user
            response = self.app.post('/login', data={"email": "test@example.com", "password": "password123"})
            output = buf.getvalue()
        #self.assertIn('パスワードが間違っています！', response.data.decode())
        self.assertIn('パスワードが間違っています！', output)

    @patch("routes.user_routes.UserDB.getUser")
    def test_login_successful(self, mock_get_user):
        mock_user = {
            "uid": 123,
            "email": "test@example.com",
            "password": hashlib.sha256("password123".encode('utf-8')).hexdigest()
        }
        mock_get_user.return_value = mock_user
        with self.app:
            response = self.app.post('/login', data={"email": "test@example.com", "password": "password123"})
            self.assertEqual(session["uid"], 123)
            self.assertEqual(response.status_code, 302)  # リダイレクトのHTTPステータスコード

if __name__ == '__main__':
    unittest.main()
