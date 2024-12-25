from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

# 用戶註冊表單
class RegistrationForm(FlaskForm):
    """
    用於新用戶註冊的表單，包含用戶名、電子郵件、密碼、確認密碼和提交按鈕。
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # 驗證用戶名是否已被註冊
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已被註冊
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# 用戶登入表單
class LoginForm(FlaskForm):
    """
    用於用戶登入的表單，包含電子郵件、密碼、記住我選項和提交按鈕。
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# 用戶帳戶更新表單
class UpdateAccountForm(FlaskForm):
    """
    用於更新用戶帳戶資訊的表單，包含用戶名、電子郵件、更新頭像的選項和提交按鈕。
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    # 驗證用戶名是否已被其他人使用
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已被其他人使用
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# 密碼重設請求表單
class RequestResetForm(FlaskForm):
    """
    用於提交密碼重設請求的表單，包含電子郵件欄位和提交按鈕。
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # 驗證電子郵件是否存在於資料庫中
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

# 密碼重設表單
class ResetPasswordForm(FlaskForm):
    """
    用於重設密碼的表單，包含密碼、確認密碼和提交按鈕。
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
