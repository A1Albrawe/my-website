# 📝 عدل العنوان من هنا مباشرة في السطر الثاني دون البحث في الأكواد!
PROJECTS_MAIN_TITLE = "مستودع ومشاريع المهندس البراوي"

import os
from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route('/projects')
def projects_page():
    dynamic_links = generate_sidebar_html()
    folder_path = os.path.join('static', 'my_projects')
    cards_html = ""
    project_count = 0

    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if not file_name.startswith('.'):
                file_path = os.path.join(folder_path, file_name)
                project_count += 1
                
                _, file_extension = os.path.splitext(file_name)
                ext_name = file_extension.replace('.', '').upper() or "FILE"
                file_size = round(os.path.getsize(file_path) / 1024, 2)
                
                cards_html += f"""
                <div class="project-card">
                    <h4 class="proj-title"><i class="fas fa-file-code"></i> {file_name}</h4>
                    <p class="proj-desc">مستند برمجي مستضاف سحابياً داخل المستودع المركزي للموقع كأحد المشاريع النشطة.</p>
                    <div class="proj-footer">
                        <span class="proj-tech">صيغة الملف: {ext_name} ({file_size} KB)</span>
                        <a href="/static/my_projects/{file_name}" target="_blank" class="proj-link">تحميل أو عرض الملف 🔗</a>
                    </div>
                </div>
                """

    if not cards_html:
        cards_html = '<p style="text-align:center; color:#8b949e;">المستودع فارغ حالياً! ارفع أي ملف أو تطبيق داخل مجلد static/my_projects/ ليظهر هنا فوراً.</p>'

    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المشاريع - Albrawe</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            body {{ font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
            .header-nav {{ background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; }}
            .menu-toggle {{ background: #21262d; border: 1px solid #30363d; color: #a371f7; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }}
            .sidebar-curtain {{ position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #a371f7; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }}
            .sidebar-curtain.active {{ right: 0; }}
            .close-btn {{ background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }}
            .menu-links {{ display: flex; flex-direction: column; gap: 12px; }}
            .main-container {{ flex: 1; display: flex; flex-direction: column; align-items: center; padding: 40px 20px; gap: 20px; }}
            .project-card {{ background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 25px; max-width: 600px; width: 100%; text-align: right; box-shadow: 0 10px 20px rgba(0,0,0,0.4); box-sizing: border-box; }}
            .main-card-title {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px 25px; width: 100%; max-width: 600px; box-sizing: border-box; text-align: right; color: #f0f6fc; margin: 0; font-size: 18px; }}
            .proj-title {{ margin: 0 0 10px 0; color: #58a6ff; font-size: 15px; font-family: monospace; direction: ltr; text-align: right; }}
            .proj-desc {{ line-height: 1.6; font-size: 13.5px; color: #8b949e; margin: 0 0 15px 0; }}
            .proj-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #21262d; padding-top: 12px; }}
            .proj-tech {{ font-size: 11px; color: #a371f7; font-weight: bold; }}
            .proj-link {{ color: #58a6ff; text-decoration: none; font-size: 13px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">🚀 مستودع المشاريع ({project_count})</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">{dynamic_links}</div>
        </div>
        <div class="main-container">
            <h3 class="main-card-title"><i class="fas fa-code-branch" style="color: #a371f7; margin-left: 8px;"></i> {PROJECTS_MAIN_TITLE}</h3>
            {cards_html}
        </div>
        <script>
            function toggleSidebar(o) {{
                const curtain = document.getElementById('sidebarCurtain');
                if(o) curtain.classList.add('active'); else curtain.classList.remove('active');
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html)
