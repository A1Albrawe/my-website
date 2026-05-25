from flask import Flask, render_template_string

app = Flask(__name__)

# تصميم الموقع المحدث مع القائمة الجانبية وزر التليجرام
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع Albrawe</title>
    <!-- استدعاء أيقونات FontAwesome لشعار التليجرام والقائمة -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background-color: #f0f2f5; 
            padding: 50px; 
            margin: 0;
            transition: margin-right 0.3s ease;
        }
        
        /* زر فتح القائمة الجانبية */
        .menu-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            font-size: 24px;
            background: #1877f2;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        /* تصميم القائمة الجانبية */
        .sidebar {
            height: 100%;
            width: 0;
            position: fixed;
            z-index: 999;
            top: 0;
            right: 0;
            background-color: #1a1a1a;
            overflow-x: hidden;
            transition: 0.3s ease;
            padding-top: 60px;
            text-align: right;
            box-shadow: -2px 0 10px rgba(0,0,0,0.3);
        }

        /* روابط القائمة الجانبية بالترتيب المطلوب */
        .sidebar a {
            padding: 15px 25px;
            text-decoration: none;
            font-size: 20px;
            color: #b3b3b3;
            display: block;
            transition: 0.2s;
            border-bottom: 1px solid #2d2d2d;
        }

        .sidebar a:hover {
            color: white;
            background-color: #1877f2;
            padding-right: 35px;
        }

        /* زر إغلاق القائمة الجانبية */
        .sidebar .close-btn {
            position: absolute;
            top: 15px;
            left: 25px;
            font-size: 30px;
            color: #bbb;
            cursor: pointer;
        }
        .sidebar .close-btn:hover { color: white; }

        /* المحتوى الرئيسي الحالي للموقع */
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            display: inline-block; 
            max-width: 500px;
            margin-top: 40px;
        }
        h1 { color: #1877f2; margin-bottom: 10px; }
        p { color: #555; font-size: 18px; line-height: 1.6; }
        
        /* زر حساب التليجرام */
        .telegram-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #0088cc;
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
            box-shadow: 0 4px 10px rgba(0, 136, 204, 0.3);
            transition: all 0.3s ease;
        }
        .telegram-btn i { margin-left: 10px; font-size: 22px; }
        .telegram-btn:hover {
            background-color: #0077b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 136, 204, 0.4);
        }

        .footer { margin-top: 20px; color: #888; font-size: 14px; }
    </style>
</head>
<body>

    <!-- زر فتح القائمة -->
    <button class="menu-btn" onclick="toggleNav()"><i class="fas fa-bars"></i> القائمة</button>

    <!-- القائمة الجانبية المحدثة بالترتيب المطلوب -->
    <div id="mySidebar" class="sidebar">
        <span class="close-btn" onclick="toggleNav()">&times;</span>
        <a href="#"><i class="fas fa-home"></i> الصفحة الرئيسية</a>
        <a href="#"><i class="fas fa-code"></i> المشاريع</a>
        <a href="#"><i class="fas fa-link"></i> روابط أخرى</a>
        <a href="#"><i class="fas fa-info-circle"></i> حول هذا</a>
    </div>

    <!-- الحفاظ على البيانات والمحتوى الحالي للموقع -->
    <div class="container">
        <h1>مرحباً بك في موقع albrawe</h1>
        <p>تم تشغيل الموقع بنجاح وهو الآن متاح للجميع على الإنترنت!</p>
        
        <!-- إضافة زر التليجرام الخاص بك -->
        <a href="https://t.me" target="_blank" class="telegram-btn">
            <i class="fab fa-telegram-plane"></i> تليجرام @a1albrawe
        </a>

        <div class="footer">يعمل بواسطة Python & Flask</div>
    </div>

    <!-- كود الجافا سكريبت لفتح وإغلاق القائمة بسلاسة -->
    <script>
        let sidebarOpen = false;
        function toggleNav() {
            const sidebar = document.getElementById("mySidebar");
            if (!sidebarOpen) {
                sidebar.style.width = "250px";
                sidebarOpen = true;
            } else {
                sidebar.style.width = "0";
                sidebarOpen = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
