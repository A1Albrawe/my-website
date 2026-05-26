from flask import Blueprint, render_template_string

clicker_blueprint = Blueprint('clicker', __name__)

CLICKER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Albrawe - Speed Clicker</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #3fb950; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #3fb950; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .click-box { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #3fb950; border-radius: 12px; padding: 35px; width: 100%; max-width: 320px; box-shadow: 0 10px 20px rgba(0,0,0,0.4); text-align: center; }
        .circle-target { width: 100px; height: 100px; background: #3fb950; border-radius: 50%; margin: 20px auto; display: flex; justify-content: center; align-items: center; font-size: 14px; font-weight: bold; color: #000; cursor: pointer; user-select: none; transition: 0.1s; }
        .circle-target:active { transform: scale(0.9); }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="font-weight:bold; color:#fff;">⚡ اختبار النقر السريع</span>
    </div>
    <div class="main-container">
        <div class="click-box">
            <div style="font-size:18px; font-weight:bold; color:#58a6ff;" id="timer">الوقت المتبقي: 10 ثوانٍ</div>
            <div style="font-size:24px; font-weight:bold; margin-top:10px;" id="scoreDisplay">النقاط: 0</div>
            <div class="circle-target" id="target" onclick="hitTarget()">اضغط هنا!</div>
        </div>
    </div>
    <script>
        let score = 0, timeLeft = 10, gameStarted = false, interval;

        function hitTarget() {
            if(timeLeft <= 0) return;
            if(!gameStarted) { gameStarted = true; interval = setInterval(countdown, 1000); }
            score++;
            document.getElementById('scoreDisplay').innerText = `النقاط: ${score}`;
            moveTarget();
        }

        function moveTarget() {
            const t = document.getElementById('target');
            t.style.backgroundColor = currentPlayerColor();
        }
        function currentPlayerColor() { return '#' + Math.floor(Math.random()*16777215).toString(16); }

        function countdown() {
            timeLeft--;
            document.getElementById('timer').innerText = `الوقت المتبقي: ${timeLeft} ثوانٍ`;
            if(timeLeft <= 0) { clearInterval(interval); alert(`انتهى الوقت! مجموع نقراتك: ${score}`); window.location.reload(); }
        }
    </script>
</body>
</html>
"""

@clicker_blueprint.route('/clicker')
def clicker_page():
    return render_template_string(CLICKER_TEMPLATE)
