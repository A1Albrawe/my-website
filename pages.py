from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

pages_blueprint = Blueprint('pages', __name__)

# رابط مكتبة الأيقونات الموحد
FA_CDN = '<link rel="stylesheet" href="https://cloudflare.com">'

def G_TEMPLATE(title, border_color, header, card_icon, card_title, card_text):
    """قالب مرن موحد لإنشاء الصفحات بشكل متناسق وتقليل تكرار الأكواد"""
    dynamic_links = generate_sidebar_html()
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Albrawe</title>
        {cdn}
        <style>
            body {{ font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
            .header-nav {{ background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid {color}; }}
            .menu-toggle {{ background: #21262d; border: 1px solid #30363d; color: {color}; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }}
            .sidebar-curtain {{ position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid {color}; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }}
            .close-btn {{ background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }}
            .menu-links {{ display: flex; flex-direction: column; gap: 12px; }}
            .menu-item {{ display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; }}
            .main-container {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }}
            .card {{ background: #161b22; border: 1px solid #30363d; border-top: 4px solid {color}; border-radius: 12px; padding: 30px; max-width: 500px; width: 100%; text-align: right; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }}
        </style>
    </head>
    <body>
        <div class="header-nav">
            <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
            <span style="color:#fff; font-weight:bold;">{header}</span>
        </div>
        <div class="sidebar-curtain" id="sidebarCurtain">
            <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
            <div class="menu-links">{links}</div>
        </div>
        <div class="main-container">
            <div class="card">
                <h3 style="color:#f0f6fc; margin-top:0;"><i class="{card_icon}"></i> {card_title}</h3>
                <p style="line-height:1.6; font-size:14px; color:#8b949e;">{card_text}</p>
            </div>
        </div>
        <script>
            function toggleSidebar(o) {{ document.getElementById('sidebarCurtain').style.right = o ? '0px' : '-300px'; }}
        </script>
    </body>
    </html>
    """.format(title=title, cdn=FA_CDN, color=border_color, header=header, links=dynamic_links, card_icon=card_icon, card_title=card_title, card_text=card_text)

@pages_blueprint.route('/projects')
def projects_page():
    return render_template_string(G_TEMPLATE("المشاريع", "#a371f7", "🚀 معرض المشاريع", "fas fa-code-branch", "مستودع ومشاريع المهندس البراوي", "يتم حالياً جرد وتحديث حزمة المشاريع البرمجية وتطوير واجهاتها السحابية لتظهر هنا قريباً بأعلى معايير الحماية والأمان."))

@pages_blueprint.route('/about')
def about_page():
    return render_template_string(G_TEMPLATE("من نحن", "#ff7b72", "👤 من نحن (About us)", "fas fa-user-shield", "الهوية البرمجية للمهندس البراوي", "نحن متخصصون في هندسة وتعديل تطبيقات البايثون (Flask Framework)، معالجة البيانات، وتأمين الواجهات السيبرانية من الثغرات البرمجية بأعلى كفاءة."))

@pages_blueprint.route('/scripts')
def scripts_page():
    return render_template_string(G_TEMPLATE("إسكربتات بايثون", "#388bfd", "⚙️ إسكربتات بايثون", "fab fa-python", "مكتبة الأدوات والأتمتة", "يتم رفع وفحص الإسكربتات البرمجية والأدوات الخدمية المصغرة المصممة بلغة البايثون لتوفيرها بشكل آمن قريباً."))

@pages_blueprint.route('/maintenance')
def maintenance_page():
    return render_template_string(G_TEMPLATE("تحت الصيانة", "#f85149", "🛠️ النظام تحت الصيانة", "fas fa-tools", "عذراً، القسم مغلق مؤقتاً", "بناءً على تحديثات الأمان الأخيرة، تم إيقاف استقبال الشكاوى المباشرة وتجري إعادة تهيئة شاملة لقواعد البيانات."))
