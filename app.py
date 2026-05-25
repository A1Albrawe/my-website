from flask import Flask
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint
from admin import admin_blueprint # استيراد نظام الرقابة والتحليلات المحمية

app = Flask(__name__)

# مفتاح التشفير السري الإلزامي لتأمين جلسات الباسورد ومنع تزوير الاختراق
app.secret_key = "ALBRAWE_CYBER_KEY_SECURITY_2026"

app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(admin_blueprint) # تسجيل لوحة البيانات في السيرفر

handler = app

if __name__ == '__main__':
    app.run()
