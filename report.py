import json
import urllib.request
from flask import Blueprint, request, jsonify, render_template_string

# إنشاء البلوبرينت الموحد لنظام الشات المتكامل والتليجرام المتوافق مع Vercel
report_blueprint = Blueprint('report', __name__)

# 🎯 تفعيل وتثبيت بيانات حسابك والتوكن الجديد القياسي والموثق
ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "8196656039:AAGtnN77ZnuZmZ3iP4T5nY9VflXjxqM2E8o"

# دالة إرسال الرسائل الفورية المبنية على urllib القياسية لضمان استقرار السيرفر 100%
def send_to_telegram(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception:
        pass

# مسار استقبال الشكاوى والمحادثات من واجهة الموقع وتمريرها لتليجرامك فوراً
@report_blueprint.route('/api/send_message', methods=['POST'])
def send_msg_from_site():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول')
    msg_type = data.get('type', 'محادثة حية')
    details = data.get('details', '')

    if not details:
        return jsonify({"status": "error", "message": "الرسالة فارغة"}), 400

    tg_text = (
        f"📥 *رسالة دعم فني جديدة من الموقع*\n\n"
        f"👤 *الاسم:* {user}\n"
        f"🏷️ *النوع:* {msg_type}\n"
        f"💬 *الرسالة:* {details}\n\n"
        f"📌 يمكنك التواصل مع المستخدم بشكل مباشر إذا كان معرّفه مسجلاً."
    )
    
    send_to_telegram(tg_text)
    return jsonify({"status": "success", "message": "تم الإرسال بنجاح"})
REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>إرسال مشكلة - Albrawe</title>
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #121212;
            color: #8c9f21; 
            padding: 10px; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            box-sizing: border-box;
            overscroll-behavior-y: contain;
        }
        .back-btn { 
            background: #111; 
            color: #8c9f21; 
            border: 2px solid #8c9f21; 
            padding: 8px 16px; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            font-weight: bold; 
            margin-bottom: 20px; 
            font-size: 13px;
        }
        
        .nokia-phone-style { 
            background: #3a4d5c; 
            border: 8px solid #25333d; 
            border-radius: 40px; 
            width: 100%;
            max-width: 400px; 
            padding: 30px 20px; 
            box-shadow: 0 20px 45px rgba(0,0,0,0.8); 
            box-sizing: border-box; 
        }
        .nokia-screen-style { 
            background-color: #8c9f21; 
            border: 12px solid #111; 
            border-radius: 10px; 
            padding: 15px; 
            box-sizing: border-box; 
            box-shadow: inset 0 0 15px rgba(0,0,0,0.6);
            color: #000;
            text-align: right;
        }
        
        .screen-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            font-size: 14px;
            border-bottom: 2px solid #000;
            padding-bottom: 6px;
            margin-bottom: 12px;
        }
        .form-group { margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px; }
        label { font-weight: bold; font-size: 12px; }

        .input-field {
            padding: 8px;
            font-size: 13px;
            border: 2px solid #000;
            background: #9ab027;
            font-family: inherit;
            font-weight: bold;
            color: #000;
            border-radius: 4px;
            outline: none;
            box-sizing: border-box;
            width: 100%;
        }
        textarea.input-field { resize: none; height: 70px; }

        .submit-btn {
            background: #000;
            color: #8c9f21;
            border: 2px solid #000;
            padding: 9px 16px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            width: 100%;
            font-family: inherit;
        }

        .chat-box-area {
            margin-top: 15px;
            background: rgba(0, 0, 0, 0.08);
            padding: 10px;
            border-radius: 6px;
            font-size: 12px;
            border: 2px solid #000;
            height: 120px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .chat-bubble { padding: 6px 10px; border-radius: 6px; max-width: 90%; font-weight: bold; line-height: 1.4; word-wrap: break-word; }
        .user-bubble { background: #000; color: #8c9f21; align-self: flex-start; text-align: right; border-radius: 6px 6px 0 6px; }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">◀ القائمة الرئيسية</a>
    <div class="nokia-phone-style" style="margin-top:20px;">
        <div class="nokia-screen-style">
            <div class="screen-header">
                <span>💬 شات ومشاكل الموقع</span>
                <span>NOKIA</span>
            </div>
            
            <form id="chatForm" onsubmit="handleFormSubmit(event)">
                <div class="form-group">
                    <label for="userName">اسم المستخدم:</label>
                    <input type="text" id="userName" class="input-field" placeholder="اكتب اسمك هنا" required maxlength="15">
                </div>
                
                <div class="chat-box-area" id="chatBoxContainer">
                    <div style="text-align:center; color:rgba(0,0,0,0.5); font-weight:bold; margin:auto;" id="emptyHint">اكتب رسالتك بالأسفل لتصل فوراً للمطور...</div>
                </div>
                
                <div class="form-group" style="margin-top:12px;">
                    <textarea id="issueDetails" class="input-field" placeholder="اكتب رسالتك أو مشكلتك هنا واضغط إرسال..." required maxlength="200"></textarea>
                </div>
                
                <button type="submit" class="submit-btn">إرسال إلى التليجرام</button>
            </form>
        </div>
    </div>
    <script>
        function setupUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) { document.getElementById('userName').value = savedUser; }
        }

        function handleFormSubmit(event) {
            event.preventDefault();
            
            const user = document.getElementById('userName').value.trim();
            const details = document.getElementById('issueDetails').value.trim();
            
            if (!user || !details) return;

            appendChatBubble(user + ": " + details);
            document.getElementById('issueDetails').value = "";

            fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user: user,
                    type: "شات ومشاكل الموقع",
                    details: details
                })
            }).then(res => res.json())
              .then(data => {
                  if(data.status === "success") {
                      alert("✅ تم إرسال رسالتك بنجاح للمطور البراوي!");
                  }
              }).catch(err => {
                  alert("❌ فشل الإرسال السحابي، تأكد من الاتصال.");
              });
        }

        function appendChatBubble(text) {
            const container = document.getElementById('chatBoxContainer');
            const hint = document.getElementById('emptyHint');
            if (hint) hint.remove();
            
            const bubble = document.createElement('div');
            bubble.className = "chat-bubble user-bubble";
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

@report_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook():
    return "OK", 200

@report_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id):
    return jsonify({"status": "empty"})
