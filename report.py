from flask import Blueprint, render_template_string
from menu import generate_sidebar_html

report_blueprint = Blueprint('report', __name__)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>مركز الدعم الفني - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f85149; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #f85149; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
        
        /* ✨ تأثير النيون لاسم المهندس البراوي في المنتصف للتوجيه للرئيسية */
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #f85149, 0 0 10px #f85149; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #f85149; }
        
        .sidebar-curtain { position: fixed; top: 0; right: -320px; width: 300px; height: 100%; background-color: #161b22; border-left: 2px solid #f85149; z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; overflow-y: auto; }
        .sidebar-curtain.active { right: 0; }
        .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; width: 100%; text-align: right; }
        .menu-links { display: flex; flex-direction: column; gap: 12px; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .report-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; border-radius: 12px; padding: 35px 25px; max-width: 460px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; text-align: right; }
        
        .form-group { margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }
        .form-group label { font-size: 13px; font-weight: bold; color: #8b949e; }
        textarea { padding: 12px; background: #0d1117; border: 1px solid #30363d; border-radius: 8px; color: #fff; font-family: inherit; font-size: 13.5px; box-sizing: border-box; width: 100%; height: 120px; resize: none; }
        textarea:focus { border-color: #f85149; outline: none; box-shadow: 0 0 10px rgba(248, 81, 73, 0.15); }
        
        .submit-btn { background: #f85149; color: #fff; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 14px; width: 100%; transition: 0.2s; box-shadow: 0 4px #9e2a2b; }
        .submit-btn:active { transform: translateY(2px); box-shadow: 0 1px #9e2a2b; }
        .status-msg { display: none; padding: 10px; border-radius: 6px; font-size: 12.5px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebar(true)">☰ القائمة</button>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="color:#fff; font-weight:bold;">⚠️ البلاغات</span>
    </div>
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebar(false)">❌ إغلاق القائمة</button>
        <div class="menu-links">SIDEBAR_LINKS_PLACEHOLDER</div>
    </div>
    <div class="main-container">
        <div class="report-card">
            <h3 style="color:#f0f6fc; margin-top:0; border-bottom:1px solid #30363d; padding-bottom:8px;"><i class="fas fa-exclamation-triangle" style="color: #f85149; margin-left: 6px;"></i> مركز إرسال البلاغات الفنية</h3>
            <p style="color:#8b949e; font-size:12.5px; line-height:1.6; margin: 0 0 20px 0;">إذا واجهت أي عطل في الألعاب أو مشكلة في استقرار الواجهات، اكتب تفاصيل البلاغ أدناه وسيتم رفعه للـ الآدمن سحابياً فوراً.</p>
            
            <div class="status-msg" id="statusMessage"></div>
            
            <div class="form-group">
                <label>تفاصيل المشكلة أو الشكوى:</label>
                <textarea id="complaintDetails" placeholder="اكتب هنا ما يواجهك بالتفصيل البرمجي..."></textarea>
            </div>
            <button class="submit-btn" onclick="sendComplaintToServer()">إرسال البلاغ المشفر عبر الإنترنت 🚀</button>
        </div>
    </div>
    <script>
        function toggleSidebar(o) {
            const curtain = document.getElementById('sidebarCurtain');
            if(o) curtain.classList.add('active'); else curtain.classList.remove('active');
        }

        // ✅ معالج المزامنة الإنترنتية: رفع الشكوى من متصفح المستخدم إلى خادم السيرفر حياً
        function sendComplaintToServer() {
            const text = document.getElementById('complaintDetails').value.trim();
            const msgBox = document.getElementById('statusMessage');
            
            if(!text) {
                alert("❌ خطأ: يرجى كتابة تفاصيل الشكوى أولاً قبل الضغط على إرسال!");
                return;
            }
            
            // سحب الاسم الرمزي للزائر من ذاكرة المتصفح
            let storedUser = localStorage.getItem('snake_last_user') || 'زائر_مجهول';
            
            // إرسال طلب الـ POST للإنترنت
            fetch('/api/submit_complaint', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user: storedUser, details: text })
            })
            .then(res => res.json())
            .then(data => {
                if(data.status === 'success') {
                    msgBox.style.display = 'block';
                    msgBox.style.background = 'rgba(63, 185, 80, 0.15)';
                    msgBox.style.color = '#3fb950';
                    msgBox.innerText = "✅ تم إرسال بلاغك بنجاح عبر الإنترنت وتخزينه في لوحة التحكم!";
                    document.getElementById('complaintDetails').value = ""; // تصفير الحقل
                }
            })
            .catch(() => {
                alert("❌ خطأ سحابي: تعذر الاتصال بالسيرفر! تحقق من شبكة الإنترنت.");
            });
        }
    </script>
</body>
</html>
""".replace("SIDEBAR_LINKS_PLACEHOLDER", generate_sidebar_html())

# تشغيل المسار وإلغاء صفحة الصيانة القديمة تماماً
@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)

# التوجيه التلقائي للمسار الاحتياطي ليعود لصفحة البلاغات النشطة
@report_blueprint.route('/maintenance')
def old_report_page():
    return render_template_string(REPORT_TEMPLATE)
