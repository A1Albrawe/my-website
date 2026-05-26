from flask import Flask
from home import home_blueprint
from report import report_blueprint
from admin import admin_blueprint
from api import api_blueprint

# 🎯 استيراد الألعاب حصرياً من داخل حزمتها الموحدة (games_package)
from games_package.snake import snake_blueprint
from games_package.tetris import tetris_blueprint
from games_package.xo import xo_blueprint
from games_package.shooter import shooter_blueprint
from games_package.clicker import clicker_blueprint

# 📂 استيراد بقية الصفحات مباشرة ومن نفس مكانها الحالي في جذر الموقع (Root)
from projects import projects_blueprint
from about import about_blueprint
from scripts import scripts_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل جميع الحزم والواجهات بالسيرفر
app.register_blueprint(home_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(api_blueprint)

# تسجيل مسارات الألعاب المجمعة
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(xo_blueprint)
app.register_blueprint(shooter_blueprint)
app.register_blueprint(clicker_blueprint)

# تسجيل مسارات صفحات الجذر الثابتة والمستقلة
app.register_blueprint(projects_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(scripts_blueprint)

@app.after_request
def inject_clean_dropdown_fix(response):
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        vercel_tracking_script = "<!-- Vercel Web Analytics --><script defer src='/_vercel/insights/script.js'></script>"
        if "</body>" in text:
            text = text.replace("</body>", f"{vercel_tracking_script}</body>")
        response.set_data(text)
    return response

if __name__ == '__main__':
    app.run(debug=True)
