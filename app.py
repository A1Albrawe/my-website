from flask import Flask, render_template_string
import vercel_analytics  # 1. استيراد مكتبة التحليلات الرسمية

# استيراد الصفحات والألعاب الجاهزة بمشروعك
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

app = Flask(__name__)

# 2. تفعيل خطاف التتبع البرمجي التلقائي داخل السيرفر السحابي
vercel_analytics.init(app)

# مفتاح سري معزول كلياً لتثبيت أمان النواة
app.secret_key = "ALBRAWE_LOCKED_SECURITY_2026"

# تسجيل المسارات والألعاب الأساسية للموقع
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)

handler = app

if __name__ == '__main__':
    app.run()
