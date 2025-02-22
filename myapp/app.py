from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import init_routes
from models import db  # ここで models.py から db をインポート

def create_app():
    """ Flaskアプリケーションの初期化関数 """
    app = Flask(__name__)

    # 設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    # FlaskアプリとSQLAlchemyをリンク
    db.init_app(app)

    # ルートの初期化
    init_routes(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # データベースを作成
    app.run(debug=True)

