import os
from flask import Blueprint, render_template_string, current_app

menu_blueprint = Blueprint('menu', __name__)

# عزل التنسيقات في كتل نصية مضغوطة ومحمية 100% لمنع تسريب الأكواد خارج صناديق النسخ
MENU_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; text-align: center; padding: 40px 15px; margin: 0; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; }
    .box { background: #0d1117; border: 1px solid #30363d; border-top: 4px solid #58a6ff; max-width: 400px; width: 100%; margin: 0 auto; padding: 25px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: right; box-sizing: border-box; border-bottom: 4px solid #58a6ff; }
    
    .btn { display: block; background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 12px; margin: 10px 0; border-radius: 6px; text-decoration: none; font-weight: bold; transition: 0.2s ease; font-size: 14px; text-align: right; }
    .btn:hover { background: #58a6ff; color: #06090d; box-shadow: 0 0 15px #58a6ff; transform: translateY(-2px); }
    
    .dropdown-trigger-btn { background: #161b22; border: 1px solid #30363d; color: #3fb950; font-size: 14.5px; font-weight: bold; width: 100%; padding: 12px; border-radius: 6px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; margin: 10px 0; transition: 0.2s; box-shadow: 0 4px 12px rgba(63,185,80,0.06); }
    .dropdown-trigger-btn:hover { border-color: #3fb950; box-shadow: 0 0 12px rgba(63,185,80,0.2); }
    .dropdown-trigger-btn i.arrow-icon { transition: transform 0.3s ease; font-size: 12px; }
    .dropdown-trigger-btn.open-state i.arrow-icon { transform: rotate(180deg); }
    
    .dropdown-content-panel { display: none; background: #090d12; border: 1px solid #21262d; border-radius: 6px; padding: 4px 12px; margin-bottom: 10px; flex-direction: column; }
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 9px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; border-bottom: 1px dashed #161b22; }
    .game-link-btn:last-child { border-bottom: none; }
    .game-link-btn:hover { padding-right: 6px; text-shadow: 0 0 10px currentColor; }
</style>
"""
@menu_blueprint.route('/menu')
def menu_page():
    games_list_nodes = []
    try:
        games_dir = os.path.join(current_app.root_path, 'static', 'my_games')
        if os.path.exists(games_dir):
            for filename in sorted(os.listdir(games_dir)):
                if filename.endswith('.txt'):
                    # بتر وتطهير اسم الملف الصريح لمنع الـ 404
                    game_slug = filename.replace('.txt', '').replace('\\n', '').replace('\\r', '').strip()
                    file_path = os.path.join(games_dir, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # 🛡️ خوارزمية التصفية الشاملة لسطور الملف النصي وسحق الرموز المعلقة قسرياً
                        raw_lines = f.readlines()
                        lines = []
                        for line in raw_lines:
                            clean_line = line.replace('\\n', '').replace('\\r', '').strip()
                            if clean_line:
                                lines.append(clean_line)
                        
                    game_name = lines[0] if len(lines) > 0 else game_slug
                    game_icon = lines[1] if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines[2] if len(lines) > 2 else "#fff"
                    
                    # حقن الروابط الصافية تماماً والمبرأة من التلف والـ 404
                    node_html = f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>'
                    games_list_nodes.append(node_html)
    except Exception:
        games_list_nodes = ['<p style="color:#8b949e; font-size:12px; padding:8px 0;">خطأ في مواءمة وحفظ مسارات الألعاب.</p>']

    dynamic_games_html = "".join(games_list_nodes) if games_list_nodes else '<p style="color:#8b949e; font-size:12px; padding:8px 0;">قائمة النظام التلقائية فارغة حالياً.</p>'
    MENU_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دليل الخدمات الشامل | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    """ + MENU_CSS + """
</head>
<body>
    <div class="box">
        <h2 style="color:#fff; margin-top:0; text-align:center;"><i class="fas fa-bars" style="color:#58a6ff; margin-left:6px;"></i> دليل المنصة الشامل</h2>
        <p style="font-size:12px; color:#8b949e; margin-bottom:20px; text-align:center;">اختر وجهتك البرمجية بداخل خادم المهندس البراوي:</p>
        
        <a href="/" class="btn"><i class="fas fa-user-shield"></i> الواجهة التعريفية المعتمدة</a>
        
        <button class="dropdown-trigger-btn" id="gamesMenuTrigger" onclick="toggleGamesDropdown()">
            <span><i class="fas fa-gamepad" style="margin-left:5px;"></i> قائمة ألعاب النظام</span>
            <i class="fas fa-chevron-down arrow-icon"></i>
        </button>
        <div class="dropdown-content-panel" id="gamesDropdownPanel">
            """ + dynamic_games_html + """
        </div>
        
        <a href="/projects" class="btn"><i class="fas fa-folder-open"></i> مستودع المشروعات الهندسية</a>
        <a href="/scripts" class="btn"><i class="fas fa-code"></i> مستودع السكريبتات والأكواد</a>
    </div>

    <script>
        function toggleGamesDropdown() {
            const trigger = document.getElementById("gamesMenuTrigger");
            const panel = document.getElementById("gamesDropdownPanel");
            
            if (panel.style.display === "flex") {
                panel.style.display = "none";
                trigger.classList.remove("open-state");
            } else {
                panel.style.display = "flex";
                trigger.classList.add("open-state");
            }
        }
    </script>
</body>
</html>
"""
    return render_template_string(MENU_HTML)
