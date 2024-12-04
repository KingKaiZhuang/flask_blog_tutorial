import sys
import os

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # 將專案根目錄添加到 sys.path

from flaskblog import app, db
from flaskblog.models import Post

with app.app_context():  # 確保設置應用程序上下文
    # 假設用戶 ID 是 1
    new_post = Post(title='My First Post', content='This is the content of my first post', user_id=1)

    # 暫存新用戶
    db.session.add(new_post)

    # 存入到資料庫
    db.session.commit()

    print("Post added successfully!")
