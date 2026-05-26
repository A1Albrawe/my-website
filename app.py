from flask import Flask, request, session, redirect, render_template_string
from home import home_blueprint
from report import report_blueprint
from admin import admin_blueprint
from api import api_blueprint

# استدعاء باقة الألعاب الخمسة المحدثة والمطورة كلياً من مجلداتها القياسية
from games_package.snake import snake_blueprint
from games_package.tetris import tetris_blueprint
from games_package.xo import xo_blueprint
from games_package.shooter import shooter_blueprint
from games_package.clicker import clicker_blueprint

from projects import projects_blueprint
from about import about_blueprint
from scripts import scripts_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل جميع حزم الـ Blueprints لصفحات وأدوات خادم الخادم المركزي للموقع
app.register_blueprint(home_blueprint)
app.register_blueprint(report_blueprint)

# ✅ تسجيل وتوجيه لوحة المسؤول صراحة إلى نطاقك التكميلي الجديد المحمي
app.register_blueprint(admin_blueprint, url_prefix='/albrawe-admin-panel-2026')

app.register_blueprint(api_blueprint)

# تسجيل ألعاب مجلد باقة الألعاب المحدثة (games_package)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(xo_blueprint)
app.register_blueprint(shooter_blueprint)
app.register_blueprint(clicker_blueprint)

# تسجيل مسارات صفحات جذر الخادم المستقلة لتعديل نصوصها بحرية
app.register_blueprint(projects_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(scripts_blueprint)

@app.after_request
def inject_global_analytics_tracker(response):
    """
    مُحرك الرصد العالمي المطور سيبرانياً!
    يقوم بحقن سكريبت التتبع تلقائياً في المتصفحات، مع حظر تتبع نطاق الإدارة الجديد نهائياً،
    وتثبيت هوية وأسماء الزوار للأبد عبر الذاكرة الصلبة لمنع تصفير الأوقات عند العودة.
    """
    if response.content_type and response.content_type.startswith('text/html'):
        try:
            text = response.get_data(as_text=True)
            
            # 🕵️ جدار الحماية السيبراني: حظر الرصد تماماً إذا كان المسار المفتوح هو النطاق التكميلي الجديد لمنع التداخل والوميض
            if "albrawe-admin-panel-2026" in request.path or "albrawe-admin" in request.path:
                return response
                
            global_tracker_script = """
            <!-- Global Albrawe Persistent Tracking System -->
            <script>
                document.addEventListener("DOMContentLoaded", () => {
                    let storedUser = localStorage.getItem('albrawe_tracker_username');
                    if(!storedUser) {
                        storedUser = 'لاعب_مستمر_' + Math.floor(100 + Math.random() * 900);
                        localStorage.setItem('albrawe_tracker_username', storedUser);
                    }
                    
                    let userLocation = "القاهرة - مصر 🇪🇬";
                    fetch('https://ipapi.co')
                    .then(res => res.json())
                    .then(geo => {
                        if(geo.city && geo.region && geo.country_name) {
                            userLocation = geo.city + "، " + geo.region + " - " + geo.country_name;
                        } else if(geo.city && geo.country_name) {
                            userLocation = geo.city + " - " + geo.country_name;
                        }
                        sendPayloadToServer();
                    })
                    .catch(() => { sendPayloadToServer(); });

                    function sendPayloadToServer() {
                        fetch('/api/log_visit', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({ username: storedUser, location: userLocation })
                        });
                    }
                    
                    let currentPath = window.location.pathname.replace('/', '') || 'site';
                    
                    setInterval(() => {
                        if (typeof isPaused !== 'undefined' && isPaused) return;
                        if (typeof isGameOver !== 'undefined' && isGameOver) return;
                        
                        fetch('/api/update_duration', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({ username: storedUser, game: currentPath })
                        });
                    }, 5000);
                });
            </script>
            <script defer src='/_vercel/insights/script.js'></script>
            """
            if "</body>" in text:
                text = text.replace("</body>", global_tracker_script + "</body>")
            response.set_data(text)
        except Exception:
            pass
    return response

if __name__ == '__main__':
    app.run(debug=True)
