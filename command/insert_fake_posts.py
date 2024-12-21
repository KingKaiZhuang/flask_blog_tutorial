import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskblog import app, db
from flaskblog.models import User, Post

def insert_fake_posts():
    with app.app_context():
        user = User.query.first()
        if not user:
            print("No user found. Creating a test user...")
            user = User(username="TestUser", email="testuser@example.com", password="password123")
            db.session.add(user)
            db.session.commit()

        fake_posts = [
            {"title": f"Post Title {i+1}", "content": f"This is the content of fake post number {i+1}. Enjoy!"}
            for i in range(30)
        ]

        for post_data in fake_posts:
            if Post.query.filter_by(title=post_data["title"]).first():
                print(f"Post '{post_data['title']}' already exists. Skipping...")
                continue
            post = Post(title=post_data["title"], content=post_data["content"], author=user)
            db.session.add(post)

        db.session.commit()
        print("30 fake posts added!")

if __name__ == "__main__":
    insert_fake_posts()
