import datetime
import os
import json
from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

# المسارات البرمجية للملفات النصية لتخزين البيانات للأبد سحابياً على خوادم Vercel
ANALYTICS_FILE = "static/analytics_storage.json"
COMPLAINTS_FILE = "static/complaints_storage.json"
VISITS_COUNT_FILE = "static/visits_counter.txt"

def load_data_from_storage():
    """دالة استرجاع البيانات المخزنة مسبقاً لحظر مسح السجل تلقائياً"""
    analytics = []
    complaints = []
    visits = 0
    try:
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                analytics = json.load(f)
        if os.path.exists(COMPLAINTS_FILE):
            with open(COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
                complaints = json.load(f)
        if os.path.exists(VISITS_COUNT_FILE):
            with open(VISITS_COUNT_FILE, 'r', encoding='utf-8') as f:
                visits = int(f.read().strip())
    except Exception:
        pass
    return analytics, complaints, visits

def save_data_to_storage(analytics, complaints, visits):
    """دالة الكتابة الفورية والصلبة للبيانات داخل مستندات السيرفر لمنع ضياعها"""
    try:
        os.makedirs("static", exist_ok=True)
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, ensure_ascii=False, indent=4)
        with open(COMPLAINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(complaints, f, ensure_ascii=False, indent=4)
        with open(VISITS_COUNT_FILE, 'w', encoding='utf-8') as f:
            f.write(str(visits))
    except Exception:
        pass

@api_blueprint.route('/api/log_visit', methods=['POST'])
def log_visit():
    """رصد وحقن الزوار حياً ومزامنتهم مع السجل الدائم الذي لا يُحذف"""
    analytics, complaints, visits = load_data_from_storage()
    data = request.get_json() or {}
    username = data.get('username', 'زائر مجهول').strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    location = data.get('location', 'جاري جلب الموقع...').strip()
    
    device_model = "كمبيوتر / غير معروف"
    ua_lower = user_agent.lower()
    if "android" in ua_lower:
        device_model = "هاتف أندرويد عالي الحماية"
        if "samsung" in ua_lower or "sm-" in ua_lower: device_model = "Samsung Galaxy 📱"
        elif "redmi" in ua_lower or "xiaomi" in ua_lower or "mi " in ua_lower: device_model = "Xiaomi / Redmi 📱"
        elif "huawei" in ua_lower or "hua" in ua_lower: device_model = "Huawei Phone 📱"
        elif "oppo" in ua_lower: device_model = "Oppo Phone 📱"
        elif "infinix" in ua_lower: device_model = "Infinix Phone 📱"
    elif "iphone" in ua_lower:
        device_model = "iPhone 🍏"
        if "iphone os 16" in ua_lower: device_model = "iPhone 14/15 Pro 🍏"
        elif "iphone os 17" in ua_lower: device_model = "iPhone 15/16 Pro 🍏"
        elif "iphone os 18" in ua_lower: device_model = "iPhone 16/17 Pro 🍏"
    elif "windows" in ua_lower: device_model = "Windows PC 💻"
    elif "macintosh" in ua_lower: device_model = "MacBook / macOS 💻"

    user_entry = next((item for item in analytics if item["username"] == username), None)
    
    if not user_entry:
        visits += 1 # تحديث العداد التاريخي كلياً للأبد
        user_entry = {
            "username": username,
            "deviceModel": device_model,
            "location": location,
            "loginTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": 0, "snakeTime": 0, "tetrisTime": 0, "xoTime": 0, "shooterTime": 0, "clickerTime": 0   
        }
        analytics.append(user_entry)
    else:
        user_entry["location"] = location
        user_entry["deviceModel"] = device_model
        
    save_data_to_storage(analytics, complaints, visits)
    return jsonify({"status": "success"})
@api_blueprint.route('/api/update_duration', methods=['POST'])
def update_duration():
    analytics, complaints, visits = load_data_from_storage()
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    game_type = data.get('game', '')
    
    if username:
        user_entry = next((item for item in analytics if item["username"] == username), None)
        if user_entry:
            if game_type == 'snake': user_entry["snakeTime"] += 5
            elif game_type == 'tetris': user_entry["tetrisTime"] += 5
            elif game_type == 'xo':
                if "xoTime" not in user_entry: user_entry["xoTime"] = 0
                user_entry["xoTime"] += 5
            elif game_type == 'shooter':
                if "shooterTime" not in user_entry: user_entry["shooterTime"] = 0
                user_entry["shooterTime"] += 5
            elif game_type == 'clicker':
                if "clickerTime" not in user_entry: user_entry["clickerTime"] = 0
                user_entry["clickerTime"] += 5
            else:
                user_entry["duration"] += 5
                
    save_data_to_storage(analytics, complaints, visits)
    return jsonify({"status": "success"})

@api_blueprint.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    analytics, complaints, visits = load_data_from_storage()
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول').strip()
    details = data.get('details', '').strip()
    if details:
        complaint_entry = {
            "user": user, "details": details,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        complaints.append(complaint_entry)
        save_data_to_storage(analytics, complaints, visits)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    analytics, complaints, visits = load_data_from_storage()
    return jsonify({
        "analytics": analytics,
        "reports": complaints,
        "historicalVisits": visits
    })

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    """تصفير السجلات الفردية والنشطة بطلب من الآدمن مع الحفاظ على العداد التاريخي والشكاوى للأبد"""
    analytics, complaints, visits = load_data_from_storage()
    # يتم مسح سجل تصفح الحركة الحالي فقط مع الإبقاء على ملفات المحتوى التاريخي ثابتة وحية ومؤمنة
    save_data_to_storage([], complaints, visits)
    return jsonify({"status": "cleared"})
