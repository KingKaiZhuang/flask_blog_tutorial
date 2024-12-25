from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# 定義一個 Blueprint，處理與用戶相關的路由
users = Blueprint('users', __name__)

# 用戶註冊路由
@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    處理用戶註冊的邏輯。
    如果用戶已經登入，重定向到主頁。
    如果表單提交並驗證通過，創建新用戶並存入資料庫。
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# 用戶登入路由
@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    處理用戶登入的邏輯。
    如果用戶已經登入，重定向到主頁。
    如果表單提交並驗證通過，檢查用戶憑證並登入。
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# 用戶登出路由
@users.route("/logout")
def logout():
    """
    處理用戶登出的邏輯，重定向到主頁。
    """
    logout_user()
    return redirect(url_for('main.home'))

# 用戶帳戶管理路由
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    處理用戶帳戶更新的邏輯。
    如果表單提交並驗證通過，更新用戶資料（包括頭像）。
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# 用戶文章列表路由
@users.route("/user/<string:username>")
def user_posts(username):
    """
    顯示指定用戶的文章列表，支援分頁功能。
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

# 密碼重設請求路由
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    處理密碼重設請求的邏輯。
    如果用戶已經登入，重定向到主頁。
    如果表單提交並驗證通過，向用戶發送密碼重設郵件。
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# 密碼重設處理路由
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    處理密碼重設邏輯。
    驗證 token 是否有效，並允許用戶重設密碼。
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
