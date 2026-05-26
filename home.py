from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

# حقن كافة تنسيقات النيون لعام 2026 بشكل صافٍ ومحمي تماماً من التداخل النصي
HOME_CSS = """
<style>
    body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; margin: 0; padding: 15px; box-sizing: border-box; display: flex; flex-direction: column; min-height: 100vh; }
    .container { width: 100%; max-width: 1200px; margin: 0 auto; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    
    .main-title { font-size: 26px; font-weight: bold; color: #fff; text-shadow: 0 0 10px #58a6ff; margin-bottom: 5px; text-align: center; }
    .sub-title { font-size: 13px; color: #8b949e; text-align: center; margin-bottom: 30px; font-weight: bold; }
    
    .arcade-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; margin-bottom: 30px; }
    
    .game-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; text-decoration: none; color: inherit; transition: 0.2s ease; display: flex; flex-direction: column; align-items: center; gap: 10px; position: relative; overflow: hidden; }
    .game-card:hover { transform: translateY(-3px); border-color: #58a6ff; box-shadow: 0 10px 25px rgba(88,166,255,0.15); }
    
    .game-icon { font-size: 36px; margin-bottom: 5px; }
    .game-title { font-size: 16px; font-weight: bold; color: #fff; margin: 0; }
    .game-desc { font-size: 11.5px; color: #8b949e; margin: 0; line-height: 1.4; }
    
    .card-snake { border-top: 4px solid #3fb950; }
    .card-snake .game-icon { color: #3fb950; }
    .card-tetris { border-top: 4px solid #d29922; }
    .card-tetris .game-icon { color: #d29922; }
    .card-xo { border-top: 4px solid #a371f7; }
    .card-xo .game-icon { color: #a371f7; }
    .card-shooter { border-top: 4px solid #388bfd; }
    .card-shooter .game-icon { color: #388bfd; }
    .card-clicker { border-top: 4px solid #ff7b72; }
    .card-clicker .game-icon { color: #ff7b72; }
    .card-cards { border-top: 4px solid #58a6ff; }
    .card-cards .game-icon { color: #58a6ff; }
    
    .footer-bar { text-align: center; padding-top: 15px; border-top: 1px solid #21262d; font-size: 11px; color: #8b949e; font-family: monospace; }
    .footer-bar a { color: #58a6ff; text-decoration: none; font-weight: bold; }
</style>
"""
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe Arcade | المنصة الرئيسية الموحدة</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    
    <!-- 🟢 1. أيقونة تبويب المتصفح الصغيرة الفلورسنتية (Favicon) -->
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">

    <!-- 🟢 2. وسوم البطاقة المصغرة الكبرى لمنصات السوشيال (WhatsApp / Facebook) -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://vercel.app">
    <meta property="og:title" content="Albrawe Arcade & Cyber Analytics">
    <meta property="og:description" content="البوابة الرسمية لألعاب الأركيد النيونية ومنظومة الرصد البياني الذكي">
    <meta property="og:image" content="https://vercel.appstatic/thumbnail.png">

    <!-- 🟢 3. وسوم البطاقة المصغرة المخصصة لمنصة X -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Albrawe Arcade & Cyber Analytics">
    <meta name="twitter:description" content="البوابة الرسمية لألعاب الأركيد النيونية ومنظومة الرصد البياني الذكي">
    <meta name="twitter:image" content="https://vercel.appstatic/thumbnail.png">
    
    """ + HOME_CSS + """
</head>
<body>
    <div class="container">
        <h1 class="main-title"><i class="fas fa-gamepad" style="color:#58a6ff;"></i> منصة أركيد البراوي العالمية</h1>
        <p class="sub-title">اختر بوابتك التنافسية المفضلة؛ جميع مدد اللعب مرصودة ومحمية سيبرانياً للأبد 🛰️</p>
        
        <div class="arcade-grid">
            <!-- 🐍 1. لعبة الثعبان -->
            <a href="/snake" class="game-card card-snake">
                <div class="game-icon">🐍</div>
                <h3 class="game-title">ثعبان النيون</h3>
                <p class="game-desc">التقط التفاح المشع وحطم الأرقام القياسية مع تفعيل خوارزمية التسارع اللانهائي.</p>
            </a>
            
            <!-- 🧱 2. لعبة التترس -->
            <a href="/tetris" class="game-card card-tetris">
                <div class="game-icon">🧱</div>
                <h3 class="game-title">تترس التطور</h3>
                <p class="game-desc">قم بتركيب المكعبات الهندسية الفلورسنتية القياسية مع ميزة التفاف الحواف الفوري.</p>
            </a>
            
            <!-- ❌ 3. لعبة XO -->
            <a href="/xo" class="game-card card-xo">
                <div class="game-icon">❌</div>
                <h3 class="game-title">مصفوفة X-O</h3>
                <p class="game-desc">المواجهة الثنائية الكلاسيكية داخل لوحة الذكاء الفوري النيونية المضيئة.</p>
            </a>
            
            <!-- 🚀 4. قاصف الفضاء -->
            <a href="/shooter" class="game-card card-shooter">
                <div class="game-icon">🚀</div>
                <h3 class="game-title">قاصف الفضاء الكلاسيكي</h3>
                <p class="game-desc">احمِ المجرة بواسطة 3 قلوب محاولات، ودمر أسراب الأعداء وواجه الزعيم الأكبر.</p>
            </a>
            
            <!-- ⚡ 5. تحدي النقر -->
            <a href="/clicker" class="game-card card-clicker">
                <div class="game-icon">⚡</div>
                <h3 class="game-title">تحدي النقر السريع</h3>
                <p class="game-desc">اختبر سرعة استجابة أصابعك واجمع مئات النقرات الصاعقة خلال 10 ثوانٍ فقط.</p>
            </a>
            
            <!-- 🃏 6. لعبة البطاقات الجديدة -->
            <a href="/card_game" class="game-card card-cards">
                <div class="game-icon">🃏</div>
                <h3 class="game-title">تحدي كروت الذاكرة</h3>
                <p class="game-desc">اللعبة السادسة الجديدة! قم بمطابقة الرموز المخفية واختبر كفاءة ذاكرتك اللحظية.</p>
            </a>
        </div>
        
        <div class="footer-bar">
            <span>منصة Albrawe لعام 2026 © جميع الحقوق محفوظة برمجياً ومحمية بالكامل. | </span>
            <a href="/albrawe-admin-panel-2026?key=open_gate_key_final_2026" target="_blank">لوحة المراقبة 🔐</a>
        </div>
    </div>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_HTML)
