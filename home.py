from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

HOME_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; margin: 0; padding: 25px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; overflow-x: hidden; }
    
    /* 🌐 إصلاح وضبط شريط التوجيه بالكامل لتلافي الانعكاس البصري المضلل */
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1200px; margin: 0 auto 35px auto; border-bottom: 2px solid #21262d; padding-bottom: 14px; box-sizing: border-box; }
    .brand-logo { font-size: 24px; font-weight: bold; color: #fff; text-shadow: 0 0 8px #58a6ff; font-family: monospace; text-decoration: none; margin: 0; padding: 0; }
    .menu-btn-trigger { background: #161b22; border: 1px solid #30363d; color: #58a6ff; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 6px; transition: 0.2s ease; font-family: inherit; margin: 0; }
    .menu-btn-trigger:hover { background: #58a6ff; color: #06090d; box-shadow: 0 0 12px #58a6ff; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    
    /* 💻 تعريض المنظومة لتتناسب تماماً مع شاشات الكمبيوتر العريضة وتملأ الأبعاد بفخامة سينمائية */
    .responsive-profile-wrapper { display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1200px; background: #0d1117; border: 1px solid #30363d; border-radius: 18px; padding: 45px; box-shadow: 0 30px 60px rgba(0,0,0,0.7); border-bottom: 4px solid #58a6ff; box-sizing: border-box; align-items: center; direction: rtl; }
    
    /* 🖼️ تأمين مرونة أبعاد الجناح الأيمن للصورة لمنع الاختفاء والضغط السحابي */
    .profile-sidebar-zone { flex: 1; max-width: 280px; display: flex; flex-direction: column; align-items: center; text-align: center; border-left: 2px solid #21262d; padding-left: 30px; box-sizing: border-box; }
    .profile-content-zone { flex: 2; display: flex; flex-direction: column; justify-content: center; text-align: right; box-sizing: border-box; padding-right: 10px; }
    
    @media (max-width: 850px) {
        body { padding: 15px; }
        .top-nav { max-width: 100%; }
        .responsive-profile-wrapper { flex-direction: column; align-items: center; padding: 25px; max-width: 440px; }
        .profile-sidebar-zone { flex: none; width: 100%; max-width: 100%; border-left: none; border-bottom: 2px solid #21262d; padding-left: 0; padding-bottom: 25px; margin-bottom: 20px; }
        .profile-content-zone { width: 100%; padding-right: 0; }
    }
</style>
"""
HOME_CSS_EXT = """
<style>
    .avatar-wrapper { width: 145px; height: 145px; border-radius: 16px; border: 2px solid #58a6ff; overflow: hidden; box-shadow: 0 0 20px rgba(88,166,255,0.3); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; background: #04060a; }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; display: block; }
    
    .profile-name { font-size: 28px; font-weight: bold; color: #fff; margin: 0 0 8px 0; text-shadow: 0 0 5px rgba(255,255,255,0.2); }
    .profile-title { font-size: 11.5px; font-weight: bold; color: #58a6ff; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .details-sub-box { display: flex; flex-direction: column; gap: 16px; font-size: 14.5px; line-height: 1.65; }
    .meta-item { display: block; color: #c9d1d9; }
    .meta-label { font-weight: bold; color: #fff; }
    .tech-highlight { color: #58a6ff; font-weight: bold; font-family: monospace; }
</style>
"""

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
    """ + HOME_CSS + HOME_CSS_EXT + """
</head>
<body>

    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <!-- 🎯 دالة سحب وحقن كرت الستارة المنفصلة حياً وفوراً داخل نفس الصفحة -->
        <button class="menu-btn-trigger" onclick="loadAndOpenSidebarMenu()"><i class="fas fa-bars"></i> القائمة</button>
    </div>

    <!-- صندوق الحاوية الشاغر لحقن الـ Sidebar التابع لـ menu حياً -->
    <div id="dynamicMenuInjectionZone"></div>

    <div class="main-container">
        <div class="responsive-profile-wrapper">
            
            <div class="profile-sidebar-zone">
                <div class="avatar-wrapper">
                    <!-- ✅ الملاءمة الرقمية المطلقة لمسار الأفاتار الصافي من جذر مجلد السيرفر لتنبثق صورتك حياً بدون حجب -->
                    <img class="avatar-img" src="/static/avatar.png" alt="Albrawe Profile" onerror="this.src='https://flagcdn.com'">
                </div>
                <h1 class="profile-name">Albrawe</h1>
                <div class="profile-title">Architecture Engineer & Software Engineer</div>
            </div>
            
            <div class="profile-content-zone">
                <div class="details-sub-box">
                    <span class="meta-item">
                        ⚡ <span class="meta-label">نبذة عني:</span> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكريبتات البايثون مع حماية الأكواد السحابية من الثغرات البرمجية.
                    </span>
                    <span class="meta-item">
                        🚀 <span class="meta-label">مجالات الخبرة:</span> هندسة خوادم الويب المتكاملة، معالجة البيانات المحلية، والواجهات الذكية.
                    </span>
                    <span class="meta-item" style="border-top: 1px dashed #21262d; padding-top: 12px; margin-top: 2px;">
                        🛠️ <span class="meta-label">التقنيات الأساسية:</span>
                        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 5px;">
                            <div>🔹 <span class="tech-highlight">Python (Flask)</span></div>
                            <div>🔹 <span class="tech-highlight">JavaScript (ES6)</span></div>
                        </div>
                    </span>
                </div>
            </div>
            
        </div>
    </div>

    <script>
        // 🚀 تم إصلاح وضبط الرابط بالملي ليتوافق مع نطاق app.py الصافي بدون تكرار وسحب الستارة حياً
        function loadAndOpenSidebarMenu() {
            const zone = document.getElementById("dynamicMenuInjectionZone");
            
            if (zone.innerHTML.trim() !== "") {
                toggleSidebarMenu(true);
                return;
            }
            
            fetch('/api/get_sidebar_menu')
            .then(res => res.json())
            .then(data => {
                const styleNode = document.createElement("style");
                styleNode.innerHTML = data.css;
                document.head.appendChild(styleNode);
                
                zone.innerHTML = data.html;
                setTimeout(() => { toggleSidebarMenu(true); }, 30);
            }).catch(() => { alert("❌ عطل طارئ: تعذر سحب مستودع الستارة الجانبية."); });
        }

        function toggleSidebarMenu(openState) {
            const sidebar = document.getElementById("slidingSidebarMenu");
            if (sidebar) {
                if(openState) sidebar.classList.add("active");
                else sidebar.classList.remove("active");
            }
        }

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

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
