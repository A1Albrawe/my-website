from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

about_blueprint = Blueprint('about', __name__)

@about_blueprint.route('/about')
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
            .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #ff7b72; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }
            .sidebar-curtain.active { right: 0; }
            .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }
            .menu-links { display: flex; flex-direction: column; gap: 12px; }
            .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #ff7b72; border-radius: 12px; padding: 30px; max-width: 500px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">👤 (About us)</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">SIDEBAR_LINKS_PLACEHOLDER</div>
        </div>
        <div class="main-container">
            <div class="card">
                <h3 style="color:#f0f6fc; margin-top:0;"><i class="fas fa-user-shield"></i> ALBRAWE - البراوي</h3>
                <p style="line-height:1.6; font-size:14px; color:#8b949e;">نحن متخصصون في هندسة وتعديل تطبيقات البايثون (Flask Framework)، معالجة البيانات، وتعديل الواجهات البرمجية بأعلى كفاءة.</p>
            </div>
        </div>
        <script>
            function toggleSidebar(o) {
                const curtain = document.getElementById('sidebarCurtain');
                if(o) curtain.classList.add('active'); else curtain.classList.remove('active');
            }
        </script>
    </body>
    </html>
    """.replace("SIDEBAR_LINKS_PLACEHOLDER", dynamic_links)
    return render_template_string(html)
