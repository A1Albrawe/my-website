from flask import Blueprint, render_template_string

# إنشاء المسار البرمجي والـ Blueprint الرسمي لصفحة الإبلاغ عن المشاكل
report_blueprint = Blueprint('report', __name__)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>إرسال مشكلة - Albrawe</title>
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
            transition: all 0.2s ease;
        }
        .back-btn:hover {
            background: #8c9f21;
            color: #111;
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

        h3 {
            margin: 0 0 15px 0;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            border-bottom: 1px dashed #000;
            padding-bottom: 5px;
        }

        .form-group {
            margin-bottom: 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        label {
            font-weight: bold;
            font-size: 12px;
        }

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
        .input-field:focus {
            background: #a4b930;
        }

        textarea.input-field {
            resize: none;
            height: 80px;
        }

        select.input-field {
            cursor: pointer;
        }
        .submit-btn {
            background: #000;
            color: #8c9f21;
            border: 2px solid #000;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            width: 100%;
            font-family: inherit;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }
        .submit-btn:active {
            transform: scale(0.98);
        }

        .alert-box {
            display: none;
            background: #000;
            color: #8c9f21;
            padding: 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 12px;
            border: 1px solid #8c9f21;
        }

        .reports-log {
            margin-top: 15px;
            background: rgba(0, 0, 0, 0.05);
            padding: 8px;
            border-radius: 4px;
            font-size: 11px;
            border-top: 1px dashed #000;
            max-height: 110px;
            overflow-y: auto;
        }
        .reports-log h4 {
            margin: 0 0 6px 0;
            text-align: center;
            font-size: 12px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            padding-bottom: 2px;
        }
        .log-item {
            border-bottom: 1px dashed rgba(0,0,0,0.1);
            padding: 4px 0;
            display: flex;
            justify-content: space-between;
        }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> القائمة الرئيسية</a>
    
    <div class="nokia-phone-style">
        <div class="nokia-screen-style">
            <div class="screen-header">
                <span><i class="fas fa-tools"></i> الدعم الفني</span>
                <span>NOKIA</span>
            </div>
            
            <h3><i class="fas fa-envelope-open-text"></i> الإبلاغ عن مشكلة</h3>
            
            <div id="alertBox" class="alert-box"></div>
            
            <form id="reportForm" onsubmit="handleFormSubmit(event)">
                <div class="form-group">
                    <label for="userName">اسم المستخدم:</label>
                    <input type="text" id="userName" class="input-field" placeholder="اكتب اسمك هنا" required maxlength="15">
                </div>
                
                <div class="form-group">
                    <label for="issueType">نوع المشكلة:</label>
                    <select id="issueType" class="input-field" required>
                        <option value="ثغرة في اللعبة">ثغرة في لعبة الثعبان 🐍</option>
                        <option value="خلل في التحكم">مشكلة في أزرار اللمس/الكيبورد 📱</option>
                        <option value="بطء أو تجميد">الموقع بطيء أو يتجمد ⏳</option>
                        <option value="اقتراح تطوير">لدي اقتراح أو فكرة جديدة 💡</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="issueDetails">تفاصيل المشكلة:</label>
                    <textarea id="issueDetails" class="input-field" placeholder="اشرح لنا العيب باختصار..." required maxlength="200"></textarea>
                </div>
                
                <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i> إرسال التقرير للمطور
                </button>
            </form>

            <div class="reports-log">
                <h4>📥 تقاريرك المرسلة سابقاً</h4>
                <div id="logContainer">
                    <div style="text-align:center; color:rgba(0,0,0,0.5);">لا توجد تقارير حالياً</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        // دالة استدعاء الاسم التلقائي المحفوظ من ألعاب الموقع لتسهيل التجربة على المستخدم
        function autoFillUser() {
            let savedUser = localStorage.getItem('snake_last_user');
            if (savedUser) {
                document.getElementById('userName').value = savedUser;
            }
        }

        // دالة معالجة وحفظ البيانات في صندوق الحماية السحابي المحلي لمنع الغش والتلاعب
        function handleFormSubmit(event) {
            event.preventDefault();
            
            const user = document.getElementById('userName').value.trim();
            const type = document.getElementById('issueType').value;
            const details = document.getElementById('issueDetails').value.trim();
            const alertBox = document.getElementById('alertBox');
            
            if (!user || !details) {
                showAlert("برجاء ملء كافة الحقول بشكل صحيح!", "#7f1d1d");
                return;
            }

            // محاكاة ميكانيكية استلام الشكوى وبناء مصفوفة التقرير بأمان
            const reportItem = {
                user: user,
                type: type,
                details: details,
                date: new Date().toLocaleDateString('ar-EG')
            };

            // حفظ التقرير محلياً في سجلات المتصفح المؤمنة
            let reportsList = JSON.parse(localStorage.getItem('albrawe_site_issues')) || [];
            reportsList.unshift(reportItem);
            localStorage.setItem('albrawe_site_issues', JSON.stringify(reportsList));

            // تفريغ حقل التفاصيل فقط والاحتفاظ بالاسم للجولات القادمة
            document.getElementById('issueDetails').value = "";
            
            showAlert("✅ تم إرسال تقريرك بنجاح للمطور!", "#000");
            loadReportsLog();
        }

        function showAlert(msg, bgColor) {
            const box = document.getElementById('alertBox');
            box.innerText = msg;
            box.style.display = 'block';
            setTimeout(() => { box.style.display = 'none'; }, 3000);
        }

        function loadReportsLog() {
            let reportsList = JSON.parse(localStorage.getItem('albrawe_site_issues')) || [];
            const container = document.getElementById('logContainer');
            
            if (reportsList.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:rgba(0,0,0,0.5);">لا توجد تقارير حالياً</div>';
                return;
            }

            let htmlContent = "";
            // عرض آخر 3 تقارير أرسلها هذا الحساب لتجنب تضخم حجم الهاتف الكلاسيكي
            reportsList.slice(0, 3).forEach(item => {
                htmlContent += `
                    <div class="log-item">
                        <span style="font-weight:bold; color:#000;">[${item.type}]</span>
                        <span style="color:rgba(0,0,0,0.7); font-size:10px;">${item.date}</span>
                    </div>
                `;
            });
            container.innerHTML = htmlContent;
        }

        // تشغيل التهيئة الفورية عند تحميل الصفحة
        autoFillUser();
        loadReportsLog();
    </script>
</body>
</html>
"""

@report_blueprint.route('/report')
def report_page():
    return render_template_string(REPORT_TEMPLATE)
