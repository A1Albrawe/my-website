import json
import urllib.request
from flask import Blueprint, request, jsonify

# إنشاء Blueprint رسمي ومستقل لنظام التليجرام متوافق كلياً مع معايير Vercel
tg_bot_blueprint = Blueprint('tg_bot', __name__)

# تثبيت بيانات حسابك السري والتوكين الفعلي الخاص بك
ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "1892403076:AAHOyUXyGNkNlYvDfJKuWrHZ4hUg3m22GYs"

# دالة مساعدة معزولة ومبنية على urllib الأساسية لضمان عدم انهيار السيرفر نهائياً
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
# مسار استقبال الشكاوى والمحادثات الحية من واجهة الموقع وتمريرها إليك فوراً
@tg_bot_blueprint.route('/api/send_message', methods=['POST'])
def send_msg_from_site():
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول')
    msg_type = data.get('type', 'محادثة حية')
    details = data.get('details', '')

    if not details:
        return jsonify({"status": "error", "message": "الرسالة فارغة"}), 400

    # تنسيق الرسالة لتظهر في حسابك على تليجرام بشكل منظم وجذاب جداً
    tg_text = (
        f"📥 *رسالة جديدة من الموقع*\n\n"
        f"👤 *الاسم:* {user}\n"
        f"🏷️ *النوع:* {msg_type}\n"
        f"💬 *الرسالة:* {details}\n\n"
        f"📌 يمكنك التواصل مع المستخدم عبر التليجرام إذا كان اسمه مسجلاً."
    )
    
    send_to_telegram(tg_text)
    return jsonify({"status": "success", "message": "تم الإرسال بنجاح"})
# مسارات معزولة مفرغة لضمان التوافق التام مع البنية التحتية السحابية لـ Vercel
@tg_bot_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook():
    return "OK", 200

@tg_bot_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id):
    return jsonify({"status": "empty"})
