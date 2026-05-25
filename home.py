from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - المطور المحترف</title>
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
        
        /* شريط علوي مستوحى من شاشات الكود */
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
            padding: 6px 12px;
            border-radius: 6px;
            transition: 0.2s;
        }
        .menu-toggle:hover {
            background: #30363d;
            color: #79c0ff;
        }

        /* ستارة القائمة الجانبية السيبرانية المحدثة */
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
        /* بطاقة البيانات الشخصية الاحترافية الكبرى في منتصف الشاشة */
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

        .dev-avatar {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: #21262d;
            border: 2px solid #58a6ff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: #58a6ff;
            margin: 0 auto 20px auto;
            box-shadow: 0 0 15px rgba(88, 166, 255, 0.2);
        }

        .dev-name { margin: 0; font-size: 24px; color: #f0f6fc; text-align: center; font-weight: bold; }
        .dev-title { font-size: 13px; color: #58a6ff; text-align: center; margin: 5px 0 20px 0; font-weight: bold; }

        .info-section {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .info-line { font-size: 13px; margin: 8px 0; line-height: 1.6; color: #c9d1d9; }
        .info-line strong { color: #79c0ff; }

        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .skill-badge {
            background: #21262d;
            border: 1px solid #30363d;
            color: #3fb950;
            padding: 4px 10px;
            font-size: 12px;
            border-radius: 20px;
            font-weight: bold;
        }

        .quick-btn {
            background: #238636;
            color: #ffffff;
            border: 1px solid #2ea44f;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            transition: 0.2s;
            width: 100%;
            justify-content: center;
            box-sizing: border-box;
        }
        .quick-btn:hover {
            background: #2ea44f;
            box-shadow: 0 0 10px rgba(46, 164, 79, 0.4);
        }
    </style>
</head>
<body>

    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebarCurtain(true)"><i class="fas fa-code"></i> المنيو</button>
        <span style="font-weight: bold; font-size: 16px; color: #f0f6fc; font-family: monospace;">console.log("Albrawe");</span>
    </div>

    <!-- ستارة القائمة الجانبية المطورة بالأسلوب البرمجي الشامل -->
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebarCurtain(false)"><i class="fas fa-terminal"></i> exit_menu</button>
        
        <div class="menu-links">
            <a href="/" class="menu-item"><i class="fas fa-folder"></i> main.exe</a>
            <a href="/snake" class="menu-item" style="color: #3fb950;"><i class="fas fa-gamepad"></i> nokia_snake.py 🐍</a>
            <a href="/tetris" class="menu-item" style="color: #d29922;"><i class="fas fa-cubes"></i> retro_tetris.js 🧱</a>
            <a href="/report" class="menu-item" style="color: #f85149;"><i class="fas fa-bug"></i> report_bug.log 🛠️</a>
        </div>
    </div>

    <div class="main-container">
        <!-- لوحة التفاصيل الشخصية المحترفة في المنتصف -->
        <div class="dev-portfolio-card">
            <div class="terminal-header">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            
            <div class="dev-avatar"><i class="fas fa-user-code"></i></div>
            <h2 class="dev-name">المطور البراوي | Albrawe</h2>
            <div class="dev-title">Full-Stack Developer & Game Architecture Engineer</div>
            
            <div class="info-section">
                <div class="info-line">⚡ <strong>نبذة عني:</strong> مهندس برمجيات متخصص في بناء وتطوير تطبيقات الويب الكاملة، وتصميم الألعاب الكلاسيكية بأسلوب البكسل مع حماية الأكواد السحابية من الثغرات.</div>
                <div class="info-line">🚀 <strong>مجالات الخبرة:</strong> هندسة الخوادم (Backend API)، معالجة البيانات المحلية، والواجهات الأمامية المتجاوبة الذكية.</div>
                <div class="info-line">🛠️ <strong>اللغات والتقنيات الأساسية:</strong></div>
                <div class="skills-container">
                    <span class="skill-badge">Python (Flask)</span>
                    <span class="skill-badge">JavaScript (ES6)</span>
                    <span class="skill-badge">HTML5 Canvas</span>
                    <span class="skill-badge">Cyber Security</span>
                    <span class="skill-badge">Git & GitHub</span>
                </div>
            </div>
            
            <button class="quick-btn" onclick="toggleSidebarCurtain(true)"><i class="fas fa-arrow-left"></i> تصفح واختبر مشاريعي البرمجية</button>
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
