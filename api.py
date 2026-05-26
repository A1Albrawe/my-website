import datetime
from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

# 🔒 الذاكرة السحابية المركزية المؤقتة بداخل السيرفر لجمع وتحليل البيانات عبر الإنترنت
CENTRAL_ANALYTICS_DB = []
CENTRAL_COMPLAINTS_DB = []

@api_blueprint.route('/api/log_visit', methods=['POST'])
def log_visit():
    """مسار رصد وحقن مستخدم جديد قادم للموقع"""
    global CENTRAL_ANALYTICS_DB
    data = request.get_json() or {}
    username = data.get('username', 'زائر مجهول').strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    
    user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
    
    # تأمين الهيكلية الشاملة لتسجيل العدادات الخماسية للألعاب كاملة دون نسيان
    if not user_entry:
        user_entry = {
            "username": username,
            "userAgent": user_agent,
            "loginTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": 0,
            "snakeTime": 0,
            "tetrisTime": 0,
            "xoTime": 0,       # عداد لعبة XO المضافة حديثاً
            "shooterTime": 0,  # عداد لعبة قاصف الفضاء
            "clickerTime": 0   # عداد لعبة اختبار النقر السريع
        }
        CENTRAL_ANALYTICS_DB.append(user_entry)
        
    return jsonify({"status": "success"})
@api_blueprint.route('/api/update_duration', methods=['POST'])
def update_duration():
    """تحديث نبضات عداد بقاء المستخدم والمدد المستغرقة في الألعاب حياً بالثانية"""
    global CENTRAL_ANALYTICS_DB
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    game_type = data.get('game', '')
    
    if username:
        user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
        if user_entry:
            # معالجة فرز نبضات الـ 5 ثوانٍ السحابية الموجهة من المتصفح تلقائياً
            if game_type == 'snake':
                user_entry["snakeTime"] += 5
            elif game_type == 'tetris':
                user_entry["tetrisTime"] += 5
            elif game_type == 'xo':
                # تأمين التحديث لعداد لعبة XO في الخلفية حياً
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
    """تلقي الشكاوى والبلاغات الفنية عبر الإنترنت وحفظها سحابياً بالتوقيت الحالي لعام 2026"""
    global CENTRAL_COMPLAINTS_DB
    data = request.get_json() or {}
    user = data.get('user', 'زائر مجهول').strip()
    details = data.get('details', '').strip()
    
    if details:
        complaint_entry = {
            "user": user,
            "details": details,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M") # المزامنة السحابية الحية للوقت
        }
        CENTRAL_COMPLAINTS_DB.append(complaint_entry)
        return jsonify({"status": "success"})
        
    return jsonify({"status": "error", "message": "No text provided"}), 400

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    """تغذية لوحة الآدمن بالتحليلات وبلاغات الشكاوى الحية فوراً من أي جهاز"""
    return jsonify({
        "analytics": CENTRAL_ANALYTICS_DB,
        "reports": CENTRAL_COMPLAINTS_DB
    })

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    """تصفير قاعدة البيانات السحابية المؤقتة بطلب من لوحة الآدمن"""
    global CENTRAL_ANALYTICS_DB, CENTRAL_COMPLAINTS_DB
    CENTRAL_ANALYTICS_DB = []
    CENTRAL_COMPLAINTS_DB = []
    return jsonify({"status": "cleared"})
