from flask import Flask
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint # استدعاء الملف المدمج والجاهز
from admin import admin_blueprint

app = Flask(__name__)

app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint) # تسجيل مسارات التقرير والبوت المدمجة
app.register_blueprint(admin_blueprint)

handler = app

if __name__ == '__main__':
    app.run()
