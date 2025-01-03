import sys
import os

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskblog import app, db
from flaskblog.models import User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"User: {user.username}, Email: {user.email}")
        for post in user.posts:
            print(f"  - Post Title: {post.title}, Content: {post.content}")


    
