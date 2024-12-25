from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# 定義一個 Blueprint，用於管理與文章相關的路由
posts = Blueprint('posts', __name__)

# 路由：新建文章
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    處理創建新文章的請求。
    - 僅已登入用戶可訪問。
    - 支援 GET 方法以顯示表單，POST 方法以提交數據。
    """
    form = PostForm()  # 建立文章表單實例
    if form.validate_on_submit():  # 驗證表單是否通過
        # 建立新文章，將當前用戶設置為作者
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)  # 將文章加入資料庫會話
        db.session.commit()  # 提交變更
        flash('Your post has been created!', 'success')  # 顯示成功訊息
        return redirect(url_for('main.home'))  # 返回主頁
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')  # 渲染新建文章模板

# 路由：查看單篇文章
@posts.route("/post/<int:post_id>")
def post(post_id):
    """
    處理查看特定文章的請求。
    - 根據文章 ID 從資料庫查詢文章。
    - 若找不到文章則返回 404 錯誤。
    """
    post = Post.query.get_or_404(post_id)  # 根據 ID 查詢文章，找不到則拋出 404
    return render_template('post.html', title=post.title, post=post)  # 渲染文章內容模板

# 路由：更新文章
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    處理更新文章的請求。
    - 僅作者本人可更新文章，否則返回 403 錯誤。
    - 支援 GET 方法顯示更新表單，POST 方法提交更新數據。
    """
    post = Post.query.get_or_404(post_id)  # 查詢目標文章
    if post.author != current_user:  # 檢查是否為文章作者
        abort(403)  # 若不是作者，返回 403 錯誤
    form = PostForm(request.form if request.method == 'POST' else None)  # 初始化表單
    if form.validate_on_submit():  # 若表單驗證通過
        post.title = form.title.data  # 更新文章標題
        post.content = form.content.data  # 更新文章內容
        db.session.commit()  # 提交變更
        flash('Your post has been updated!', 'success')  # 顯示成功訊息
        return redirect(url_for('posts.post', post_id=post.id))  # 返回文章詳情頁
    elif request.method == 'GET':  # 若為 GET 請求，將現有數據填充至表單
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  # 渲染更新表單模板

# 路由：刪除文章
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    處理刪除文章的請求。
    - 僅作者本人可刪除文章，否則返回 403 錯誤。
    - 僅支援 POST 方法。
    """
    post = Post.query.get_or_404(post_id)  # 查詢目標文章
    if post.author != current_user:  # 檢查是否為文章作者
        abort(403)  # 若不是作者，返回 403 錯誤
    db.session.delete(post)  # 刪除文章
    db.session.commit()  # 提交變更
    flash('Your post has been deleted!', 'success')  # 顯示成功訊息
    return redirect(url_for('main.home'))  # 返回主頁
