from flask import Blueprint, render_template_string

shooter_blueprint = Blueprint('shooter', __name__)

SHOOTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Space Shooter - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #388bfd; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #388bfd; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        /* ✨ تأثير النيون لاسم المهندس البراوي في المنتصف للتوجيه للرئيسية */
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #388bfd, 0 0 10px #388bfd; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #388bfd; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .shooter-phone { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #388bfd; border-radius: 20px; width: 100%; max-width: 360px; padding: 20px 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 10px; color: #388bfd; align-items: center; }
        .level-badge { color: #ffd700; font-weight: bold; }
        
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #000; display: block; border: 2px solid #30363d; border-radius: 6px; max-width: 100%; height: auto; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #388bfd; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 100%; max-width: 260px; margin-left: auto; margin-right: auto; }
        .ctrl-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; padding: 14px; font-size: 18px; color: #388bfd; cursor: pointer; user-select: none; font-weight: bold; box-shadow: 0 3px #0d1117; }
        .ctrl-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <!-- حقن رابط المطور المركزي في منتصف شريط التنقل -->
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#388bfd;">🚀 الفضاء</span>
    </div>
    <div class="main-container">
        <div class="shooter-phone">
            <div class="score-container">
                <span id="scoreDisplay">النقاط: 0</span>
                <span id="levelDisplay" class="level-badge">المرحلة: 1 / 10 👑</span>
                <span>SPACE</span>
            </div>
            <div class="game-area">
                <canvas id="gameCanvas" width="300" height="400"></canvas>
                <div id="pauseOverlay" class="overlay-txt">مؤقت ⏸️</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0; color:#388bfd;">غازي الفضاء السريع</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:8px 20px; font-size:13px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="startGame()">إقلاع فوري 🚀</button>
                </div>
            </div>
            <div class="control-pad">
                <button class="ctrl-btn" onmousedown="moveLeft(true)" onmouseup="moveLeft(false)" ontouchstart="moveLeft(true)" ontouchend="moveLeft(false)">◀</button>
                <button class="ctrl-btn" onclick="shootLaser()">🔥</button>
                <button class="ctrl-btn" onmousedown="moveRight(true)" onmouseup="moveRight(false)" ontouchstart="moveRight(true)" ontouchend="moveRight(false)">▶</button>
                <div></div>
                <button class="ctrl-btn" onclick="togglePause()"><i class="fas fa-pause"></i></button>
                <div></div>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas'), ctx = canvas.getContext('2d');
        let player, lasers, enemies, score, level, isGameOver = true, isPaused = false, gameInterval, musicInterval;
        let leftPressed = false, rightPressed = false;

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const bkgNotes = [110, 130.81, 146.83, 164.81];

        function playSound(t) {
            if(isGameOver || audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            if(t==='shoot'){ o.type='square'; o.frequency.setValueAtTime(600, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1500, audioCtx.currentTime+0.08); g.gain.setValueAtTime(0.02, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.08); }
            else if(t==='hit'){ o.type='sawtooth'; o.frequency.setValueAtTime(200, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(40, audioCtx.currentTime+0.15); g.gain.setValueAtTime(0.06, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.15); }
            else if(t==='levelUp'){ o.type='sine'; o.frequency.setValueAtTime(523.25, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1046.50, audioCtx.currentTime+0.25); g.gain.setValueAtTime(0.08, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.25); }
            else if(t==='lose'){ o.type='sawtooth'; o.frequency.setValueAtTime(150, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(30, audioCtx.currentTime+0.5); g.gain.setValueAtTime(0.15, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.5); }
        }

        function playMusic() {
            if(isGameOver || isPaused) return;
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
            let note = bkgNotes[Math.floor(Math.random() * bkgNotes.length)] + (level * 12);
            o.frequency.setValueAtTime(note, audioCtx.currentTime); g.gain.setValueAtTime(0.015, audioCtx.currentTime);
            g.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.25); o.connect(g); g.connect(audioCtx.destination);
            o.start(); o.stop(audioCtx.currentTime + 0.3);
        }

        function startGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            player = { x: 135, y: 360, w: 30, h: 15, speed: 5 }; lasers = []; enemies = []; score = 0; level = 1; isGameOver = false; isPaused = false;
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            document.getElementById('levelDisplay').innerText = "المرحلة: " + level + " / 10 👑";
            if(gameInterval) clearInterval(gameInterval); if(musicInterval) clearInterval(musicInterval);
            gameInterval = setInterval(gameLoop, 1000 / 60); musicInterval = setInterval(playMusic, 350);
        }

        function moveLeft(b) { leftPressed = b; } function moveRight(b) { rightPressed = b; }
        function shootLaser() { if(!isGameOver && !isPaused) { lasers.push({ x: player.x + player.w/2 - 2, y: player.y, w: 4, h: 10 }); playSound('shoot'); } }

        document.addEventListener('keydown', e => { if(e.key==='ArrowLeft') leftPressed=true; if(e.key==='ArrowRight') rightPressed=true; if(e.key===' ') shootLaser(); });
        document.addEventListener('keyup', e => { if(e.key==='ArrowLeft') leftPressed=false; if(e.key==='ArrowRight') rightPressed=false; });

        function togglePause() {
            if(isGameOver) return;
            isPaused = !isPaused;
            document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none';
        }

        function gameLoop() {
            if (isPaused) return;
            ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 300, 400);
            
            if(leftPressed) player.x = Math.max(0, player.x - player.speed);
            if(rightPressed) player.x = Math.min(300 - player.w, player.x + player.speed);

            ctx.fillStyle = '#388bfd'; ctx.fillRect(player.x, player.y, player.w, player.h);

            lasers.forEach((l, i) => { l.y -= 7; ctx.fillStyle = '#ffd700'; ctx.fillRect(l.x, l.y, l.w, l.h); if(l.y < 0) lasers.splice(i, 1); });

            // تصعيد تدريجي لنسبة التوليد والسرعة مع تصاعد مستويات الـ 10 مراحل
            if(Math.random() < 0.02 + (level * 0.006) && enemies.length < 6) {
                enemies.push({ x: Math.random() * 270, y: 0, w: 22, h: 18, speed: 1.2 + (level * 0.35) });
            }

            enemies.forEach((e, ei) => {
                e.y += e.speed; ctx.fillStyle = '#f85149'; ctx.fillRect(e.x, e.y, e.w, e.h);
                if(e.y + e.h > player.y && e.x < player.x + player.w && e.x + e.w > player.x) { endGame(); }
                if(e.y > 400) { endGame(); }

                lasers.forEach((l, li) => {
                    if(l.x < e.x + e.w && l.x + l.w > e.x && l.y < e.y + e.h && l.y + l.h > e.y) {
                        enemies.splice(ei, 1); lasers.splice(li, 1); score += 10; playSound('hit');
                        document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
                        
                        // تصعيد شاشات المستوى كل 100 نقطة
                        if(score % 100 === 0 && level < 10) { level++; player.speed += 0.5; document.getElementById('levelDisplay').innerText = "المرحلة: " + level + " / 10 👑"; playSound('levelUp'); }
                    }
                });
            });
        }

        function endGame() {
            isGameOver = true; clearInterval(gameInterval); clearInterval(musicInterval); playSound('lose');
            document.getElementById('goTitle').innerText = "انتهت اللعبة! 💀";
            document.getElementById('finalScoreText').innerText = "أحرزت: " + score + " نقطة في المرحلة " + level;
            document.getElementById('gameOverScreen').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@shooter_blueprint.route('/shooter')
def shooter_page():
    return render_template_string(SHOOTER_TEMPLATE)
