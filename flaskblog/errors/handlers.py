from flask import Blueprint, render_template

# 建立一個 Blueprint，命名為 'errors'，用於處理錯誤頁面的邏輯
# Blueprint 是 Flask 用於模組化應用程式的工具
errors = Blueprint('errors', __name__)

# 設置 404 錯誤處理器
@errors.app_errorhandler(404)
def error_404(error):
    """
    當用戶請求的資源不存在時，返回自定義的 404 錯誤頁面。
    :param error: 發生的錯誤物件
    :return: 404.html 模板與 HTTP 狀態碼 404
    """
    return render_template('errors/404.html'), 404

# 設置 403 錯誤處理器
@errors.app_errorhandler(403)
def error_403(error):
    """
    當用戶嘗試訪問沒有權限的資源時，返回自定義的 403 錯誤頁面。
    :param error: 發生的錯誤物件
    :return: 403.html 模板與 HTTP 狀態碼 403
    """
    return render_template('errors/403.html'), 403

# 設置 500 錯誤處理器
@errors.app_errorhandler(500)
def error_500(error):
    """
    當伺服器內部出現錯誤時，返回自定義的 500 錯誤頁面。
    :param error: 發生的錯誤物件
    :return: 500.html 模板與 HTTP 狀態碼 500
    """
    return render_template('errors/500.html'), 500
