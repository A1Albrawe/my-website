import json
import urllib.request
from flask import Blueprint, request, jsonify, render_template_string

# إنشاء البلوبرينت الموحد لنظام الشات المتكامل والتليجرام
report_blueprint = Blueprint('report', __name__)

# الحساب الشخصي وتوكين البوت المعتمد والجاهز للربط الفوري
ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "1892403076:AAHOyUXyGNkNlYvDfJKuWrHZ4hUg3m22GYs"

# دالة إرسال الرسائل إلى تليجرام المطور ومبنية على urllib الأساسية لمنع الانهيار
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

# مسار استقبال حزم الشات الفورية من واجهة الموقع وتمريرها لتليجرامك
@report_blueprint.route('/api/send_message', methods=['POST'])
def send_msg_from_site():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول')
    msg_type = data.get('type', 'محادثة حية')
    details = data.get('details', '')
    session_id = data.get('session_id', '0')

    if not details:
        return jsonify({"status": "error", "message": "الرسالة فارغة"}), 400

    tg_text = (
        f"📥 *محادثة حية جديدة من الموقع*\n\n"
        f"👤 *الاسم:* {user}\n"
        f"🏷️ *النوع:* {msg_type}\n"
        f"💬 *الرسالة:* {details}\n\n"
        f"📌 للرد على هذا المستخدم، قم بعمل Reply على هذه الرسالة واكتب ردك فوراً.\n"
        f"`ID:{session_id}`" # معرّف الجلسة السري المعتمد للتوجيه العكسي
    )
    
    send_to_telegram(tg_text)
    return jsonify({"status": "success", "message": "تم الإرسال"})

# مسار الـ Webhook المحدث الذي يلتقط ردود الـ Reply من تليجرامك بأمان ويخزنها مؤقتاً
@report_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json() or {}
    
    if "message" in update and "reply_to_message" in update["message"]:
        message = update["message"]
        sender_id = str(message["from"]["id"])
        
        # التأكد من أن الرد قادم من حسابك الشخصي المعتمد فقط لحظر الغش والتسلل
        if sender_id == str(ADMIN_CHAT_ID):
            reply_text = message.get("text", "")
            original_text = message["reply_to_message"].get("text", "")
            
            if "ID:" in original_text:
                try:
                    session_id = original_text.split("ID:")[-1].strip()
                    if not hasattr(report_blueprint, 'live_replies'):
                        report_blueprint.live_replies = {}
                    report_blueprint.live_replies[session_id] = reply_text
                except Exception:
                    pass

    return "OK", 200

# مسار الفحص الإطاري (Polling API) لمتصفح الزائر لسحب ردودك الحية وعرضها له
@report_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id):
    if not hasattr(report_blueprint, 'live_replies'):
        report_blueprint.live_replies = {}
        
    reply = report_blueprint.live_replies.pop(session_id, None)
    if reply:
        return jsonify({"status": "found", "reply": reply})
    return jsonify({"status": "empty"})
REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Chat</title>
    <link rel="stylesheet" href="https://cloudflare.com">
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
            display: inline-flex;
            align-items: center;
            gap: 6px;
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
        h3 { margin: 0 0 15px 0; text-align: center; font-size: 15px; font-weight: bold; border-bottom: 1px dashed #000; padding-bottom: 5px; }
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
        textarea.input-field { resize: none; height: 60px; }

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
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }

        /* حاوية الشات الحي المطور التناظرية لتبادل الرسائل والردود */
        .chat-box-area {
            margin-top: 15px;
            background: rgba(0, 0, 0, 0.08);
            padding: 10px;
            border-radius: 6px;
            font-size: 12px;
            border: 2px solid #000;
            height: 130px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .chat-bubble { padding: 6px 10px; border-radius: 6px; max-width: 85%; font-weight: bold; line-height: 1.4; word-wrap: break-word; }
        .user-bubble { background: #000; color: #8c9f21; align-self: flex-start; text-align: right; border-radius: 6px 6px 0 6px; }
        .admin-bubble { background: #cbd3d8; color: #000; align-self: flex-end; text-align: right; border-radius: 6px 6px 6px 0; border: 1px solid #000; }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> القائمة الرئيسية</a>
    
    <div class="nokia-phone-style">
        <div class="nokia-screen-style">
            <div class="screen-header">
                <span><i class="fas fa-comments"></i> شات الدعم الفني المباشر</span>
                <span>NOKIA</span>
            </div>
            
            <form id="chatForm" onsubmit="handleFormSubmit(event)">
                <div class="form-group" style="display:none;">
                    <input type="text" id="userName" class="input-field" value="زائر" required maxlength="15">
                </div>
                
                <div class="chat-box-area" id="chatBoxContainer">
                    <div style="text-align:center; color:rgba(0,0,0,0.5); font-weight:bold; margin:auto;" id="emptyHint">افتح محادثة حية واكتب رسالتك بالأسفل...</div>
                </div>
                
                <div class="form-group" style="margin-top:12px;">
                    <textarea id="issueDetails" class="input-field" placeholder="اكتب رسالتك هنا واضغط إرسال..." required maxlength="200"></textarea>
                </div>
                
                <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i> إرسال الرسالة للبوت
                </button>
            </form>
        </div>
    </div>
    <script>
        // توليد معرّف جلسة عشوائي ومستقل لكل زائر لمنع تداخل الرسائل والردود بين المستخدمين
        const currentSessionId = "session_" + Math.floor(Math.random() * 899999 + 100000);

        function setupUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) { document.getElementById('userName').value = savedUser; }
        }

        function handleFormSubmit(event) {
            event.preventDefault();
            
            const user = document.getElementById('userName').value.trim();
            const details = document.getElementById('issueDetails').value.trim();
            
            if (!details) return;

            // طباعة رسالة الزائر فوراً داخل صندوق الشات بلون نوكيا الأسود والأخضر
            appendChatBubble(details, "user-bubble");
            document.getElementById('issueDetails').value = "";

            // إرسال الحزمة الفورية لخادم بايثون لتوصيلها إلى تليجرامك الشخصي عبر البوت
            fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user: user,
                    type: "شات حي المطور",
                    details: details,
                    session_id: currentSessionId
                })
            });
        }

        function appendChatBubble(text, className) {
            const container = document.getElementById('chatBoxContainer');
            const hint = document.getElementById('emptyHint');
            if (hint) hint.remove();
            
            const bubble = document.createElement('div');
            bubble.className = "chat-bubble " + className;
            bubble.innerText = text;
            container.appendChild(bubble);
            container.scrollTop = container.scrollHeight;
        }

        // الفحص التلقائي الإطاري (Long-Polling) للاستماع لردودك من التليجرام كل ثانيتين
        setInterval(() => {
            fetch('/api/get_reply/' + currentSessionId)
            .then(res => res.json())
            .then(data => {
                if (data.status === "found") {
                    // طباعة رد المطور فوراً داخل صندوق الشات بلون رمادي كلاسيكي مميز
                    appendChatBubble(data.reply, "admin-bubble");
                }
            });
        }, 2000);

        setupUser();
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
