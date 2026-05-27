import os
import sys

# إضافة المسار الرئيسي للمشروع لضمان قراءة باقي الملفات
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import app
from serverless_wsgi import handle_request

def handler(event, context):
    return handle_request(app, event, context)
