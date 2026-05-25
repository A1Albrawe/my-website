import requests
from flask import Blueprint, request, jsonify

# إنشاء Blueprint رسمي ومستقل لنظام التليجرام متوافق مع سيرفرات Vercel
tg_bot_blueprint = Blueprint('tg_bot', __name__)

# تثبيت بيانات حسابك السري والتوكين الفعلي الخاص بك
ADMIN_CHAT_ID = "1178062571"
BOT_TOKEN = "1892403076:AAHOyUXyGNkNlYvDfJKuWrHZ4hUg3m22GYs"

# دالة مساعدة معزولة لإرسال الرسائل والمحادثات الحية إلى حسابك في تليجرام بأمان
def send_to_telegram(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
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
        f"📌 يمكنك فتح حساب المستخدم أو التواصل معه عبر التليجرام إذا كان اسمه مسجلاً."
    )
    
    send_to_telegram(tg_text)
    return jsonify({"status": "success", "message": "تم الإرسال بنجاح"})
# مسارات الأمان المعزولة المفرغة لضمان استقرار السيرفر وعدم قراءة أي ردود وهمية تتسبب في تحطيم الموقع
@tg_bot_blueprint.route('/api/telegram_webhook', methods=['POST'])
def telegram_webhook():
    return "OK", 200

@tg_bot_blueprint.route('/api/get_reply/<session_id>', methods=['GET'])
def get_reply(session_id):
    return jsonify({"status": "empty"})
