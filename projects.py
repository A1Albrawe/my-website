from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route('/projects')
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
            .header-nav { background-color: #161b22; padding: 12px 20px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; border-bottom: 2px solid #a371f7; }
            .menu-toggle-wrapper { text-align: right; }
            .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #a371f7; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
            .center-title-link { grid-column: 2; text-decoration: none; color: #fff; font-weight: bold; font-size: 19px; font-family: 'Courier New', Courier, monospace; text-shadow: 0 0 5px #a371f7; }
            .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #a371f7; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }
            .sidebar-curtain.active { right: 0; }
            .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }
            .menu-links { display: flex; flex-direction: column; gap: 12px; }
            .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 30px; max-width: 500px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        </style>
    </head>
    <body>
        <div class="header-nav">
            <div class="menu-toggle-wrapper">
                <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            </div>
            <a href="/" class="center-title-link">Albrawe</a>
            <div style="color: #a371f7; font-weight: bold; text-align: left; font-size: 14px;"><i class="fas fa-project-diagram"></i> المشاريع</div>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">SIDEBAR_LINKS_PLACEHOLDER</div>
        </div>
        <div class="main-container">
            <div class="card">
                <h3 style="color:#f0f6fc; margin-top:0;"><i class="fas fa-code-branch"></i> مستودع ومشاريع المهندس البراوي</h3>
                <p style="line-height:1.6; font-size:14px; color:#8b949e;">يتم حالياً جرد وتحديث حزمة المشاريع البرمجية وتطوير واجهاتها السحابية لتظهر هنا قريباً بأعلى معايير الحماية والأمان.</p>
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
    """
    return render_template_string(html.replace("SIDEBAR_LINKS_PLACEHOLDER", dynamic_links))
