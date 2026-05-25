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
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; overflow-x: hidden; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #58a6ff; font-size: 20px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
        .neon-text-style { font-size: 18px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff; animation: neonPulseAnim 1.5s ease-in-out infinite alternate; }
        @keyframes neonPulseAnim { from { opacity: 0.8; } to { opacity: 1; } }
        .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #58a6ff; box-shadow: -10px 0 30px rgba(0,0,0,0.7); z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; }
        .sidebar-curtain.active { right: 0; }
        .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-weight: bold; font-family: inherit; }
        .menu-links { display: flex; flex-direction: column; gap: 12px; }
        .menu-item { display: flex; align-items: center; gap: 12px; color: #c9d1d9; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; transition: 0.2s; }
        .menu-item:hover { border-color: #58a6ff; color: #58a6ff; transform: translateX(-5px); }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px 20px; }
        .dev-portfolio-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 12px; padding: 35px 25px; max-width: 550px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; text-align: right; }
        .dev-avatar-img { width: 110px; height: 110px; border-radius: 16px; object-fit: cover; border: 2px solid #58a6ff; display: block; margin: 0 auto 20px auto; background: #0d1117; }
        .dev-name { margin: 0; font-size: 24px; color: #f0f6fc; text-align: center; font-weight: bold; }
        .dev-title { font-size: 13px; color: #58a6ff; text-align: center; margin: 5px 0 20px 0; font-weight: bold; }
        .info-section { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
        .info-line { font-size: 13px; margin: 10px 0; line-height: 1.6; color: #c9d1d9; }
        .info-line strong { color: #79c0ff; }
        .skills-container { display: flex; flex-direction: column; gap: 6px; margin-top: 10px; }
        .skill-badge { color: #3fb950; font-size: 13px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebar(true)"><i class="fas fa-bars"></i> القائمة</button>
        <span class="neon-text-style">Albrawe</span>
    </div>
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebar(false)"><i class="fas fa-times"></i> إغلاق القائمة</button>
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
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAADmElEQVR4nO2by3LbMAxFj+S99f9/uunGlS0nmSg6gZPr3AsYgZ6Z9lgisbYIArwSgKQEICmBSEoAklIEJC6fO6C+FvV1U19rUf9/FvV9S87Xg7F9WwREfV/V17vqHjFp789v6vszOf/7Vv9vXbC3fcsCIur7S0wWq9Xqf6uC/e1bFhB6V90jJu2FvWwRkNvqHjFpf/uWBYTeVTcm7YW9bBGQ++oeMWl/+5YFhN5VNybthb1sEZD76h4xaX/7lgaE3pEak/bCXtSAnK/Z/fNve6V2pMY0bS/sRQtIep7T85wexfXUEx6pMRE7gYw9RGoX6Y6e96TeAen+XGMXO8GMOvG8f++wEzsh6Y6eEzuJnXjev3fYiZ2Q7ggydiY78bx/77ATOyHpAInu6Dmxk9iJ5/17h53YCemOMGNnshPP+/cOO7ETImYfOnYmO4GMCUgn8v69w07shKQDxNiZ7AQyJiCdyPv3DjuxE5LuADJ2JjvxvH/vsBM7IekAie7oObGT2Innvb9FhD1E6pUak/bCXrSI0DtSY9Je2IsakPM1u3/+ba/UjtSYpu2FvWgBSc9zep7To7ieesIjNSZiJ5Cxh0jtIt3R857UOyDdn2vsYieYUSee9+8ddmInJN3Rc2InsRPP+/cOO7ET0h1Bxs5kJ5737x12YickHSDCHT0ndhI78bx/77ATOyHdEWbsTHbiGf987oD6WtTXTX2tRf3/WdT3LTlfD8b2bREQ9X1VX++qe8SkvT+/qe/P5PzvW/2/dcHe9vX6F4R6m7fPqX1C7vNve6F+6eX7hGgBof+R8m96X6pxjRtL+xFC0h6ntPznB7F9dQTHqkxEf9K7Y6eEzuJnXjee1vvALpD6v5cYxc7wYw68bz3tggIe9Z6f4vUfX9qTPT+U6/wYw9hD5F6D0i9wvtPeMRE7IDUXU/I/wVIdzx9f+zETmInPInV/vIOfyD/GZCOn/ePEzuJnXAnvPrn/6TscYg66fXp/uH92XvYCe78Wvtbe9h7CHfCPfG9g/YQ7oR74nsH7SHcCc/E977/H+wE7YRn4vvff+9gJ2gnPBPvff8bX9oJ7oT74vsA7CHcCTbEFFD2EO6EGmEfbA/hTggRthG0h3An6Ai6CbSHcCfUCNpDeM6EEDH/B1/aCdqJN8L9N760E9wJ7oT7A9gJ7gR3gjsH7gR3gjsH7ty3+g/Oq3Zf8mD7lgVExPhg+5YFBM/vXzT76N6h/pA6AAAAAElFTkSuQmCC" alt="Albrawe" class="dev-avatar-img">
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
        function toggleSidebar(o) { document.getElementById('sidebarCurtain').style.right = o ? '0px' : '-300px'; }
    </script>
</body>
</html>
"""

@home_blueprint.route('/')
def home_page():
    return render_template_string(HOME_TEMPLATE)
