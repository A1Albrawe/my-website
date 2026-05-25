from flask import Blueprint, render_template_string

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
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #0d1117;
            color: #c9d1d9; 
            padding: 0; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        
        .header-nav {
            background-color: #161b22;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #58a6ff;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }

        .menu-toggle {
            background: #21262d;
            border: 1px solid #30363d;
            color: #58a6ff;
            font-size: 20px;
            cursor: pointer;
            outline: none;
            padding: 6px 15px;
            border-radius: 6px;
            transition: 0.2s;
            font-family: inherit;
            font-weight: bold;
        }
        .menu-toggle:hover {
            background: #30363d;
            color: #79c0ff;
        }

        .neon-text-style {
            font-family: 'Courier New', Courier, monospace;
            font-size: 18px;
            font-weight: bold;
            color: #fff;
            text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff, 0 0 20px #0052cc, 0 0 40px #0052cc;
            animation: neonPulseAnim 1.5s ease-in-out infinite alternate;
            letter-spacing: 1px;
        }
        @keyframes neonPulseAnim {
            from { text-shadow: 0 0 4px #58a6ff, 0 0 8px #58a6ff, 0 0 15px #0052cc, 0 0 30px #0052cc; opacity: 0.9; }
            to { text-shadow: 0 0 6px #58a6ff, 0 0 14px #58a6ff, 0 0 25px #0052cc, 0 0 50px #0052cc; opacity: 1; }
        }

        .sidebar-curtain {
            position: fixed;
            top: 0;
            right: -300px;
            width: 280px;
            height: 100%;
            background-color: #161b22;
            border-left: 2px solid #58a6ff;
            box-shadow: -10px 0 30px rgba(0,0,0,0.7);
            z-index: 1000;
            transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 20px;
            box-sizing: border-box;
            text-align: right;
        }
        .sidebar-curtain.active {
            right: 0;
        }

        .close-btn {
            background: none;
            border: none;
            color: #f85149;
            font-size: 16px;
            cursor: pointer;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: inherit;
            font-weight: bold;
        }

        .menu-links {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #c9d1d9;
            text-decoration: none;
            font-weight: bold;
            font-size: 15px;
            padding: 12px;
            border: 1px solid #30363d;
            border-radius: 6px;
            background: #21262d;
            transition: all 0.2s ease;
        }
        .menu-item:hover {
            border-color: #58a6ff;
            color: #58a6ff;
            background: rgba(88, 166, 255, 0.05);
            transform: translateX(-5px);
        }

        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px 20px;
        }
        .dev-portfolio-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-top: 4px solid #58a6ff;
            border-radius: 12px;
            padding: 35px 25px;
            max-width: 550px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            box-sizing: border-box;
            text-align: right;
            position: relative;
        }

        .terminal-header {
            display: flex;
            gap: 6px;
            position: absolute;
            top: 12px;
            left: 15px;
        }
        .dot { width: 10px; height: 10px; border-radius: 50%; }
        .dot-r { background: #f85149; }
        .dot-y { background: #d29922; }
        .dot-g { background: #3fb950; }

        .dev-avatar-img {
            width: 110px;
            height: 110px;
            border-radius: 16px;
            object-fit: cover;
            border: 2px solid #58a6ff;
            display: block;
            margin: 0 auto 20px auto;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
            background: #0d1117;
        }

        .dev-name { margin: 0; font-size: 24px; color: #f0f6fc; text-align: center; font-weight: bold; }
        .dev-title { font-size: 13px; color: #58a6ff; text-align: center; margin: 5px 0 20px 0; font-weight: bold; }

        .info-section {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
        }
        .info-line { font-size: 13px; margin: 10px 0; line-height: 1.6; color: #c9d1d9; }
        .info-line strong { color: #79c0ff; }

        .skills-container {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 10px;
            padding-right: 15px;
        }
        .skill-badge {
            color: #3fb950;
            font-size: 13px;
            font-weight: bold;
            display: block;
            text-align: right;
        }
    </style>
</head>
<body>

    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebarCurtain(true)"><i class="fas fa-bars"></i> القائمة</button>
        <span class="neon-text-style">Albrawe</span>
    </div>

    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebarCurtain(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        
        <div class="menu-links">
            <a href="/" class="menu-item"><i class="fas fa-home"></i> البوابة الرئيسية</a>
            <a href="/snake" class="menu-item" style="color: #3fb950;"><i class="fas fa-gamepad"></i> لعبة الثعبان الكلاسيكية 🐍</a>
            <a href="/tetris" class="menu-item" style="color: #d29922;"><i class="fas fa-cubes"></i> لعبة التترس البكسلية 🧱</a>
            <a href="/scripts" class="menu-item" style="color: #388bfd;"><i class="fab fa-python"></i> إسكربتات بايثون ⚙️</a>
            <a href="/report" class="menu-item" style="color: #f85149;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة بالموقع 🛠️</a>
            <a href="https://t.me" target="_blank" class="menu-item" style="color: #58a6ff;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام 🌐</a>
        </div>
    </div>

    <div class="main-container">
        <div class="dev-portfolio-card">
            <div class="terminal-header">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            
            <!-- 🎯 قراءة الصورة المحلية المرفوعة داخل الحاوية في مجلد static بثبات 100% وبدون روابط خارجية -->
            <img src="/static/avatar.png" alt="Albrawe" class="dev-avatar-img" onerror="this.src='https://cloudflare.com'">
            
            <h2 class="dev-name">Albrawe</h2>
            <div class="dev-title">Game Architecture Engineer & Software Specialist</div>
            
            <div class="info-section">
                <div class="info-line">⚡ <strong>نبذة عني:</strong> بناء وتطوير تطبيقات الويب الكاملة، وتصميم وتعديل اسكربتات البايثون مع حماية الأكواد السحابية من الثغرات البرمجية.</div>
                <div class="info-line">🚀 <strong>مجالات الخبرة:</strong> هندسة خوادم الويب المتكاملة، معالجة البيانات المحلية ، والواجهات الذكية.</div>
                <div class="info-line">🛠️ <strong>التقنيات الأساسية:</strong></div>
                <div class="skills-container">
                    <span class="skill-badge"><i class="fab fa-python"></i> Python (Flask)</span>
                    <span class="skill-badge"><i class="fab fa-js-square"></i> JavaScript (ES6)</span>
                </div>
            </div>
        </div>
    </div>
    <script>
        function toggleSidebarCurtain(open) {
            const curtain = document.getElementById('sidebarCurtain');
            if (open) {
                curtain.classList.add('active');
            } else {
                curtain.classList.remove('active');
            }
        }
        
        document.querySelectorAll('.menu-item').forEach(link => {
            link.addEventListener('click', () => { toggleSidebarCurtain(false); });
        });
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_TEMPLATE)
