import sys
import os

# تأمين مسار المشروع الحالي لضمان قراءة كافة الـ Blueprints والحزم دون أخطاء استيراد
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استدعاء متغير التطبيق النواة من ملف app.py
from app import app

# Vercel يتوقع استقبال المتغير باسم app ليقوم بالإقلاع السحابي الفوري
app = app
