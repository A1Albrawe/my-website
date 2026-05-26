# 📝 عدل العناوين والنصوص من هنا مباشرة في السطور الأولى دون البحث في الأكواد!
SCRIPTS_MAIN_TITLE = "مكتبة الأدوات و الاسكربتات"
SCRIPTS_SUB_TEXT   = "يستعرض المحرك أدناه الأكواد المصدرية الداخلية للملف المرفوع بشكل مباشر وحي من السيرفر:"
EMPTY_FOLDER_TEXT  = "المستودع فارغ حالياً! ارفع أي ملف أو تطبيق بايثون (.py) داخل مجلد static/my_scripts/ ليظهر كوده هنا فوراً."

import os
from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

scripts_blueprint = Blueprint('scripts', __name__)

@scripts_blueprint.route('/scripts')
def scripts_page():
    dynamic_links = generate_sidebar_html()
    folder_path = os.path.join('static', 'my_scripts')
    scripts_html = ""
    script_count = 0

    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if not file_name.startswith('.'):
                file_path = os.path.join(folder_path, file_name)
                script_count += 1
                
                # محاولة قراءة الكود الداخلي للملف لعرضه حياً للزوار
                file_content = "تعذر قراءة محتوى هذا الملف النصي أو أنه ملف ثنائي مصمت."
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except Exception:
                    pass
                
                scripts_html += f"""
                <div class="script-card">
                    <h4 class="script-title"><i class="fab fa-python"></i> ملف البرمجة: {file_name}</h4>
                    <p class="script-purpose">{SCRIPTS_SUB_TEXT}</p>
                    <pre class="code-block"><code>{file_content}</code></pre>
                </div>
                """

    if not scripts_html:
        scripts_html = f'<p style="text-align:center; color:#8b949e; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; width: 100%; max-width: 650px; box-sizing: border-box; font-size: 13.5px; line-height: 1.6;">{EMPTY_FOLDER_TEXT}</p>'

    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>إسكربتات بايثون - Albrawe</title>
        <link rel="stylesheet" href="https://cloudflare.com">
        <style>
            body {{ font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
            .header-nav {{ background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #388bfd; }}
            .menu-toggle {{ background: #21262d; border: 1px solid #30363d; color: #388bfd; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }}
            .sidebar-curtain {{ position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #388bfd; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }}
            .sidebar-curtain.active {{ right: 0; }}
            .close-btn {{ background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }}
            .menu-links {{ display: flex; flex-direction: column; gap: 12px; }}
            .main-container {{ flex: 1; display: flex; flex-direction: column; align-items: center; padding: 40px 20px; gap: 25px; }}
            .main-card-title {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px 25px; width: 100%; max-width: 650px; box-sizing: border-box; text-align: right; color: #f0f6fc; margin: 0; font-size: 18px; }}
            .script-card {{ background: #161b22; border: 1px solid #30363d; border-top: 4px solid #388bfd; border-radius: 12px; padding: 25px; max-width: 650px; width: 100%; text-align: right; box-shadow: 0 10px 20px rgba(0,0,0,0.4); box-sizing: border-box; }}
            .script-title {{ margin: 0 0 10px 0; color: #58a6ff; font-size: 16px; font-family: monospace; direction: ltr; text-align: right; }}
            .script-purpose {{ line-height: 1.6; font-size: 13.5px; color: #8b949e; margin: 0 0 15px 0; }}
            .code-block {{ background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; font-family: 'Consolas', monospace; font-size: 13px; color: #79c0ff; overflow-x: auto; text-align: left; direction: ltr; margin: 0; }}
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">⚙️ مكتبة الأدوات ({script_count})</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">{dynamic_links}</div>
        </div>
        <div class="main-container">
            <h3 class="main-card-title"><i class="fas fa-terminal" style="color: #388bfd; margin-left: 8px;"></i> {SCRIPTS_MAIN_TITLE}</h3>
            {scripts_html}
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
