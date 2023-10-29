from flask import Flask
from routes.user_routes import user_routes

app = Flask(__name__)
app.register_blueprint(user_routes, url_prefix='/')

if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True) #開発中はTrue