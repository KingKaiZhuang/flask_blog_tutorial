from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flaskblog import db, login_manager, app
from flask_login import UserMixin

# 登入用戶的加載函數
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login 用戶加載回調函數。
    根據用戶 ID 查詢資料庫，返回對應的用戶。
    """
    return User.query.get(int(user_id))

# 用戶模型
class User(db.Model, UserMixin):
    """
    用戶表模型，包含用戶基本信息和與文章的關聯。
    """
    id = db.Column(db.Integer, primary_key=True)  # 用戶唯一 ID
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件
    image_file = db.Column(db.String(20), unique=False, default='default.jpg')  # 頭像文件名
    password = db.Column(db.String(60), nullable=False)  # 加密密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 與文章的關聯

    def get_reset_token(self, expires_sec=1800):
        """
        為用戶生成密碼重設 token。
        :param expires_sec: Token 的有效期（秒）
        :return: 加密的 token 字符串
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': self.id})
        return token.decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        驗證密碼重設 token 的有效性。
        :param token: 待驗證的 token
        :return: 對應的用戶對象，或 None 如果 token 無效
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """
        返回用戶對象的字符串表示，用於調試。
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 文章模型
class Post(db.Model):
    """
    文章表模型，包含文章標題、內容、發佈日期和作者。
    """
    id = db.Column(db.Integer, primary_key=True)  # 文章唯一 ID
    title = db.Column(db.String(100), nullable=False)  # 文章標題
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期
    content = db.Column(db.Text, nullable=False)  # 文章內容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 作者 ID（外鍵）

    def __repr__(self):
        """
        返回文章對象的字符串表示，用於調試。
        """
        return f"Post('{self.title}', '{self.date_posted}')"
