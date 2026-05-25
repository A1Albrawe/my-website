from flask import Flask, render_template_string
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

app = Flask(__name__)

# مفتاح سري معزول كلياً لتثبيت أمان النواة بعد الإغلاق
app.secret_key = "ALBRAWE_LOCKED_SECURITY_2026"

# تسجيل المسارات والألعاب الأساسية للموقع فقط
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)

# 🎯 تم تدمير وحذف مسار الـ /PASS والـ Admin APIs نهائياً لقطع الوصول تماماً
handler = app

if __name__ == '__main__':
    app.run()
