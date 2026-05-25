from flask import Flask
# استيراد الصفحات والألعاب من الملفات المنفصلة بدقة تامة
from home import home_blueprint
from snake import snake_blueprint
from report import report_blueprint
from telegram_bot import tg_bot_blueprint

app = Flask(__name__)

# تسجيل الصفحات في الخادم الرئيسي وتثبيت مسارات التوجيه بأمان
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(tg_bot_blueprint)

# 🎯 الصياغة المعمارية الصحيحة المعتمدة رسمياً من Vercel للربط السحابي (WSGI Handler)
handler = app

if __name__ == '__main__':
    app.run()
