from flask import Flask
# استيراد كافة الصفحات والألعاب ولوحة التحكم السرية بدقة تامة
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint
from admin import admin_blueprint # تم استيراد لوحة التحكم بنجاح

app = Flask(__name__)

# تسجيل المسارات البرمجية في الخادم ليفهم الروابط التوجيهية الحية
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(admin_blueprint) # تم تفعيل وتسجيل الرابط السري في السيرفر الآمن

# الصياغة القياسية الصحيحة المعتمدة رسمياً من Vercel للبث المباشر
handler = app

if __name__ == '__main__':
    app.run()
