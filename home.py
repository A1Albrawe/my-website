from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

home_blueprint = Blueprint('home', __name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; overflow-x: hidden; }
        
        /* ضبط الهيدر بنظام grid لضمان بقاء الاسم في السنتر الفعلي تماماً */
        .header-nav { background-color: #161b22; padding: 12px 20px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; border-bottom: 2px solid #58a6ff; box-shadow: 0 4px 20px rgba(0,0,0,0.4); position: relative; z-index: 10; }
        .menu-toggle-wrapper { text-align: right; }
        .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #58a6ff; font-size: 16px; cursor: pointer; outline: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-family: inherit; transition: 0.2s; }
        .menu-toggle:hover { background: #30363d; border-color: #58a6ff; }
        
        /* تحويل الاسم لزر انتقال نيون في المنتصف */
        .neon-link-center { grid-column: 2; text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 19px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff; transition: 0.2s; }
        .neon-link-center:hover { text-shadow: 0 0 10px #58a6ff, 0 0 20px #58a6ff; transform: scale(1.02); }
        
        .sidebar-curtain { position: fixed; top: 0; right: -320px; width: 300px; height: 100%; background-color: #161b22; border-left: 2px solid #58a6ff; box-shadow: -10px 0 30px rgba(0,0,0,0.7); z-index: 1000; transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1); padding: 25px 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }
        .sidebar-curtain.active { right: 0; }
        .close-btn { background: none; border: none; color: #f85149; font-size: 15px; cursor: pointer; margin-bottom: 25px; font-family: inherit; font-weight: bold; display: flex; align-items: center; gap: 8px; width: 100%; justify-content: flex-start; padding: 0; }
        .menu-links { display: flex; flex-direction: column; gap: 14px; margin-top: 10px; }
        .menu-item { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 14px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; box-sizing: border-box; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; box-sizing: border-box; position: relative; z-index: 1; }
        .dev-portfolio-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 12px; padding: 35px 25px; max-width: 550px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; text-align: right; }
        .dev-avatar-img { width: 110px; height: 110px; border-radius: 16px; object-fit: cover; border: 2px solid #58a6ff; display: block; margin: 0 auto 20px auto; background: #0d1117; }
        .dev-name { margin: 0; font-size: 24px; color: #f0f6fc; text-align: center; font-weight: bold; }
        .dev-title { font-size: 13px; color: #58a6ff; text-align: center; margin: 5px 0 25px 0; font-weight: bold; letter-spacing: 0.5px; }
        .info-section { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 20px; box-sizing: border-box; }
        .info-line { font-size: 13.5px; margin: 12px 0; line-height: 1.7; color: #c9d1d9; display: flex; align-items: flex-start; gap: 8px; }
        .info-line strong { color: #79c0ff; white-space: nowrap; }
    </style>
</head>
<body>
    <div class="header-nav">
        <div class="menu-toggle-wrapper">
            <button class="menu-toggle" onclick="toggleSidebarCurtain(true)">☰ القائمة</button>
        </div>
        <!-- ✅ الاسم في السنتر تماماً ومربوط بالرابط الرئيسي -->
        <a href="/" class="neon-link-center">Albrawe</a>
        <div></div>
    </div>
    
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebarCurtain(false)">❌ إغلاق القائمة</button>
        <div class="menu-links">
            SIDEBAR_LINKS_PLACEHOLDER
        </div>
    </div>
    
    <div class="main-container">
        <div class="dev-portfolio-card">
            <img src="/static/avatar.png" alt="Albrawe" class="dev-avatar-img" onerror="this.src='https://flaticon.com'">
            <h2 class="dev-name">Albrawe</h2>
            <div class="dev-title">Architecture Engineer & Software Engineer</div>
            <div class="info-section">
                <div class="info-line">⚡ <span><strong>نبذة عني:</strong> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكربتات البايثون مع حماية الأكواد السحابية من الثغرات البرمجية.</span></div>
                <div class="info-line">🚀 <span><strong>مجالات الخبرة:</strong> هندسة خوادم الويب المتكاملة، معالجة البيانات المحلية، والواجهات الذكية.</span></div>
                <div class="info-line">🛠️ <strong>التقنيات الأساسية:</strong></div>
                <div style="color: #3fb950; font-size: 13px; font-weight: bold; text-align: right; margin: 6px 15px 0 0; display: flex; align-items: center; gap: 6px;">🔹 Python (Flask)</div>
                <div style="color: #3fb950; font-size: 13px; font-weight: bold; text-align: right; margin: 6px 15px 0 0; display: flex; align-items: center; gap: 6px;">🔹 JavaScript (ES6)</div>
            </div>
        </div>
    </div>
    <script>
        function toggleSidebarCurtain(open) {
            const curtain = document.getElementById('sidebarCurtain');
            if (open) curtain.classList.add('active'); else curtain.classList.remove('active');
        }
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    dynamic_links = generate_sidebar_html()
    rendered_template = HOME_TEMPLATE.replace("SIDEBAR_LINKS_PLACEHOLDER", dynamic_links)
    return render_template_string(rendered_template)
