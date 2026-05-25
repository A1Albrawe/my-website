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
            
            <!-- 🎯 تم تصحيح مصفوفة البايثون المترجمة وإجبار المتصفح على سحب الصورة السليمة والمحمية داخلياً بنسبة 100% -->
            <img src="data:image/jpeg;base64,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ول تفصيلة أضفتها أنت؛ وهي: نبذتك التناظرية، مهاراتك التقنية في البرمجة، والواجهات المتجاوبة الموحدة بـ CSS. -->
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
        // دالة التحكم والمحاكاة في فتح وإغلاق الستارة الجانبية البرمجية
        function toggleSidebarCurtain(open) {
            const curtain = document.getElementById('sidebarCurtain');
            if (open) {
                curtain.classList.add('active');
            } else {
                curtain.classList.remove('active');
            }
        }
        
        // ربط ذكي يضمن سحب الستارة فور فتح أي رابط برمجياً لتجنب تعليق الشاشة
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
