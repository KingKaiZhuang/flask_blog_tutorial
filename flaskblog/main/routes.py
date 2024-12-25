from flask import render_template, request, Blueprint
from flaskblog.models import Post  # 導入 Post 模型，用於查詢資料庫中的文章

# 建立一個 Blueprint，命名為 'main'，用於處理主要的應用路由
main = Blueprint('main', __name__)

# 定義首頁路由
@main.route("/")
@main.route("/home")
def home():
    """
    處理首頁的請求，顯示最新的文章列表，支持分頁功能。
    - 路徑："/" 或 "/home"
    - 預設每頁顯示 5 篇文章
    - 分頁參數從 URL 的 'page' 查詢字串中獲取（預設為第 1 頁）
    """
    # 獲取當前頁數，若無參數則預設為第 1 頁
    page = request.args.get('page', 1, type=int)
    
    # 從資料庫中查詢文章，按發佈日期降序排列，並進行分頁
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    # 渲染 'home.html' 模板，並將查詢結果傳遞到模板
    return render_template('home.html', posts=posts)

# 定義關於頁面的路由
@main.route("/about")
def about():
    """
    處理關於頁面的請求，顯示關於網站或開發者的資訊。
    - 路徑："/about"
    """
    # 渲染 'about.html' 模板，並設定標題為 'About'
    return render_template('about.html', title='About')
