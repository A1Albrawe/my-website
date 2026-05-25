import json
import urllib.request
from flask import Blueprint, request, jsonify, render_template_string

report_blueprint = Blueprint('report', __name__)

ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "1892403076:AAHOyUXyGNkNlYvDfJKuWrHZ4hUg3m22GYs"

def send_to_telegram(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=5) as response: pass
    except Exception: pass

@report_blueprint.route('/api/send_message', methods=['POST'])
def send_msg_from_site():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول')
    msg_type = data.get('type', 'محادثة حية')
    details = data.get('details', '')
    if not details: return jsonify({"status": "error"}), 400
    tg_text = f"📥 *رسالة دعم فني جديدة*\n👤 *الاسم:* {user}\n🏷️ *النوع:* {msg_type}\n💬 *الرسالة:* {details}"
    send_to_telegram(tg_text)
    return jsonify({"status": "success"})

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>إرسال مشكلة - Albrawe</title>
    <style>
        body { font-family: monospace; text-align: center; background: #121212; color: #8c9f21; padding: 10px; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; box-sizing: border-box; }
        .back-btn { background: #111; color: #8c9f21; border: 2px solid #8c9f21; padding: 8px 16px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-bottom: 20px; font-size: 13px; }
        .nokia-phone-style { background: #3a4d5c; border: 8px solid #25333d; border-radius: 40px; width: 100%; max-width: 400px; padding: 30px 20px; box-shadow: 0 20px 45px rgba(0,0,0,0.8); box-sizing: border-box; }
        .nokia-screen-style { background-color: #8c9f21; border: 12px solid #111; border-radius: 10px; padding: 15px; box-sizing: border-box; color: #000; text-align: right; }
        .form-group { margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px; }
        .input-field { padding: 8px; font-size: 13px; border: 2px solid #000; background: #9ab027; font-family: inherit; font-weight: bold; color: #000; width: 100%; box-sizing: border-box; }
        .submit-btn { background: #000; color: #8c9f21; border: 2px solid #000; padding: 9px 16px; font-weight: bold; cursor: pointer; width: 100%; font-family: inherit; }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">◀ القائمة الرئيسية</a>
    <div class="nokia-phone-style">
        <div class="nokia-screen-style">
            <h3 style="text-align:center;">🛠️ الإبلاغ عن مشكلة بالموقع</h3>
            <form onsubmit="handleFormSubmit(event)">
                <div class="form-group">
                    <label>اسم المستخدم:</label>
                    <input type="text" id="userName" class="input-field" required maxlength="15">
                </div>
                <div class="form-group">
                    <label>تفاصيل المشكلة:</label>
                    <textarea id="issueDetails" class="input-field" rows="3" required maxlength="200"></textarea>
                </div>
                <button type="submit" class="submit-btn">🚀 إرسال التقرير للتليجرام</button>
            </form>
        </div>
    </div>
    <script>
        function handleFormSubmit(e) {
            e.preventDefault();
            fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user: document.getElementById('userName').value, type: 'شكوى دعم فني', details: document.getElementById('issueDetails').value })
            }).then(() => { alert('✅ تم الإرسال بنجاح للمطور البراوي!'); document.getElementById('issueDetails').value = ''; });
        }
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page(): return render_template_string(REPORT_TEMPLATE)

@report_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook(): return "OK", 200

@report_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id): return jsonify({"status": "empty"})
