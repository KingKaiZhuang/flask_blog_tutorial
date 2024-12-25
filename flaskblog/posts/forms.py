from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# 定義一個表單類別，用於處理文章的提交
class PostForm(FlaskForm):
    """
    表單類別，用於用戶創建或編輯文章時提交資料。
    - 使用 Flask-WTF 和 WTForms 模組進行表單處理。
    """
    # 文章標題欄位
    title = StringField(
        'Title',  # 標籤名稱
        validators=[DataRequired()]  # 檢查此欄位是否為必填
    )

    # 文章內容欄位
    content = TextAreaField(
        'Content',  # 標籤名稱
        validators=[DataRequired()]  # 檢查此欄位是否為必填
    )

    # 提交按鈕
    submit = SubmitField('Post')  # 定義提交表單的按鈕，按鈕標籤為 "Post"
