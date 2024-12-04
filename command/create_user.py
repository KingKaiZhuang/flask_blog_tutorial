import sys
import os

# 添加項目根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flaskblog import app, db
from flaskblog.models import User

with app.app_context():
    user_1 = User(username='莊鈞凱', email='pudy6511@gmail.com', password='password')
    db.session.add(user_1)
    db.session.commit()
    print("User added successfully!")
