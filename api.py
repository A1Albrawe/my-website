import datetime
from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

# 🔒 الذاكرة السحابية المركزية المؤقتة بداخل السيرفر لجمع البيانات
CENTRAL_ANALYTICS_DB = []
CENTRAL_COMPLAINTS_DB = []

@api_blueprint.route('/api/log_visit', methods=['POST'])
def log_visit():
    """مسار استقبال وحقن حركة دخول الزائر وتسجيل نظامه"""
    global CENTRAL_ANALYTICS_DB
    data = request.get_json() or {}
    username = data.get('username', 'زائر مجهول').strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    
    # التحقق مما إذا كان الزائر مسجلاً مسبقاً لتحديث بياناته أو إنشائه
    user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
    
    if not user_entry:
        user_entry = {
            "username": username,
            "userAgent": user_agent,
            "loginTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": 0,
            "snakeTime": 0,
            "tetrisTime": 0
        }
        CENTRAL_ANALYTICS_DB.append(user_entry)
        
    return jsonify({"status": "success"})

@api_blueprint.route('/api/update_duration', methods=['POST'])
def update_duration():
    """تحديث الوقت المستغرق للزائر حياً في الموقع وفي الألعاب"""
    global CENTRAL_ANALYTICS_DB
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    game_type = data.get('game', '') # snake أو tetris أو site
    
    if username:
        user_entry = next((item for item in CENTRAL_ANALYTICS_DB if item["username"] == username), None)
        if user_entry:
            if game_type == 'snake':
                user_entry["snakeTime"] += 5
            elif game_type == 'tetris':
                user_entry["tetrisTime"] += 5
            else:
                user_entry["duration"] += 5
                
    return jsonify({"status": "success"})

@api_blueprint.route('/api/admin_get_all_data', methods=['GET'])
def admin_get_all_data():
    """تغذية لوحة الإدارة بكافة التحليلات والشكاوى المخزنة سحابياً"""
    return jsonify({
        "analytics": CENTRAL_ANALYTICS_DB,
        "reports": CENTRAL_COMPLAINTS_DB
    })

@api_blueprint.route('/api/admin_clear_data', methods=['POST'])
def admin_clear_data():
    """مسح وتصفير الذاكرة السحابية بالكامل بطلب من الآدمن"""
    global CENTRAL_ANALYTICS_DB, CENTRAL_COMPLAINTS_DB
    CENTRAL_ANALYTICS_DB = []
    CENTRAL_COMPLAINTS_DB = []
    return jsonify({"status": "cleared"})
