import os
from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route('/projects')
def projects_page():
    dynamic_links = generate_sidebar_html()
    
    # المسار الفعلي لمجلد المشاريع داخل static
    folder_path = os.path.join('static', 'my_projects')
    cards_html = ""
    project_count = 0

    # فحص وقراءة الملفات النصية تلقائياً إذا كان المجلد موجوداً
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().split('---')
                        if len(content) >= 4:
                            project_count += 1
                            title = content[0].strip()
                            desc = content[1].strip()
                            tech = content[2].strip()
                            link = content[3].strip()
                            
                            cards_html += f"""
                            <div class="project-card">
                                <h4 class="proj-title"><i class="fas fa-folder-open"></i> {title}</h4>
                                <p class="proj-desc">{desc}</p>
                                <div class="proj-footer">
                                    <span class="proj-tech">⚙️ {tech}</span>
                                    <a href="{link}" class="proj-link">استعراض الكود 🔗</a>
                                </div>
                            </div>
                            """
                except Exception:
                    pass

    if not cards_html:
        cards_html = '<p style="text-align:center; color:#8b949e;">لا توجد مشاريع مرفوعة حالياً داخل مجلد static/my_projects/</p>'

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
            .proj-title {{ margin: 0 0 10px 0; color: #f0f6fc; font-size: 18px; }}
            .proj-desc {{ line-height: 1.6; font-size: 14px; color: #8b949e; margin: 0 0 15px 0; }}
            .proj-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #21262d; padding-top: 12px; }}
            .proj-tech {{ font-size: 12px; color: #a371f7; font-weight: bold; }}
            .proj-link {{ color: #58a6ff; text-decoration: none; font-size: 13px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">🚀 معرض المشاريع ({project_count})</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">{dynamic_links}</div>
        </div>
        <div class="main-container">
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
