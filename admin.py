from flask import Blueprint, request, jsonify, render_template_string, session, redirect

admin_blueprint = Blueprint('admin', __name__)

# 🔒 بيانات اعتماد لوحة الإدارة المحصنة (تعدل من هنا بأي وقت)
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
        .container { max-width: 1250px; margin: 0 auto; }
        .main-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; padding-bottom: 15px; margin-bottom: 25px; }
        .logout-btn { background: #f85149; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; font-family: inherit; }
        .analytics-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        
        .complaints-inbox-card { background: #1c1616; border: 1px solid #492626; border-top: 4px solid #f85149; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(248,81,73,0.15); }
        .complaints-grid { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; max-height: 250px; overflow-y: auto; padding-left: 5px; }
        
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; }
        .stat-box h5 { margin: 0 0 6px 0; color: #8b949e; font-size: 13px; }
        .stat-box p { margin: 0; font-size: 22px; font-weight: bold; color: #58a6ff; }
        
        .sub-stat-label { display: block; font-size: 11px; font-weight: 500; color: #8b949e; margin-top: 5px; border-top: 1px dashed #21262d; padding-top: 4px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #0d1117; border-radius: 8px; overflow: hidden; }
        th, td { padding: 12px 15px; text-align: right; border-bottom: 1px solid #30363d; font-size: 12.5px; }
        th { background-color: #21262d; color: #79c0ff; font-weight: bold; }
        tr:hover { background-color: rgba(88, 166, 255, 0.03); }
        
        .device-tag { color: #ffd700; font-weight: bold; }
        .loc-tag { color: #3fb950; font-weight: bold; }
        .total-games-time { color: #ffd700; font-weight: bold; background: rgba(255,215,0,0.05); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(255,215,0,0.2); }
        
        .game-tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; margin: 1px; background: rgba(255,255,255,0.02); border: 1px solid #30363d; }
        .report-txt { background: #211b1b; border-right: 4px solid #f85149; padding: 12px; margin: 2px 0; border-radius: 0 6px 6px 0; font-size: 13px; line-height: 1.5; color: #ff7b72; display: flex; justify-content: space-between; align-items: center; }
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
        
        <div class="complaints-inbox-card">
            <h3 style="margin:0; color:#ff7b72; font-size:16px; border-bottom:1px solid #492626; padding-bottom:8px;"><i class="fas fa-inbox"></i> صندوق الشكاوى والبلاغات السحابي الموحد</h3>
            <div class="complaints-grid" id="globalComplaintsInbox"></div>
        </div>

        <div class="grid-stats">
            <div class="stat-box"><h5>الزيارات النشطة حالياً</h5><p id="totalViews">0</p></div>
            <div class="stat-box" style="border-color: #d29922;"><h5 style="color: #ffd700;">إجمالي زيارات الموقع الكلية</h5><p id="historicalViews" style="color: #ffd700;">0</p></div>
            
            <div class="stat-box" style="border-color: #388bfd;">
                <h5 style="color: #388bfd;">إجمالي مدة استخدام الموقع</h5>
                <p id="totalUsageTime" style="color: #388bfd;">0 ثانية</p>
                <span class="sub-stat-label" id="avgUsageTime">متوسط الاستخدام: 0 ثانية ⏱️</span>
            </div>
            
            <div class="stat-box"><h5>إجمالي بلاغات الصندوق</h5><p id="totalComplaints">0</p></div>
        </div>
        
        <div class="analytics-card">
            <h3 style="margin-top:0; color:#79c0ff; border-bottom:1px solid #30363d; padding-bottom:8px;">👥 سجل تدقيق حركات المستخدمين وعدادات الألعاب</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>الاسم الرمزي</th>
                            <th>الموديل الدقيق للجهاز 📱</th>
                            <th>الموقع الجغرافي 🌍</th>
                            <th>وقت الدخول</th>
                            <th>إجمالي وقت الألعاب ⏳</th>
                            <th>تفصيل عدادات الألعاب الخمسة 🎮</th>
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
                let historicalCount = data.historicalVisits || 0;
                
                document.getElementById('totalViews').innerText = db.length;
                document.getElementById('historicalViews').innerText = historicalCount;
                document.getElementById('totalComplaints').innerText = complDB.length;
                
                let totalSeconds = 0;
                db.forEach(item => { totalSeconds += (item.duration || 0); });
                
                document.getElementById('totalUsageTime').innerText = totalSeconds + " ثانية";
                let avgCalc = db.length > 0 ? Math.round(totalSeconds / db.length) : 0;
                document.getElementById('avgUsageTime').innerText = "متوسط الاستخدام: " + avgCalc + " ثانية ⏱️";
                
                let inboxHtml = "";
                if(complDB.length === 0) {
                    inboxHtml = '<p style="color:#8b949e; font-size:13px; text-align:center; margin:10px 0;">الصندوق نظيف كلياً؛ لا توجد أي شكاوى مرفوعة حالياً من زوار الويب. ✨</p>';
                } else {
                    complDB.forEach(c => {
                        // ✅ تم الإصلاح الفني الحاسم: إضافة الهروب المائل لمنع تضارب بايثون مع الـ JavaScript المتغير في الصورة
                        inboxHtml += `
                        <div class="report-txt">
                            <span><i class="fas fa-user" style="color:#8b949e; margin-left:6px;"></i> <strong>\${c.user}</strong>: \${c.details}</span>
                            <span style="color:#8b949e; font-size:11px; font-family:monospace;"><i class="far fa-clock"></i> \${c.date}</span>
                        </div>`;
                    });
                }
                document.getElementById('globalComplaintsInbox').innerHTML = inboxHtml;
                
                let html = "";
                if(db.length === 0) {
                    html = '<tr><td colspan="6" style="text-align:center; color:#8b949e;">لا توجد بيانات حركة مستخدمين مسجلة حتى الآن.</td></tr>';
                } else {
                    db.forEach(user => {
                        let snake = user.snakeTime || 0; let tetris = user.tetrisTime || 0; let xo = user.xoTime || 0; let shooter = user.shooterTime || 0; let clicker = user.clickerTime || 0;
                        let totalGamesSeconds = snake + tetris + xo + shooter + clicker;
                        
                        let gameDuration = `
                            <div class="game-tag" style="color:#3fb950;"><i class="fas fa-dragon"></i> ثعبان: \${snake}ث</div>
                            <div class="game-tag" style="color:#d29922;"><i class="fas fa-cubes"></i> تترس: \${tetris}ث</div>
                            <div class="game-tag" style="color:#a371f7;"><i class="fas fa-times-circle"></i> X-O: \${xo}ث</div>
                            <div class="game-tag" style="color:#388bfd;"><i class="fas fa-space-shuttle"></i> فضاء: \${shooter}ث</div>
                            <div class="game-tag" style="color:#ff7b72;"><i class="fas fa-bolt"></i> نيون: \${clicker}ث</div>
                        `;
                        
                        html += `<tr>
                            <td style="font-weight:bold; color:#fff;">\${user.username}</td>
                            <td class="device-tag"><i class="fas fa-mobile-alt"></i> \${user.deviceModel || "غير معروف"}</td>
                            <td class="loc-tag"><i class="fas fa-map-marker-alt"></i> \${user.location || "جاري التحديد..."}</td>
                            <td>\${user.loginTime}</td>
                            <td><span class="total-games-time"><i class="fas fa-hourglass-half"></i> \${totalGamesSeconds} ثانية</span></td>
                            <td>\${gameDuration}</td>
                        </tr>`;
                    });
                }
                document.getElementById('logsTableBody').innerHTML = html;
            });
        }
        function clearLogsDatabase() {
            if(confirm("هل أنت متأكد من تصفير ومسح سجل الحركة الفردي الحالي من السيرفر؟")) {
                fetch('/api/admin_clear_data', { method: 'POST' }).then(() => fetchAndRenderAnalytics());
            }
        }
        fetchAndRenderAnalytics();
        setInterval(fetchAndRenderAnalytics, 4000);
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
