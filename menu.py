import os
from flask import Blueprint, render_template_string, current_app

home_blueprint = Blueprint('home', __name__)

# عزل كافة تنسيقات النيون القياسية لعام 2026 لحمايتها تماماً من التداخل النصي لبايثون
HOME_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; margin: 0; padding: 15px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; position: relative; overflow-x: hidden; }
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 600px; margin: 0 auto 20px auto; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
    
    .brand-logo { font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 8px #58a6ff; font-family: monospace; }
    .menu-btn-trigger { background: #161b22; border: 1px solid #30363d; color: #58a6ff; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13.5px; display: flex; align-items: center; gap: 6px; transition: 0.2s ease; }
    .menu-btn-trigger:hover { background: #58a6ff; color: #06090d; box-shadow: 0 0 12px #58a6ff; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    
    .profile-card { background: #0d1117; border: 1px solid #30363d; border-radius: 14px; width: 100%; max-width: 440px; padding: 30px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); position: relative; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; border-bottom: 4px solid #58a6ff; }
    .avatar-wrapper { width: 120px; height: 120px; border-radius: 12px; border: 2px solid #58a6ff; overflow: hidden; box-shadow: 0 0 15px rgba(88,166,255,0.25); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; background: #04060a; }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; }
    
    .profile-name { font-size: 22px; font-weight: bold; color: #fff; margin: 0 0 6px 0; text-shadow: 0 0 5px rgba(255,255,255,0.2); letter-spacing: 0.5px; }
    .profile-title { font-size: 11px; font-weight: bold; color: #58a6ff; margin: 0 0 25px 0; letter-spacing: 0.5px; max-width: 90%; line-height: 1.4; text-transform: uppercase; }
    
    .details-sub-box { background: #06090d; border: 1px solid #21262d; border-radius: 10px; padding: 20px; width: 100%; box-sizing: border-box; text-align: right; font-size: 13px; line-height: 1.6; display: flex; flex-direction: column; gap: 14px; }
    .meta-item { display: block; color: #c9d1d9; }
    .meta-label { font-weight: bold; color: #fff; }
    .tech-highlight { color: #58a6ff; font-weight: bold; font-family: monospace; }
</style>
"""
    /* 🕹️ معمارية الـ Sidebar المنزلق المستنسخ كلياً من تفاصيل لقطات شاشتك بدقة */
    .sidebar-overlay { position: fixed; top: 0; right: -100%; width: 100%; max-width: 290px; height: 100vh; background: rgba(13, 17, 23, 0.97); border-left: 2px solid #58a6ff; box-shadow: -10px 0 30px rgba(0, 0, 0, 0.7); z-index: 9999; display: flex; flex-direction: column; padding: 20px; box-sizing: border-box; transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1); overflow-y: auto; }
    .sidebar-overlay.active { right: 0; }
    
    .close-menu-btn { background: none; border: none; color: #f85149; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 5px; align-self: flex-end; margin-bottom: 25px; font-family: inherit; }
    .close-menu-btn:hover { text-shadow: 0 0 8px #f85149; }
    
    .sidebar-links-wrapper { display: flex; flex-direction: column; text-align: right; padding-right: 5px; }
    
    .section-menu-divider { font-size: 15px; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: flex-start; margin-top: 15px; margin-bottom: 12px; border-bottom: 1px dashed #21262d; padding-bottom: 6px; }
    
    /* محرك استعراض خطوط روابط الألعاب النيونية المضيئة */
    .game-link-btn { text-decoration: none; font-size: 14px; font-family: inherit; padding: 8px 0; display: block; transition: 0.15s ease; width: 100%; text-align: right; font-weight: 500; }
    .game-link-btn:hover { padding-right: 5px; text-shadow: 0 0 8px currentColor; }
    
    .general-link-item { text-decoration: none; font-size: 13.5px; color: #8b949e; padding: 6px 0; display: block; font-weight: bold; }
    .general-link-item:hover { color: #fff; text-shadow: 0 0 6px #fff; }
</style>
"""
@home_blueprint.route('/')
def home_page():
    # 🧠 الخوارزمية الذكية: تفحص ملفات static/my_games/ لإنتاج أزرار القائمة حياً وتلقائياً
    dynamic_games_html = ""
    try:
        # الإشارة المباشرة لمستودع الملفات النصية المستقلة بداخل مجلد static
        games_dir = os.path.join(current_app.root_path, 'static', 'my_games')
        if os.path.exists(games_dir):
            for filename in sorted(os.listdir(games_dir)):
                if filename.endswith('.txt'):
                    game_slug = filename.replace('.txt', '')
                    file_path = os.path.join(games_dir, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        
                    # تفكيك الأسطر الثلاثة الملقنة (الاسم المعرب، الأيقونة، كود اللون النيوني)
                    game_name = lines[0] if len(lines) > 0 else game_slug
                    game_icon = lines[1] if len(lines) > 1 else "fas fa-gamepad"
                    game_color = lines[2] if len(lines) > 2 else "#fff"
                    
                    # ربط الزر التلقائي بالمسار البرمجي المقابل والمفعّل صراحة بداخل الـ games_package
                    dynamic_games_html += f'<a href="/{game_slug}" class="game-link-btn" style="color: {game_color};"><i class="{game_icon}"></i> {game_name}</a>\\n'
    except Exception:
        dynamic_games_html = '<p style="color:#8b949e; font-size:12px;">خطأ في جلب مستودع الألعاب الذكي.</p>'

    if not dynamic_games_html:
        dynamic_games_html = '<p style="color:#8b949e; font-size:12px;">قائمة النظام التلقائية فارغة حالياً.</p>'

    HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe | البوابة الرسمية الموحدة</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">
    """ + HOME_CSS + """
</head>
<body>

    <div class="top-nav">
        <span class="brand-logo">Albrawe</span>
        <button class="menu-btn-trigger" onclick="toggleSidebarMenu(true)"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- 🕹️ الـ Sidebar الجانبي المنزلق الملقن تلقائياً ومباشرة بمخرجات محرك فحص my_games المستقل كلياً -->
    <div class="sidebar-overlay" id="slidingSidebarMenu">
        <button class="close-menu-btn" onclick="toggleSidebarMenu(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        
        <div class="sidebar-links-wrapper">
            <a href="/" class="general-link-item" style="color:#fff; margin-bottom:5px;">البوابة الرئيسية 🏠</a>
            
            <div class="section-menu-divider" style="color: #3fb950; border-color: #3fb950;"><i class="fas fa-gamepad"></i> قائمة ألعاب النظام</div>
            
            <!-- 🔥 توليد وحقن أزرار باقة ألعابك الستة تلقائياً بنسق ألوانها المضيئة القياسي -->
            """ + dynamic_games_html + """
            
            <div class="section-menu-divider" style="color:#8b949e; margin-top:20px;"><i class="fas fa-folder-open"></i> مسارات إضافية</div>
            <a href="/projects" class="general-link-item">معرض المشاريع</a>
            <a href="/about" class="general-link-item">(About us)</a>
            <a href="/scripts" class="general-link-item">إسكربتات بايثون</a>
            <a href="/report" class="general-link-item" style="color:#ff7b72;">الإبلاغ عن مشكلة (صيانة)</a>
            <a href="https://t.me" target="_blank" class="general-link-item" style="color:#388bfd;">حسابي في التليجرام</a>
        </div>
    </div>
    <div class="main-container">
        <div class="profile-card">
            <div class="avatar-wrapper">
                <img class="avatar-img" src="/static/avatar.png" alt="Albrawe Profile" onerror="this.src='https://flagcdn.com'">
            </div>
            
            <h1 class="profile-name">Albrawe</h1>
            <div class="profile-title">Architecture Engineer & Software Engineer</div>
            
            <div class="details-sub-box">
                <span class="meta-item">
                    ⚡ <span class="meta-label">نبذة عني:</span> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكريبتات البايثون مع حماية الأكواد السحابية من الثغرات البرمجية.
                </span>
                <span class="meta-item">
                    🚀 <span class="meta-label">مجالات الخبرة:</span> هندسة خوادم الويب المتكاملة، معالجة البيانات المحلية، والواجهات الذكية.
                </span>
                <span class="meta-item" style="border-top: 1px dashed #21262d; padding-top: 10px; margin-top: 2px;">
                    🛠️ <span class="meta-label">التقنيات الأساسية:</span>
                    <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 5px;">
                        <div>🔹 <span class="tech-highlight">Python (Flask)</span></div>
                        <div>🔹 <span class="tech-highlight">JavaScript (ES6)</span></div>
                    </div>
                </span>
            </div>
        </div>
    </div>

    <script>
        function toggleSidebarMenu(openState) {
            const sidebar = document.getElementById("slidingSidebarMenu");
            if(openState) sidebar.classList.add("active");
            else sidebar.classList.remove("active");
        }
    </script>
</body>
</html>
"""
    return render_template_string(HOME_HTML)
