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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لوحة التحليلات والرقابة السيبرانية | Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #06090d; color: #c9d1d9; padding: 15px; margin: 0; box-sizing: border-box; }
        .container { width: 100%; max-width: 1400px; margin: 0 auto; }
        .main-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 20px; }
        @media (max-width: 600px) { .main-header { flex-direction: column; gap: 10px; text-align: center; } }
        .logout-btn { background: #f85149; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; font-family: inherit; font-size: 12.5px; transition: 0.2s; }
        .logout-btn:hover { background: #da3633; box-shadow: 0 0 12px #f85149; }
        .complaints-inbox-card { background: #161212; border: 1px solid #492626; border-top: 3px solid #f85149; border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(248,81,73,0.08); }
        .complaints-grid { display: flex; flex-direction: column; gap: 8px; max-height: 150px; overflow-y: auto; }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-box { background: #0d1117; border: 1px solid #30363d; padding: 18px 12px; border-radius: 10px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .stat-box h5 { margin: 0 0 6px 0; color: #8b949e; font-size: 12.5px; font-weight: bold; }
        .stat-box p { margin: 0; font-size: 24px; font-weight: bold; color: #58a6ff; font-family: monospace; }
        .sub-stat-label { display: block; font-size: 11px; font-weight: bold; color: #8b949e; margin-top: 5px; border-top: 1px dashed #21262d; padding-top: 4px; }
        .section-title { color: #79c0ff; margin: 20px 0 10px 0; font-size: 16px; border-bottom: 1px solid #30363d; padding-bottom: 6px; text-align: right; }
        .cards-mesh { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 15px; margin-top: 15px; }
        .user-panel-card { background: #0d1117; border: 1px solid #30363d; border-right: 4px solid #a371f7; border-radius: 10px; padding: 16px; box-shadow: 0 5px 15px rgba(0,0,0,0.4); display: flex; flex-direction: column; gap: 10px; text-align: right; transition: 0.2s; }
        .user-panel-card:hover { border-color: #58a6ff; transform: translateY(-2px); }
        .card-top-info { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
        .card-username { font-size: 14px; font-weight: bold; color: #fff; }
        .card-device { font-size: 11.5px; color: #ffd700; font-weight: bold; }
        .card-meta-line { font-size: 12px; color: #c9d1d9; display: flex; align-items: center; gap: 6px; }
        .card-meta-line i { color: #8b949e; width: 16px; text-align: center; }
        .flag-img { width: 18px; height: 13px; border-radius: 2px; object-fit: cover; box-shadow: 0 0 3px rgba(255,255,255,0.2); }
        .time-badge { color: #58a6ff; font-weight: bold; background: rgba(88,166,255,0.05); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(88,166,255,0.15); font-family: monospace; }
        .games-total-badge { color: #3fb950; font-weight: bold; background: rgba(63,185,80,0.05); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(63,185,80,0.15); font-family: monospace; }
        .games-dashboard { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; background: #161b22; padding: 8px; border-radius: 6px; border: 1px solid #21262d; margin-top: 4px; }
        .mini-game-tag { font-size: 11px; font-weight: bold; display: flex; align-items: center; justify-content: space-between; padding: 3px 5px; background: #0d1117; border-radius: 4px; border: 1px solid #30363d; font-family: monospace; }
        .clear-db-btn { background: #21262d; border: 1px solid #d29922; color: #d29922; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 12px; transition: 0.2s; }
        .clear-db-btn:hover { background: #d29922; color: #000; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h2><i class="fas fa-chart-network" style="color:#a371f7; margin-left:6px;"></i> رادار الرقابة والتحليلات المطور V3</h2>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="clear-db-btn" onclick="clearLogsDatabase()"><i class="fas fa-trash-alt"></i> تصفير Sجلات</button>
                <a href="/albrawe-admin/logout" class="logout-btn">تسجيل الخروج 🚪</a>
            </div>
        </div>
        <div class="complaints-inbox-card">
            <h3 style="margin:0; color:#ff7b72; font-size:14px; border-bottom:1px solid #492626; padding-bottom:6px;"><i class="fas fa-envelope-open-text"></i> صندوق الشكاوى والبلاغات الحي المباشر</h3>
            <div class="complaints-grid" id="globalComplaintsInbox"></div>
        </div>
        <div class="grid-stats">
            <div class="stat-box" style="border-top: 3px solid #58a6ff;"><h5>الزيارات النشطة حالياً</h5><p id="totalViews">0</p></div>
            <div class="stat-box" style="border-top: 3px solid #d29922;"><h5>إجمالي زيارات الموقع الكلية</h5><p id="historicalViews" style="color: #d29922;">0</p></div>
            <div class="stat-box" style="border-top: 3px solid #3fb950;">
                <h5>مجموع وقت استخدام جميع الزوار</h5>
                <p id="totalGlobalUsageTime" style="color: #3fb950;">0 ثانية</p>
                <span class="sub-stat-label" id="avgUsageTime">متوسط الاستخدام الفردي: 0 ثانية ⏱️</span>
            </div>
            <div class="stat-box" style="border-top: 3px solid #f85149;"><h5>إجمالي بلاغات الصندوق</h5><p id="totalComplaints" style="color: #f85149;">0</p></div>
        </div>
        <h3 class="section-title"><i class="fas fa-users"></i> مستودع بيانات الزوار ومسارات التصفح</h3>
        <div class="cards-mesh" id="logsCardsContainer"></div>
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
                if (historicalCount > lastSavedHistorical) { localStorage.setItem('backup_historical', historicalCount); } else { historicalCount = lastSavedHistorical; }
                if (historicalCount < archiveDB.length) { historicalCount = archiveDB.length; localStorage.setItem('backup_historical', historicalCount); }
                
                document.getElementById('totalViews').innerText = liveDB.length;
                document.getElementById('historicalViews').innerText = historicalCount;
                document.getElementById('totalComplaints').innerText = complDB.length;
                
                let totalSeconds = 0;
                archiveDB.forEach(item => { totalSeconds += (item.duration || 0); });
                document.getElementById('totalGlobalUsageTime').innerText = totalSeconds + " ثانية";
                let avgCalc = archiveDB.length > 0 ? Math.round(totalSeconds / archiveDB.length) : 0;
                document.getElementById('avgUsageTime').innerText = "متوسط الاستخدام الفردي: " + avgCalc + " ثانية ⏱️";
                
                let inboxHtml = "";
                if(complDB.length === 0) { inboxHtml = '<p style="color:#8b949e; font-size:12px; text-align:center; margin:10px 0;">الصندوق نظيف كلياً.</p>'; } else {
                    complDB.forEach(c => {
                        inboxHtml += '<div class="report-txt"><span><i class="fas fa-user"></i> <strong>' + c.user + '</strong>: ' + c.details + '</span><span>' + c.date + '</span></div>';
                    });
                }
                document.getElementById('globalComplaintsInbox').innerHTML = inboxHtml;
                
                let cardsHtml = "";
                if(archiveDB.length === 0) { cardsHtml = '<p style="grid-column:1/-1; text-align:center; color:#8b949e; padding:20px;">لا توجد سجلات مستخدمين مؤرشفة حتى الآن.</p>'; } else {
                    archiveDB.slice().reverse().forEach(user => {
                        let snake = user.snakeTime || 0; let tetris = user.tetrisTime || 0; let xo = user.xoTime || 0; let shooter = user.shooterTime || 0; let clicker = user.clickerTime || 0;
                        let totalGamesSeconds = snake + tetris + xo + shooter + clicker;
                        let currentLoc = user.location || "القاهرة - مصر";
                        let countryCode = "eg";
                        let locLower = currentLoc.toLowerCase();
                        if (locLower.includes("saudi") || locLower.includes("السعودية") || locLower.includes("رياض") || locLower.includes("مكة")) countryCode = "sa";
                        else if (locLower.includes("emirates") || locLower.includes("دبي") || locLower.includes("إمارات")) countryCode = "ae";
                        else if (locLower.includes("kuwait") || locLower.includes("الكويت")) countryCode = "kw";
                        
                        let flagImgHtml = '<img class="flag-img" src="https://flagcdn.com' + countryCode + '.png" alt="Flag">';
                        let currentDevice = user.deviceModel || "Android Device 📱";
                        let stepsList = user.browsingHistory || ["الرئيسية 🏠"];
                        
                        cardsHtml += '<div class="user-panel-card">' +
                            '<div class="card-top-info"><span class="card-username"><i class="fas fa-user-circle"></i> ' + user.username + '</span><span class="card-device">' + currentDevice + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-map-marker-alt"></i> ' + flagImgHtml + ' <span class="loc-tag">' + currentLoc + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-clock"></i> <span>الدخول: ' + user.loginTime + '</span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-browser"></i> <span>الموقع الأم: <span class="time-badge">' + (user.duration || 0) + 'ث</span></span></div>' +
                            '<div class="card-meta-line"><i class="fas fa-hourglass-half"></i> <span>إجمالي الألعاب: <span class="games-total-badge">' + totalGamesSeconds + 'ث</span></span></div>' +
                            '<div class="route-path-box">' + stepsList.join(' ➔ ') + '</div>' +
                            '<div class="games-dashboard">' +
                                '<div class="mini-game-tag" style="color:#3fb950;"><span>🐍 ثعبان</span><span>' + snake + 'ث</span></div>' +
                                '<div class="mini-game-tag" style="color:#d29922;"><span>🧱 تترس</span><span>' + tetris + 'ث</span></div>' +
                                '<div class="mini-game-tag" style="color:#a371f7;"><span>❌ X-O</span><span>' + xo + 'ث</span></div>' +
                                '<div class="mini-game-tag" style="color:#388bfd;"><span>🚀 فضاء</span><span>' + shooter + 'ث</span></div>' +
                                '<div class="mini-game-tag" style="color:#ff7b72; grid-column:span 2;"><span>⚡ نيون النقر</span><span>' + clicker + 'ث</span></div>' +
                            '</div>' +
                        '</div>';
                    });
                }
                document.getElementById('logsCardsContainer').innerHTML = cardsHtml;
            });
        }
        function clearLogsDatabase() { if(confirm("هل أنت متأكد من مسح الأرشيف التراكمي وتصفير السجلات؟")) { localStorage.removeItem('permanent_archive_db'); localStorage.removeItem('backup_historical'); fetch('/api/admin_clear_data', { method: 'POST' }).then(() => fetchAndRenderAnalytics()); } }
        fetchAndRenderAnalytics(); setInterval(fetchAndRenderAnalytics, 4000);
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
        <form method="POST" action="/albrawe-admin-panel-2026">
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

# ✅ نظام التثبيت الصارم: تأمين تفعيل المسارين معاً لمنع تعارض الـ Serverless وتحجيم خطأ الـ 404 نهائياً
@admin_blueprint.route('/albrawe-admin-panel-2026', methods=['GET', 'POST'])
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
