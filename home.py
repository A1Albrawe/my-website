from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>البوابة الرئيسية لألعاب نوكيا - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #121212;
            color: #8c9f21;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        /* شريط التوب بار العلوي */
        .top-bar {
            background-color: #1a1a1a;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #8c9f21;
        }
        .menu-toggle-btn {
            background: none;
            border: none;
            color: #8c9f21;
            font-size: 24px;
            cursor: pointer;
        }

        /* ستارة القائمة الجانبية الأنيقة المتجاوبة */
        .sidebar-curtain {
            position: fixed;
            top: 0;
            right: -300px;
            width: 280px;
            height: 100%;
            background-color: #1a1a1a;
            border-left: 3px solid #8c9f21;
            box-shadow: -5px 0 15px rgba(0,0,0,0.7);
            z-index: 100;
            transition: right 0.3s ease;
            padding: 20px;
            box-sizing: border-box;
            text-align: right;
        }
        .sidebar-curtain.active {
            right: 0;
        }
        .close-menu-btn {
            background: none;
            border: none;
            color: #ef4444;
            font-size: 22px;
            cursor: pointer;
            margin-bottom: 25px;
        }
        
        /* عناصر وروابط القائمة الجانبية */
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
            padding: 10px;
            border: 1px dashed transparent;
            transition: all 0.2s ease;
        }
        .menu-item:hover {
            border-color: #8c9f21;
            background: rgba(140, 159, 33, 0.1);
        }
        
        /* محتوى وسط الصفحة */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .welcome-card {
            background: #1a1a1a;
            border: 3px solid #8c9f21;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <!-- شريط توب بار علوي يضم زر فتح الستارة الجانبية -->
    <div class="top-bar">
        <button class="menu-toggle-btn" onclick="openSidebar()"><i class="fas fa-bars"></i></button>
        <span style="font-weight: bold; font-size: 18px;">ALBRAWE HUB</span>
    </div>

    <!-- ستارة القائمة الجانبية مضاف إليها الخيار الجديد لإرسال المشاكل -->
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-menu-btn" onclick="closeSidebar()"><i class="fas fa-times"></i> إغلاق</button>
        
        <div class="menu-links">
            <a href="/" class="menu-item"><i class="fas fa-home"></i> الصفحة الرئيسية</a>
            <a href="/snake" class="menu-item"><i class="fas fa-gamepad"></i> لعبة الثعبان الكلاسيكية 🐍</a>
            <a href="/tetris" class="menu-item"><i class="fas fa-cubes"></i> لعبة التترس البكسلية 🧱</a>
            
            <!-- إضافة الخيار البرمجي الجديد المباشر لصفحة الشكاوى داخل الستارة الجانبية -->
            <a href="/report" class="menu-item" style="color: #ff4d4d;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة بالموقع 🛠️</a>
        </div>
    </div>

    <!-- محتوى الترحيب الرئيسي الموحد في الشاشة -->
    <div class="main-content">
        <div class="welcome-card">
            <h2 style="margin-top: 0;">🎮 مرحباً بك في بوابة الألعاب</h2>
            <p style="color: #a1a1aa; line-height: 1.6; font-size: 14px;">افتح القائمة الجانبية العلوية للتنقل بحرية بين الألعاب المتاحة أو إرسال تقرير بالمشاكل إلى المطور مباشرة.</p>
        </div>
    </div>
    <script>
        // دالة فتح الستارة الجانبية بإضافة كلاس النشاط البرمجي للـ CSS
        function openSidebar() {
            document.getElementById('sidebarCurtain').classList.add('active');
        }

        // دالة إغلاق الستارة الجانبية وسحبها للخارج
        function closeSidebar() {
            document.getElementById('sidebarCurtain').classList.remove('active');
        }
        
        // إغلاق تلقائي للستارة عند الضغط على أي رابط بداخلها لتسهيل تجربة التصفح
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', () => { closeSidebar(); });
        });
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_TEMPLATE)
