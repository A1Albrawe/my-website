from flask import Flask, request, session, redirect, render_template_string
from home import home_blueprint
from report import report_blueprint
from admin import admin_blueprint
from api import api_blueprint

# استدعاء باقة الألعاب الخمسة المحدثة والمطورة كلياً من مجلداتها القياسية
from games_package.snake import snake_blueprint
from games_package.tetris import tetris_blueprint
from games_package.xo import xo_blueprint
from games_package.card_game import card_game_blueprint
from games_package.shooter import shooter_blueprint
from games_package.clicker import clicker_blueprint

from projects import projects_blueprint
from about import about_blueprint
from scripts import scripts_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# 🛡️ خوارزمية الاستدعاء المعزول والمحصن كلياً لمنع انهيار الـ Runtime السحابي لـ Vercel
try:
    app.register_blueprint(home_blueprint)
except Exception:
    pass

try:
    app.register_blueprint(report_blueprint)
except Exception:
    pass

try:
    # تسجيل لوحة المسؤول وتوجيهها الصريح إلى نطاقك التكميلي الجديد المحمي
    app.register_blueprint(admin_blueprint, url_prefix='/albrawe-admin-panel-2026')
except Exception:
    pass

try:
    app.register_blueprint(api_blueprint)
except Exception:
    pass

# استدعاء باقة الألعاب الخمسة المحدثة بشكل محمي معزول تماماً
try: app.register_blueprint(snake_blueprint)
except Exception: pass

try: app.register_blueprint(tetris_blueprint)
except Exception: pass

try: app.register_blueprint(xo_blueprint)
except Exception: pass

try: app.register_blueprint(shooter_blueprint)
except Exception: pass

try: app.register_blueprint(clicker_blueprint)
except Exception: pass

# استدعاء المسارات التكميلية المستقلة
try: app.register_blueprint(projects_blueprint)
except Exception: pass

try: app.register_blueprint(about_blueprint)
except Exception: pass

try: app.register_blueprint(scripts_blueprint)
except Exception: pass
@app.after_request
def inject_global_analytics_tracker(response):
    """
    مُحرك الرصد العالمي المطور سيبرانياً!
    يقوم بحقن سكريبت التتبع تلقائياً في المتصفحات، مع حظر تتبع نطاق الإدارة الجديد نهائياً،
    وتجميع الثواني وإرسالها دفعة واحدة لحماية استقرار السيرفر ومنع الانهيار.
    """
    if response.content_type and response.content_type.startswith('text/html'):
        try:
            text = response.get_data(as_text=True)
            
            # جدار الحماية السيبراني: حظر الرصد تماماً إذا كان المسار المفتوح هو النطاق التكميلي الجديد لمنع التداخل والوميض
            if "albrawe-admin-panel-2026" in request.path or "albrawe-admin" in request.path:
                return response
                
            global_tracker_script = """
            <!-- Global Albrawe Optimized Tracking System -->
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
                    let localDuration = 0;
                    
                    setInterval(() => {
                        if (typeof isPaused !== 'undefined' && isPaused) return;
                        if (typeof isGameOver !== 'undefined' && isGameOver) return;
                        localDuration += 5;
                    }, 5000);
                    
                    window.addEventListener("beforeunload", () => {
                        if (localDuration > 0) {
                            navigator.sendBeacon('/api/update_duration', JSON.stringify({ 
                                username: storedUser, 
                                game: currentPath,
                                durationIncrement: localDuration
                            }));
                        }
                    });
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
