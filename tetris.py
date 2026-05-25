from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

@tetris_blueprint.route('/tetris')
def tetris_game():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head><title>Tetris</title></head>
<body style="background:#121212; color:#fff; text-align:center; font-family:monospace; padding:50px;">
    <h2>🧱 لعبة التترس قيد التطوير الصارم حالياً</h2>
    <a href="/" style="color:#8c9f21;">العودة للرئيسية</a>
</body>
</html>
""")
