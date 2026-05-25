from flask import Flask
# استيراد الصفحات والألعاب من الملفات المنفصلة
from home import home_blueprint
from snake import snake_blueprint
from tetris import tetris_blueprint

app = Flask(__name__)

# تسجيل الصفحات في الخادم الرئيسي ليقوم بالتوجيه إليها
app.register_blueprint(home_blueprint)
app.register_blueprint(snake_blueprint)
app.register_blueprint(tetris_blueprint)

if __name__ == '__main__':
    app.run()
