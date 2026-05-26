from flask import Blueprint, render_template_string

shooter_blueprint = Blueprint('shooter', __name__)

SHOOTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Space Shooter Classic - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #04060a; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; user-select: none; -webkit-user-select: none; }
        .header-nav { background-color: #0d1117; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #388bfd; box-shadow: 0 4px 25px rgba(56, 139, 253, 0.25); }
        .back-btn { background: #161b22; border: 1px solid #30363d; color: #388bfd; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #388bfd, 0 0 10px #388bfd; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; box-sizing: border-box; }
        .shooter-arcade-cabinet { background: #0d1117; border: 2px solid #21262d; border-top: 4px solid #388bfd; border-radius: 24px; width: 100%; max-width: 400px; padding: 18px; box-shadow: 0 25px 60px rgba(0,0,0,0.8); box-sizing: border-box; position: relative; }
        
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 13.5px; border-bottom: 1px solid #21262d; padding-bottom: 8px; margin-bottom: 12px; color: #388bfd; align-items: center; }
        .stage-badge { color: #ffd700; font-weight: bold; text-shadow: 0 0 5px #ffd700; }
        
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #020305; display: block; border: 2px solid #21262d; border-radius: 12px; max-width: 100%; height: auto; }
        
        /* 🚨 واجهة الإنذار والتحذير عند ظهور الزعيم الأكبر */
        .boss-alert { display: none; position: absolute; top: 15%; width: 100%; color: #f85149; font-size: 18px; font-weight: bold; text-shadow: 0 0 10px #f85149; animation: blinker 0.8s linear infinite; z-index: 4; }
        @keyframes blinker { 50% { opacity: 0; } }
        
        .overlay-txt { display: none; position: absolute; font-size: 20px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(13, 17, 23, 0.98); border: 2px solid #388bfd; padding: 25px; border-radius: 14px; text-align: center; width: 88%; box-shadow: 0 0 30px rgba(56, 139, 253, 0.4); box-sizing: border-box; z-index: 5; }
        
        /* 🕹️ أزرار القيادة الكلاسيكية الكبيرة مع تباعد هندسي ممتاز ومريح للمس */
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: 1fr 1.3fr 1fr; gap: 12px; width: 100%; }
        .ctrl-btn { background: #161b22; border: 1px solid #30363d; border-radius: 16px; padding: 15px; font-size: 22px; color: #388bfd; cursor: pointer; transition: 0.1s; display: flex; align-items: center; justify-content: center; touch-action: none; box-shadow: 0 4px #05070b; }
        .ctrl-btn:active { transform: translateY(2px); box-shadow: 0 2px #05070b; }
        
        .fire-btn { background: #2d1e1f; border: 2px solid #f85149; color: #f85149; text-shadow: 0 0 5px #f85149; font-size: 24px; box-shadow: 0 4px #05070b; }
        .fire-btn:active { background: #f85149; color: #fff; }
        
        .pause-action-btn { grid-column: span 3; background: #161b22; border: 1px solid #8b949e; color: #8b949e; font-size: 13px; font-weight: bold; border-radius: 10px; padding: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 4px; font-family: inherit; touch-action: none; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe Space</a>
        <span style="font-weight:bold; color:#388bfd;"><i class="fas fa-space-shuttle"></i> أركيد الفضاء</span>
    </div>
    <div class="main-container">
        <div class="shooter-arcade-cabinet">
            <div class="score-container">
                <span id="scoreDisplay">النقاط: 0</span>
                <span id="stageDisplay" class="stage-badge">المرحلة: 1 🌌</span>
                <span>RETRO</span>
            </div>
            
            <div class="game-area">
                <!-- 🚨 نص الإنذار الكلاسيكي عند قدوم الزعيم -->
                <div id="bossAlertText" class="boss-alert">⚠️ تحذير: اقتراب سفينة الزعيم الأكبر! ⚠️</div>
                
                <canvas id="gameCanvas" width="360" height="460"></canvas>
                <div id="pauseOverlay" class="overlay-txt"><i class="fas fa-pause-circle"></i> تم تعليق القتال ⏸️</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 8px 0; color:#388bfd;">معركة المجرة الكلاسيكية</h4>
                    <p id="finalScoreText" style="margin:0 0 12px 0; font-size:13px; font-weight:bold; color:#8b949e;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:10px 25px; font-size:14px; font-weight:bold; cursor:pointer; border-radius:8px; box-shadow: 0 0 12px #238636;" onclick="startGame()">تشغيل محرك الإقلاع 🚀</button>
                </div>
            </div>
            
            <!-- 🕹️ تم تصحيح الاتجاهات المعكوسة بالملّي: اليسار (◀) ينقل يساراً، واليمين (▶) ينقل يميناً بشكل طبيعي ومجرب -->
            <div class="control-pad">
                <button class="ctrl-btn" 
                        ontouchstart="event.preventDefault(); handleButtonPress('L', true)" 
                        ontouchend="event.preventDefault(); handleButtonPress('L', false)"
                        onmousedown="handleButtonPress('L', true)" 
                        onmouseup="handleButtonPress('L', false)"><i class="fas fa-chevron-left"></i></button>
                        
                <button class="ctrl-btn fire-btn" 
                        ontouchstart="event.preventDefault(); handleButtonPress('F', true)"
                        ontouchend="event.preventDefault(); handleButtonPress('F', false)"
                        onmousedown="handleButtonPress('F', true)"
                        onmouseup="handleButtonPress('F', false)"><i class="fas fa-crosshairs"></i></button>
                        
                <button class="ctrl-btn" 
                        ontouchstart="event.preventDefault(); handleButtonPress('R', true)" 
                        ontouchend="event.preventDefault(); handleButtonPress('R', false)"
                        onmousedown="handleButtonPress('R', true)" 
                        onmouseup="handleButtonPress('R', false)"><i class="fas fa-chevron-right"></i></button>
                
                <button class="pause-action-btn" ontouchstart="event.preventDefault(); togglePause()" onclick="togglePause()"><i class="fas fa-pause"></i> إيقاف مؤقت / استئناف القتال</button>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas'), ctx = canvas.getContext('2d');
        let player, lasers, enemyLasers, enemies, stars, meteors, particles, boss, score, currentStage, isGameOver = true, isPaused = false, gameInterval, musicInterval;
        let lastShotTime = 0, shotDelay = 200; 
        let controls = { left: false, right: false, fire: false };

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const bkgNotes = [110, 130.81, 147, 165];

        function handleButtonPress(btn, isPressed) {
            if(isPressed && audioCtx.state === 'suspended') audioCtx.resume();
            if (btn === 'L') controls.left = isPressed; // زر اليسار المصلح
            if (btn === 'R') controls.right = isPressed; // زر اليمين المصلح
            if (btn === 'F') controls.fire = isPressed;
        }

        function playSound(type) {
            if(isGameOver || audioCtx.state === 'suspended') return;
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            if(type==='shoot'){ o.type='square'; o.frequency.setValueAtTime(800, audioCtx.currentTime); o.frequency.exponentialRampToValueAtTime(1600, audioCtx.currentTime+0.05); g.gain.setValueAtTime(0.015, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.05); }
            else if(type==='hit'){ o.type='sawtooth'; o.frequency.setValueAtTime(180, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(30, audioCtx.currentTime+0.1); g.gain.setValueAtTime(0.04, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.1); }
            else if(type==='bossAlert'){ o.type='sawtooth'; o.frequency.setValueAtTime(220, audioCtx.currentTime); o.frequency.setValueAtTime(440, audioCtx.currentTime+0.15); g.gain.setValueAtTime(0.06, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.3); }
            else if(type==='lose'){ o.type='sawtooth'; o.frequency.setValueAtTime(130, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(20, audioCtx.currentTime+0.5); g.gain.setValueAtTime(0.15, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.5); }
        }

        function playMusic() {
            if(isGameOver || isPaused) return;
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
            let freq = bkgNotes[Math.floor(Math.random() * bkgNotes.length)] + (currentStage * 12);
            if(boss) freq -= 30; // موسيقى داكنة ومرعبة أثناء مواجهة الزعيم
            o.frequency.setValueAtTime(freq, audioCtx.currentTime); g.gain.setValueAtTime(0.01, audioCtx.currentTime);
            g.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.22); o.connect(g); g.connect(audioCtx.destination);
            o.start(); o.stop(audioCtx.currentTime + 0.25);
        }

        function startGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            document.getElementById('bossAlertText').style.display = 'none';
            player = { x: canvas.width / 2 - 18, y: canvas.height - 50, w: 36, h: 26, speed: 5.5 };
            lasers = []; enemyLasers = []; enemies = []; particles = []; boss = null; score = 0; currentStage = 1; isGameOver = false; isPaused = false;
            
            stars = [];
            for(let i=0; i<35; i++) { stars.push({ x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*1.8, speed: Math.random()*1.2 + 0.3 }); }
            meteors = [];
            for(let i=0; i<3; i++) { meteors.push({ x: Math.random()*canvas.width, y: -50, size: Math.random()*15+10, speed: Math.random()*2+1.5 }); }
            
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            document.getElementById('stageDisplay').innerText = "المرحلة: " + currentStage + " 🌌";
            
            if(gameInterval) clearInterval(gameInterval); if(musicInterval) clearInterval(musicInterval);
            gameInterval = setInterval(gameLoop, 1000 / 60); musicInterval = setInterval(playMusic, 350);
        }

        function createExplosion(x, y, color) {
            for(let i=0; i<12; i++) { particles.push({ x: x, y: y, vx: (Math.random()-0.5)*5, vy: (Math.random()-0.5)*5, alpha: 1.0, color: color }); }
        }
        document.addEventListener('keydown', e => { 
            if(e.key==='ArrowLeft') controls.left = true; 
            if(e.key==='ArrowRight') controls.right = true; 
            if(e.key===' ') controls.fire = true; 
        });
        document.addEventListener('keyup', e => { 
            if(e.key==='ArrowLeft') controls.left = false; 
            if(e.key==='ArrowRight') controls.right = false; 
            if(e.key===' ') controls.fire = false; 
        });

        function togglePause() { if(isGameOver) return; isPaused = !isPaused; document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none'; }

        function drawClassicPlayer(x, y, w, h) {
            // رسم السفينة الكلاسيكية الفخمة بأجنحة نيون متوهجة ومحركات بكسلية
            ctx.fillStyle = '#388bfd'; ctx.beginPath();
            ctx.moveTo(x + w/2, y); ctx.lineTo(x, y + h); ctx.lineTo(x + w/2, y + h - 6); ctx.lineTo(x + w, y + h); ctx.closePath(); ctx.fill();
            ctx.fillStyle = '#58a6ff'; ctx.fillRect(x + w/2 - 2, y + 4, 4, 12);
            ctx.fillStyle = '#ff7b72'; ctx.fillRect(x + w/2 - 3, y + h - 2, 6, Math.random()*5+3); // لهب المحرك الخلفي المتحرك حياً
        }

        function drawClassicEnemy(x, y, w, h) {
            // رسم سفن الأعداء الكلاسيكية بأعين نيون وامضة
            ctx.fillStyle = '#f85149'; ctx.fillRect(x + 4, y, w - 8, h - 6);
            ctx.fillStyle = '#ea605a'; ctx.fillRect(x, y + 6, w, 6);
            ctx.fillStyle = '#ffd700'; ctx.fillRect(x + 5, y + 4, 3, 3); ctx.fillRect(x + w - 8, y + 4, 3, 3); // الأعين
        }

        function drawClassicBoss(b) {
            // رسم سفينة الزعيم الفخمة والضخمة في عريض الشاشة
            ctx.fillStyle = '#a371f7'; ctx.fillRect(b.x, b.y + 6, b.w, b.h - 6);
            ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.moveTo(b.x + b.w/2, b.y + b.h); ctx.lineTo(b.x + b.w/2 - 20, b.y + 10); ctx.lineTo(b.x + b.w/2 + 20, b.y + 10); ctx.closePath(); ctx.fill();
            
            // شريط طاقة الزعيم النيون بالأعلى
            ctx.fillStyle = '#21262d'; ctx.fillRect(b.x, b.y - 12, b.w, 5);
            ctx.fillStyle = '#f85149'; ctx.fillRect(b.x, b.y - 12, b.w * (b.hp / b.maxHp), 5);
        }

        function gameLoop() {
            if (isPaused || isGameOver) return;
            ctx.fillStyle = '#020406'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // تحريك وتجسيد فضاء النجوم السينمائي
            ctx.fillStyle = 'rgba(255,255,255,0.4)';
            stars.forEach(s => { s.y += s.speed; if(s.y > canvas.height) s.y = 0; ctx.fillRect(s.x, s.y, s.size, s.size); });
            
            // تحريك الشهب الصخرية الكلاسيكية بالخلفية للعمق البصري
            ctx.fillStyle = '#21262d';
            meteors.forEach(m => { m.y += m.speed; if(m.y > canvas.height) { m.y = -50; m.x = Math.random()*canvas.width; } ctx.beginPath(); ctx.arc(m.x, m.y, m.size, 0, Math.PI*2); ctx.fill(); });

            // حركة اللاعب المصلحة والمنسقة هندسياً يميناً ويساراً
            if(controls.left) player.x = Math.max(0, player.x - player.speed);
            if(controls.right) player.x = Math.min(canvas.width - player.w, player.x + player.speed);
            drawClassicPlayer(player.x, player.y, player.w, player.h);

            // الإطلاق المتزن المقيد لليزر المزدوج عند الضغط المطول
            if(controls.fire) {
                let now = Date.now();
                if(now - lastShotTime > shotDelay) {
                    lasers.push({ x: player.x + 4, y: player.y, w: 3, h: 12 });
                    lasers.push({ x: player.x + player.w - 7, y: player.y, w: 3, h: 12 });
                    playSound('shoot'); lastShotTime = now;
                }
            }

            // تحديث مقذوفات ليزر اللاعب
            lasers.forEach((l, li) => { l.y -= 8; ctx.fillStyle = '#ffd700'; ctx.fillRect(l.x, l.y, l.w, l.h); if(l.y < 0) lasers.splice(li, 1); });
            
            // تحديث مقذوفات ليزر الزعيم والأعداء
            enemyLasers.forEach((el, eli) => { el.y += 5.5; ctx.fillStyle = '#ff7b72'; ctx.fillRect(el.x, el.y, el.w, el.h); if(el.y > canvas.height) enemyLasers.splice(eli, 1); if(el.y + el.h > player.y && el.x < player.x + player.w && el.x + el.w > player.x) { endGame(); } });

            // 👑 نظام معركة الزعماء (Boss Fight Trigger) عند بلوغ مضاعفات الـ 100 نقطة في المرحلة
            if (score > 0 && score % 100 === 0 && !boss) {
                document.getElementById('bossAlertText').style.display = 'block';
                playSound('bossAlert');
                boss = { x: canvas.width / 2 - 45, y: -60, w: 90, h: 35, speed: 1.5 + (currentStage * 0.3), direction: 1, hp: 4 + (currentStage * 3), maxHp: 4 + (currentStage * 3) };
                enemies = []; // تصفية الأعداء الصغار لتفريغ الساحة للزعيم
            }

            if (boss) {
                // تحريك سفينة الزعيم السينمائية العريضة
                if(boss.y < 45) boss.y += 1;
                boss.x += boss.speed * boss.direction;
                if(boss.x < 0 || boss.x + boss.w > canvas.width) boss.direction *= -1;
                drawClassicBoss(boss);

                // معدل إطلاق الزعيم لليزر الحربي المدمر عشوائياً حسب صعوبة المرحلة
                if(Math.random() < 0.02 + (currentStage * 0.005)) {
                    enemyLasers.push({ x: boss.x + boss.w/2 - 2, y: boss.y + boss.h, w: 4, h: 14 });
                    enemyLasers.push({ x: boss.x + 15, y: boss.y + boss.h, w: 4, h: 14 });
                    enemyLasers.push({ x: boss.x + boss.w - 19, y: boss.y + boss.h, w: 4, h: 14 });
                }

                // تصادم مقذوفات اللاعب مع جسم الزعيم
                lasers.forEach((l, li) => {
                    if(l.x < boss.x + boss.w && l.x + l.w > boss.x && l.y < boss.y + boss.h && l.y + l.h > boss.y) {
                        boss.hp--; lasers.splice(li, 1); playSound('hit');
                        createExplosion(l.x, l.y, '#ffd700');
                        
                        if(boss.hp <= 0) {
                            // هزيمة وعزل الزعيم والانتقال الفوري للمرحلة التالية بنجاح كلاسيكي
                            createExplosion(boss.x + boss.w/2, boss.y + boss.h/2, '#a371f7');
                            score += 50; boss = null; currentStage++;
                            document.getElementById('bossAlertText').style.display = 'none';
                            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
                            document.getElementById('stageDisplay').innerText = "المرحلة: " + currentStage + " 🌌";
                            playSound('shoot');
                        }
                    }
                });
            } else {
                // في غياب الزعيم، تولد سفن الأعداء الصغار العادية تدريجياً وبدون تداخل
                if(Math.random() < 0.016 * (1 + currentStage*0.2) && enemies.length < 5) {
                    let spawnX = Math.random() * (canvas.width - 26);
                    let overlapping = enemies.some(e => Math.abs(e.x - spawnX) < 32 && e.y < 40);
                    if(!overlapping) enemies.push({ x: spawnX, y: -22, w: 26, h: 20, speed: 1.2 + (currentStage * 0.25) });
                }
            }

            // حركة وتصادمات الأعداء الصغار
            enemies.forEach((e, ei) => {
                e.y += e.speed; drawClassicEnemy(e.x, e.y, e.w, e.h);
                if(e.y + e.h > player.y && e.x < player.x + player.w && e.x + e.w > player.x) { endGame(); return; }
                if(e.y > canvas.height) { endGame(); return; }

                lasers.forEach((l, li) => {
                    if(l.x < e.x + e.w && l.x + l.w > e.x && l.y < e.y + e.h && l.y + l.h > e.y) {
                        enemies.splice(ei, 1); lasers.splice(li, 1); score += 10; playSound('hit');
                        createExplosion(e.x + e.w/2, e.y + e.h/2, '#f85149');
                        document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
                    }
                });
            });

            // تحديث جزيئات الانفجارات البكسلية التكتيكية
            particles.forEach((p, pi) => { p.x += p.vx; p.y += p.vy; p.alpha -= 0.025; ctx.fillStyle = p.color; ctx.globalAlpha = p.alpha; ctx.fillRect(p.x, p.y, 2, 2); ctx.globalAlpha = 1.0; if(p.alpha <= 0) particles.splice(pi, 1); });
        }

        function endGame() { isGameOver = true; clearInterval(gameInterval); clearInterval(musicInterval); playSound('lose'); document.getElementById('bossAlertText').style.display = 'none'; document.getElementById('goTitle').innerText = "تحطمت المركبة! 💀"; document.getElementById('finalScoreText').innerText = "أحرزت: " + score + " نقطة ووصلت للمرحلة " + currentStage; document.getElementById('gameOverScreen').style.display = 'block'; }
    </script>
