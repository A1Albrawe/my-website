# ملف إدارة وتعديل عناصر القائمة الجانبية الموحدة للموقع بالكامل
# يمكنك تعديل الأسماء، الألوان، أو الروابط من هنا مباشرة دون لمس الصفحات الأخرى

SIDEBAR_LINKS = [
    {"name": "📂 البوابة الرئيسية", "url": "/", "color": "#c9d1d9"},
    {"name": "🐍 لعبة الثعبان الكلاسيكية", "url": "/snake", "color": "#3fb950"},
    {"name": "🧱 لعبة التترس البكسلية", "url": "/tetris", "color": "#d29922"},
    {"name": "⚙️ إسكربتات بايثون", "url": "/scripts", "color": "#388bfd"},
    {"name": "🛠️ الإبلاغ عن مشكلة بالموقع", "url": "/report", "color": "#f85149"},
    {"name": "🌐 حسابي في التليجرام", "url": "https://t.me", "color": "#58a6ff", "external": True}
]

def generate_sidebar_html():
    """دالة توليد كود الـ HTML الخاص بالستارة ديناميكياً بناءً على المصفوفة أعلاه"""
    html_content = ""
    for link in SIDEBAR_LINKS:
        target = 'target="_blank"' if link.get("external") else ''
        html_content += f"""
        <a href="{link['url']}" {target} class="menu-item" style="color: {link['color']};">
            {link['name']}
        </a>
        """
    return html_content
