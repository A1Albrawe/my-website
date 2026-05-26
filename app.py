from flask import Flask
from home import home_blueprint
from report import report_blueprint
from admin import admin_blueprint
from api import api_blueprint

# استيراد الألعاب من داخل حزمتها الموحدة المخصصة (games_package)
from games_package.snake import snake_blueprint
from games_package.tetris import tetris_blueprint
from games_package.xo import xo_blueprint
from games_package.shooter import shooter_blueprint
from games_package.clicker import clicker_blueprint

# استيراد الصفحات المستقلة من جذر الموقع (Root) مباشرة
from projects import projects_blueprint
from about import about_blueprint
from scripts import scripts_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل جميع حزم الـ Blueprints لصفحات وأدوات خادم الموقع
app.register_blueprint(home_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(api_blueprint)

# تسجيل ألعاب مجلد (games_package)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(xo_blueprint)
app.register_blueprint(shooter_blueprint)
app.register_blueprint(clicker_blueprint)

# تسجيل مسارات صفحات الجذر المستقلة
app.register_blueprint(projects_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(scripts_blueprint)

@app.after_request
def inject_clean_dropdown_fix(response):
    """حقن سكريبت التحليلات لـ Vercel تلقائياً لضمان احتساب الزيارات حياً"""
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        vercel_tracking_script = "<!-- Vercel Web Analytics --><script defer src='/_vercel/insights/script.js'></script>"
        if "</body>" in text:
            text = text.replace("</body>", f"{vercel_tracking_script}</body>")
        response.set_data(text)
    return response

if __name__ == '__main__':
    app.run(debug=True)
