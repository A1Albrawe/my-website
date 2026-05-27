import os
import sys

# لتضمين الملفات والمجلدات البرمجية الأساسية في المسار
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# استيراد تطبيق فلاسك الخاص بك من ملف app.py أو index.py الرئيسي
from app import app 

# مكتبة تحويل Flask إلى Serverless متوافقة مع AWS Lambda / Netlify
from serverless_wsgi import handle_request

def handler(event, context):
    return handle_request(app, event, context)
