from flask import Flask, render_template_string

app = Flask(__name__)

# تصميم الموقع بلغة HTML و CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع Albrawe</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background-color: #f0f2f5; 
            padding: 50px; 
            margin: 0;
        }
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            display: inline-block; 
            max-width: 500px;
        }
        h1 { color: #1877f2; margin-bottom: 10px; }
        p { color: #555; font-size: 18px; line-height: 1.6; }
        .footer { margin-top: 20px; color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>مرحباً بك في موقع albrawe</h1>
        <p>تم تشغيل الموقع بنجاح وهو الآن متاح للجميع على الإنترنت!</p>
        <div class="footer">يعمل بواسطة Python & Flask</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()

