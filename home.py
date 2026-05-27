from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# حقن وعزل التنسيقات النيونية والهوية السينمائية لعام 2026 المطابقة للصورة تماماً
HOME_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; margin: 0; padding: 15px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; }
    .top-nav { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 600px; margin: 0 auto 20px auto; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
    
    .brand-logo { font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 8px #58a6ff; font-family: monospace; }
    .menu-btn { background: #161b22; border: 1px solid #30363d; color: #58a6ff; padding: 6px 14px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 13.5px; display: flex; align-items: center; gap: 6px; transition: 0.2s ease; }
    .menu-btn:hover { background: #58a6ff; color: #06090d; box-shadow: 0 0 12px #58a6ff; }
    
    .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    
    /* 🛡️ تصميم كرت الهوية الرقمي النيوني الفخم المطابق للصورة */
    .profile-card { background: #0d1117; border: 1px solid #30363d; border-radius: 14px; width: 100%; max-width: 440px; padding: 30px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); position: relative; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; border-bottom: 4px solid #58a6ff; }
    
    .avatar-wrapper { width: 120px; height: 120px; border-radius: 12px; border: 2px solid #58a6ff; overflow: hidden; box-shadow: 0 0 15px rgba(88,166,255,0.25); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; background: #04060a; }
    .avatar-img { width: 100%; height: 100%; object-fit: cover; }
    
    .profile-name { font-size: 22px; font-weight: bold; color: #fff; margin: 0 0 6px 0; text-shadow: 0 0 5px rgba(255,255,255,0.2); letter-spacing: 0.5px; }
    .profile-title { font-size: 11px; font-weight: bold; color: #58a6ff; margin: 0 0 25px 0; letter-spacing: 0.5px; max-width: 90%; line-height: 1.4; text-transform: uppercase; }
    
    /* 📝 صندوق المحتوى التفصيلي الداخلي */
    .details-sub-box { background: #06090d; border: 1px solid #21262d; border-radius: 10px; padding: 20px; width: 100%; box-sizing: border-box; text-align: right; font-size: 13px; line-height: 1.6; display: flex; flex-direction: column; gap: 14px; }
    
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
    
    <!-- استدعاء باقة الأيقونات الفاخرة المشعة حياً -->
    <link rel="stylesheet" href="https://cloudflare.com">
    
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">

    <!-- وسوم الـ Open Graph للصورة المصغرة والشعار على السوشيال ميديا -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://vercel.app">
    <meta property="og:title" content="Albrawe Arcade & Cyber Analytics">
    <meta property="og:description" content="البوابة الرسمية لألعاب الأركيد النيونية ومنظومة الرصد البياني الذكي">
    <meta property="og:image" content="https://vercel.appstatic/thumbnail.png">
    
    """ + HOME_CSS + """
</head>
<body>

    <!-- 🌐 شريط التنقل العلوي الفاخر المدمج باللوجو وزر القائمة المضيء القياسي الموجه لصفحة ألعابك -->
    <div class="top-nav">
        <span class="brand-logo">Albrawe</span>
        <a href="/menu" class="menu-btn"><i class="fas fa-bars"></i> القائمة</a>
    </div>

    <div class="main-container">
        <!-- 🛡️ كرت الهوية التعريفي النيوني الفخم المطابق للصورة بالبكسل -->
        <div class="profile-card">
            
            <div class="avatar-wrapper">
                <!-- جلب صورة الهكر المحصنة والمرفوعة بداخل مجلد الموارد الثابتة -->
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

</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
