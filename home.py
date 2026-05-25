from flask import Blueprint, render_template_string

home_blueprint = Blueprint('home', __name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع Albrawe - الرئيسية</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #f0f2f5; padding: 50px; margin: 0; }
        .menu-btn { position: fixed; top: 20px; right: 20px; font-size: 20px; background: #1877f2; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; z-index: 1000; font-weight: bold; display: flex; align-items: center; gap: 8px; }
        .sidebar { height: 100%; width: 0; position: fixed; z-index: 999; top: 0; right: 0; background-color: #1a1a1a; overflow-x: hidden; transition: 0.3s; padding-top: 80px; text-align: right; box-shadow: -4px 0 15px rgba(0,0,0,0.4); }
        .sidebar a, .sidebar .dropdown-btn { padding: 15px 25px; text-decoration: none; font-size: 18px; color: #b3b3b3; display: flex; align-items: center; gap: 12px; transition: 0.2s; border-bottom: 1px solid #2d2d2d; background: none; border-top: none; border-left: none; border-right: none; width: 100%; text-align: right; cursor: pointer; font-family: inherit; box-sizing: border-box; }
        .sidebar a:hover, .sidebar .dropdown-btn:hover { color: white; background-color: #1877f2; }
        .dropdown-container { display: none; background-color: #242424; padding-right: 20px; }
        .dropdown-container a { font-size: 16px; border-bottom: 1px solid #333; }
        .sidebar .close-btn { position: absolute; top: 20px; left: 20px; font-size: 28px; color: #bbb; cursor: pointer; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; max-width: 500px; margin-top: 60px; }
        h1 { color: #1877f2; margin-top: 0; }
        .telegram-btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; background-color: #0088cc; color: white; text-decoration: none; padding: 14px 30px; border-radius: 30px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 12px rgba(0, 136, 204, 0.3); transition: 0.3s; }
        .telegram-btn:hover { background-color: #0077b3; transform: translateY(-2px); }
        .footer { margin-top: 30px; color: #888; font-size: 14px; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
</head>
<body>
    <button class="menu-btn" onclick="toggleNav()"><i class="fas fa-bars"></i> القائمة</button>
    <div id="mySidebar" class="sidebar">
        <span class="close-btn" onclick="toggleNav()">&times;</span>
        <a href="/"><i class="fas fa-home"></i> الصفحة الرئيسية</a>
        <a href="#"><i class="fas fa-code"></i> المشاريع</a>
        <button class="dropdown-btn" onclick="toggleDropdown()"><i class="fas fa-link"></i> روابط أخرى <i class="fas fa-caret-down" style="margin-right: auto;"></i></button>
        <div id="gamesDropdown" class="dropdown-container">
            <a href="/snake"><i class="fas fa-gamepad"></i> لعبة الثعبان</a>
            <a href="/tetris"><i class="fas fa-cubes"></i> لعبة التترس</a>
        </div>
        <a href="#"><i class="fas fa-info-circle"></i> حول هذا</a>
    </div>
    <div class="container">
        <h1>مرحباً بك في موقع albrawe</h1>
        <p>تم تشغيل الموقع بنجاح وهو الآن متاح للجميع على الإنترنت!</p>
        <a href="https://t.me" target="_blank" class="telegram-btn"><i class="fab fa-telegram-plane"></i> تليجرام @a1albrawe</a>
        <div class="footer">يعمل بواسطة Python & Flask</div>
    </div>
    <script>
        let sidebarOpen = false;
        function toggleNav() { const sidebar = document.getElementById("mySidebar"); sidebar.style.width = sidebarOpen ? "0" : "250px"; sidebarOpen = !sidebarOpen; }
        function toggleDropdown() { const dropdown = document.getElementById("gamesDropdown"); dropdown.style.display = dropdown.style.display === "block" ? "none" : "block"; }
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)
