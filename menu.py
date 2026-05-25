# ملف إدارة وتعديل عناصر القائمة الجانبية الموحدة والمطورة للموقع
# تم دمج نظام القوائم المنسدلة (Dropdown) وإضافة الأقسام الجديدة بأمان كامل

def generate_sidebar_html():
    """دالة توليد كود الـ HTML المطور للستارة مع القائمة المنسدلة وأزرار التحكم"""
    
    html_content = """
    <!-- 📂 البوابة الرئيسية -->
    <a href="/" class="menu-item" style="color: #c9d1d9;"><i class="fas fa-home"></i> البوابة الرئيسية</a>
    
    <!-- 🎮 قائمة الألعاب المنسدلة (Games Dropdown) -->
    <div class="dropdown-wrapper" style="margin-bottom: 5px;">
        <button class="menu-item dropdown-toggle-btn" onclick="toggleGamesDropdown(event)" style="color: #3fb950; width: 100%; text-align: right; display: flex; justify-content: space-between; align-items: center; cursor: pointer; background: #21262d; border: 1px solid #30363d; padding: 12px; border-radius: 6px; font-weight: bold; font-family: inherit;">
            <span><i class="fas fa-gamepad"></i> الألعاب الحالية (Games) 🎮</span>
            <i class="fas fa-chevron-down" id="dropdownArrow" style="transition: 0.3s; font-size: 12px;"></i>
        </button>
        <div class="dropdown-sub-menu" id="gamesSubMenu" style="display: none; flex-direction: column; gap: 8px; padding: 8px 15px 0 0;">
            <a href="/snake" class="menu-item" style="color: #3fb950; font-size: 14px; padding: 10px;"><i class="fas fa-snake"></i> لعبة الثعبان الكلاسيكية 🐍</a>
            <a href="/tetris" class="menu-item" style="color: #d29922; font-size: 14px; padding: 10px;"><i class="fas fa-cubes"></i> لعبة التترس البكسلية 🧱</a>
        </div>
    </div>
    
    <!-- 📂 أقسام القائمة الرئيسية الجديدة المضافة بناءً على طلبك -->
    <a href="/projects" class="menu-item" style="color: #a371f7;"><i class="fas fa-project-diagram"></i> معرض المشاريع البرمجية 🚀</a>
    <a href="/about" class="menu-item" style="color: #ff7b72;"><i class="fas fa-user-shield"></i> من نحن (About us) 👤</a>
    <a href="/scripts" class="menu-item" style="color: #388bfd;"><i class="fab fa-python"></i> إسكربتات بايثون ⚙️</a>
    
    <!-- 🛠️ الشكاوى وروابط التواصل الخارجية -->
    <a href="/report" class="menu-item" style="color: #f85149;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة (تحت الصيانة) 🛠️</a>
    <a href="https://t.me" target="_blank" class="menu-item" style="color: #58a6ff;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام 🌐</a>
    
    <!-- ⚙️ سكربت جافا سكريبت المدمج للتحكم في فتح وإغلاق القائمة المنسدلة بسلاسة -->
    <script>
        function toggleGamesDropdown(event) {
            event.preventDefault();
            const subMenu = document.getElementById('gamesSubMenu');
            const arrow = document.getElementById('dropdownArrow');
            
            if (subMenu.style.display === 'none' || subMenu.style.display === '') {
                subMenu.style.display = 'flex';
                arrow.style.transform = 'rotate(180deg)';
                arrow.style.color = '#3fb950';
            } else {
                subMenu.style.display = 'none';
                arrow.style.transform = 'rotate(0deg)';
                arrow.style.color = '#58a6ff';
            }
        }
    </script>
    """
    return html_content
