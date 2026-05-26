from flask import Flask
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

# استيراد الحزم (Blueprints) الجديدة التي تم فصلها
from pages import pages_blueprint
from api import api_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل جميع الحزم البرمجية القديمة والجديدة
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(pages_blueprint)
app.register_blueprint(api_blueprint)

@app.after_request
def inject_clean_dropdown_fix(response):
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        response.set_data(text)
    return response

if __name__ == '__main__':
    app.run(debug=True)
