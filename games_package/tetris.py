from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

TETRIS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tetris Evolution - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #080c10; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #d29922; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #d29922; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #d29922, 0 0 10px #d29922; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #d29922; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .tetris-phone { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #d29922; border-radius: 20px; width: 100%; max-width: 350px; padding: 20px 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 12px; color: #d29922; align-items: center; }
        .speed-badge { color: #ffd700; font-weight: bold; font-size: 12px; }
        
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #0b0e14; display: block; border: 2px solid #30363d; border-radius: 8px; box-shadow: 0 0 20px rgba(210, 153, 34, 0.15); }
        
        .overlay-txt { display: none; position: absolute; font-size: 20px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(13, 17, 23, 0.96); border: 2px solid #d29922; padding: 20px; border-radius: 12px; text-align: center; width: 85%; box-shadow: 0 0 25px #d29922; box-sizing: border-box; z-index: 5; }
        
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 240px; margin-left: auto; margin-right: auto; }
        .ctrl-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; padding: 15px; font-size: 20px; color: #d29922; cursor: pointer; user-select: none; -webkit-user-select: none; font-weight: bold; box-shadow: 0 4px #0d1117; transition: 0.1s; touch-action: none; }
        .ctrl-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
        
        .pause-action-btn { grid-column: span 3; background: #21262d; border: 1px solid #f85149; color: #f85149; font-size: 14px; font-weight: bold; border-radius: 8px; padding: 10px; cursor: pointer; box-shadow: 0 3px #0d1117; display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 5px; font-family: inherit; user-select: none; -webkit-user-select: none; touch-action: none; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#d29922;">🧱 تترس التطور</span>
    </div>

    <div class="main-container">
        <div class="tetris-phone">
            <div class="score-container">
                <span id="tetrisScore">النقاط: 0</span>
                <span id="tetrisSpeed" class="speed-badge">السرعة: 1.0x ⚡</span>
                <span>TETRIS</span>
            </div>
            <div class="game-area">
                <!-- ✅ الأبعاد الهندسية القياسية الثابتة للميدان لمنع التشوه البصري -->
                <canvas id="tetrisCanvas" width="220" height="440"></canvas>
                <div id="pauseOverlay" class="overlay-txt"><i class="fas fa-pause-circle"></i> اللعبة موقوتة ⏸️</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0; color:#d29922;">محرك تترس المطور</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:8px 20px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="initGame()">بدء اللعب اللانهائي 🎮</button>
                </div>
            </div>
            
            <!-- 🕹️ تصحيح اتجاه الأزرار (يسار، تدوير، يمين) متوافق 100% مع الشاشات والمعالج -->
            <div class="control-pad">
                <button class="ctrl-btn" ontouchstart="handleTetrisTouch(event, 'L')" onmousedown="moveBlock('L')">◀</button>
                <button class="ctrl-btn" ontouchstart="handleTetrisTouch(event, 'RTV')" onmousedown="rotateBlock()">🔄</button>
                <button class="ctrl-btn" ontouchstart="handleTetrisTouch(event, 'R')" onmousedown="moveBlock('R')">▶</button>
                
                <div></div>
                <button class="ctrl-btn" ontouchstart="handleTetrisTouch(event, 'D')" onmousedown="moveBlock('D')">▼</button>
                <div></div>
                
                <button class="pause-action-btn" ontouchstart="handleTetrisTouch(event, 'PAUSE')" onmousedown="togglePause()"><i class="fas fa-pause"></i> إيقاف مؤقت / استئناف اللعب</button>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('tetrisCanvas'), ctx = canvas.getContext('2d');
        const ROW = 20, COL = 10, SQ = 22, VACANT = "#0d1117";
        let board = [], score = 0, linesCleared = 0, currentSpeed = 1000, gameInterval = null, musicInterval = null;
        let isGameOver = true, isPaused = false;

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const musicNotes = [523.25, 587.33, 659.25, 523.25, 659.25, 587.33, 392.00, 440.00];

        function handleTetrisTouch(e, action) {
            e.preventDefault(); 
            if(action === 'L') moveBlock('L');
            else if(action === 'R') moveBlock('R');
            else if(action === 'D') moveBlock('D');
            else if(action === 'RTV') rotateBlock();
            else if(action === 'PAUSE') togglePause();
        }

        function playSound(t) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination); o.type = 'square';
            if (t === 'move') { o.frequency.setValueAtTime(300, audioCtx.currentTime); g.gain.setValueAtTime(0.01, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.02); }
            else if (t === 'clear') { o.frequency.setValueAtTime(587.33, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1174.66, audioCtx.currentTime + 0.12); g.gain.setValueAtTime(0.05, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.12); }
            else if (t === 'lose') { o.frequency.setValueAtTime(180, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(50, audioCtx.currentTime + 0.4); g.gain.setValueAtTime(0.12, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.4); }
        }

        function playMusic() {
            if (isGameOver || isPaused) return;
            let tp = audioCtx.currentTime;
            musicNotes.forEach(f => {
                const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
                o.frequency.setValueAtTime(f + (linesCleared * 2), tp); g.gain.setValueAtTime(0.01, tp);
                g.gain.linearRampToValueAtTime(0, tp + 0.18); o.connect(g); g.connect(audioCtx.destination);
                o.start(tp); o.stop(tp + 0.2); tp += 0.2;
            });
        }
        function startMusic() { stopMusic(); if(!isGameOver) { playMusic(); musicInterval = setInterval(playMusic, musicNotes.length * 200); } }
        function stopMusic() { if(musicInterval) clearInterval(musicInterval); }

        // ✅ حقن بكسلات مصفوفات الأشكال السبعة القياسية بجميع وضعيات الالتفاف بدقة هندسية مطلقة
        const I = [
            [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
            [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]],
            [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]],
            [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]
        ];
        const T = [
            [[0,1,0],[1,1,1],[0,0,0]],
            [[0,1,0],[0,1,1],[0,1,0]],
            [[0,0,0],[1,1,1],[0,1,0]],
            [[0,1,0],[1,1,0],[0,1,0]]
        ];
        const Z = [
            [[1,1,0],[0,1,1],[0,0,0]],
            [[0,0,1],[0,1,1],[0,1,0]],
            [[0,0,0],[1,1,0],[0,1,1]],
            [[0,1,0],[1,1,0],[1,0,0]]
        ];
        const S = [
            [[0,1,1],[1,1,0],[0,0,0]],
            [[0,1,0],[0,1,1],[0,0,1]],
            [[0,0,0],[0,1,1],[1,1,0]],
            [[1,0,0],[1,1,0],[0,1,0]]
        ];
        const O = [
            [[1,1],[1,1]]
        ];
        const L = [
            [[0,0,1],[1,1,1],[0,0,0]],
            [[0,1,0],[0,1,0],[0,1,1]],
            [[0,0,0],[1,1,1],[1,0,0]],
            [[1,1,0],[0,1,0],[0,1,0]]
        ];
        const J = [
            [[1,0,0],[1,1,1],[0,0,0]],
            [[0,1,1],[0,1,0],[0,1,0]],
            [[0,0,0],[1,1,1],[0,0,1]],
            [[0,1,0],[0,1,0],[1,1,0]]
        ];

        const PIECES = [
            [I, "#388bfd"], [T, "#a371f7"], [Z, "#f85149"], 
            [S, "#3fb950"], [O, "#ffd700"], [L, "#ff7b72"], [J, "#db6d28"]
        ];
        class Piece {
            constructor(tetromino, color) { this.tetromino = tetromino; this.color = color; this.tetrominoN = 0; this.activeTetromino = this.tetromino[this.tetrominoN]; this.x = 3; this.y = -2; }
            draw() { this.fill(this.color); }
            unuse() { this.fill(VACANT); }
            fill(color) {
                for(let r=0; r<this.activeTetromino.length; r++) {
                    for(let c=0; c<this.activeTetromino[r].length; c++) {
                        if(this.activeTetromino[r][c]) {
                            ctx.fillStyle = color; ctx.fillRect((this.x+c)*SQ, (this.y+r)*SQ, SQ, SQ);
                            ctx.strokeStyle = "#161b22"; ctx.strokeRect((this.x+c)*SQ, (this.y+r)*SQ, SQ, SQ);
                        }
                    }
                }
            }
            moveDown() { if(!this.collision(0,1,this.activeTetromino)) { this.unuse(); this.y++; this.draw(); } else { this.lock(); p = randomPiece(); } }
            moveRight() { if(!this.collision(1,0,this.activeTetromino)) { this.unuse(); this.x++; this.draw(); playSound('move'); } }
            moveLeft() { if(!this.collision(-1,0,this.activeTetromino)) { this.unuse(); this.x--; this.draw(); playSound('move'); } }
            
            // ✅ الدوران الاحترافي (Wall-Kick): يمنع التجميد والانهيار عند الالتصاق التام بالحواف الجانبية للكانفاس
            rotate() {
                let nextN = (this.tetrominoN + 1) % this.tetromino.length;
                let nextPattern = this.tetromino[nextN];
                let kick = 0;
                if(this.collision(0,0,nextPattern)) {
                    if(this.x > COL/2) kick = -1; else kick = 1;
                    if(this.activeTetromino.length === 4) { if(this.x > COL/2) kick = -2; else kick = 2; }
                }
                if(!this.collision(kick,0,nextPattern)) { this.unuse(); this.x += kick; this.tetrominoN = nextN; this.activeTetromino = nextPattern; this.draw(); playSound('move'); }
            }
            collision(x, y, piece) {
                for(let r=0; r<piece.length; r++) {
                    for(let c=0; c<piece[r].length; c++) {
                        if(!piece[r][c]) continue;
                        let newX = this.x + c + x, newY = this.y + r + y;
                        if(newX < 0 || newX >= COL || newY >= ROW) return true;
                        if(newY < 0) continue;
                        if(board[newY][newX] !== VACANT) return true;
                    }
                }
                return false;
            }
            lock() {
                for(let r=0; r<this.activeTetromino.length; r++) {
                    for(let c=0; c<this.activeTetromino[r].length; c++) {
                        if(!this.activeTetromino[r][c]) continue;
                        if(this.y + r < 0) { endGame(); return; }
                        board[this.y+r][this.x+c] = this.color;
                    }
                }
                let rowsClearedThisTurn = 0;
                for(let r=0; r<ROW; r++) {
                    let isRowFull = true;
                    for(let c=0; c<COL; c++) { if(board[r][c] === VACANT) isRowFull = false; }
                    if(isRowFull) {
                        rowsClearedThisTurn++;
                        for(let y=r; y>1; y--) { for(let c=0; c<COL; c++) { board[y][c] = board[y-1][c]; } }
                        for(let c=0; c<COL; c++) { board[0][c] = VACANT; }
                    }
                }
                if(rowsClearedThisTurn > 0) {
                    score += rowsClearedThisTurn * 100;
                    linesCleared += rowsClearedThisTurn;
                    playSound('clear');
                    document.getElementById('tetrisScore').innerText = "النقاط: " + score;
                    
                    // 📈 حساب الجاذبية المتسارعة تلقائياً مع زيادة مسح السطور وتحديث العداد
                    currentSpeed = Math.max(150, 1000 - (linesCleared * 35));
                    let speedFactor = (1000 / currentSpeed).toFixed(1);
                    document.getElementById('tetrisSpeed').innerText = "السرعة: " + speedFactor + "x ⚡";
                    runEngineInterval();
                }
                drawBoard();
            }
        }

        let p = null;
        function randomPiece() { let r = Math.floor(Math.random() * PIECES.length); return new Piece(PIECES[r][0], PIECES[r][1]); }

        function initGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            score = 0; linesCleared = 0; currentSpeed = 1000; isGameOver = false; isPaused = false;
            document.getElementById('tetrisScore').innerText = "النقاط: " + score;
            document.getElementById('tetrisSpeed').innerText = "السرعة: 1.0x ⚡";
            
            for(let r=0; r<ROW; r++) { board[r] = []; for(let c=0; c<COL; c++) { board[r][c] = VACANT; } }
            drawBoard(); p = randomPiece(); p.draw(); startMusic(); runEngineInterval();
        }

        function runEngineInterval() { if(gameInterval) clearInterval(gameInterval); gameInterval = setInterval(() => { if(!isPaused && !isGameOver) p.moveDown(); }, currentSpeed); }
        function drawBoard() { for(let r=0; r<ROW; r++) { for(let c=0; c<COL; c++) { ctx.fillStyle = board[r][c]; ctx.fillRect(c*SQ, r*SQ, SQ, SQ); ctx.strokeStyle = "#161b22"; ctx.strokeRect(c*SQ, r*SQ, SQ, SQ); } } }

        function moveBlock(dir) { if(isGameOver || isPaused) return; if(dir==='L') p.moveLeft(); if(dir==='R') p.moveRight(); if(dir==='D') p.moveDown(); }
        function rotateBlock() { if(isGameOver || isPaused) return; p.rotate(); }

        document.addEventListener('keydown', e => {
            if(e.key === 'ArrowLeft') moveBlock('L'); // تحريك لليسار بالضغط للكمبيوتر
            if(e.key === 'ArrowUp') rotateBlock();
            if(e.key === 'ArrowRight') moveBlock('R'); // تحريك لليمين
            if(e.key === 'ArrowDown') moveBlock('D');
        });

        function togglePause() { if(isGameOver) return; isPaused = !isPaused; document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none'; }
        function endGame() { isGameOver = true; clearInterval(gameInterval); stopMusic(); playSound('lose'); document.getElementById('goTitle').innerText = "انتهت اللعبة! 💀"; document.getElementById('finalScoreText').innerText = "أحرزت: " + score + " نقطة تراكمية"; document.getElementById('gameOverScreen').style.display = 'block'; }
    </script>
</body>
</html>
"""

@tetris_blueprint.route('/tetris')
def tetris_page():
    return render_template_string(TETRIS_TEMPLATE)
