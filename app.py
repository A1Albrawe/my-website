from flask import Flask
from home import home_blueprint
from report import report_blueprint
from admin import admin_blueprint
from api import api_blueprint

# استدعاء حزمة الألعاب والصفحات المستقلة
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

# تسجيل كافة الـ Blueprints في السيرفر المركزي
app.register_blueprint(home_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(api_blueprint)

app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(xo_blueprint)
app.register_blueprint(shooter_blueprint)
app.register_blueprint(clicker_blueprint)

app.register_blueprint(projects_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(scripts_blueprint)
@app.after_request
def inject_global_analytics_tracker(response):
    """
    مُحرك التتبع الشامل والخارق!
    يقوم بفحص أي صفحة يفتحها الزائر (الرئيسية، المشاريع، أو أي لعبة من الألعاب الخمس)
    ويحقن بداخلها كود الرصد وحساب الوقت تلقائياً دون تعديل ملفات الألعاب الأصلية.
    """
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        
        # 📊 كود الجافا سكريبت الشامل الذي سيتم حقنه تلقائياً في متصفح الزائر
        global_tracker_script = """
        <!-- Global Albrawe Tracking System -->
        <script>
            document.addEventListener("DOMContentLoaded", () => {
                // 1. تحديد اسم الزائر أو صناعة اسم فريد له وحفظه
                let storedUser = localStorage.getItem('snake_last_user') || 'زائر_مجهول_' + Math.floor(Math.random() * 900);
                localStorage.setItem('snake_last_user', storedUser);
                
                // 2. إرسال نبضة الدخول الفورية إلى api.py
                fetch('/api/log_visit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: storedUser })
                });
                
                // 3. قراءة المسار الحالي تلقائياً لمعرفة أين يتواجد الزائر الآن (هل هو في لعبة أم صفحة عادية)
                let currentPath = window.location.pathname.replace('/', '') || 'site';
                
                // 4. إرسال نبضة دورية كل 5 ثوانٍ لتحديث عداد الوقت للقسم الحالي حياً في لوحة الإدارة
                setInterval(() => {
                    // التحقق مما إذا كان الزائر يتصفح اللعبة فعلياً (وليس متوقف مؤقتاً في الثعبان أو التترس إن وجد متغير)
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
        
        <!-- Vercel Insights -->
        <script defer src='/_vercel/insights/script.js'></script>
        """
        
        # حقن الكود الشامل تلقائياً في نهاية جسم الصفحة قبل الإغلاق ليعمل في كل مكان
        if "</body>" in text:
            text = text.replace("</body>", f"{global_tracker_script}</body>")
            
        response.set_data(text)
    return response

if __name__ == '__main__':
    app.run(debug=True)
