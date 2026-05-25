from flask import Flask
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint
from telegram_bot import tg_bot_blueprint # 1. استيراد ملف البوت الجديد

app = Flask(__name__)

app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(tg_bot_blueprint) # 2. تسجيل مسارات البوت في السيرفر

if __name__ == '__main__':
    app.run()
