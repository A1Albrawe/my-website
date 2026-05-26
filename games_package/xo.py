from flask import Blueprint, render_template_string

xo_blueprint = Blueprint('xo', __name__)

XO_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Advanced X-O</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #a371f7; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #a371f7, 0 0 10px #a371f7; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #a371f7; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .game-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 25px; width: 100%; max-width: 350px; box-shadow: 0 15px 30px rgba(0,0,0,0.5); box-sizing: border-box; }
        
        .mode-selector { display: flex; gap: 8px; margin-bottom: 15px; }
        .mode-btn { flex: 1; background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 8px; border-radius: 6px; cursor: pointer; font-family: inherit; font-weight: bold; font-size: 12px; transition: 0.2s; }
        .mode-btn.active { background: #a371f7; color: #fff; border-color: #a371f7; }
        
        .level-badge { background: #0d1117; border: 1px solid #30363d; padding: 6px; border-radius: 6px; font-size: 13px; font-weight: bold; color: #ffd700; margin-bottom: 12px; display: block; }
        .status { font-size: 15px; font-weight: bold; margin-bottom: 15px; color: #58a6ff; min-height: 22px; }
        
        .board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
        .cell { background: #0d1117; border: 1px solid #30363d; height: 85px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size: 36px; font-weight: bold; cursor: pointer; user-select: none; transition: 0.1s; }
        .cell:hover { background: #21262d; border-color: #a371f7; }
        .cell.X { color: #f85149; text-shadow: 0 0 8px #f85149; } 
        .cell.O { color: #58a6ff; text-shadow: 0 0 8px #58a6ff; }
        
        .reset-btn { width: 100%; background: #238636; color: #fff; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; font-family: inherit; font-size: 14px; }
        .reset-btn:hover { background: #2ea44f; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#a371f7;">🎮 لعبة X-O</span>
    </div>
    <div class="main-container">
        <div class="game-card">
            <div class="mode-selector">
                <button class="mode-btn active" id="btnAi" onclick="setMode('ai')">ضد الكمبيوتر 🤖</button>
                <button class="mode-btn" id="btnPvp" onclick="setMode('pvp')">لعب ثنائي 👥</button>
            </div>
            <div class="level-badge" id="levelDisplay">المرحلة الحالية: 1 / 10 👑</div>
            <div class="status" id="gameStatus">بدء المعركة، دور اللاعب X</div>
            <div class="board" id="gameBoard">
                <div class="cell" onclick="playerMove(this, 0)"></div>
                <div class="cell" onclick="playerMove(this, 1)"></div>
                <div class="cell" onclick="playerMove(this, 2)"></div>
                <div class="cell" onclick="playerMove(this, 3)"></div>
                <div class="cell" onclick="playerMove(this, 4)"></div>
                <div class="cell" onclick="playerMove(this, 5)"></div>
                <div class="cell" onclick="playerMove(this, 6)"></div>
                <div class="cell" onclick="playerMove(this, 7)"></div>
                <div class="cell" onclick="playerMove(this, 8)"></div>
            </div>
            <button class="reset-btn" onclick="resetBoard()">تطهير الساحة وإعادة 🔄</button>
        </div>
    </div>
    <script>
        let board = ["", "", "", "", "", "", "", "", ""];
        let currentPlayer = "X";
        let gameActive = true;
        let gameMode = "ai"; 
        let currentLevel = 1;
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            if(type === 'click') { osc.frequency.setValueAtTime(currentPlayer==='X'?440:554.37, audioCtx.currentTime); gain.gain.setValueAtTime(0.04, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.04); }
            else if(type === 'win') { osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(1174.66, audioCtx.currentTime + 0.3); gain.gain.setValueAtTime(0.08, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.3); }
            else if(type === 'lose') { osc.frequency.setValueAtTime(220, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(110, audioCtx.currentTime + 0.4); gain.gain.setValueAtTime(0.12, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        }

        function setMode(mode) {
            gameMode = mode;
            document.getElementById('btnAi').classList.toggle('active', mode==='ai');
            document.getElementById('btnPvp').classList.toggle('active', mode==='pvp');
            currentLevel = 1; 
            document.getElementById('levelDisplay').style.display = mode==='ai'?'block':'none';
            resetBoard();
        }

        function playerMove(cell, index) {
            if(board[index] !== "" || !gameActive) return;
            
            // تنفيذ الحركة الحالية للاعب (سواء كان X أو O في الوضع الثنائي)
            executeMove(cell, index);
            
            // ✅ تشغيل ذكاء الكمبيوتر فقط وحصرياً إذا كان الوضع "ضد الكمبيوتر" والدور عليه
            if(gameActive && gameMode === "ai" && currentPlayer === "O") {
                document.getElementById('gameBoard').style.pointerEvents = 'none'; // حظر النقرات أثناء تفكير الـ AI
                setTimeout(aiEngineMove, 300);
            }
        }

        function executeMove(cell, index) {
            board[index] = currentPlayer;
            cell.innerText = currentPlayer;
            cell.classList.add(currentPlayer);
            playSound('click');
            checkGameResult();
        }

        function aiEngineMove() {
            if(!gameActive) { document.getElementById('gameBoard').style.pointerEvents = 'auto'; return; }
            let targetIdx = -1;
            let randomness = Math.random() * 10;
            
            if(randomness > (10 - currentLevel)) {
                for (let pattern of winPatterns) {
                    let counts = pattern.map(i => board[i]);
                    let xCount = counts.filter(v => v === 'X').length;
                    let oCount = counts.filter(v => v === 'O').length;
                    let emptyIdx = pattern.find(i => board[i] === "");
                    if(oCount === 2 && emptyIdx !== undefined) { targetIdx = emptyIdx; break; }
                    if(xCount === 2 && emptyIdx !== undefined && targetIdx === -1) { targetIdx = emptyIdx; }
                }
            }
            if(targetIdx === -1 && board[4] === "") targetIdx = 4;
            if(targetIdx === -1) {
                let avail = board.map((v,i) => v===""?i:null).filter(v => v!==null);
                targetIdx = avail[Math.floor(Math.random()*avail.length)];
            }
            if(targetIdx !== -1) {
                const cells = document.querySelectorAll('.cell');
                executeMove(cells[targetIdx], targetIdx);
            }
            document.getElementById('gameBoard').style.pointerEvents = 'auto'; // إعادة تمكين التحكم للمستخدم
        }

        function checkGameResult() {
            let won = false;
            for(let pattern of winPatterns) {
                if(board[pattern[0]] && board[pattern[0]]===board[pattern[1]] && board[pattern[0]]===board[pattern[2]]) { won = true; break; }
            }
            if(won) {
                gameActive = false;
                if(gameMode === 'pvp') { 
                    document.getElementById('gameStatus').innerText = `النصر حليف اللاعب ${currentPlayer}! 🎉`; 
                    playSound('win'); 
                } else {
                    if(currentPlayer === 'X') {
                        playSound('win');
                        if(currentLevel < 10) { 
                            currentLevel++; 
                            document.getElementById('gameStatus').innerText = `تفوقت على النظام! جاري الانتقال للمرحلة ${currentLevel} 🚀`; 
                            setTimeout(resetBoard, 1500); 
                        } else { 
                            document.getElementById('gameStatus').innerText = "تهانينا! دمرت كمبيوتر النظام بالكامل وختمت المراكز الـ 10! 👑"; 
                        }
                    } else { 
                        document.getElementById('gameStatus').innerText = "سحقك الذكاء الاصطناعي! حظاً أوفر 💀"; 
                        playSound('lose'); 
                        currentLevel = 1; 
                    }
                }
                document.getElementById('levelDisplay').innerText = `المرحلة الحالية: ${currentLevel} / 10 👑`;
                return;
            }
            if(!board.includes("")) { document.getElementById('gameStatus').innerText = "معركة طاحنة، تعادل حتمي! 🤝"; gameActive = false; return; }
            
            // تبديل الرموز بمرونة بالتناوب
            currentPlayer = currentPlayer === "X" ? "O" : "X";
            document.getElementById('gameStatus').innerText = `دور اللاعب: ${currentPlayer}`;
        }

        function resetBoard() {
            board = ["", "", "", "", "", "", "", "", ""]; currentPlayer = "X"; gameActive = true;
            document.getElementById('gameStatus').innerText = "بدء المعركة، دور اللاعب X";
            document.querySelectorAll('.cell').forEach(c => { c.innerText = ""; c.className = "cell"; });
        }
    </script>
</body>
</html>
"""

@xo_blueprint.route('/xo')
def xo_page():
    return render_template_string(XO_TEMPLATE)
