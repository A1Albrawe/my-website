from flask import Blueprint, render_template_string

admin_blueprint = Blueprint('admin', __name__)

# قالب واجهة لوحة التحكم السرية للمطور والمبنية بالتصميم السيبراني الداكن المتناسق
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لوحة الإدارة السرية - Albrawe</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; direction: rtl; text-align: right; }
        .panel-title { color: #f85149; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; margin-top: 0; font-size: 22px; }
        .container { max-width: 700px; margin: 30px auto; background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; border-radius: 12px; padding: 25px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
        .report-item { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 8px; margin-bottom: 12px; position: relative; }
        .delete-btn { position: absolute; top: 15px; left: 15px; background: #f85149; color: #fff; border: none; padding: 5px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; font-family: inherit; }
        .delete-btn:hover { background: #da3633; }
        .info-header { color: #58a6ff; font-weight: bold; font-size: 14px; margin-bottom: 4px; }
        .info-date { color: #8b949e; font-size: 11px; margin-bottom: 8px; }
        .info-msg { color: #c9d1d9; font-size: 14px; line-height: 1.5; background: rgba(255,255,255,0.02); padding: 8px; border-radius: 4px; border-right: 3px solid #58a6ff; }
    </style>
</head>
<body>
    <div class="container">
        <h3 class="panel-title">🛠️ لوحة تحكم الإدارة واستعراض الشكاوى والمشاكل</h3>
        <div id="adminReportsContainer"></div>
    </div>

    <script>
        function loadAdminReports() {
            let allReports = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            const container = document.getElementById('adminReportsContainer');
            
            if (allReports.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:#8b949e; padding: 20px;">لا توجد شكاوى أو تقارير محفوظة في قاعدة البيانات حالياً.</div>';
                return;
            }
            
            let html = "";
            allReports.forEach(item => {
                html += `
                    <div class="report-item">
                        <button class="delete-btn" onclick="deleteReport(${item.id})">مسح التقرير ❌</button>
                        <div class="info-header">👤 المرسل: ${item.user}</div>
                        <div class="info-date">📅 التاريخ: ${item.date}</div>
                        <div class="info-msg">💬 تفاصيل المشكلة: ${item.details}</div>
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

        loadAdminReports();
    </script>
</body>
</html>
"""

# 🎯 تفعيل المسار الحصري والسري المباشر الجديد الخاص بك لحماية وتأمين الشكاوى
@admin_blueprint.route('/PASS')
def admin_page():
    return render_template_string(ADMIN_TEMPLATE)
