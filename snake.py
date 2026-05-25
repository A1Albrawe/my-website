from flask import Blueprint, render_template_string, request, jsonify

# إنشاء البلوبرينت القياسي للعبة الثعبان
snake_blueprint = Blueprint('snake', __name__)

# مصفوفة سحابية مركزية مؤمنة داخل السيرفر لحفظ توب 3 لاعبين على مستوى العالم
GLOBAL_LEADERBOARD = [
    {"name": "البروي 👑", "score": 150},
    {"name": "لاعب 2", "score": 0},
    {"name": "لاعب 3", "score": 0}
]

# مسار سحابي لاستدعاء لوحة الصدارة الموحدة لكل المستخدمين
@snake_blueprint.route('/api/get_leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify(GLOBAL_LEADERBOARD)

# مسار سحابي لاستقبال النتيجة الجديدة وتدقيقها وترتيبها عالمياً في السيرفر
@snake_blueprint.route('/api/submit_score', methods=['POST'])
def submit_score():
    global GLOBAL_LEADERBOARD
    data = request.get_json() or {}
    name = data.get('name', 'لاعب مجهول').strip()
    score = int(data.get('score', 0))
    
    if score > 0 and name:
        GLOBAL_LEADERBOARD.append({"name": name, "score": score})
        # ترتيب المصفوفة من الأعلى للأقل وقصها لتستعرض أفضل 3 لاعبين فقط عالمياً
        GLOBAL_LEADERBOARD.sort(key=lambda x: x['score'], reverse=True)
        GLOBAL_LEADERBOARD = GLOBAL_LEADERBOARD[:3]
        
    return jsonify({"status": "success", "leaderboard": GLOBAL_LEADERBOARD})


SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Snake</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .nokia-phone { background: #161b22; border: 3px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 20px; width: 100%; max-width: 370px; padding: 25px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .nokia-screen { background-color: #0d1117; border: 2px solid #30363d; border-radius: 10px; padding: 10px; position: relative; box-sizing: border-box; touch-action: none; }
        .flash { background-color: #238636 !important; }
        .highscore-flash { animation: rf 0.15s ease infinite alternate; }
        @keyframes rf { 0% { background-color: #0d1117; } 100% { background-color: #21262d; border-color: #ffd700; } }
        .score-container { display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 10px; color: #58a6ff; }
        .audio-controls { display: flex; align-items: center; gap: 4px; }
        .mute-btn { background: none; border: none; font-size: 14px; cursor: pointer; color: #58a6ff; padding: 0; }
        .volume-bar { width: 55px; accent-color: #58a6ff; height: 3px; cursor: pointer; }
        .canvas-container { width: 100%; display: flex; justify-content: center; position: relative; }
        canvas { background-color: #161b22; display: block; max-width: 100%; height: auto; border: 1px solid #30363d; border-radius: 4px; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #58a6ff; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        .leaderboard { margin-top: 10px; background: rgba(0, 0, 0, 0.2); padding: 8px; border-radius: 6px; font-size: 11px; text-align: right; border: 1px solid #30363d; }
        .leaderboard h4 { margin: 0 0 6px 0; text-align: center; font-size: 12px; color: #79c0ff; }
        .score-row { display: flex; justify-content: space-between; padding: 2px 0; font-weight: bold; color: #c9d1d9; }
        .nokia-dpad { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 160px; height: 160px; margin-left: auto; margin-right: auto; }
        .arrow-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; color: #58a6ff; cursor: pointer; box-shadow: 0 4px #0d1117; user-select: none; -webkit-user-select: none; }
        .arrow-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
        .dpad-empty { pointer-events: none; visibility: hidden; }
        .dpad-center-btn { background: #30363d; border: 1px solid #58a6ff; border-radius: 50%; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 14px; color: #fff; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="font-weight:bold; color:#fff;">🐍 لعبة الثعبان السحابية </span>
    </div>
"""
SNAKE_TEMPLATE_BODY = """
    <div class="main-container">
        <div class="nokia-phone" id="phoneWrapper">
            <div class="nokia-screen" id="nokiaScreen">
                <div class="score-container">
                    <span id="snakeScore">النقاط: 0</span>
                    <div class="audio-controls">
                        <button class="mute-btn" id="muteToggle" onclick="toggleMute()"><i class="fas fa-volume-up"></i></button>
                        <input type="range" id="volumeSlider" class="volume-bar" min="0" max="1" step="0.1" value="0.5" oninput="updateVolume(this.value)">
                    </div>
                    <span>ALBRAWE</span>
                </div>
                
                <div class="canvas-container">
                    <canvas id="snakeCanvas" width="240" height="160"></canvas>
                    <div id="pauseOverlay" class="overlay-txt">مؤقت ⏸️</div>
                    <div id="recordOverlay" class="overlay-txt" style="background:#ffd700; color:#000; border-color:#000;">🏆 رقم قياسي عالمي جديد! 🏆</div>
                    
                    <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                        <h4 id="goTitle" style="margin:0 0 5px 0; color:#58a6ff;">مرحباً بك</h4>
                        <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                        <input type="text" id="playerName" style="padding:6px; font-size:12px; border:1px solid #30363d; background:#0d1117; color:#fff; margin-bottom:8px; text-align:center; width:85%; font-family:inherit; font-weight:bold; box-sizing:border-box;" placeholder="اسم المستخدم" maxlength="10">
                        <br><button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:6px 15px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="submitPlayer()">بدء اللعب الفوري</button>
                    </div>
                </div>

                <div class="leaderboard">
                    <h4>🏆 لوحة صدارة أفضل نتائج اللاعبين عالمياً</h4>
                    <div id="leaderboardContent"></div>
                </div>
            </div>

            <div class="nokia-dpad">
                <div class="dpad-empty"></div>
                <div class="arrow-btn" onclick="changeDirection('UP')">▲</div>
                <div class="dpad-empty"></div>
                
                <div class="arrow-btn" onclick="changeDirection('LEFT')">◀</div>
                <div class="dpad-center-btn" onclick="togglePause()"><i class="fas fa-pause"></i></div>
                <div class="arrow-btn" onclick="changeDirection('RIGHT')">▶</div>
                
                <div class="dpad-empty"></div>
                <div class="arrow-btn" onclick="changeDirection('DOWN')">▼</div>
                <div class="dpad-empty"></div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('snakeCanvas'), ctx = canvas.getContext('2d'), box = 10;
        let score = 0, snake = [], food = {x: 0, y: 0}, d = "RIGHT", gameInterval = null, musicInterval = null;
        let isGameOver = true, isPaused = false, isMuted = false, globalVolume = 0.5, currentUser = "";
        let canScore = true;

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const musicNotes = [659.25, 587.33, 392.00, 440.00, 523.25, 493.88, 293.66, 329.63];

        function toggleMute() { isMuted = !isMuted; document.getElementById('muteToggle').innerHTML = isMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>'; document.getElementById('volumeSlider').value = isMuted ? 0 : globalVolume; if(isMuted) stopMusic(); else if(!isGameOver && !isPaused) startMusic(); }
        function updateVolume(v) { globalVolume = parseFloat(v); isMuted = globalVolume === 0; document.getElementById('muteToggle').innerHTML = isMuted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>'; stopMusic(); if(!isMuted && !isGameOver && !isPaused) startMusic(); }
        
        function playSound(t) {
            if (!audioCtx || isMuted || globalVolume === 0) return;
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination); o.type = 'square';
            if (t === 'eat') { o.frequency.setValueAtTime(600, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.06); g.gain.setValueAtTime(0.08 * globalVolume, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.06); }
            else if (t === 'lose') { o.frequency.setValueAtTime(220, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(50, audioCtx.currentTime + 0.5); g.gain.setValueAtTime(0.25 * globalVolume, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.5); }
            else if (t === 'win') { const now = audioCtx.currentTime; o.frequency.setValueAtTime(523, now); o.frequency.setValueAtTime(659, now + 0.08); o.frequency.setValueAtTime(784, now + 0.16); g.gain.setValueAtTime(0.15 * globalVolume, now); o.start(); o.stop(now + 0.3); }
        }

        function playMusic() {
            if (!audioCtx || isGameOver || isMuted || globalVolume === 0 || isPaused) return;
            let tp = audioCtx.currentTime;
            musicNotes.forEach(f => {
                const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
                o.frequency.setValueAtTime(f, tp); g.gain.setValueAtTime(0.02 * globalVolume, tp);
                g.gain.linearRampToValueAtTime(0, tp + 0.18); o.connect(g); g.connect(audioCtx.destination);
                o.start(tp); o.stop(tp + 0.2); tp += 0.2;
            });
        }
        
        function startMusic() { stopMusic(); if(!isMuted && globalVolume > 0 && !isPaused) { playMusic(); musicInterval = setInterval(playMusic, musicNotes.length * 200); } }
        function stopMusic() { if(musicInterval) clearInterval(musicInterval); }
        function togglePause() { if(isGameOver) return; isPaused = !isPaused; document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none'; if(isPaused) stopMusic(); else startMusic(); }

        function submitPlayer() {
            let n = document.getElementById('playerName').value.trim(); if(!n) return;
            currentUser = n; localStorage.setItem('snake_last_user', n);
            document.getElementById('gameOverScreen').style.display = 'none';
            isGameOver = false; initGame();
        }
        function initGame() {
            if(gameInterval) clearInterval(gameInterval); 
            stopMusic();

            score = 0; isPaused = false; isGameOver = false; canScore = true;
            document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('recordOverlay').style.display = 'none';
            document.getElementById('nokiaScreen').classList.remove('highscore-flash');
            
            snake = [{x: 100, y: 80}, {x: 90, y: 80}, {x: 80, y: 80}];
            genFood(); d = "RIGHT";
            gameInterval = setInterval(draw, 120); 
            startMusic();
        }
        
        function genFood() { 
            food = { x: Math.floor(Math.random() * 24) * box, y: Math.floor(Math.random() * 16) * box }; 
            for(let i = 0; i < snake.length; i++) { if(snake[i].x === food.x && snake[i].y === food.y) genFood(); } 
            canScore = true;
        }

        document.onkeydown = function(e) {
            if(e.keyCode === 32) { e.preventDefault(); togglePause(); return; }
            if(isGameOver || isPaused) return; const k = e.keyCode, c = e.key ? e.key.toLowerCase() : "";
            if ((k === 37 || c === 'a' || c === 'ص') && d !== "RIGHT") d = "LEFT";
            else if ((k === 38 || c === 'w' || c === 'ص') && d !== "DOWN") d = "UP";
            else if ((k === 39 || c === 'd' || c === 'ي') && d !== "LEFT") d = "RIGHT";
            else if ((k === 40 || c === 's' || c === 'س') && d !== "UP") d = "DOWN";
        };
        
        function changeDirection(dir) {
            if(isGameOver || isPaused) return;
            if(dir === "LEFT" && d !== "RIGHT") d = "LEFT";
            if(dir === "UP" && d !== "DOWN") d = "UP";
            if(dir === "RIGHT" && d !== "LEFT") d = "RIGHT";
            if(dir === "DOWN" && d !== "UP") d = "DOWN";
        }

        let tsX = 0, tsY = 0;
        window.addEventListener('touchstart', e => { if(e.touches && e.touches.length > 0) { tsX = e.touches.screenX; tsY = e.touches.screenY; } }, {passive: true});
        window.addEventListener('touchend', e => {
            if(isPaused || isGameOver || !e.changedTouches || e.changedTouches.length === 0) return; 
            const xDiff = e.changedTouches.screenX - tsX, yDiff = e.changedTouches.screenY - tsY;
            if(Math.abs(xDiff) > Math.abs(yDiff)) { if(Math.abs(xDiff) > 30) changeDirection(xDiff > 0 ? 'RIGHT' : 'LEFT'); }
            else { if(Math.abs(yDiff) > 30) changeDirection(yDiff > 0 ? 'DOWN' : 'UP'); }
        }, {passive: true});

        function draw() {
            if (isPaused || isGameOver) return; 
            ctx.clearRect(0, 0, 240, 160);
            
            ctx.fillStyle = "#f85149"; ctx.fillRect(food.x + 1, food.y + 1, box - 2, box - 2);
            snake.forEach((c, i) => { ctx.fillStyle = i === 0 ? "#58a6ff" : "#3fb950"; ctx.fillRect(c.x + 1, c.y + 1, box - 2, box - 2); });

            let hX = snake[0].x, hY = snake[0].y;
            if(d === "LEFT") hX -= box; else if(d === "UP") hY -= box; else if(d === "RIGHT") hX += box; else if(d === "DOWN") hY += box;
            let nH = {x: hX, y: hY};

            if(hX < 0 || hX >= 240 || hY < 0 || hY >= 160 || snake.some(c => c.x === nH.x && c.y === nH.y)) { endGame(); return; }

            if(hX === food.x && hY === food.y) {
                if(canScore) { score += 10; document.getElementById('snakeScore').innerText = "النقاط: " + score; playSound('eat'); canScore = false; genFood(); }
            } else { snake.pop(); }
            snake.unshift(nH);
        }

        function endGame() {
            clearInterval(gameInterval); stopMusic(); isGameOver = true; playSound('lose');
            
            // 🎯 ضخ النتيجة الجديدة مباشرة إلى السيرفر السحابي الموحد لكل العالم عبر الـ FETCH
            fetch('/api/submit_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: currentUser, score: score })
            }).then(res => res.json())
              .then(data => {
                  displayLeaderboard(data.leaderboard);
                  if(data.leaderboard.length > 0 && data.leaderboard[0].name === currentUser && score > 0) {
                      playSound('win');
                      document.getElementById('recordOverlay').style.display = 'block';
                      document.getElementById('nokiaScreen').classList.add('highscore-flash');
                  }
              });

            document.getElementById('goTitle').innerText = "انتهت اللعبة";
            document.getElementById('finalScoreText').innerText = "نقاط الجولة المحققة: " + score;
            document.getElementById('playerName').value = currentUser;
            document.getElementById('gameOverScreen').style.display = 'block';
        }

        // 🎯 سحب وعرض اللوحة الموحدة فور فتح الصفحة
        function loadLead() {
            fetch('/api/get_leaderboard')
            .then(res => res.json())
            .then(data => displayLeaderboard(data));
        }

        function displayLeaderboard(list) {
            let h = "";
            list.forEach((s, i) => { h += `<div class="score-row"><span>${i+1}. ${s.name}</span><span>${s.score}</span></div>`; });
            document.getElementById('leaderboardContent').innerHTML = h;
        }

        let lastUser = localStorage.getItem('snake_last_user');
        if(lastUser) { document.getElementById('playerName').value = lastUser; }
        loadLead();
    </script>
    <script>
      window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
    </script>
    <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

# دمج الأجزاء الثلاثة البرمجية وعرض القالب الكامل لـ Flask
@snake_blueprint.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE + SNAKE_TEMPLATE_BODY)
