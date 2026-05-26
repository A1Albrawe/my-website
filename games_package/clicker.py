from flask import Blueprint, render_template_string

clicker_blueprint = Blueprint('clicker', __name__)

CLICKER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Clicker - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #080c10; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff7b72; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #ff7b72; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #ff7b72, 0 0 10px #ff7b72; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .clicker-box { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #ff7b72; border-radius: 20px; width: 100%; max-width: 340px; padding: 25px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; }
        
        .score-txt { font-size: 42px; font-weight: bold; color: #ff7b72; margin: 15px 0; text-shadow: 0 0 15px rgba(255,123,114,0.3); font-family: monospace; }
        .timer-txt { font-size: 14px; color: #8b949e; margin-bottom: 20px; font-weight: bold; }
        
        .click-trigger-btn { width: 140px; height: 140px; border-radius: 50%; background: #21262d; border: 3px solid #ff7b72; color: #ff7b72; font-size: 24px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; box-shadow: 0 0 20px rgba(255,123,114,0.15); transition: 0.1s ease; user-select: none; -webkit-user-select: none; touch-action: manipulation; }
        .click-trigger-btn:active { transform: scale(0.94); background: #ff7b72; color: #0d1117; box-shadow: 0 0 25px #ff7b72; }
        
        .reset-game-btn { background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 8px 20px; font-size: 13px; font-weight: bold; cursor: pointer; border-radius: 6px; font-family: inherit; width: 100%; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#ff7b72;">⚡ تحدي النقر</span>
    </div>

    <div class="main-container">
        <div class="clicker-box">
            <div class="timer-txt" id="timerDisplay">الوقت المتبقي: 10 ثوانٍ ⏱️</div>
            <div class="score-txt" id="clicksCount">0</div>
            <button class="click-trigger-btn" id="clickBtn" onclick="registerClick()">انقر! ⚡</button>
            <br>
            <button class="reset-game-btn" onclick="resetClicker()">إعادة التحدي 🔄</button>
        </div>
    </div>

    <script>
        let clicks = 0, timeLeft = 10, timerInterval = null, isPlaying = false;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playClickSound() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = 'sine'; o.frequency.setValueAtTime(400 + (clicks * 5), audioCtx.currentTime);
            g.gain.setValueAtTime(0.02, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.03);
        }

        function registerClick() {
            if(timeLeft <= 0) return;
            if(!isPlaying) { isPlaying = true; startTimer(); }
            clicks++; playClickSound();
            document.getElementById('clicksCount').innerText = clicks;
        }

        function startTimer() {
            timerInterval = setInterval(() => {
                timeLeft--;
                document.getElementById('timerDisplay').innerText = "الوقت المتبقي: " + timeLeft + " ثوانٍ ⏱️";
                if(timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('clickBtn').disabled = true;
                    document.getElementById('timerDisplay').innerText = "انتهى الوقت! 🏁";
                }
            }, 1000);
        }

        function resetClicker() {
            clearInterval(timerInterval); clicks = 0; timeLeft = 10; isPlaying = false;
            document.getElementById('clicksCount').innerText = "0";
            document.getElementById('timerDisplay').innerText = "الوقت المتبقي: 10 ثوانٍ ⏱️";
            document.getElementById('clickBtn').disabled = false;
        }
    </script>
</body>
</html>
"""

@clicker_blueprint.route('/clicker')
def clicker_page():
    return render_template_string(CLICKER_TEMPLATE)
