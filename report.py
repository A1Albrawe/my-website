from flask import Blueprint, render_template_string

report_blueprint = Blueprint('report', __name__)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>مركز الدعم الفني - Albrawe</title>
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #0d1117;
            color: #c9d1d9; 
            padding: 0; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            box-sizing: border-box;
        }
        .header-nav {
            background-color: #161b22;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #f85149;
        }
        .back-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #58a6ff;
            padding: 6px 15px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
        }
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .maintenance-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-top: 4px solid #f85149;
            border-radius: 12px;
            padding: 40px 25px;
            max-width: 480px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            box-sizing: border-box;
        }
        .warn-icon {
            font-size: 50px;
            color: #f85149;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="color:#fff; font-weight:bold;">⚠️ حالة النظام</span>
    </div>

    <div class="main-container">
        <div class="maintenance-card">
            <div class="warn-icon">⚙️</div>
            <h2 style="color:#f0f6fc; margin:0 0 10px 0;">تحت الصيانة</h2>
            <!-- 🎯 تم مسح دوال الاستقبال والحفظ وقطع قنوات الاتصال بالكامل وتثبيت لوحة التعليق -->
            <p style="color:#f85149; font-weight:bold; font-size:16px; margin:0; line-height:1.6;">
                تم تعليق التفاعل وإيقاف استقبال الشكاوى والبلاغات مؤقتاً.<br>
                هذا القسم مغلق وتحت الصيانة الفنية الصارمة الآن.
            </p>
        </div>
    </div>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
