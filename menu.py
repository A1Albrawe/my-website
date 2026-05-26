# ملف إدارة وتعديل عناصر القائمة الجانبية الموحدة والمطورة للموقع

def generate_sidebar_html():
    """دالة توليد كود الـ HTML المطور للستارة بتنسيق بصري أنيق وقوائم شجرية خفيفة"""
    
    html_content = """
    <style>
        /* 👥 تنسيق روابط القائمة الجانبية الجديد والأنيق */
        .sidebar-links-wrapper {
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-top: 10px;
        }
        
        .menu-item-clean {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            padding: 10px 12px;
            border-radius: 6px;
            transition: all 0.2s ease;
            background: transparent;
            border: 1px solid transparent;
            color: #c9d1d9;
        }
        
        /* تأثير التمرير الخفيف والأنيق وبدون ألوان رمادية مصمتة */
        .menu-item-clean:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.1);
            padding-right: 16px; /* حركة إزاحة صغيرة جمالية عند التمرير */
        }
        
        /* 🎮 تنسيق الزر الرئيسي لقائمة الألعاب المنسدلة */
        .dropdown-toggle-btn-clean {
            width: 100%;
            text-align: right;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            background: transparent;
            border: 1px solid transparent;
            padding: 10px 12px;
            border-radius: 6px;
            font-weight: bold;
            font-family: inherit;
            color: #3fb950;
            transition: all 0.2s ease;
        }
        
        .dropdown-toggle-btn-clean:hover {
            background: rgba(63, 185, 80, 0.1);
            border-color: rgba(63, 185, 80, 0.2);
        }
        
        /* 🧱 التنسيق الشجري الداخلي للألعاب */
        .dropdown-sub-menu-clean {
            display: none;
            flex-direction: column;
            gap: 2px;
            padding: 4px 20px 4px 0;
            margin-right: 12px;
            border-right: 1px dashed rgba(88, 166, 255, 0.3); /* خط شجري جانبي خفيف يربط الألعاب ببعضها */
        }
    </style>

    <div class="sidebar-links-wrapper">
        <!-- 📂 البوابة الرئيسية -->
        <a href="/" class="menu-item-clean" style="color: #c9d1d9;"><i class="fas fa-home" style="color: #8b949e;"></i> البوابة الرئيسية</a>
        
        <!-- 🎮 قائمة الألعاب المنسدلة المعزولة والشجرية -->
        <div class="dropdown-wrapper" style="margin: 4px 0;">
            <button class="dropdown-toggle-btn-clean" onclick="toggleGamesDropdown(event)">
                <span><i class="fas fa-gamepad" style="margin-left: 8px;"></i> الألعاب الحالية (Games)</span>
                <i class="fas fa-chevron-down" id="dropdownArrow" style="transition: 0.3s; font-size: 11px; color: #58a6ff;"></i>
            </button>
            <div class="dropdown-sub-menu-clean" id="gamesSubMenu">
                <a href="/snake" class="menu-item-clean" style="color: #3fb950; font-size: 13.5px;"><i class="fas fa-dragon"></i> لعبة الثعبان الكلاسيكية</a>
                <a href="/tetris" class="menu-item-clean" style="color: #d29922; font-size: 13.5px;"><i class="fas fa-cubes"></i> لعبة التترس البكسلية</a>
            </div>
        </div>
        
        <!-- 📂 أقسام القائمة الرئيسية المحدثة بتنسيق ناعم وشديد التناسق -->
        <a href="/projects" class="menu-item-clean" style="color: #a371f7;"><i class="fas fa-project-diagram"></i> معرض المشاريع البرمجية</a>
        <a href="/about" class="menu-item-clean" style="color: #ff7b72;"><i class="fas fa-user-shield"></i> من نحن (About us)</a>
        <a href="/scripts" class="menu-item-clean" style="color: #388bfd;"><i class="fab fa-python"></i> إسكربتات بايثون</a>
        
        <!-- فاصل جمالي خفيف لفصل الصفحات الأساسية عن روابط التواصل والصيانة -->
        <hr style="border: 0; border-top: 1px solid #21262d; margin: 8px 0; width: 100%;">
        
        <!-- 🛠️ الروابط الفرعية والدعم -->
        <a href="/maintenance" class="menu-item-clean" style="color: #f85149; font-size: 13px; opacity: 0.8;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة (صيانة)</a>
        <a href="https://t.me" target="_blank" class="menu-item-clean" style="color: #58a6ff; font-size: 13px;"><i class="fab fa-telegram-plane"></i> حسابي في التليجرام</a>
    </div>
    
    <script>
        function toggleGamesDropdown(event) {
            event.stopPropagation();
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
