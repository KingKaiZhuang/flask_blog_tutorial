# 引入 flaskblog 應用的創建函數
from flaskblog import create_app

# 創建 Flask 應用實例
app = create_app()

# 如果此腳本是直接執行的主程序
if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    # debug=True 啟用除錯模式，方便開發時追蹤錯誤
    # host='127.0.0.1' 指定伺服器的主機為本機
    # port=5000 指定伺服器運行的埠號為 5000
    app.run(debug=True, host='127.0.0.1', port=5000)
