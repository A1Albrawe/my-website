import requests
from flask import Blueprint, request, jsonify

# إنشاء Blueprint رسمي ومستقل لنظام الدعم الفني والتليجرام
tg_bot_blueprint = Blueprint('tg_bot', __name__)

# تفعيل وتثبيت بيانات حسابك السري والتوكين الفعلي المرفق من طرفك
ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "1892403076:AAHOyUXyGNkNlYvDfJKuWrHZ4hUg3m22GYs"

# دالة مساعدة لإرسال الرسائل والمحادثات الحية إلى حسابك في تليجرام
def send_to_telegram(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass
# مسار استقبال الشكاوى والمحادثات الحية من واجهة الموقع وتمريرها إليك
@tg_bot_blueprint.route('/api/send_message', methods=['POST'])
def send_msg_from_site():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول')
    msg_type = data.get('type', 'محادثة حية')
    details = data.get('details', '')
    session_id = data.get('session_id', '0')

    if not details:
        return jsonify({"status": "error", "message": "الرسالة فارغة"}), 400

    # تنسيق الرسالة لتظهر في حسابك على تليجرام بشكل منظم جداً مع كود الـ Reply
    tg_text = (
        f"📥 *رسالة جديدة من الموقع*\n\n"
        f"👤 *الاسم:* {user}\n"
        f"🏷️ *النوع:* {msg_type}\n"
        f"💬 *الرسالة:* {details}\n\n"
        f"📌 للرد على هذا المستخدم، قم بعمل Reply على هذه الرسالة واكتب ردك.\n"
        f"`ID:{session_id}`" # هذا السطر البرمجي مشفر ليتعرف البوت على الزائر عند ردك
    )
    
    send_to_telegram(tg_text)
    return jsonify({"status": "success", "message": "تم الإرسال"})
# مسار الـ Webhook السري الذي يستمع لردودك داخل التليجرام وينقلها للمتصفح فوراً
@tg_bot_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json() or {}
    
    # التأكد من أن الرسالة عبارة عن "رد" (Reply) ومن حسابك الشخصي المعتمد فقط لضمان الأمان
    if "message" in update and "reply_to_message" in update["message"]:
        message = update["message"]
        sender_id = str(message["from"]["id"])
        
        if sender_id == str(ADMIN_CHAT_ID):
            reply_text = message.get("text", "")
            original_text = message["reply_to_message"].get("text", "")
            
            # استخراج الـ Session ID الخاص بالزائر لإعادة توجيه ردك إليه في نفس اللحظة
            if "ID:" in original_text:
                try:
                    session_id = original_text.split("ID:")[-1].strip()
                    if not hasattr(tg_bot_blueprint, 'replies'):
                        tg_bot_blueprint.replies = {}
                    tg_bot_blueprint.replies[session_id] = reply_text
                except Exception:
                    pass

    return "OK", 200

# مسار يقوم متصفح الزائر بفحصه بانتظام كل ثانيتين لمعرفة هل قمت بالرد عليه أم لا
@tg_bot_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id):
    if not hasattr(tg_bot_blueprint, 'replies'):
        tg_bot_blueprint.replies = {}
        
    reply = tg_bot_blueprint.replies.pop(session_id, None)
    if reply:
        return jsonify({"status": "found", "reply": reply})
    return jsonify({"status": "empty"})
