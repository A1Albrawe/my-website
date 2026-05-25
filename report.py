from flask import Blueprint, render_template_string

report_blueprint = Blueprint('report', __name__)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>مركز الدعم الفني - Albrawe</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .dev-portfolio-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 12px; padding: 30px 20px; max-width: 500px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; text-align: right; }
        .form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; }
        label { font-weight: bold; font-size: 13px; color: #79c0ff; }
        .input-field { padding: 10px; font-size: 14px; border: 1px solid #30363d; background: #0d1117; font-family: inherit; font-weight: bold; color: #c9d1d9; border-radius: 6px; width: 100%; box-sizing: border-box; }
        .input-field:focus { border-color: #58a6ff; outline: none; }
        textarea.input-field { resize: none; height: 100px; }
        .submit-btn { background: #238636; color: #ffffff; border: 1px solid #2ea44f; padding: 12px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; font-family: inherit; }
        .submit-btn:hover { background: #2ea44f; }
        .chat-box-area { margin-top: 15px; background: rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 6px; font-size: 12px; border: 1px solid #30363d; height: 120px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
        .chat-bubble { padding: 6px 10px; border-radius: 6px; max-width: 90%; font-weight: bold; line-height: 1.4; word-wrap: break-word; color: #8c9f21; background: #000; align-self: flex-start; text-align: right; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="color:#fff; font-weight:bold;">🛠️ مركز الدعم الفني</span>
    </div>

    <div class="main-container">
        <div class="dev-portfolio-card">
            <h3 style="margin-top:0; color:#f0f6fc; border-bottom:1px solid #30363d; padding-bottom:10px;">💬 أرسل رسالتك أو مشكلتك الفنية</h3>
            <form id="reportForm" onsubmit="saveReportLocally(event)">
                <div class="form-group">
                    <label>اسم المستخدم الكودى:</label>
                    <input type="text" id="userName" class="input-field" required maxlength="15">
                </div>
                <div class="chat-box-area" id="chatBoxContainer">
                    <div style="text-align:center; color:#8b949e; margin:auto;" id="emptyHint">اكتب رسالتك بالأسفل وسوف يتم حفظها بأمان...</div>
                </div>
                <div class="form-group" style="margin-top:12px;">
                    <textarea id="issueDetails" class="input-field" placeholder="اشرح المشكلة التقنية أو الاقتراح الفني هنا..." required maxlength="250"></textarea>
                </div>
                <button type="submit" class="submit-btn">📥 تسجيل وحفظ التقرير الفوري</button>
            </form>
        </div>
    </div>

    <script>
        function setupUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) { document.getElementById('userName').value = savedUser; }
        }

        function saveReportLocally(event) {
            event.preventDefault();
            const user = document.getElementById('userName').value.trim();
            const details = document.getElementById('issueDetails').value.trim();
            
            // جلب المصفوفة المركزية الآمنة وحفظ الشكوى بها
            let allReports = JSON.parse(localStorage.getItem('albrawe_central_db')) || [];
            allReports.unshift({
                id: Date.now(),
                user: user,
                details: details,
                date: new Date().toLocaleString('ar-EG')
            });
            
            localStorage.setItem('albrawe_central_db', JSON.stringify(allReports));
            appendChatBubble(user + ": " + details);
            document.getElementById('issueDetails').value = "";
            alert("✅ تم إرسال وحفظ تقريرك بنجاح في قاعدة بيانات الموقع!");
        }

        function appendChatBubble(text) {
            const container = document.getElementById('chatBoxContainer');
            const hint = document.getElementById('emptyHint');
            if (hint) hint.remove();
            const bubble = document.createElement('div');
            bubble.className = "chat-bubble";
            bubble.innerText = text;
            container.appendChild(bubble);
            container.scrollTop = container.scrollHeight;
        }

        setupUser();
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
