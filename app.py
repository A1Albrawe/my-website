from flask import Flask, render_template_string
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

app = Flask(__name__)

# مفتاح سري معزول ومحدث كلياً لقفل النواة
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل المسارات والألعاب النشطة فقط
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)

# 🎯 تم تدمير وحذف سطر @app.route('/PASS') وأي دوال متعلقة به نهائياً من قلب السيرفر
handler = app

if __name__ == '__main__':
    app.run()
