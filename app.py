from flask import Flask
# استيراد كافة المسارات والألعاب من الملفات المنفصلة بشكل دقيق
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint
from telegram_bot import tg_bot_blueprint

app = Flask(__name__)

# تسجيل كافة الصفحات في الخادم الرئيسي لتعمل بالتوازي
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(tg_bot_blueprint)

# التعريف السليم المعتمد من منصة Vercel للبث المباشر
handler = app

if __name__ == '__main__':
    app.run()
