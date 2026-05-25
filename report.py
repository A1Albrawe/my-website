from flask import Blueprint, render_template_string

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
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #0d1117;
            color: #c9d1d9; 
            padding: 0; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            box-sizing: border-box;
        }
        .header-nav {
            background-color: #161b22;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #58a6ff;
        }
        .back-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #58a6ff;
            padding: 6px 15px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
        }
        .neon-title {
            color: #fff;
            font-weight: bold;
            text-shadow: 0 0 5px #58a6ff;
            cursor: pointer;
            user-select: none;
        }
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .dev-portfolio-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-top: 4px solid #58a6ff;
            border-radius: 12px;
            padding: 30px 20px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            box-sizing: border-box;
            text-align: right;
        }
        .form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; }
        label { font-weight: bold; font-size: 13px; color: #79c0ff; }
        .input-field {
            padding: 10px;
            font-size: 14px;
            border: 1px solid #30363d;
            background: #0d1117;
            font-family: inherit;
            font-weight: bold;
            color: #c9d1d9;
            border-radius: 6px;
            width: 100%;
            box-sizing: border-box;
        }
        .input-field:focus { border-color: #58a6ff; outline: none; }
        textarea.input-field { resize: none; height: 80px; }
        .submit-btn {
            background: #238636;
            color: #ffffff;
            border: 1px solid #2ea44f;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            font-family: inherit;
            transition: 0.2s;
        }
        .submit-btn:hover { background: #2ea44f; }
        
        /* لوحة التحكم السرية بالمشاكل والتقارير */
        .admin-panel-area {
            display: none;
            margin-top: 20px;
            background: #161b22;
            border: 1px solid #f85149;
            border-radius: 8px;
            padding: 15px;
            width: 100%;
            box-sizing: border-box;
        }
        .report-item {
            background: #0d1117;
            border: 1px solid #30363d;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 10px;
            position: relative;
        }
        .delete-report-btn {
            position: absolute;
            top: 10px;
            left: 10px;
            background: #f85149;
            color: #fff;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span class="neon-title" onclick="triggerAdminCount()">💾 مركز الشكاوى وقاعدة البيانات</span>
    </div>

    <div class="main-container">
        <div class="dev-portfolio-card">
            <h3 style="margin-top:0; color:#f0f6fc; border-bottom:1px solid #30363d; padding-bottom:10px;"><i class="fas fa-tools"></i> الإبلاغ عن مشكلة أو اقتراح</h3>
            <form id="reportForm" onsubmit="saveReportLocally(event)">
                <div class="form-group">
                    <label>اسم المستخدم الكودى:</label>
                    <input type="text" id="userName" class="input-field" required maxlength="15">
                </div>
                <div class="form-group">
                    <label>تفاصيل المشكلة الفنية:</label>
                    <textarea id="issueDetails" class="input-field" placeholder="اشرح المشكلة التقنية أو الاقتراح الفني هنا..." required maxlength="250"></textarea>
                </div>
                <button type="submit" class="submit-btn">📥 تسجيل وحفظ التقرير الفوري</button>
            </form>
            
            <!-- لوحة المدير السرية المستعرضة للبيانات المتراكمة -->
            <div class="admin-panel-area" id="adminPanel">
                <h4 style="margin-top:0; color:#f85149; border-bottom:1px solid #30363d; padding-bottom:5px;">🛠️ لوحة تحكم الإدارة واستعراض الشكاوى</h4>
                <div id="adminReportsContainer"></div>
            </div>
        </div>
    </div>

    <script>
        function setupUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) { document.getElementById('userName').value = savedUser; }
            loadAdminReports();
        }

        function saveReportLocally(event) {
            event.preventDefault();
            const user = document.getElementById('userName').value.trim();
            const details = document.getElementById('issueDetails').value.trim();
            
            let allReports = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            allReports.unshift({
                id: Date.now(),
                user: user,
                details: details,
                date: new Date().toLocaleString('ar-EG')
            });
            
            localStorage.setItem('albrawe_central_db', JSON.stringify(allReports));
            document.getElementById('issueDetails').value = "";
            alert("✅ تم حفظ تقريرك بنجاح داخل قاعدة البيانات الموحدة للموقع!");
            loadAdminReports();
        }

        function loadAdminReports() {
            let allReports = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            const container = document.getElementById('adminReportsContainer');
            if (allReports.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:#8b949e;">لا توجد شكاوى أو تقارير محفوظة حالياً.</div>';
                return;
            }
            let html = "";
            allReports.forEach(item => {
                html += `
                    <div class="report-item">
                        <button class="delete-report-btn" onclick="deleteReport(${item.id})">حذف ❌</button>
                        <div style="color:#58a6ff; font-weight:bold; font-size:12px;">👤 المرسل: ${item.user}</div>
                        <div style="color:#8b949e; font-size:11px; margin:4px 0;">📅 التاريخ: ${item.date}</div>
                        <div style="color:#c9d1d9; font-size:13px; line-height:1.4;">💬 التفاصيل: ${item.details}</div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        function deleteReport(id) {
            let allReports = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            allReports = allReports.filter(item => item.id !== id);
            localStorage.setItem('albrawe_central_db', JSON.stringify(allReports));
            loadAdminReports();
        }

        // كود تشغيل اللوحة السرية بالضغط 3 مرات متتالية على العنوان العلوي
        let clickCount = 0;
        function triggerAdminCount() {
            clickCount++;
            if (clickCount >= 3) {
                const panel = document.getElementById('adminPanel');
                panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
                clickCount = 0;
            }
        }

        setupUser();
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
