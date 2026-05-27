from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# عزل التنسيقات النيونية المتجاوبة لحماية النواة البرمجية تماماً وتسهيل النسخ الصافي
HOME_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; margin: 0; padding: 15px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; justify-content: center; }
    
    /* 🌐 شريط الإقلاع العلوي المصحح: الاسم يميناً وزر القائمة يساراً بنقاء بصري قياسي وثابت */
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 1000px; margin: 0 auto 30px auto; border-bottom: 2px solid #21262d; padding-bottom: 12px; direction: ltr; }
    .brand-logo { font-size: 22px; font-weight: bold; color: #fff; text-shadow: 0 0 8px #58a6ff; font-family: monospace; order: 1; text-decoration: none; }
    .menu-btn-link { background: #161b22; border: 1px solid #30363d; color: #58a6ff; padding: 7px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13.5px; display: flex; align-items: center; gap: 6px; transition: 0.2s ease; order: 2; font-family: inherit; text-decoration: none; }
    .menu-btn-link:hover { background: #58a6ff; color: #06090d; box-shadow: 0 0 12px #58a6ff; transform: translateY(-1px); }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    
    /* 💻 الهيكل المزدوج المطور لتغطية شاشات الكمبيوتر بكفاءة استعراضية فاخرة تملأ الأبعاد */
    .responsive-profile-wrapper { display: flex; flex-direction: row; gap: 30px; width: 100%; max-width: 1000px; background: #0d1117; border: 1px solid #30363d; border-radius: 16px; padding: 35px; box-shadow: 0 25px 50px rgba(0,0,0,0.6); border-bottom: 4px solid #58a6ff; box-sizing: border-box; align-items: stretch; direction: rtl; }
    
    .profile-sidebar-zone { flex: 0 0 240px; display: flex; flex-direction: column; align-items: center; text-align: center; border-left: 1px solid #21262d; padding-left: 25px; box-sizing: border-box; justify-content: center; }
    .profile-content-zone { flex: 1; display: flex; flex-direction: column; justify-content: center; text-align: right; box-sizing: border-box; padding-right: 5px; }
    
    /* 📱 التوافق الذكي التلقائي لشاشات الموبايل الرشيقة */
    @media (max-width: 768px) {
        .top-nav { max-width: 100%; }
        .responsive-profile-wrapper { flex-direction: column; align-items: center; padding: 25px; max-width: 440px; }
        .profile-sidebar-zone { flex: none; width: 100%; border-left: none; border-bottom: 1px solid #21262d; padding-left: 0; padding-bottom: 20px; margin-bottom: 15px; }
        .profile-content-zone { width: 100%; padding-right: 0; }
    }
</style>
"""
# حقن تنسيقات الكرت وصندوق السيرة الذاتية النيوني المضيء
HOME_CSS_EXT = """
<style>
    .avatar-wrapper { width: 135px; height: 135px; border-radius: 14px; border: 2px solid #58a6ff; overflow: hidden; box-shadow: 0 0 15px rgba(88,166,255,0.25); margin-bottom: 18px; display: flex; align-items: center; justify-content: center; background: #04060a; }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; }
    
    .profile-name { font-size: 25px; font-weight: bold; color: #fff; margin: 0 0 6px 0; text-shadow: 0 0 5px rgba(255,255,255,0.2); letter-spacing: 0.5px; }
    .profile-title { font-size: 11px; font-weight: bold; color: #58a6ff; margin: 0; letter-spacing: 0.5px; line-height: 1.4; text-transform: uppercase; }
    
    .details-sub-box { display: flex; flex-direction: column; gap: 14px; font-size: 14px; line-height: 1.6; }
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
    <title>Albrawe | الصفحة الرئيسية الموحدة</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <link rel="icon" type="image/x-icon" href="static/favicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="static/favicon.ico">
    """ + HOME_CSS + HOME_CSS_EXT + """
</head>
<body>

    <div class="top-nav">
        <a href="/" class="brand-logo">Albrawe</a>
        <!-- 🎯 التوجيه التكتيكي الصارم: ربط الزر ليتوجه صراحة وقسراً لمسار صفحة القائمة والمنسدلة /menu المصلحة الشاملة -->
        <a href="/menu" class="menu-btn-link"><i class="fas fa-bars"></i> القائمة</a>
    </div>

    <div class="main-container">
        <!-- الهيكل المزدوج ثنائي الأجنحة الفاخر للكمبيوتر والمتحول للموبايل حياً بكفاءة تشغيلية كاملة 100% -->
        <div class="responsive-profile-wrapper">
            
            <!-- جناح الهوية البصرية والمظهر الرقمي -->
            <div class="profile-sidebar-zone">
                <div class="avatar-wrapper">
                    <!-- ✅ تثبيت مسار الصورة الصافي من الجذر المباشر ليتعرف عليه Vercel فوراً ويقفل منابع الحجب -->
                    <img class="avatar-img" src="static/avatar.png" alt="Albrawe Profile" onerror="this.src='https://flagcdn.com'">
                </div>
                <h1 class="profile-name">Albrawe</h1>
                <div class="profile-title">Architecture Engineer & Software Engineer</div>
            </div>
            
            <!-- جناح النبذة والخبرات والتقنيات القياسية -->
            <div class="profile-content-zone">
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
    </div>

</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
