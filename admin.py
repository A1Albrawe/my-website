from flask import Blueprint, request, jsonify, render_template_string, session, redirect, abort

admin_blueprint = Blueprint('admin', __name__)

ADMIN_USER = "albrawe"
ADMIN_PASS = "PASS2026"
SECRET_GATE_KEY = "open_gate_key_final_2026"

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الرقابة والتحليلات السيبرانية | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #080c10; color: #c9d1d9; padding: 25px; margin: 0; }
        .container { max-width: 1400px; margin: 0 auto; }
        
        .main-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; padding-bottom: 18px; margin-bottom: 30px; }
        .logout-btn { background: #f85149; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; text-decoration: none; font-family: inherit; transition: 0.2s; box-shadow: 0 0 10px rgba(248,81,73,0.3); }
        .logout-btn:hover { background: #da3633; box-shadow: 0 0 15px #f85149; }
        
        .complaints-inbox-card { background: #161212; border: 1px solid #492222; border-top: 4px solid #f85149; border-radius: 14px; padding: 22px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(248,81,73,0.12); }
        .complaints-grid { display: flex; flex-direction: column; gap: 12px; margin-top: 15px; max-height: 250px; overflow-y: auto; padding-left: 5px; }
        
        /* 📊 شبكة الكروت المطورة والمعززة بالخانات الخمسة */
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-box { background: #10151b; border: 1px solid #21262d; padding: 22px 18px; border-radius: 12px; text-align: center; box-shadow: 0 6px 16px rgba(0,0,0,0.4); position: relative; overflow: hidden; transition: 0.3s ease; }
        .stat-box:hover { transform: translateY(-3px); border-color: #30363d; }
        .stat-box h5 { margin: 0 0 10px 0; color: #8b949e; font-size: 13.5px; font-weight: bold; letter-spacing: 0.5px; }
        .stat-box p { margin: 0; font-size: 28px; font-weight: bold; color: #58a6ff; font-family: monospace; text-shadow: 0 0 10px rgba(88,166,255,0.2); }
        .sub-stat-label { display: block; font-size: 11.5px; font-weight: bold; color: #8b949e; margin-top: 8px; border-top: 1px dashed #21262d; padding-top: 6px; }
        
        .analytics-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 14px; padding: 25px; margin-bottom: 25px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #0d1117; border-radius: 10px; overflow: hidden; box-shadow: inset 0 0 20px rgba(0,0,0,0.6); }
        th, td { padding: 16px 14px; text-align: right; border-bottom: 1px solid #21262d; font-size: 13px; }
        th { background-color: #1f242c; color: #79c0ff; font-weight: bold; position: sticky; top: 0; border-bottom: 2px solid #30363d; letter-spacing: 0.3px; }
        tr:hover { background-color: rgba(163, 113, 247, 0.03); }
        
        .device-tag { color: #ffd700; font-weight: bold; font-family: inherit; }
        .loc-tag { color: #3fb950; font-weight: bold; }
        .total-site-time { color: #58a6ff; font-weight: bold; background: rgba(88,166,255,0.06); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(88,166,255,0.2); font-family: monospace; }
        .total-games-time { color: #ffd700; font-weight: bold; background: rgba(255,215,0,0.06); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(255,215,0,0.2); font-family: monospace; }
        
        .route-path-box { font-size: 11.5px; color: #a371f7; font-weight: bold; background: rgba(163,113,247,0.05); padding: 6px 10px; border-radius: 8px; border: 1px dashed rgba(163,113,247,0.25); line-height: 1.5; word-break: break-all; max-width: 280px; }
        .game-tag { display: inline-block; padding: 3px 7px; border-radius: 5px; font-size: 11px; font-weight: bold; margin: 2px 1px; background: rgba(255,255,255,0.02); border: 1px solid #21262d; font-family: monospace; }
        .report-txt { background: #1c1818; border-right: 4px solid #f85149; padding: 12px; margin: 4px 0; border-radius: 0 6px 6px 0; font-size: 13px; color: #ff7b72; display: flex; justify-content: space-between; align-items: center; }
        .clear-db-btn { background: #21262d; border: 1px solid #d29922; color: #d29922; padding: 7px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 12px; transition: 0.2s; }
        .clear-db-btn:hover { background: #d29922; color: #000; box-shadow: 0 0 10px rgba(210,153,34,0.4); }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h2><i class="fas fa-terminal" style="color:#a371f7; margin-left:8px;"></i> رادار الرقابة وتحليلات الزوار المركزي</h2>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="clear-db-btn" onclick="clearLogsDatabase()"><i class="fas fa-trash-alt"></i> تصفير السجلات</button>
                <a href="/albrawe-admin/logout" class="logout-btn">تسجيل الخروج 🚪</a>
            </div>
        </div>
        
        <div class="complaints-inbox-card">
            <h3 style="margin:0; color:#ff7b72; font-size:16px; border-bottom:1px solid #492626; padding-bottom:8px;"><i class="fas fa-envelope-open-text"></i> صندوق الشكاوى والبلاغات السحابي الموحد</h3>
            <div class="complaints-grid" id="globalComplaintsInbox"></div>
        </div>

        <div class="grid-stats">
            <div class="stat-box" style="border-top: 3px solid #58a6ff;"><h5>الزيارات النشطة حالياً</h5><p id="totalViews">0</p></div>
            <div class="stat-box" style="border-top: 3px solid #d29922;"><h5>إجمالي زيارات الموقع الكلية</h5><p id="historicalViews" style="color: #d29922;">0</p></div>
            
            <!-- ⚡ خانة مجموع الوقت المستغرق من جميع الزوار مجتمعين عبر الإنترنت للأبد -->
            <div class="stat-box" style="border-top: 3px solid #3fb950;">
                <h5 style="color: #3fb950;">مجموع وقت استخدام جميع الزوار</h5>
                <p id="totalGlobalUsageTime" style="color: #3fb950;">0 ثانية</p>
                <span class="sub-stat-label" id="avgUsageTime">متوسط الاستخدام الفردي: 0 ثانية ⏱️</span>
            </div>
            
            <div class="stat-box" style="border-top: 3px solid #f85149;"><h5>إجمالي بلاغات الصندوق</h5><p id="totalComplaints" style="color: #f85149;">0</p></div>
        </div>
        
        <div class="analytics-card">
            <h3 style="margin-top:0; color:#79c0ff; border-bottom:1px solid #30363d; padding-bottom:10px;"><i class="fas fa-users-cog"></i> الأرشيف التاريخي الشامل ومستودع بيانات الزوار</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>الاسم الرمزي</th>
                            <th>الموديل الدقيق 📱</th>
                            <th>الموقع الجغرافي 🌍</th>
                            <th>تاريخ ووقت الدخول 📅</th>
                            <th>الموقع الأم 🖥️</th>
                            <th>مسار التنقل والصفحات 🗺️</th>
                            <th>وقت الألعاب ⏳</th>
                            <th>تفصيل العدادات الخمسة 🎮</th>
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
                let liveDB = data.analytics || [];
                let complDB = data.reports || [];
                let historicalCount = data.historicalVisits || 0;
                
                let archiveDB = JSON.parse(localStorage.getItem('permanent_archive_db') || "[]");
                
                liveDB.forEach(liveUser => {
                    let existingIndex = archiveDB.findIndex(archiveUser => archiveUser.username === liveUser.username);
                    if (existingIndex !== -1) {
                        let currentStep = 'الرئيسية';
                        if (liveUser.snakeTime > 0) currentStep = 'لعبة الثعبان 🐍';
                        else if (liveUser.tetrisTime > 0) currentStep = 'لعبة التترس 🧱';
                        else if (liveUser.xoTime > 0) currentStep = 'لعبة X-O ❌';
                        else if (liveUser.shooterTime > 0) currentStep = 'قاصف الفضاء 🚀';
                        else if (liveUser.clickerTime > 0) currentStep = 'تحدي النقر ⚡';
                        
                        let historyArray = archiveDB[existingIndex].browsingHistory || ["الرئيسية 🏠"];
                        if (historyArray[historyArray.length - 1] !== currentStep) {
                            historyArray.push(currentStep);
                        }
                        liveUser.browsingHistory = historyArray;
                        archiveDB[existingIndex] = liveUser;
                    } else {
                        liveUser.browsingHistory = ["الرئيسية 🏠"];
                        archiveDB.push(liveUser);
                    }
                });
                
                localStorage.setItem('permanent_archive_db', JSON.stringify(archiveDB));

                let lastSavedHistorical = parseInt(localStorage.getItem('backup_historical') || "0");
                if (historicalCount > lastSavedHistorical) {
                    localStorage.setItem('backup_historical', historicalCount);
                } else {
                    historicalCount = lastSavedHistorical;
                }
                if (historicalCount < archiveDB.length) {
                    historicalCount = archiveDB.length;
                    localStorage.setItem('backup_historical', historicalCount);
                }

                if (complDB.length === 0 && localStorage.getItem('backup_complaints')) {
                    complDB = JSON.parse(localStorage.getItem('backup_complaints'));
                } else if (complDB.length > 0) {
                    localStorage.setItem('backup_complaints', JSON.stringify(complDB));
                }
                
                document.getElementById('totalViews').innerText = liveDB.length;
                document.getElementById('historicalViews').innerText = historicalCount;
                document.getElementById('totalComplaints').innerText = complDB.length;
                
                // ⏱️ حساب مجموع وقت الاستخدام التراكمي لجميع الزوار من مصفوفة الأرشيف للأبد
                let totalSeconds = 0;
                archiveDB.forEach(item => { totalSeconds += (item.duration || 0); });
                document.getElementById('totalGlobalUsageTime').innerText = totalSeconds + " ثانية";
                
                let avgCalc = archiveDB.length > 0 ? Math.round(totalSeconds / archiveDB.length) : 0;
                document.getElementById('avgUsageTime').innerText = "متوسط الاستخدام الفردي: " + avgCalc + " ثانية ⏱️";
                
                let inboxHtml = "";
                if(complDB.length === 0) {
                    inboxHtml = '<p style="color:#8b949e; font-size:13px; text-align:center; margin:10px 0;">الصندوق نظيف كلياً؛ لا توجد أي شكاوى مرفوعة حالياً من زوار الويب. ✨</p>';
                } else {
                    complDB.forEach(c => {
                        inboxHtml += '<div class="report-txt">' +
                            '<span><i class="fas fa-user" style="color:#8b949e; margin-left:6px;"></i> <strong>' + c.user + '</strong>: ' + c.details + '</span>' +
                            '<span style="color:#8b949e; font-size:11px; font-family:monospace;"><i class="far fa-clock"></i> ' + c.date + '</span>' +
                        '</div>';
                    });
                }
                document.getElementById('globalComplaintsInbox').innerHTML = inboxHtml;
                
                let html = "";
                if(archiveDB.length === 0) {
                    html = '<tr><td colspan="8" style="text-align:center; color:#8b949e;">لا توجد بيانات حركة مستخدمين مؤرشفة حتى الآن.</td></tr>';
                } else {
                    archiveDB.slice().reverse().forEach(user => {
                        let snake = user.snakeTime || 0; let tetris = user.tetrisTime || 0; let xo = user.xoTime || 0; let shooter = user.shooterTime || 0; let clicker = user.clickerTime || 0;
                        let totalGamesSeconds = snake + tetris + xo + shooter + clicker;
                        
                        let currentLoc = user.location;
                        if (!currentLoc || currentLoc.includes("جاري")) currentLoc = "القاهرة - مصر 🇪🇬";
                        let currentDevice = user.deviceModel;
                        if (!currentDevice || currentDevice.includes("عالي الحماية")) currentDevice = "Android Device 📱";
                        
                        let stepsList = user.browsingHistory || ["الرئيسية 🏠"];
                        let stepsHtml = '<div class="route-path-box">' + stepsList.join(' ➔ ') + '</div>';
                        
                        let gameDuration = '<div class="game-tag" style="color:#3fb950;">ثعبان: ' + snake + 'ث</div>' +
                            '<div class="game-tag" style="color:#d29922;">تترس: ' + tetris + 'ث</div>' +
                            '<div class="game-tag" style="color:#a371f7;">X-O: ' + xo + 'ث</div>' +
                            '<div class="game-tag" style="color:#388bfd;">فضاء: ' + shooter + 'ث</div>' +
                            '<div class="game-tag" style="color:#ff7b72;">نيون: ' + clicker + 'ث</div>';
                        
                        html += '<tr>' +
                            '<td style="font-weight:bold; color:#fff;">' + user.username + '</td>' +
                            '<td class="device-tag"><i class="fas fa-mobile-alt"></i> ' + currentDevice + '</td>' +
                            '<td class="loc-tag"><i class="fas fa-map-marker-alt"></i> ' + currentLoc + '</td>' +
                            '<td>' + user.loginTime + '</td>' +
                            '<td><span class="total-site-time"><i class="fas fa-window-maximize"></i> ' + (user.duration || 0) + 'ث</span></td>' +
                            '<td>' + stepsHtml + '</td>' +
                            '<td><span class="total-games-time"><i class="fas fa-hourglass-half"></i> ' + totalGamesSeconds + 'ث</span></td>' +
                            '<td>' + gameDuration + '</td>' +
                        '</tr>';
                    });
                }
                document.getElementById('logsTableBody').innerHTML = html;
            });
        }
        function clearLogsDatabase() {
            if(confirm("هل أنت متأكد من مسح السجل التراكمي وتصفير الأرشيف التاريخي بالكامل من لوحتك؟")) {
                localStorage.removeItem('permanent_archive_db');
                localStorage.removeItem('backup_historical');
                localStorage.removeItem('backup_complaints');
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
    gate_key = request.args.get('key', '')
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        if user == ADMIN_USER and passwd == ADMIN_PASS:
            session['admin_logged_in'] = True
            session['gate_key_authenticated'] = True
            return render_template_string(ADMIN_HTML)
        else:
            return render_template_string(LOGIN_HTML + "<script>alert('❌ خطأ فادح: بيانات الاعتماد غير صحيحة!');</script>")
    if session.get('admin_logged_in') and session.get('gate_key_authenticated'):
        return render_template_string(ADMIN_HTML)
    if gate_key == SECRET_GATE_KEY:
        session['gate_key_authenticated'] = True
        return render_template_string(LOGIN_HTML)
    abort(404)

@admin_blueprint.route('/albrawe-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('gate_key_authenticated', None)
    return redirect('/')
