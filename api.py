import datetime
from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

# 🔒 الذاكرة السحابية المركزية المؤقتة بداخل السيرفر لجمع وتحليل البيانات عبر الإنترنت
CENTRAL_ANALYTICS_DB = []
CENTRAL_COMPLAINTS_DB = []

# 📈 العداد التاريخي الشامل لحساب جميع الزيارات الكلية للموقع منذ تشغيله دون تصفير
TOTAL_HISTORICAL_VISITS = 0

@api_blueprint.route('/api/log_visit', methods=['POST'])
def log_visit():
    """مسار رصد وحقن مستخدم جديد قادم للموقع بالتفصيل الجغرافي والموديل الدقيق"""
    global CENTRAL_ANALYTICS_DB, TOTAL_HISTORICAL_VISITS
    data = request.get_json() or {}
    username = data.get('username', 'زائر مجهول').strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    
    location = data.get('location', 'جاري جلب الموقع...').strip()
    
    device_model = "كمبيوتر / غير معروف"
    ua_lower = user_agent.lower()
    
    if "android" in ua_lower:
        device_model = "هاتف أندرويد عالي الحماية"
        if "samsung" in ua_lower or "sm-" in ua_lower:
            device_model = "Samsung Galaxy 📱"
        elif "redmi" in ua_lower or "xiaomi" in ua_lower or "mi " in ua_lower:
            device_model = "Xiaomi / Redmi 📱"
        elif "huawei" in ua_lower or "hua" in ua_lower:
            device_model = "Huawei Phone 📱"
        elif "oppo" in ua_lower:
            device_model = "Oppo Phone 📱"
        elif "infinix" in ua_lower:
            device_model = "Infinix Phone 📱"
    elif "iphone" in ua_lower:
        device_model = "iPhone 🍏"
        if "iphone os 16" in ua_lower: device_model = "iPhone 14/15 Pro 🍏"
        elif "iphone os 17" in ua_lower: device_model = "iPhone 15/16 Pro 🍏"
        elif "iphone os 18" in ua_lower: device_model = "iPhone 16/17 Pro 🍏"
    elif "windows" in ua_lower:
        device_model = "Windows PC 💻"
    elif "macintosh" in ua_lower:
        device_model = "MacBook / macOS 💻"

    user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
    
    if not user_entry:
        # 📈 زيادة عداد الزيارات الشامل فوراً عند رصد بصمة زائر جديد كلياً
        TOTAL_HISTORICAL_VISITS += 1
        
        user_entry = {
            "username": username,
            "deviceModel": device_model,
            "location": location,
            "loginTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": 0,
            "snakeTime": 0,
            "tetrisTime": 0,
            "xoTime": 0,       
            "shooterTime": 0,  
            "clickerTime": 0   
        }
        CENTRAL_ANALYTICS_DB.append(user_entry)
    else:
        user_entry["location"] = location
        user_entry["deviceModel"] = device_model
        
    return jsonify({"status": "success"})
@api_blueprint.route('/api/update_duration', methods=['POST'])
def update_duration():
    global CENTRAL_ANALYTICS_DB
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    game_type = data.get('game', '')
    
    if username:
        user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
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
    return jsonify({"status": "success"})

@api_blueprint.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    global CENTRAL_COMPLAINTS_DB
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول').strip()
    details = data.get('details', '').strip()
    if details:
        complaint_entry = {
            "user": user,
            "details": details,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        CENTRAL_COMPLAINTS_DB.append(complaint_entry)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    return jsonify({
        "analytics": CENTRAL_ANALYTICS_DB,
        "reports": CENTRAL_COMPLAINTS_DB,
        "historicalVisits": TOTAL_HISTORICAL_VISITS
    })

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    global CENTRAL_ANALYTICS_DB, CENTRAL_COMPLAINTS_DB
    CENTRAL_ANALYTICS_DB = []
    CENTRAL_COMPLAINTS_DB = []
    return jsonify({"status": "cleared"})
