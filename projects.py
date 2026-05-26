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

    # ✅ المحرك المطور: مسح مجلد static/my_projects وقراءة أي ملف حياً للزوار
    if os.path.exists(folder_path):
        for file_name in sorted(os.listdir(folder_path)):
            if not file_name.startswith('.'):
                file_path = os.path.join(folder_path, file_name)
                project_count += 1
                
                # جلب نوع الملف وحجمه لتقديمه بشكل احترافي
                _, file_extension = os.path.splitext(file_name)
                ext_name = file_extension.replace('.', '').upper() or "FILE"
                file_size = round(os.path.getsize(file_path) / 1024, 2)
                
                cards_html += f"""
                <div class="project-card">
                    <h4 class="proj-title"><i class="fas fa-file-code" style="color: #a371f7; margin-left: 6px;"></i> {file_name}</h4>
                    <p class="proj-desc">مستند برمجي وتطبيق مستضاف سحابياً داخل المستودع المركزي للموقع كأحد المشاريع النشطة الجاهزة للاستعراض.</p>
                    <div class="proj-footer">
                        <span class="proj-tech">صيغة الملف: {ext_name} ({file_size} KB)</span>
                        <a href="/static/my_projects/{file_name}" target="_blank" class="proj-link">استعراض أو تحميل 🔗</a>
                    </div>
                </div>
                """

    # إذا كان المجلد فارغاً يظهر الكرت الافتراضي الذي أرسلته أنت بتنسيقه الكامل
    if not cards_html:
        cards_html = """
        <div class="card">
            <h3 style="color:#f0f6fc; margin-top:0;"><i class="fas fa-code-branch"></i> ALBRAWE - البراوي</h3>
            <p style="line-height:1.6; font-size:14px; color:#8b949e;">يتم حالياً جرد وتحديث حزمة المشاريع البرمجية وتطوير واجهاتها السحابية لتظهر هنا قريباً بأعلى معايير الحماية والأمان.</p>
        </div>
        """
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المشاريع - Albrawe</title>
        <!-- ✅ تم تصحيح رابط الأيقونات لتعمل كافة الأشكال والرموز في الموقع -->
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            body {{ font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
            .header-nav {{ background-color: #161b22; padding: 12px 20px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; border-bottom: 2px solid #a371f7; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
            .menu-toggle-wrapper {{ text-align: right; }}
            .menu-toggle {{ background: #21262d; border: 1px solid #30363d; color: #a371f7; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }}
            
            /* ✨ تأثير النيون لاسم المطور للتوجيه الفوري للرئيسية */
            .brand-center-link {{ grid-column: 2; text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #a371f7, 0 0 10px #a371f7; transition: 0.2s; }}
            .brand-center-link:hover {{ text-shadow: 0 0 10px #fff, 0 0 20px #a371f7; }}
            
            .sidebar-curtain {{ position: fixed; top: 0; right: -320px; width: 300px; height: 100%; background-color: #161b22; border-left: 2px solid #a371f7; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }}
            .sidebar-curtain.active {{ right: 0; }}
            .close-btn {{ background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }}
            .menu-links {{ display: flex; flex-direction: column; gap: 12px; }}
            
            .main-container {{ flex: 1; display: flex; flex-direction: column; align-items: center; padding: 40px 20px; gap: 20px; box-sizing: border-box; }}
            .card {{ background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 30px; max-width: 600px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; }}
            
            /* كروت جرد الملفات النشطة تلقائياً */
            .project-card {{ background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 25px; max-width: 600px; width: 100%; text-align: right; box-shadow: 0 10px 20px rgba(0,0,0,0.4); box-sizing: border-box; }}
            .proj-title {{ margin: 0 0 10px 0; color: #f0f6fc; font-size: 15px; font-family: monospace; direction: ltr; text-align: right; }}
            .proj-desc {{ line-height: 1.6; font-size: 13.5px; color: #8b949e; margin: 0 0 15px 0; }}
            .proj-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #21262d; padding-top: 12px; }}
            .proj-tech {{ font-size: 11px; color: #a371f7; font-weight: bold; }}
            .proj-link {{ color: #58a6ff; text-decoration: none; font-size: 13px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header-nav">
            <div class="menu-toggle-wrapper">
                <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            </div>
            <a href="/" class="brand-center-link">Albrawe</a>
            <div style="color: #a371f7; font-weight: bold; text-align: left; font-size: 14px;"><i class="fas fa-project-diagram"></i> المشاريع ({project_count})</div>
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
