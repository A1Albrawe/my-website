from flask import Flask
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint
from report import report_blueprint

# استيراد الحزم (Blueprints) المخصصة للصفحات والـ API ولوحة الإدارة
from pages import pages_blueprint
from api import api_blueprint

app = Flask(__name__)
app.secret_key = "ALBRAWE_FINAL_LOCKED_2026"

# تسجيل جميع الحزم البرمجية الخاصة بصفحات وألعاب موقعك
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)
app.register_blueprint(report_blueprint)
app.register_blueprint(pages_blueprint)
app.register_blueprint(api_blueprint)

@app.after_request
def inject_clean_dropdown_fix(response):
    """
    دالة حقن معالجة الاستجابة السحابية.
    تقوم بفحص صفحات الـ HTML وتلقائياً بحقن سكريبت التتبع لـ Vercel Analytics 
    قبل وسم الإغلاق لضمان احتساب الزيارات والـ Page Views في لوحة التحكم بشكل حي ومستقر.
    """
    if response.content_type.startswith('text/html'):
        text = response.get_data(as_text=True)
        
        # كود سكريبت التتبع القياسي لـ Vercel المطلوب في لوحة التحكم لديك لجمع البيانات حياً
        vercel_tracking_script = """
        <!-- Vercel Web Analytics Tracking Code -->
        <script defer src="/_vercel/insights/script.js"></script>
        """
        
        # حقن السكريبت تلقائياً قبل إغلاق جسم الصفحة ليعمل في كافة أرجاء الموقع
        if "</body>" in text:
            text = text.replace("</body>", f"{vercel_tracking_script}</body>")
            
        response.set_data(text)
    return response

if __name__ == '__main__':
    app.run(debug=True)
