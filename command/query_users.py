import sys
import os

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# query_users.py
from flaskblog import app, db, User, Post

with app.app_context():
    post_1 = Post(title='Blog Post 1', content='First post content', user_id=1)
    post_2 = Post(title='Blog Post 2', content='Second post content', user_id=1)
    db.session.add(post_1)
    db.session.add(post_2)
    db.session.commit()
    print("Posts added successfully!")
    user = User.query.filter_by(username='Corey').first()
    print(user.posts)
    
