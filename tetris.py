from flask import Blueprint, render_template_string, request, jsonify
from menu import generate_sidebar_html # استدعاء القائمة الجانبية الموحدة تلقائياً

tetris_blueprint = Blueprint('tetris', __name__)

# مصفوفة سحابية مركزية موحدة داخل السيرفر لحفظ توب 3 لاعبين تترس على مستوى العالم
GLOBAL_TETRIS_LEADERBOARD = [
    {"name": "البروي 👑", "score": 1000},
    {"name": "لاعب 2", "score": 0},
    {"name": "لاعب 3", "score": 0}
]

@tetris_blueprint.route('/api/get_tetris_leaderboard', methods=['GET'])
def get_tetris_leaderboard():
    return jsonify(GLOBAL_TETRIS_LEADERBOARD)

@tetris_blueprint.route('/api/submit_tetris_score', methods=['POST'])
def submit_tetris_score():
    global GLOBAL_TETRIS_LEADERBOARD
    data = request.get_json() or {}
    name = data.get('name', 'لاعب مجهول').strip()
    score = int(data.get('score', 0))
    
    if score > 0 and name:
        GLOBAL_TETRIS_LEADERBOARD.append({"name": name, "score": score})
        GLOBAL_TETRIS_LEADERBOARD.sort(key=lambda x: x['score'], reverse=True)
        GLOBAL_TETRIS_LEADERBOARD = GLOBAL_TETRIS_LEADERBOARD[:3]
        
    return jsonify({"status": "success", "leaderboard": GLOBAL_TETRIS_LEADERBOARD})

