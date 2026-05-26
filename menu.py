import os

def generate_sidebar_html():
    """دالة توليد كود الـ HTML المطور للستارة لتقرأ الألعاب ديناميكياً من المجلد"""
    
    # 🎯 محرك قراءة الألعاب الذكي تلقائياً من مجلد static/my_games
    folder_path = os.path.join('static', 'my_games')
    games_list_html = ""
    
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                # جلب اسم المسار البرمجي من اسم الملف (مثلاً snake.txt يصبح /snake)
                route_name = os.path.splitext(file_name)[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().split('---')
                        if len(content) >= 3:
                            game_title = content[0].strip()
                            game_icon  = content[1].strip()
                            game_color = content[2].strip()
                            
                            # بناء سطر اللعبة ديناميكياً وحقنه في القائمة
                            games_list_html += f"""
                            <a href="/{route_name}" class="menu-item-clean" style="color: {game_color}; font-size: 13.5px;">
                                <i class="{game_icon}"></i> {game_title}
                            </a>
                            """
                except Exception:
                    pass

    # إذا كان المجلد فارغاً تماماً عرض رسالة تنبيهية
    if not games_list_html:
        games_list_html = '<p style="color:#8b949e; font-size:12px; text-align:center; padding:5px 0; margin:0;">لا توجد ألعاب نشطة حالياً</p>'

    html_content = f"""
    <style>
        .sidebar-links-wrapper {{ display: flex; flex-direction: column; gap: 4px; padding-top: 10px; }}
        .menu-item-clean {{ display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: 500; font-size: 14px; padding: 10px 12px; border-radius: 6px; transition: all 0.2s ease; background: transparent; border: 1px solid transparent; color: #c9d1d9; box-sizing: border-box; }}
        .menu-item-clean:hover {{ background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1); padding-right: 16px; }}
        .dropdown-toggle-btn-clean {{ width: 100%; text-align: right; display: flex; justify-content: space-between; align-items: center; cursor: pointer; background: transparent; border: 1px solid transparent; padding: 10px 12px; border-radius: 6px; font-weight: bold; font-family: inherit; color: #3fb950; transition: all 0.2s ease; }}
        .dropdown-toggle-btn-clean:hover {{ background: rgba(63, 185, 80, 0.1); border-color: rgba(63, 185, 80, 0.2); }}
        .dropdown-sub-menu-clean {{ display: none; flex-direction: column; gap: 2px; padding: 4px 20px 4px 0; margin-right: 12px; border-right: 1px dashed rgba(88, 166, 255, 0.3); }}
    </style>

    <div class="sidebar-links-wrapper">
        <a href="/" class="menu-item-clean" style="color: #c9d1d9;"><i class="fas fa-home" style="color: #8b949e;"></i> البوابة الرئيسية</a>
        
        <!-- 🎮 قائمة الألعاب الديناميكية المنسدلة والمقروءة بالكامل من مجلد السيرفر -->
        <div class="dropdown-wrapper" style="margin: 4px 0;">
            <button class="dropdown-toggle-btn-clean" onclick="toggleGamesDropdown(event)">
                <span><i class="fas fa-gamepad" style="margin-left: 8px;"></i> قائمة ألعاب النظام 🎮</span>
                <i class="fas fa-chevron-down" id="dropdownArrow" style="transition: 0.3s; font-size: 11px; color: #58a6ff;"></i>
            </button>
            <div class="dropdown-sub-menu-clean" id="gamesSubMenu">
                {games_list_html}
            </div>
        </div>
        
        <a href="/projects" class="menu-item-clean" style="color: #a371f7;"><i class="fas fa-project-diagram"></i> معرض المشاريع البرمجية</a>
        <a href="/about" class="menu-item-clean" style="color: #ff7b72;"><i class="fas fa-user-shield"></i> من نحن (About us)</a>
        <a href="/scripts" class="menu-item-clean" style="color: #388bfd;"><i class="fab fa-python"></i> إسكربتات بايثون</a>
        
        <hr style="border: 0; border-top: 1px solid #21262d; margin: 8px 0; width: 100%;">
        
        <a href="/maintenance" class="menu-item-clean" style="color: #f85149; font-size: 13px; opacity: 0.8;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة (صيانة)</a>
        <a href="https://t.me" target="_blank" class="menu-item-clean" style="color: #58a6ff; font-size: 13px;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام</a>
    </div>
    
    <script>
        function toggleGamesDropdown(event) {{
            event.stopPropagation(); event.preventDefault();
            const subMenu = document.getElementById('gamesSubMenu'), arrow = document.getElementById('dropdownArrow');
            if (subMenu.style.display === 'none' || subMenu.style.display === '') {{
                subMenu.style.display = 'flex'; arrow.style.transform = 'rotate(180deg)'; arrow.style.color = '#3fb950';
            }} else {{
                subMenu.style.display = 'none'; arrow.style.transform = 'rotate(0deg)'; arrow.style.color = '#58a6ff';
            }}
        }}
    </script>
    """
    return html_content
