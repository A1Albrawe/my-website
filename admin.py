from flask import Blueprint, request, jsonify, render_template_string, session, redirect

admin_blueprint = Blueprint('admin', __name__)

# 🔒 بيانات اعتماد لوحة الإدارة المحصنة (يمكنك تعديلها من هنا بأي وقت)
ADMIN_USER = "albrawe"
ADMIN_PASS = "PASS2026"

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحليلات والرقابة السرية | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; }
        .container { max-width: 1100px; margin: 0 auto; }
        .main-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; padding-bottom: 15px; margin-bottom: 25px; }
        .logout-btn { background: #f85149; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; font-family: inherit; }
        .analytics-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; }
        .stat-box h5 { margin: 0 0 8px 0; color: #8b949e; font-size: 13px; }
        .stat-box p { margin: 0; font-size: 22px; font-weight: bold; color: #58a6ff; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #0d1117; border-radius: 8px; overflow: hidden; }
        th, td { padding: 12px 15px; text-align: right; border-bottom: 1px solid #30363d; font-size: 13px; }
        th { background-color: #21262d; color: #79c0ff; font-weight: bold; }
        tr:hover { background-color: rgba(88, 166, 255, 0.03); }
        .badge { padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; color: #fff; }
        .bg-android { background: #3fb950; } .bg-iphone { background: #ffd700; color: #000; } .bg-windows { background: #1f6feb; }
        .report-txt { background: rgba(248, 81, 73, 0.1); border-right: 3px solid #f85149; padding: 6px; margin: 4px 0; border-radius: 0 4px 4px 0; font-size: 12px; }
        .clear-db-btn { background: #d29922; color: #000; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 12px; }
    </style>
</head>
"""
<body>
    <div class="container">
        <div class="main-header">
            <h2 style="margin:0; color:#fff;">📊 رادار الرقابة وتحليلات الزوار المركزي</h2>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="clear-db-btn" onclick="clearLogsDatabase()">تصفير السجلات 🗑️</button>
                <a href="/albrawe-admin/logout" class="logout-btn">تسجيل الخروج 🚪</a>
            </div>
        </div>
        <div class="grid-stats">
            <div class="stat-box"><h5>إجمالي الزيارات النشطة</h5><p id="totalViews">0</p></div>
            <div class="stat-box"><h5>متوسط الوقت بالموقع</h5><p id="avgTime">0 ثانية</p></div>
            <div class="stat-box"><h5>إجمالي الشكاوى النشطة</h5><p id="totalComplaints">0</p></div>
        </div>
        <div class="analytics-card">
            <h3 style="margin-top:0; color:#79c0ff; border-bottom:1px solid #30363d; padding-bottom:8px;">👥 سجل حركة بيانات المستخدمين بالتفصيل</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>الاسم الرمزي</th>
                            <th>نوع الهاتف / المتصفح</th>
                            <th>وقت الدخول</th>
                            <th>الوقت المستغرق</th>
                            <th>مدة الألعاب (ثعبان / تترس)</th>
                            <th>الشكاوى والبلاغات المرسلة</th>
                        </tr>
                    </thead>
                    <tbody id="logsTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>
    <script>
        function fetchAndRenderAnalytics() {
            fetch('/api/admin_get_all_data')
            .then(res => res.json())
            .then(data => {
                let db = data.analytics || [];
                let complDB = data.reports || [];
                document.getElementById('totalViews').innerText = db.length;
                document.getElementById('totalComplaints').innerText = complDB.length;
                let totalSeconds = 0;
                db.forEach(item => { totalSeconds += (item.duration || 0); });
                document.getElementById('avgTime').innerText = db.length > 0 ? Math.round(totalSeconds / db.length) + " ثانية" : "0 ثانية";
                let html = "";
                if(db.length === 0) {
                    html = '<tr><td colspan="6" style="text-align:center; color:#8b949e;">لا توجد بيانات حركة مستخدمين مسجلة حتى الآن.</td></tr>';
                } else {
                    db.forEach(user => {
                        let deviceBadge = '<span class="badge bg-windows">Windows/PC</span>';
                        let ua = (user.userAgent || "").toLowerCase();
                        if(ua.includes('android')) deviceBadge = '<span class="badge bg-android">Android 📱</span>';
                        else if(ua.includes('iphone') || ua.includes('ipad')) deviceBadge = '<span class="badge bg-iphone">iPhone 🍏</span>';
                        let userComplaints = complDB.filter(c => (c.user || "").toLowerCase() === (user.username || "").toLowerCase());
                        let complHtml = '<span style="color:#8b949e;">لا يوجد</span>';
                        if(userComplaints.length > 0) {
                            complHtml = "";
                            userComplaints.forEach(c => { complHtml += `<div class="report-txt">⚠️ [${c.date}]: ${c.details}</div>`; });
                        }
                        let gameDuration = `🐍 ${user.snakeTime || 0}ث | 🧱 ${user.tetrisTime || 0}ث`;
                        html += `<tr>
                            <td style="font-weight:bold; color:#fff;">${user.username}</td>
                            <td>${deviceBadge}</td>
                            <td>${user.loginTime}</td>
                            <td style="color:#58a6ff; font-weight:bold;">${user.duration || 0} ثانية</td>
                            <td>${gameDuration}</td>
                            <td>${complHtml}</td>
                        </tr>`;
                    });
                }
                document.getElementById('logsTableBody').innerHTML = html;
            });
        }
        function clearLogsDatabase() {
            if(confirm("هل أنت متأكد من تصفير ومسح كافة تحليلات الزوار وقاعدة البيانات بالكامل؟")) {
                fetch('/api/admin_clear_data', { method: 'POST' }).then(() => fetchAndRenderAnalytics());
            }
        }
        fetchAndRenderAnalytics();
        setInterval(fetchAndRenderAnalytics, 4000); // تحديث دوري رصدي تلقائي كل 4 ثوانٍ
    </script>
</body>
</html>
"""
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل دخول الإدارة | Albrawe</title>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .login-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; padding: 30px; border-radius: 12px; width: 100%; max-width: 360px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        .form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; text-align: right; }
        input { padding: 10px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #fff; font-family: inherit; width: 100%; box-sizing: border-box; }
        input:focus { border-color: #f85149; outline: none; }
        .btn { background: #f85149; color: #fff; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-family: inherit; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h3 style="margin-top:0; text-align:center; color:#fff;">🔐 نظام تفتيش الإدارة السرية</h3>
        <form method="POST" action="/albrawe-secure-panel-2026">
            <div class="form-group">
                <label>اسم المسؤول:</label>
                <input type="text" name="username" required autocomplete="off">
            </div>
            <div class="form-group">
                <label>كلمة المرور التكتيكية:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn">تأكيد الهوية البيومترية 🛡️</button>
        </form>
    </div>
</body>
</html>
"""

@admin_blueprint.route('/albrawe-secure-panel-2026', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        if user == ADMIN_USER and passwd == ADMIN_PASS:
            session['admin_logged_in'] = True
            return render_template_string(ADMIN_HTML)
        else:
            return render_template_string(LOGIN_HTML + "<script>alert('❌ خطأ فادح: بيانات الاعتماد غير صحيحة!');</script>")
    if session.get('admin_logged_in'):
        return render_template_string(ADMIN_HTML)
    return render_template_string(LOGIN_HTML)

@admin_blueprint.route('/albrawe-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/albrawe-secure-panel-2026')