TETRIS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Tetris</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #d29922; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #d29922; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .menu-toggle { background: #21262d; border: 1px solid #30363d; color: #d29922; font-size: 18px; cursor: pointer; padding: 6px 15px; border-radius: 6px; font-weight: bold; font-family: inherit; }
        .sidebar-curtain { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background-color: #161b22; border-left: 2px solid #d29922; box-shadow: -10px 0 30px rgba(0,0,0,0.7); z-index: 1000; transition: right 0.3s ease; padding: 20px; box-sizing: border-box; text-align: right; }
        .sidebar-curtain.active { right: 0; }
        .close-btn { background: none; border: none; color: #f85149; font-size: 16px; cursor: pointer; margin-bottom: 30px; font-family: inherit; font-weight: bold; }
        .menu-links { display: flex; flex-direction: column; gap: 12px; }
        .menu-item { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: bold; font-size: 15px; padding: 12px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .tetris-phone { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #d29922; border-radius: 20px; width: 100%; max-width: 360px; padding: 20px 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 10px; color: #d29922; align-items: center; }
        .audio-controls { display: flex; align-items: center; gap: 4px; }
        .mute-btn { background: none; border: none; font-size: 14px; cursor: pointer; color: #d29922; padding: 0; }
        .volume-bar { width: 55px; accent-color: #d29922; height: 3px; cursor: pointer; }
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #0d1117; display: block; border: 2px solid #30363d; border-radius: 6px; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #d29922; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        .leaderboard { margin-top: 10px; background: rgba(0, 0, 0, 0.2); padding: 8px; border-radius: 6px; font-size: 11px; text-align: right; border: 1px solid #30363d; }
        .leaderboard h4 { margin: 0 0 6px 0; text-align: center; font-size: 12px; color: #79c0ff; }
        .score-row { display: flex; justify-content: space-between; padding: 2px 0; font-weight: bold; color: #c9d1d9; }
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 100%; max-width: 220px; margin-left: auto; margin-right: auto; }
        .ctrl-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; padding: 12px; font-size: 18px; color: #d29922; cursor: pointer; user-select: none; font-weight: bold; box-shadow: 0 3px #0d1117; }
        .ctrl-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
    </style>
</head>
<body>
    <div class="header-nav">
        <button class="menu-toggle" onclick="toggleSidebarCurtain(true)">☰ القائمة</button>
        <span style="font-weight:bold; color:#fff;">🧱 لعبة التترس الموحدة</span>
    </div>
    <div class="sidebar-curtain" id="sidebarCurtain">
        <button class="close-btn" onclick="toggleSidebarCurtain(false)">❌ إغلاق القائمة</button>
        <div class="menu-links">
            <!--DYNAMIC_SIDEBAR_LINKS_PLACEHOLDER-->
        </div>
    </div>
    <div class="main-container">
        <div class="tetris-phone">
            <div class="score-container">
                <span id="tetrisScore">النقاط: 0</span>
                <div class="audio-controls">
                    <button class="mute-btn" id="muteToggle" onclick="toggleMute()"><i class="fas fa-volume-up"></i></button>
                    <input type="range" id="volumeSlider" class="volume-bar" min="0" max="1" step="0.1" value="0.5" oninput="updateVolume(this.value)">
                </div>
                <span>TETRIS</span>
            </div>
            <div class="game-area">
                <canvas id="tetrisCanvas" width="200" height="400"></canvas>
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0; color:#d29922;">مرحباً بك في التترس</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <input type="text" id="playerName" style="padding:6px; font-size:12px; border:1px solid #30363d; background:#0d1117; color:#fff; margin-bottom:8px; text-align:center; width:85%; font-family:inherit; font-weight:bold; box-sizing:border-box;" placeholder="اسم المستخدم" maxlength="10">
                    <br><button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:6px 15px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="submitPlayer()">بدء اللعب الفوري</button>
                </div>
            </div>
            <div class="control-pad">
                <button class="ctrl-btn" onclick="moveBlock('L')">◀</button>
                <button class="ctrl-btn" onclick="rotateBlock()">🔄</button>
                <button class="ctrl-btn" onclick="moveBlock('R')">▶</button>
                <div></div>
                <button class="ctrl-btn" onclick="moveBlock('D')">▼</button>
                <div></div>
            </div>
            <div class="leaderboard">
                <h4>🏆 لوحة صدارة أفضل نتائج التترس عالمياً</h4>
                <div id="leaderboardContent"></div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('tetrisCanvas'), ctx = canvas.getContext('2d');
        const ROW = 20, COL = 10, SQ = 20, VACANT = "#0d1117";
        let board = [], score = 0, gameInterval = null, musicInterval = null;
        let isGameOver = true, isPaused = false, isMuted = false, globalVolume = 0.5, currentUser = "";

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const musicNotes = [523.25, 587.33, 659.25, 523.25, 659.25, 587.33, 392.00, 440.00];

        function toggleMute() { isMuted = !isMuted; document.getElementById('muteToggle').innerHTML = isMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>'; document.getElementById('volumeSlider').value = isMuted ? 0 : globalVolume; if(isMuted) stopMusic(); else if(!isGameOver) startMusic(); }
        function updateVolume(v) { globalVolume = parseFloat(v); isMuted = globalVolume === 0; document.getElementById('muteToggle').innerHTML = isMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>'; stopMusic(); if(!isMuted && !isGameOver) startMusic(); }

        function playSound(t) {
            if (!audioCtx || isMuted || globalVolume === 0) return;
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination); o.type = 'square';
            if (t === 'move') { o.frequency.setValueAtTime(300, audioCtx.currentTime); g.gain.setValueAtTime(0.04 * globalVolume, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.03); }
            else if (t === 'clear') { o.frequency.setValueAtTime(600, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1); g.gain.setValueAtTime(0.1 * globalVolume, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.1); }
            else if (t === 'lose') { o.frequency.setValueAtTime(200, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(60, audioCtx.currentTime + 0.4); g.gain.setValueAtTime(0.2 * globalVolume, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.4); }
        }

        function playMusic() {
            if (!audioCtx || isGameOver || isMuted || globalVolume === 0) return;
            let tp = audioCtx.currentTime;
            musicNotes.forEach(f => {
                const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
                o.frequency.setValueAtTime(f, tp); g.gain.setValueAtTime(0.02 * globalVolume, tp);
                g.gain.linearRampToValueAtTime(0, tp + 0.18); o.connect(g); g.connect(audioCtx.destination);
                o.start(tp); o.stop(tp + 0.2); tp += 0.2;
            });
        }
        function startMusic() { stopMusic(); if(!isMuted && globalVolume > 0) { playMusic(); musicInterval = setInterval(playMusic, musicNotes.length * 200); } }
        function stopMusic() { if(musicInterval) clearInterval(musicInterval); }

        // 🎯 تم الحل الهندسي النهائي: إدراج مصفوفات تدوير الأشكال السبعة القياسية كاملة لمنع تشوه المكعبات
        const I = [ [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]], [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]], [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]], [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]] ];
        const T = [ [[0,1,0],[1,1,1],[0,0,0]], [[0,1,0],[0,1,1],[0,1,0]], [[0,0,0],[1,1,1],[0,1,0]], [[0,1,0],[1,1,0],[0,1,0]] ];
        const Z = [ [[1,1,0],[0,1,1],[0,0,0]], [[0,0,1],[0,1,1],[0,1,0]], [[0,0,0],[1,1,0],[0,1,1]], [[0,1,0],[1,1,0],[1,0,0]] ];
        const S = [ [[0,1,1],[1,1,0],[0,0,0]], [[0,1,0],[0,1,1],[0,0,1]], [[0,0,0],[0,1,1],[1,1,0]], [[1,0,0],[1,1,0],[0,1,0]] ];
        const O = [ [[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]] ];
        const L = [ [[1,0,0],[1,1,1],[0,0,0]], [[0,1,1],[0,1,0],[0,1,0]], [[0,0,0],[1,1,1],[0,0,1]], [[0,1,0],[0,1,0],[1,1,0]] ];
        const J = [ [[0,0,1],[1,1,1],[0,0,0]], [[0,1,0],[0,1,0],[0,1,1]], [[0,0,0],[1,1,1],[1,0,0]], [[1,1,0],[0,1,0],[0,1,0]] ];

        const PIECES = [ [I,"#58a6ff"], [T,"#3fb950"], [Z,"#f85149"], [S,"#d29922"], [O,"#ffffff"], [L,"#a371f7"], [J,"#ff7b72"] ];

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
            rotate() {
                let nextPattern = this.tetromino[(this.tetrominoN + 1) % this.tetromino.length];
                if(!this.collision(0,0,nextPattern)) { this.unuse(); this.tetrominoN = (this.tetrominoN + 1) % this.tetromino.length; this.activeTetromino = nextPattern; this.draw(); playSound('move'); }
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
                for(let r=0; r<ROW; r++) {
                    let isRowFull = true;
                    for(let c=0; c<COL; c++) { if(board[r][c] === VACANT) isRowFull = false; }
                    if(isRowFull) {
                        for(let y=r; y>1; y--) { for(let c=0; c<COL; c++) { board[y][c] = board[y-1][c]; } }
                        for(let c=0; c<COL; c++) { board[c] = VACANT; }
                        score += 100; playSound('clear');
                        document.getElementById('tetrisScore').innerText = "النقاط: " + score;
                    }
                }
                drawBoard();
            }
        }

        let p = null;
        function randomPiece() { let r = Math.floor(Math.random() * PIECES.length); return new Piece(PIECES[r][0], PIECES[r][1]); }

        function submitPlayer() {
            let n = document.getElementById('playerName').value.trim(); if(!n) return;
            currentUser = n; localStorage.setItem('snake_last_user', n);
            document.getElementById('gameOverScreen').style.display = 'none';
            isGameOver = false; initGame();
        }

        function initGame() {
            if(gameInterval) clearInterval(gameInterval);
            stopMusic(); score = 0; isGameOver = false;
            document.getElementById('tetrisScore').innerText = "النقاط: " + score;
            document.getElementById('gameOverScreen').style.display = 'none';
            
            for(let r=0; r<ROW; r++) { board[r] = []; for(let c=0; c<COL; c++) { board[r][c] = VACANT; } }
            drawBoard(); p = randomPiece(); p.draw();
            gameInterval = setInterval(() => { if(!isGameOver) p.moveDown(); }, 500);
            startMusic();
        }

        function drawBoard() { for(let r=0; r<ROW; r++) { for(let c=0; c<COL; c++) { drawSquare(c, r, board[r][c]); } } }
        function drawSquare(x, y, color) { ctx.fillStyle = color; ctx.fillRect(x*SQ, y*SQ, SQ, SQ); ctx.strokeStyle = "#161b22"; ctx.strokeRect(x*SQ, y*SQ, SQ, SQ); }

        function moveBlock(dir) { if(isGameOver) return; if(dir==='L') p.moveLeft(); if(dir==='R') p.moveRight(); if(dir==='D') p.moveDown(); }
        function rotateBlock() { if(!isGameOver) p.rotate(); }

        document.onkeydown = function(e) {
            if(isGameOver) return;
            if(e.keyCode === 37 || e.key === 'a') p.moveLeft();
            if(e.keyCode === 38 || e.key === 'w') p.rotate();
            if(e.keyCode === 39 || e.key === 'd') p.moveRight();
            if(e.keyCode === 40 || e.key === 's') p.moveDown();
        };

        function endGame() {
            clearInterval(gameInterval); stopMusic(); isGameOver = true; playSound('lose');
            
            // 🎯 ضخ النتيجة سحابياً ومزامنتها عالمياً فور الخسارة
            fetch('/api/submit_tetris_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: currentUser, score: score })
            }).then(res => res.json())
              .then(data => displayLeaderboard(data.leaderboard));

            document.getElementById('goTitle').innerText = "انتهت اللعبة";
            document.getElementById('finalScoreText').innerText = "نقاط الجولة المحققة: " + score;
            document.getElementById('playerName').value = currentUser;
            document.getElementById('gameOverScreen').style.display = 'block';
        }

        function loadLead() {
            fetch('/api/get_tetris_leaderboard')
            .then(res => res.json())
            .then(data => displayLeaderboard(data));
        }

        function displayLeaderboard(list) {
            let h = "";
            list.forEach((s, i) => { h += `<div class="score-row"><span>\${i+1}. \${s.name}</span><span>\${s.score}</span></div>`; });
            document.getElementById('leaderboardContent').innerHTML = h;
        }

        function toggleSidebarCurtain(open) { document.getElementById('sidebarCurtain').style.right = open ? '0px' : '-300px'; }

        let lastUser = localStorage.getItem('snake_last_user');
        if(lastUser) { document.getElementById('playerName').value = lastUser; }
        loadLead();
    </script>
</body>
</html>
"""

@tetris_blueprint.route('/tetris')
def tetris_game():
    dynamic_links = generate_sidebar_html()
    rendered_template = TETRIS_TEMPLATE.replace("<!--DYNAMIC_SIDEBAR_LINKS_PLACEHOLDER-->", dynamic_links)
    return render_template_string(rendered_template)
