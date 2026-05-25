from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>البوابة الرئيسية - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #121212;
            color: #8c9f21; 
            padding: 0; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            box-sizing: border-box;
        }
        
        .header-nav {
            background-color: #1a1a1a;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #8c9f21;
        }

        .menu-toggle {
            background: none;
            border: none;
            color: #8c9f21;
            font-size: 24px;
            cursor: pointer;
            outline: none;
        }

        /* الستارة الجانبية المحدثة والمثبتة برمجياً لتأمين الظهور */
        .sidebar-curtain {
            position: fixed;
            top: 0;
            right: -300px;
            width: 280px;
            height: 100%;
            background-color: #1a1a1a;
            border-left: 3px solid #8c9f21;
            box-shadow: -5px 0 25px rgba(0,0,0,0.8);
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
            color: #ef4444;
            font-size: 20px;
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
            gap: 15px;
        }

        .menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #8c9f21;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;
            padding: 12px;
            border: 1px dashed transparent;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .menu-item:hover {
            border-color: #8c9f21;
            background: rgba(140, 159, 33, 0.1);
        }

        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .hub-card {
            background: #1a1a1a;
            border: 3px solid #8c9f21;
            border-radius: 20px;
            padding: 35px 25px;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            box-sizing: border-box;
        }

        .logo-icon {
            font-size: 48px;
            margin-bottom: 15px;
            color: #8c9f21;
        }

        .desc-text {
            color: #a1a1aa;
            line-height: 1.6;
            font-size: 14px;
            margin: 15px 0 25px 0;
        }

        .quick-btn {
            background: #8c9f21;
            color: #121212;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .quick-btn:hover {
            background: #a4b930;
        }
    </style>
</head>
<body>

    <!-- شريط التحكم والتنقل العلوي الرئيسي لموقع البروي -->
    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebarCurtain(true)"><i class="fas fa-bars"></i></button>
        <span style="font-weight: bold; font-size: 18px; letter-spacing: 1px;">ALBRAWE HUB</span>
    </div>

    <!-- ستارة القائمة الجانبية المحصنة هندسياً ضد الاختفاء والمزودة بخانة المشاكل -->
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebarCurtain(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
        
        <div class="menu-links">
            <a href="/" class="menu-item"><i class="fas fa-home"></i> البوابة الرئيسية</a>
            <a href="/snake" class="menu-item"><i class="fas fa-gamepad"></i> لعبة الثعبان النوكيا 🐍</a>
            <a href="/tetris" class="menu-item"><i class="fas fa-cubes"></i> لعبة التترس البكسلية 🧱</a>
            
            <!-- تم دمج رابط صفحة الدعم الفني الجديد بلون مميز لسهولة الوصول لمنع عيوب العرض -->
            <a href="/report" class="menu-item" style="color: #ff4d4d; border-color: rgba(239, 68, 68, 0.2);"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة 🛠️</a>
        </div>
    </div>

    <div class="main-container">
        <div class="hub-card">
            <div class="logo-icon"><i class="fas fa-mobile-alt"></i></div>
            <h2 style="margin: 0; font-size: 22px;">مركز ألعاب نوكيا المطور</h2>
            <p class="desc-text">مرحباً بك في المنصة الخاصة بك. اضغط على الزر العلوي لفتح الستارة الجانبية والتنقل بين الألعاب الكلاسيكية أو إرسال المشاكل والشكاوى مباشرة إلى المطور.</p>
            <button class="quick-btn" onclick="toggleSidebarCurtain(true)"><i class="fas fa-folder-open"></i> تصفح القائمة الجانبية</button>
        </div>
    </div>
    <script>
        // دالة موحدة ومحسنة هندسياً للتحكم في حركة وفتح الستارة الجانبية دون تعليق
        function toggleSidebarCurtain(open) {
            const curtain = document.getElementById('sidebarCurtain');
            if (open) {
                curtain.classList.add('active');
            } else {
                curtain.classList.remove('active');
            }
        }
        
        // ربط ذكي لإغلاق القائمة فوراً عند الضغط على أي مسار لتأمين الاستجابة
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
