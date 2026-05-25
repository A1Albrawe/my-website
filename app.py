from flask import Flask
# استيراد الصفحات والألعاب الموجودة والجاهزة فقط داخل المستودع حالياً
from home import home_blueprint
from snake import snake_blueprint
from report import report_blueprint
from telegram_bot import tg_bot_blueprint

app = Flask(__name__)

# تسجيل المسارات الفعالة برمجياً بأمان
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(tg_bot_blueprint)

# الصياغة القياسية الصحيحة التي تطلبها خوادم Vercel للنهوض تلقائياً
handler = app

if __name__ == '__main__':
    app.run()
