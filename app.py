from flask import Flask, render_template_string, request, jsonify, session, redirect
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint
from menu import generate_sidebar_html # استدعاء القائمة الجانبية الموحدة

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)

# 🌐 قاعدة البيانات السحابية المركزية الموحدة للشكاوى والتحليلات
CLOUD_REPORTS_DB = []
CLOUD_ANALYTICS_DB = []

@app.route('/api/cloud_submit_report', methods=['POST'])
def cloud_submit_report():
    global CLOUD_REPORTS_DB
    data = request.get_json() or {}
    CLOUD_REPORTS_DB.insert(0, {
        "id": data.get("id"), "user": data.get("user"),
        "details": data.get("details"), "date": data.get("date")
    })
    CLOUD_REPORTS_DB = CLOUD_REPORTS_DB[:100]
    return jsonify({"status": "success"})

@app.route('/api/cloud_submit_analytics', methods=['POST'])
def cloud_submit_analytics():
    global CLOUD_ANALYTICS_DB
    data = request.get_json() or {}
    CLOUD_ANALYTICS_DB.insert(0, {
        "username": data.get("username"), "userAgent": data.get("userAgent"),
        "loginTime": data.get("loginTime"), "duration": data.get("duration"),
        "snakeTime": data.get("snakeTime"), "tetrisTime": data.get("tetrisTime")
    })
    CLOUD_ANALYTICS_DB = CLOUD_ANALYTICS_DB[:50]
    return jsonify({"status": "success"})

@app.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    if not session.get('admin_logged_in'): return jsonify({"status": "unauthorized"}), 401
    return jsonify({"reports": CLOUD_REPORTS_DB, "analytics": CLOUD_ANALYTICS_DB})

@app.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    global CLOUD_REPORTS_DB, CLOUD_ANALYTICS_DB
    if not session.get('admin_logged_in'): return jsonify({"status": "unauthorized"}), 401
    CLOUD_REPORTS_DB = []; CLOUD_ANALYTICS_DB = []
    return jsonify({"status": "success"})
# 📄 مسار صفحة معرض المشاريع الموحد مع خطاف الاستدعاء المباشر للقائمة المنسدلة
@app.route('/projects')
def projects_page():
    dynamic_links = generate_sidebar_html()
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المشاريع - Albrawe</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            body { font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
            .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; }
            .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #a371f7; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
            .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #a371f7; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; }
            .sidebar-curtain.active { right: 0; }
            .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; }
            .menu-links { display: flex; flex-direction: column; gap: 12px; }
            .menu-item { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; }
            .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 30px; max-width: 500px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">🚀 معرض المشاريع</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">CHIPS_PLACEHOLDER</div>
        </div>
        <div class="main-container">
            <div class="card">
                <h3 style="color:#f0f6fc; margin-top:0;"><i class="fas fa-code-branch"></i> مستودع ومشاريع المهندس البراوي</h3>
                <p style="line-height:1.6; font-size:14px; color:#8b949e;">يتم حالياً جرد وتحديث حزمة المشاريع البرمجية وتطوير واجهاتها السحابية لتظهر هنا قريباً بأعلى معايير الحماية والأمان.</p>
            </div>
        </div>
        <script>
            function toggleSidebar(o) { document.getElementById('sidebarCurtain').style.right = o ? '0px' : '-300px'; }
        </script>
    </body>
    </html>
    """
    return render_template_string(html.replace("CHIPS_PLACEHOLDER", dynamic_links))

# 📄 مسار صفحة من نحن (About us) الموحد مع القائمة الجانبية
@app.route('/about')
def about_page():
    dynamic_links = generate_sidebar_html()
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>من نحن - Albrawe</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            body { font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
            .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff7b72; }
            .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #ff7b72; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
            .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #ff7b72; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; }
            .sidebar-curtain.active { right: 0; }
            .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; }
            .menu-links { display: flex; flex-direction: column; gap: 12px; }
            .menu-item { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; }
            .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #ff7b72; border-radius: 12px; padding: 30px; max-width: 500px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">👤 من نحن (About us)</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">CHIPS_PLACEHOLDER</div>
        </div>
        <div class="main-container">
            <div class="card">
                <h3 style="color:#f0f6fc; margin-top:0;"><i class="fas fa-user-shield"></i> الهوية البرمجية للمهندس البراوي</h3>
                <p style="line-height:1.6; font-size:14px; color:#8b949e;">نحن متخصصون في هندسة وتعديل تطبيقات البايثون (Flask Framework)، معالجة البيانات، وتأمين الواجهات السيبرانية من الثغرات البرمجية بأعلى كفاءة.</p>
            </div>
        </div>
        <script>
            function toggleSidebar(o) { document.getElementById('sidebarCurtain').style.right = o ? '0px' : '-300px'; }
        </script>
    </body>
    </html>
    """
    return render_template_string(html.replace("CHIPS_PLACEHOLDER", dynamic_links))

# 🔒 لوحة الإدارة السحابية المركزية المحمية
ADMIN_HTML = "LOCKED_ADMIN_PANEL_REMOVED_SUCCESSFULLY"
LOGIN_HTML = "LOCKED_ADMIN_LOGIN_REMOVED_SUCCESSFULLY"

@app.route('/PASS', methods=['GET', 'POST'])
def admin_page(): return "404 Not Found", 404

# 🎯 الدالة الجاذبة والذكية البديلة التي حقنتها لتصحيح تعارض سكربت الواجهة القديم دون تعديل ملف home.py
@app.after_request
def inject_clean_dropdown_fix(response):
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        # كسر وإلغاء فاعلية أمر الإغلاق التلقائي للواجهة القديمة واستبداله بالسكربت المطور المستثني لزر الألعاب
        old_script = ".querySelectorAll('.menu-item').forEach"
        new_script = ".querySelectorAll('.menu-links > a').forEach"
        if old_script in text:
            text = text.replace(old_script, new_script)
            response.set_data(text.encode('utf-8'))
    return response

handler = app

if __name__ == '__main__':
    app.run()
