# ملف إدارة وتعديل عناصر القائمة الجانبية الموحدة والمطورة للموقع

def generate_sidebar_html():
    """دالة توليد كود الـ HTML المطور للستارة مع القائمة المنسدلة الذكية والمعزولة"""
    
    html_content = """
    <!-- 📂 البوابة الرئيسية -->
    <a href="/" class="menu-item" style="color: #c9d1d9;"><i class="fas fa-home"></i> البوابة الرئيسية</a>
    
    <!-- 🎮 قائمة الألعاب المنسدلة المعزولة -->
    <div class="dropdown-wrapper" style="margin-bottom: 5px;">
        <button class="menu-item dropdown-toggle-btn" onclick="toggleGamesDropdown(event)" style="color: #3fb950; width: 100%; text-align: right; display: flex; justify-content: space-between; align-items: center; cursor: pointer; background: #21262d; border: 1px solid #30363d; padding: 12px; border-radius: 6px; font-weight: bold; font-family: inherit;">
            <span><i class="fas fa-gamepad"></i> الألعاب الحالية (Games) 🎮</span>
            <i class="fas fa-chevron-down" id="dropdownArrow" style="transition: 0.3s; font-size: 12px; color: #58a6ff;"></i>
        </button>
        <div class="dropdown-sub-menu" id="gamesSubMenu" style="display: none; flex-direction: column; gap: 8px; padding: 8px 15px 0 0;">
            <!-- تم تصحيح الأيقونة هنا إلى fa-dragon لضمان ظهورها بشكل صحيح -->
            <a href="/snake" class="menu-item" style="color: #3fb950; font-size: 14px; padding: 10px;"><i class="fas fa-dragon"></i> لعبة الثعبان الكلاسيكية 🐍</a>
            <a href="/tetris" class="menu-item" style="color: #d29922; font-size: 14px; padding: 10px;"><i class="fas fa-cubes"></i> لعبة التترس البكسلية 🧱</a>
        </div>
    </div>
    
    <!-- 📂 أقسام القائمة الرئيسية الجديدة المضافة بناءً على طلبك -->
    <a href="/projects" class="menu-item" style="color: #a371f7;"><i class="fas fa-project-diagram"></i> معرض المشاريع البرمجية 🚀</a>
    <a href="/about" class="menu-item" style="color: #ff7b72;"><i class="fas fa-user-shield"></i> من نحن (About us) 👤</a>
    <a href="/scripts" class="menu-item" style="color: #388bfd;"><i class="fab fa-python"></i> إسكربتات بايثون ⚙️</a>
    
    <!-- 🛠️ الشكاوى تم تحويل الرابط للمسار الجديد المقفل كلياً تحت الصيانة -->
    <a href="/maintenance" class="menu-item" style="color: #f85149;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة (تحت الصيانة) 🛠️</a>
    
    <!-- 🌐 تم تحديث رابط التليجرام الخاص بك بنجاح -->
    <a href="https://t.me/I_Albrawe" target="_blank" class="menu-item" style="color: #58a6ff;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام 🌐</a>
    
    <script>
        function toggleGamesDropdown(event) {
            event.stopPropagation();
            event.preventDefault();
            const subMenu = document.getElementById('gamesSubMenu');
            const arrow = document.getElementById('dropdownArrow');
            if (subMenu.style.display === 'none' || subMenu.style.display === '') {
                subMenu.style.display = 'block'; // تم تعديلها إلى block لضمان التوافق العمودي وتجنب التداخل
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
