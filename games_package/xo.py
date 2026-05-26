from flask import Blueprint, render_template_string

xo_blueprint = Blueprint('xo', __name__)

XO_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>X-O Matrix - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #080c10; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #a371f7; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #a371f7, 0 0 10px #a371f7; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .xo-phone-box { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 20px; width: 100%; max-width: 340px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; }
        
        .status-txt { font-size: 14px; font-weight: bold; color: #a371f7; margin-bottom: 15px; }
        
        /* 🕹️ شبكة مصفوفة اللعب النيونية المتجاوبة بالكامل */
        .xo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; }
        .xo-cell { aspect-ratio: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 10px; font-size: 32px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; user-select: none; -webkit-user-select: none; transition: 0.15s ease; }
        .xo-cell:hover { border-color: #a371f7; background: rgba(163,113,247,0.03); }
        
        .reset-xo-btn { background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 8px 20px; font-size: 13px; font-weight: bold; cursor: pointer; border-radius: 6px; font-family: inherit; width: 100%; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#a371f7;">❌ لعبة X-O ⭕</span>
    </div>

    <div class="main-container">
        <div class="xo-phone-box">
            <div class="status-txt" id="xoStatus">دور اللاعب: X ⚔️</div>
            <div class="xo-grid">
                <div class="xo-cell" onclick="makeMove(this, 0)"></div>
                <div class="xo-cell" onclick="makeMove(this, 1)"></div>
                <div class="xo-cell" onclick="makeMove(this, 2)"></div>
                <div class="xo-cell" onclick="makeMove(this, 3)"></div>
                <div class="xo-cell" onclick="makeMove(this, 4)"></div>
                <div class="xo-cell" onclick="makeMove(this, 5)"></div>
                <div class="xo-cell" onclick="makeMove(this, 6)"></div>
                <div class="xo-cell" onclick="makeMove(this, 7)"></div>
                <div class="xo-cell" onclick="makeMove(this, 8)"></div>
            </div>
            <button class="reset-xo-btn" onclick="resetXOGame()">تصفير اللوحة 🔄</button>
        </div>
    </div>

    <script>
        let turn = "X", gameActive = true, boardState = ["", "", "", "", "", "", "", "", ""];
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // ✅ تم الاصلاح الهندسي الحاسم: كتابة مصفوفات الفوز رقمياً وصراحة 100% بدون ترك فراغات لإسقاط Vercel
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function playSound(f) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = 'triangle'; o.frequency.setValueAtTime(f, audioCtx.currentTime);
            g.gain.setValueAtTime(0.03, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.05);
        }

        function makeMove(cell, idx) {
            if(boardState[idx] !== "" || !gameActive) return;
            boardState[idx] = turn;
            cell.innerText = turn;
            cell.style.color = (turn === "X") ? "#f85149" : "#388bfd";
            playSound((turn === "X") ? 450 : 600);
            
            checkResult();
        }

        function checkResult() {
            let roundWon = false;
            for(let i=0; i<winPatterns.length; i++) {
                const [a, b, c] = winPatterns[i];
                if(boardState[a] && boardState[a] === boardState[b] && boardState[a] === boardState[c]) {
                    roundWon = true; break;
                }
            }
            if(roundWon) {
                document.getElementById('xoStatus').innerText = "الـفـائـز هـو: " + turn + " ! 🎉";
                gameActive = false; return;
            }
            if(!boardState.includes("")) {
                document.getElementById('xoStatus').innerText = "تعادل سلبي! 🤝";
                gameActive = false; return;
            }
            turn = (turn === "X") ? "O" : "X";
            document.getElementById('xoStatus').innerText = "دور اللاعب: " + turn + " ⚔️";
        }

        function resetXOGame() {
            turn = "X"; gameActive = true; boardState.fill("");
            document.getElementById('xoStatus').innerText = "دور اللاعب: X ⚔️";
            document.querySelectorAll('.xo-cell').forEach(c => { c.innerText = ""; c.style.color = "inherit"; });
        }
    </script>
</body>
</html>
"""

@xo_blueprint.route('/xo')
def xo_page():
    return render_template_string(XO_TEMPLATE)
