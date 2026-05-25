from flask import Flask, render_template_string, request, jsonify, session, redirect
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

app = Flask(__name__)

# مفتاح التشفير السري لتأمين جلسات الباسورد ومنع الاختراق
app.secret_key = "ALBRAWE_CYBER_KEY_SECURITY_2026"

# تسجيل المسارات والألعاب الأساسية
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)

# 🔒 بيانات اعتماد لوحة الإدارة (يمكنك تعديلها من هنا بأي وقت)
ADMIN_USER = "albrawe"
ADMIN_PASS = "PASS2026"

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحليلات والرقابة السرية | Albrawe</title>
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
            <div class="stat-box"><h5>إجمالي الزيارات المؤرشفة</h5><p id="totalViews">0</p></div>
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
                            <th>الشكاوى والبلاغات</th>
                        </tr>
                    </thead>
                    <tbody id="logsTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>
    <script>
        function fetchAndRenderAnalytics() {
            let db = JSON.parse(localStorage.getItem('albrawe_master_analytics_db')) || [];
            let complDB = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            document.getElementById('totalViews').innerText = db.length;
            document.getElementById('totalComplaints').innerText = complDB.length;
            let totalSeconds = 0;
            db.forEach(item => { totalSeconds += (item.duration || 0); });
            document.getElementById('avgTime').innerText = db.length > 0 ? Math.round(totalSeconds / db.length) + " ثانية" : "0 ثانية";
            let html = "";
            if(db.length === 0) {
                html = '<tr><td colspan="6" style="text-align:center; color:#8b949e;">لا توجد بيانات مستخدمين مسجلة.</td></tr>';
            } else {
                db.forEach(user => {
                    let deviceBadge = '<span class="badge bg-windows">Windows/PC</span>';
                    let ua = user.userAgent.toLowerCase();
                    if(ua.includes('android')) deviceBadge = '<span class="badge bg-android">Android 📱</span>';
                    else if(ua.includes('iphone') || ua.includes('ipad')) deviceBadge = '<span class="badge bg-iphone">iPhone 🍏</span>';
                    let userComplaints = complDB.filter(c => c.user.toLowerCase() === user.username.toLowerCase());
                    let complHtml = '<span style="color:#8b949e;">لا يوجد</span>';
                    if(userComplaints.length > 0) {
                        complHtml = "";
                        userComplaints.forEach(c => { complHtml += `<div class="report-txt">⚠️ [${c.date}]: ${c.details}</div>`; });
                    }
                    html += `<tr><td>\${user.username}</td><td>\${deviceBadge}</td><td>\${user.loginTime}</td><td>\${user.duration || 0} ثانية</td><td>🐍 \${user.snakeTime || 0}ث | 🧱 \${user.tetrisTime || 0}ث</td><td>\${complHtml}</td></tr>`;
                });
            }
            document.getElementById('logsTableBody').innerHTML = html;
        }
        function clearLogsDatabase() {
            if(confirm("هل أنت متأكد من تصفير المسح؟")) { localStorage.removeItem('albrawe_master_analytics_db'); fetchAndRenderAnalytics(); }
        }
        fetchAndRenderAnalytics();
    </script>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تسجيل دخول الإدارة | Albrawe</title>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .login-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #f85149; padding: 30px; border-radius: 12px; width: 100%; max-width: 340px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); text-align: right; }
        .form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; }
        input { padding: 10px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #fff; font-family: inherit; }
        .btn { background: #f85149; color: #fff; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-family: inherit; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h3 style="margin-top:0; text-align:center; color:#fff;">🔐 نظام الإدارة السرية</h3>
        <form method="POST" action="/PASS">
            <div class="form-group">
                <label>اسم المسؤول:</label>
                <input type="text" name="username" required autocomplete="off">
            </div>
            <div class="form-group">
                <label>كلمة المرور:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn">تأكيد الهوية البيومترية 🛡️</button>
        </form>
    </div>
</body>
</html>
"""

# 🎯 تفعيل امتداد الرابط المباشر /PASS داخل نواة السيرفر الرئيسية
@app.route('/PASS', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        if user == ADMIN_USER and passwd == ADMIN_PASS:
            session['admin_logged_in'] = True
            return render_template_string(ADMIN_HTML)
        else:
            return render_template_string(LOGIN_HTML + "<script>alert('❌ بيانات الاعتماد غير صحيحة!');</script>")
    if session.get('admin_logged_in'):
        return render_template_string(ADMIN_HTML)
    return render_template_string(LOGIN_HTML)

@app.route('/albrawe-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/PASS')

handler = app

if __name__ == '__main__':
    app.run()
