# manage.py
from flaskblog import app, db, User

with app.app_context():
    user_2 = User(username='JohnDoe', email='J@demo.com', password='password')
    db.session.add(user_2)
    db.session.commit()
    print("User added successfully!")
