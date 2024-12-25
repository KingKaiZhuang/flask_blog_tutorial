# 引入 os 模組，用於操作系統環境變數
import os

# 引入 dotenv 用於加載 .env 檔案中的環境變數
from dotenv import load_dotenv

# 加載 .env 檔案中的環境變數
load_dotenv()

# 配置類，用於集中管理應用配置
class Config:
    # 應用的密鑰，用於保持數據安全（例如防範 CSRF 攻擊）
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 資料庫的連接 URI，應從環境變數中獲取
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # 郵件伺服器設置
    MAIL_SERVER = 'smtp.googlemail.com'  # 使用 Google Mail 作為郵件伺服器
    MAIL_PORT = 587  # 郵件伺服器的端口號
    MAIL_USE_TLS = True  # 啟用傳輸層安全協議（TLS）

    # 郵件用戶名和密碼，從環境變數中獲取
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # 郵件伺服器用戶名
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # 郵件伺服器密碼

    # 設置預設的郵件發送者地址
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')
