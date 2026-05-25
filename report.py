from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

# إعادة تهيئة المسار للامتداد المعزول الجديد لكسر الكاش
report_blueprint = Blueprint('report', __name__)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>مركز الدعم الفني - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f85149; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #f85149; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
        .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #f85149; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; }
        .sidebar-curtain.active { right: 0; }
        .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; }
        .menu-links { display: flex; flex-direction: column; gap: 12px; }
        .menu-item { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .maintenance-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; border-radius: 12px; padding: 40px 25px; max-width: 480px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; }
        .warn-icon { font-size: 50px; color: #f85149; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
        <span style="color:#fff; font-weight:bold;">⚠️ حالة النظام</span>
    </div>
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
        <div class="menu-links">CHIPS_PLACEHOLDER</div>
    </div>
    <div class="main-container">
        <div class="maintenance-card">
            <div class="warn-icon">⚙️</div>
            <h2 style="color:#f0f6fc; margin:0 0 10px 0;">تحت الصيانة</h2>
            <p style="color:#f85149; font-weight:bold; font-size:16px; margin:0; line-height:1.6;">
                تم تعليق التفاعل وإيقاف استقبال الشكاوى والبلاغات مؤقتاً.<br>
                هذا القسم مغلق وتحت الصيانة الفنية الصارمة الآن.
            </p>
        </div>
    </div>
    <script>
        function toggleSidebar(o) { document.getElementById('sidebarCurtain').style.right = o ? '0px' : '-300px'; }
    </script>
</body>
</html>
"""

# 🎯 تم تغيير الرابط البرمجي الفرعي ليكون الامتداد الصافي الجديد المغلق إجبارياً
@report_blueprint.route('/maintenance')
def report_page():
    dynamic_links = generate_sidebar_html()
    return render_template_string(REPORT_TEMPLATE.replace("CHIPS_PLACEHOLDER", dynamic_links))

# قفل التوجيه التلقائي للمسار القديم ليصبح ملغياً تماماً ويعطي خطأ حظر
@report_blueprint.route('/report')
def old_report_page():
    return "403 Forbidden: This section has been permanently disabled.", 403
