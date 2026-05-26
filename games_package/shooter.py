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
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #388bfd; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #388bfd; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        /* 🌌 تأثير النيون المطور لاسم المهندس البراوي في المنتصف للتوجيه للرئيسية */
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #388bfd, 0 0 10px #388bfd; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #388bfd; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; box-sizing: border-box; }
        
        /* 📱 ترقية الهيكل الحاضن ليصبح لوحة قيادة فضائية متناسقة وواسعة */
        .shooter-arcade-cabinet { background: #161b22; border: 2px solid #30363d; border-top: 4px solid #388bfd; border-radius: 24px; width: 100%; max-width: 440px; padding: 20px; box-shadow: 0 25px 50px rgba(0,0,0,0.7); box-sizing: border-box; position: relative; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 12px; color: #388bfd; align-items: center; }
        .level-badge { color: #ffd700; font-weight: bold; text-shadow: 0 0 5px #ffd700; }
        
        /* 🎴 تكبير وتوسيع شاشة اللعب السينمائية المفتوحة */
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #050508; display: block; border: 2px solid #388bfd; border-radius: 12px; max-width: 100%; height: auto; box-shadow: 0 0 20px rgba(56, 139, 253, 0.2); }
        
        /* شاشات التنبيه التفاعلية */
        .overlay-txt { display: none; position: absolute; font-size: 22px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(13, 17, 23, 0.95); border: 2px solid #388bfd; padding: 25px; border-radius: 14px; text-align: center; width: 88%; box-shadow: 0 0 30px #388bfd; box-sizing: border-box; z-index: 5; }
        
        /* 🎮 هندسة أزرار التحكم العملاقة والمنفصلة للعب الحربي المريح */
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 12px; width: 100%; }
        .ctrl-btn { background: #21262d; border: 1px solid #30363d; border-radius: 16px; padding: 16px; font-size: 22px; color: #388bfd; cursor: pointer; user-select: none; -webkit-user-select: none; font-weight: bold; box-shadow: 0 5px #0d1117; transition: 0.1s; display: flex; align-items: center; justify-content: center; }
        .ctrl-btn:active { transform: translateY(3px); box-shadow: 0 2px #0d1117; }
        
        /* زر النار المخصص القتالي */
        .fire-btn { background: #2d1e1f; border: 2px solid #f85149; color: #f85149; text-shadow: 0 0 5px #f85149; box-shadow: 0 5px #0d1117; font-size: 24px; }
        .fire-btn:active { background: #f85149; color: #fff; }
        
        /* زر الإيقاف المؤقت السفلي المعزول والمحمي */
        .pause-action-btn { grid-column: span 3; background: #21262d; border: 1px solid #8b949e; color: #8b949e; font-size: 13px; font-weight: bold; border-radius: 10px; padding: 12px; cursor: pointer; box-shadow: 0 4px #0d1117; display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 5px; font-family: inherit; }
        .pause-action-btn:active { transform: translateY(2px); box-shadow: 0 2px #0d1117; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#388bfd;">🚀 غازي الفضاء</span>
    </div>
    <div class="main-container">
        <div class="shooter-arcade-cabinet">
            <div class="score-container">
                <span id="scoreDisplay">النقاط: 0</span>
                <span id="levelDisplay" class="level-badge">المرحلة: 1 / 10 👑</span>
                <span>GALAXY</span>
            </div>
            
            <div class="game-area">
                <!-- ✅ تكبير وتوسيع أبعاد الكانفاس لتوفير مساحة قتال ومناورة واسعة وحرة -->
                <canvas id="gameCanvas" width="380" height="480"></canvas>
                <div id="pauseOverlay" class="overlay-txt"><i class="fas fa-pause-circle"></i> تم إيقاف المعركة مؤقتاً ⏸️</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 8px 0; color:#388bfd;">قاصف المجرة المطور</h4>
                    <p id="finalScoreText" style="margin:0 0 12px 0; font-size:13px; font-weight:bold; color:#8b949e;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:10px 25px; font-size:14px; font-weight:bold; cursor:pointer; border-radius:8px; box-shadow: 0 0 10px #238636;" onclick="startGame()">تشغيل محرك الإقلاع 🚀</button>
                </div>
            </div>
            
            <div class="control-pad">
                <!-- أزرار المناورة وإطلاق قذائف الليزر البارزة جداً للمس -->
                <button class="ctrl-btn" onmousedown="moveLeft(true)" onmouseup="moveLeft(false)" ontouchstart="moveLeft(true)" ontouchend="moveLeft(false)"><i class="fas fa-chevron-left"></i></button>
                <button class="ctrl-btn fire-btn" onclick="shootLaser()"><i class="fas fa-crosshairs"></i></button>
                <button class="ctrl-btn" onmousedown="moveRight(true)" onmouseup="moveRight(false)" ontouchstart="moveRight(true)" ontouchend="moveRight(false)"><i class="fas fa-chevron-right"></i></button>
                
                <button class="pause-action-btn" onclick="togglePause()"><i class="fas fa-pause"></i> تعليق القتال / استئناف الهجوم</button>
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
            if(t==='shoot'){ o.type='square'; o.frequency.setValueAtTime(700, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1600, audioCtx.currentTime+0.08); g.gain.setValueAtTime(0.02, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.08); }
            else if(t==='hit'){ o.type='sawtooth'; o.frequency.setValueAtTime(220, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(50, audioCtx.currentTime+0.15); g.gain.setValueAtTime(0.06, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.15); }
            else if(t==='levelUp'){ o.type='sine'; o.frequency.setValueAtTime(523.25, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1046.50, audioCtx.currentTime+0.25); g.gain.setValueAtTime(0.06, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.25); }
            else if(t==='lose'){ o.type='sawtooth'; o.frequency.setValueAtTime(140, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(30, audioCtx.currentTime+0.5); g.gain.setValueAtTime(0.15, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.5); }
        }

        function playMusic() {
            if(isGameOver || isPaused) return;
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
            let note = bkgNotes[Math.floor(Math.random() * bkgNotes.length)] + (level * 14);
            o.frequency.setValueAtTime(note, audioCtx.currentTime); g.gain.setValueAtTime(0.015, audioCtx.currentTime);
            g.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.25); o.connect(g); g.connect(audioCtx.destination);
            o.start(); o.stop(audioCtx.currentTime + 0.3);
        }

        function startGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            // تحسين موضع السفينة ليتناسب مع اتساع الشاشة الجديد لزيادة حرية الحركة
            player = { x: 175, y: 430, w: 32, h: 22, speed: 5.5 }; lasers = []; enemies = []; score = 0; level = 1; isGameOver = false; isPaused = false;
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            document.getElementById('levelDisplay').innerText = "المرحلة: " + level + " / 10 👑";
            if(gameInterval) clearInterval(gameInterval); if(musicInterval) clearInterval(musicInterval);
            gameInterval = setInterval(gameLoop, 1000 / 60); musicInterval = setInterval(playMusic, 350);
        }

        function moveLeft(b) { leftPressed = b; } function moveRight(b) { rightPressed = b; }
        
        function shootLaser() { 
            if(!isGameOver && !isPaused) { 
                // إطلاق ليزر مزدوج من جناحي السفينة لمظهر قتالي متقدم
                lasers.push({ x: player.x + 4, y: player.y, w: 3, h: 12 }); 
                lasers.push({ x: player.x + player.w - 7, y: player.y, w: 3, h: 12 }); 
                playSound('shoot'); 
            } 
        }

        document.addEventListener('keydown', e => { if(e.key==='ArrowLeft') leftPressed=true; if(e.key==='ArrowRight') rightPressed=true; if(e.key===' ') shootLaser(); });
        document.addEventListener('keyup', e => { if(e.key==='ArrowLeft') leftPressed=false; if(e.key==='ArrowRight') rightPressed=false; });

        function togglePause() {
            if(isGameOver) return;
            isPaused = !isPaused;
            document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none';
        }

        // دالة رسم سفينة النيون المطورة بدلاً من المربعات الصامتة والعقيمة
        function drawPlayerShip(x, y, w, h) {
            ctx.fillStyle = '#388bfd';
            ctx.beginPath();
            ctx.moveTo(x + w / 2, y); // مقدمة السفينة النيون
            ctx.lineTo(x, y + h);
            ctx.lineTo(x + w, y + h);
            ctx.closePath();
            ctx.fill();
            // أجنحة النيون الجانبية المتوهجة للحماية
            ctx.strokeStyle = '#58a6ff'; ctx.lineWidth = 2;
            ctx.strokeRect(x - 2, y + h - 6, w + 4, 3);
        }

        // دالة رسم سفن الأعداء الغازية للمجرة
        function drawEnemyShip(x, y, w, h) {
            ctx.fillStyle = '#f85149';
            ctx.fillRect(x + 4, y, w - 8, h - 4);
            ctx.fillStyle = '#ff7b72'; // محرك الدفع الخلفي للعدو
            ctx.fillRect(x, y + h - 4, w, 4);
        }

        function gameLoop() {
            if (isPaused) return;
            ctx.fillStyle = '#050508'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // رسم خلفية نجوم فضائية متحركة وخفيفة بشكل جمالي واحترافي
            ctx.fillStyle = 'rgba(255,255,255,0.3)';
            for(let i=0; i<15; i++) { ctx.fillRect((i*37)%canvas.width, (gameInterval*2 + i*80)%canvas.height, 2, 2); }
            
            if(leftPressed) player.x = Math.max(0, player.x - player.speed);
            if(rightPressed) player.x = Math.min(canvas.width - player.w, player.x + player.speed);

            drawPlayerShip(player.x, player.y, player.w, player.h);

            // تسيير أشعة الليزر النيون الذهبية
            lasers.forEach((l, i) => { l.y -= 7.5; ctx.fillStyle = '#ffd700'; ctx.fillRect(l.x, l.y, l.w, l.h); if(l.y < 0) lasers.splice(i, 1); });

            // تصعيد ميكانيكي لنسبة ظهور الأعداء وسرعتهم تبعاً لتصاعد مستوى الـ 10 مراحل الحالية
            if(Math.random() < 0.018 + (level * 0.005) && enemies.length < 7) {
                enemies.push({ x: Math.random() * (canvas.width - 24), y: -20, w: 24, h: 20, speed: 1.1 + (level * 0.38) });
            }

            enemies.forEach((e, ei) => {
                e.y += e.speed; drawEnemyShip(e.x, e.y, e.w, e.h);
                if(e.y + e.h > player.y && e.x < player.x + player.w && e.x + e.w > player.x) { endGame(); }
                if(e.y > canvas.height) { endGame(); }

                lasers.forEach((l, li) => {
                    if(l.x < e.x + e.w && l.x + l.w > e.x && l.y < e.y + e.h && l.y + l.h > e.y) {
                        enemies.splice(ei, 1); lasers.splice(li, 1); score += 10; playSound('hit');
                        document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
                        
                        // الترقية التلقائية عبر الـ 10 مراحل السحابية كل 100 نقطة قتالية
                        if(score % 100 === 0 && level < 10) { level++; player.speed += 0.4; document.getElementById('levelDisplay').innerText = "المرحلة: " + level + " / 10 👑"; playSound('levelUp'); }
                    }
                });
            });
        }

        function endGame() {
            isGameOver = true; clearInterval(gameInterval); clearInterval(musicInterval); playSound('lose');
            document.getElementById('goTitle').innerText = "تحطمت المركبة! 💀";
            document.getElementById('finalScoreText').innerText = "أحرزت: " + score + " نقطة قتالية ووصلت للمرحلة " + level;
            document.getElementById('gameOverScreen').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@shooter_blueprint.route('/shooter')
def shooter_page():
    return render_template_string(SHOOTER_TEMPLATE)
