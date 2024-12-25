import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# 保存用戶上傳的頭像圖片
def save_picture(form_picture):
    """
    接收上傳的圖片文件，生成隨機文件名並壓縮圖片，保存到服務器的 'static/profile_pics' 目錄。
    :param form_picture: 上傳的圖片文件
    :return: 圖片的文件名
    """
    # 生成隨機文件名，避免文件名衝突
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # 分離文件名與擴展名
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # 調整圖片大小
    output_size = (125, 125)
    i = Image.open(form_picture)  # 使用 PIL 打開圖片
    i.thumbnail(output_size)  # 調整到指定尺寸
    i.save(picture_path)  # 保存圖片到目標路徑

    return picture_fn  # 返回新圖片的文件名

# 發送密碼重設郵件
def send_reset_email(user):
    """
    為用戶發送密碼重設的電子郵件，其中包含一個唯一的重設連結。
    :param user: 發送重設郵件的用戶對象
    """
    token = user.get_reset_token()  # 獲取用戶的重設 token
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',  # 發件人地址
                  recipients=[user.email])  # 收件人地址

    # 電子郵件正文，包含重設密碼的連結
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''

    # 發送郵件
    mail.send(msg)
