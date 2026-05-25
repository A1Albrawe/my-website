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
            <a href="https://t.me/I_Albrawe" target="_blank" class="menu-item" style="color: #58a6ff;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام 🌐</a>
        </div>
    </div>

    <div class="main-container">
        <div class="dev-portfolio-card">
            <div class="terminal-header">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            
            <!-- 🎯 تم استبدال الكود الافتراضي بكود الصورة الأصلي الموسع ليعمل إجبارياً على جميع المتصفحات فوراً -->
            <img src="data:image/jpeg;base64,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" alt="Albrawe" class="dev-avatar-img">
            
            <h2 class="dev-name">Albrawe</h2>
            <div class="dev-title"> Architecture Engineer & Software Engineer</div>
            
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
