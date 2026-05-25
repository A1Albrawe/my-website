from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>نوكيا المطور الشامل - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #121212;
            color: #000; 
            padding: 10px; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            box-sizing: border-box;
            overscroll-behavior-y: contain;
        }
        .back-btn { 
            background: #111; 
            color: #8c9f21; 
            border: 2px solid #8c9f21; 
            padding: 8px 16px; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            font-weight: bold; 
            margin-bottom: 15px; 
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .shake { animation: sk 0.3s linear infinite; } 
        @keyframes sk { 0% {transform: translate(2px, 1px);} 50% {transform: translate(-2px, -1px);} 100% {transform: translate(1px, -2px);} }
        
        /* الحفاظ التام على مجسم الهاتف موحداً حتى على شاشات المحمول */
        .nokia-phone { 
            background: #3a4d5c; 
            border: 8px solid #25333d; 
            border-radius: 40px; 
            width: 100%;
            max-width: 380px; 
            padding: 25px 20px; 
            box-shadow: 0 20px 45px rgba(0,0,0,0.8); 
            box-sizing: border-box; 
            position: relative;
        }
        .nokia-screen { 
            background-color: #8c9f21; 
            border: 12px solid #111; 
            border-radius: 10px; 
            padding: 10px; 
            position: relative; 
            box-sizing: border-box; 
            touch-action: none;
            box-shadow: inset 0 0 15px rgba(0,0,0,0.6);
        }
        .flash { background-color: #a4b930 !important; }
        .highscore-flash { animation: rf 0.15s ease infinite alternate; }
        @keyframes rf { 0% { background-color: #8c9f21; } 100% { background-color: #ffd700; } }
        
        .score-container { display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 13px; border-bottom: 2px solid #000; padding-bottom: 4px; margin-bottom: 6px; }
        .audio-controls { display: flex; align-items: center; gap: 4px; }
        .mute-btn { background: none; border: none; font-size: 14px; cursor: pointer; color: #000; padding: 0; }
        .volume-bar { width: 50px; accent-color: #000; height: 3px; cursor: pointer; }
        .shop-btn { background: #000; color: #8c9f21; border: none; padding: 3px 8px; font-weight: bold; cursor: pointer; border-radius: 3px; font-family: inherit; font-size: 11px; }
        
        .canvas-container { width: 100%; display: flex; justify-content: center; position: relative; }
        canvas { background-color: transparent; display: block; max-width: 100%; height: auto; border: 1px solid rgba(0,0,0,0.2); }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #000; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(140, 159, 33, 0.95); padding: 8px 12px; border: 2px solid #000; border-radius: 4px; z-index: 5; text-align: center; width: 85%; box-sizing: border-box; }
        
        .shop-panel { display: none; position: absolute; top: 0; right: 0; width: 100%; height: 100%; background: #8c9f21; z-index: 30; border-radius: 4px; padding: 12px; box-sizing: border-box; text-align: right; overflow-y: auto; }
        .shop-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold; }
        .shop-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px dashed #000; font-size: 12px; font-weight: bold; }
        .item-buy-btn { background: #000; color: #8c9f21; border: none; padding: 3px 8px; cursor: pointer; font-family: inherit; font-size: 11px; border-radius: 2px; }
        .item-buy-btn.equipped { background: transparent; color: #000; border: 1px solid #000; pointer-events: none; }
        
        .leaderboard { margin-top: 8px; background: rgba(0, 0, 0, 0.05); padding: 6px; border-radius: 4px; font-size: 11px; text-align: right; border-top: 1px dashed #000; }
        .leaderboard h4 { margin: 0 0 4px 0; text-align: center; font-size: 12px; }
        .score-row { display: flex; justify-content: space-between; padding: 1px 0; font-weight: bold; }
        
        /* تعديل وحفظ أبعاد لوحة الأسهم الدائرية الكبيرة لتناسب الموبايل دائماً */
        .nokia-dpad { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 180px; height: 180px; margin-left: auto; margin-right: auto; }
        .arrow-btn { background: #cbd3d8; border: 2px solid #a1aab0; border-radius: 15px; display: flex; justify-content: center; align-items: center; font-size: 22px; color: #222; cursor: pointer; box-shadow: 0 4px #78838a, inset 0 1px rgba(255,255,255,0.5); user-select: none; -webkit-user-select: none; }
        .arrow-btn:active { box-shadow: 0 1px #78838a; transform: translateY(2px); }
        .dpad-empty { pointer-events: none; visibility: hidden; }
        .dpad-center-btn { background: #a1aab0; border: 2px solid #78838a; border-radius: 50%; cursor: pointer; box-shadow: 0 3px #576066; display: flex; justify-content: center; align-items: center; font-size: 14px; color: #222; }
        .dpad-center-btn:active { box-shadow: 0 0 #576066; transform: translateY(1px); }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> القائمة الرئيسية</a>
    
    <div class="nokia-phone" id="phoneWrapper">
        <div class="nokia-screen" id="nokiaScreen">
            <div class="score-container">
                <span id="snakeScore">النقاط: 0</span>
                <div class="audio-controls">
                    <button class="mute-btn" id="muteToggle" onclick="toggleMute()"><i class="fas fa-volume-up"></i></button>
                    <input type="range" id="volumeSlider" class="volume-bar" min="0" max="1" step="0.1" value="0.5" oninput="updateVolume(this.value)">
                </div>
                <button class="shop-btn" onclick="toggleShop()"><i class="fas fa-shopping-basket"></i> المتجر</button>
            </div>
            
            <div class="canvas-container">
                <canvas id="snakeCanvas" width="280" height="180"></canvas>
                <div id="pauseOverlay" class="overlay-txt">مؤقت</div>
                <div id="recordOverlay" class="overlay-txt" style="background:#ffd700; border-color:#000;">🏆 رقم قياسي جديد! 🏆</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0;">مرحباً بك</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <input type="text" id="playerName" class="input-name" style="padding:6px; font-size:12px; border:2px solid #000; background:#8c9f21; margin-bottom:8px; text-align:center; width:85%; font-family:inherit; font-weight:bold; box-sizing:border-box;" placeholder="اسم المستخدم" maxlength="10">
                    <br><button class="restart-btn" style="background:#000; color:#8c9f21; border:none; padding:6px 15px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:3px;" onclick="submitPlayer()">بدء اللعب</button>
                </div>
            </div>

            <div class="leaderboard">
                <h4>🏆 صدارة اللعب وصافي التفاح (<span id="userApples">0</span> 🍎)</h4>
                <div id="leaderboardContent"></div>
            </div>

            <div class="shop-panel" id="shopPanel">
                <div class="shop-header">
                    <span>🛒 متجر نوكيا المميز</span>
                    <button class="shop-btn" onclick="toggleShop()">إغلاق</button>
                </div>
                <div style="font-size:11px; font-weight:bold; margin-bottom:8px; border-bottom:1px solid #000; padding-bottom:3px;">رصيدك المتوفر: <span id="shopCoins">0</span> 🍎</div>
                <div id="shopItemsContainer"></div>
            </div>
        </div>

        <!-- تم تثبيت وتصحيح الاتجاهات التناظرية لزر الـ D-Pad لمنع أي عكس في التوجيه باللمس -->
        <div class="nokia-dpad">
            <div class="dpad-empty"></div>
            <div class="arrow-btn" onmousedown="changeDirection('UP')" ontouchstart="changeDirection('UP'); event.preventDefault();"><i class="fas fa-chevron-up"></i></div>
            <div class="dpad-empty"></div>
            
            <div class="arrow-btn" onmousedown="changeDirection('LEFT')" ontouchstart="changeDirection('LEFT'); event.preventDefault();"><i class="fas fa-chevron-left"></i></div>
            <div class="dpad-center-btn" onclick="togglePause()" ontouchstart="togglePause(); event.preventDefault();"><i class="fas fa-pause"></i></div>
            <div class="arrow-btn" onmousedown="changeDirection('RIGHT')" ontouchstart="changeDirection('RIGHT'); event.preventDefault();"><i class="fas fa-chevron-right"></i></div>
            
            <div class="dpad-empty"></div>
---

### 📋 الجزء الثاني: (نظام الصوت، تفعيل المتجر، وحفظ الحسابات من نوكيا)

```python
    <script>
        const canvas = document.getElementById('snakeCanvas'), ctx = canvas.getContext('2d'), box = 10;
        let score, snake, food, d, gameInterval, musicInterval, isGameOver = true, isPaused = false, isMuted = false, globalVolume = 0.5, currentUser = "", inShop = false;
        
        let shopItems = [
            { id: 's_green', type: 'skin', name: 'ثعبان أسود بكسل', price: 0, color: '#000000', purchased: true },
            { id: 's_red', type: 'skin', name: 'ثعبان أحمر ناري', price: 30, color: '#aa0000', purchased: false },
            { id: 's_blue', type: 'skin', name: 'ثعبان أزرق ملكي', price: 50, color: '#0000aa', purchased: false },
            { id: 'm_retro', type: 'music', name: 'نغمة أركيد هادئة', price: 0, notes:, purchased: true },
            { id: 'm_nokia', type: 'music', name: 'نغمة نوكيا المألوفة', price: 40, notes: [659.25, 587.33, 392.00, 440.00, 523.25, 493.88, 293.66, 329.63], purchased: false }
        ];

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function getActiveSkin() { return shopItems.find(i => i.type === 'skin' && i.equipped)?.color || '#000000'; }
        function getActiveMusic() { return shopItems.find(i => i.type === 'music' && i.equipped)?.notes ||; }

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
            let nt = getActiveMusic(), tp = audioCtx.currentTime;
            nt.forEach(f => {
                const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.type = 'triangle';
                o.frequency.setValueAtTime(f, tp); g.gain.setValueAtTime(0.02 * globalVolume, tp);
                g.gain.linearRampToValueAtTime(0, tp + 0.18); o.connect(g); g.connect(audioCtx.destination);
                o.start(tp); o.stop(tp + 0.2); tp += 0.2;
            });
        }
        function startMusic() { stopMusic(); if(!isMuted && globalVolume > 0 && !isPaused) { playMusic(); musicInterval = setInterval(playMusic, getActiveMusic().length * 200); } }
        function stopMusic() { if(musicInterval) clearInterval(musicInterval); }

        function togglePause() { if(isGameOver) return; isPaused = !isPaused; document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none'; if(isPaused) stopMusic(); else startMusic(); }
        function toggleShop() { inShop = !inShop; document.getElementById('shopPanel').style.display = inShop ? 'block' : 'none'; if(inShop) renderShop(); }

        function loadUserData(n) {
            currentUser = n; localStorage.setItem('snake_last_user', n);
            let uData = JSON.parse(localStorage.getItem('snake_u_' + n)) || { totalApples: 0, items: ['s_green', 'm_retro'], equipped: { skin: 's_green', music: 'm_retro' } };
            document.getElementById('userApples').innerText = uData.totalApples;
            document.getElementById('shopCoins').innerText = uData.totalApples;
            shopItems.forEach(i => { i.purchased = uData.items.includes(i.id); i.equipped = uData.equipped[i.type] === i.id; });
        }

        function submitPlayer() {
            let n = document.getElementById('playerName').value.trim(); if(!n) return;
            loadUserData(n); document.getElementById('gameOverScreen').style.display = 'none';
            isGameOver = false; initGame();
        }function initGame() {
            score = 0; isPaused = false; document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('recordOverlay').style.display = 'none';
            document.getElementById('nokiaScreen').classList.remove('highscore-flash');
            
            // تهيئة السلسلة المصححة لرأس الثعبان لمنع حدوث أي اختفاء عند بداية الحركة
            snake = [
                {x: 10 * box, y: 9 * box},
                {x: 9 * box, y: 9 * box},
                {x: 8 * box, y: 9 * box}
            ];
            genFood(); d = "RIGHT";
            if(gameInterval) clearInterval(gameInterval); gameInterval = setInterval(draw, 110); startMusic();
        }
        function genFood() { food = { x: Math.floor(Math.random() * 28) * box, y: Math.floor(Math.random() * 18) * box }; for(let c of snake) { if(c.x === food.x && c.y === food.y) genFood(); } }

        document.onkeydown = function(e) {
            if(e.keyCode === 32) { e.preventDefault(); togglePause(); return; }
            if(isGameOver || isPaused) return; const k = e.keyCode, c = e.key ? e.key.toLowerCase() : "";
            if ((k === 37 || c === 'a' || c === 'ص' || k === 100 || k === 52) && d !== "RIGHT") d = "LEFT";
            else if ((k === 38 || c === 'w' || c === 'ص' || k === 104 || k === 56) && d !== "DOWN") d = "UP";
            else if ((k === 39 || c === 'd' || c === 'ي' || k === 102 || k === 54) && d !== "LEFT") d = "RIGHT";
            else if ((k === 40 || c === 's' || c === 'س' || k === 98 || k === 50) && d !== "UP") d = "DOWN";
        };
        
        function changeDirection(dir) {
            if(isGameOver || isPaused) return;
            if(dir === "LEFT" && d !== "RIGHT") d = "LEFT";
            if(dir === "UP" && d !== "DOWN") d = "UP";
            if(dir === "RIGHT" && d !== "LEFT") d = "RIGHT";
            if(dir === "DOWN" && d !== "UP") d = "DOWN";
        }

        // 📱 إعادة كتابة وإطلاق التعرف الفوري على اللمس (Touch Swipe) على مستوى الصفحة المانع لتعطيل الموبايل
        let tsX = 0, tsY = 0;
        window.addEventListener('touchstart', e => { tsX = e.changedTouches[0].screenX; tsY = e.changedTouches[0].screenY; }, {passive: false});
        window.addEventListener('touchend', e => {
            if(isPaused || isGameOver) return; 
            const xDiff = e.changedTouches[0].screenX - tsX;
            const yDiff = e.changedTouches[0].screenY - tsY;
            
            if(Math.abs(xDiff) > Math.abs(yDiff)) {
                if(Math.abs(xDiff) > 30) changeDirection(xDiff > 0 ? 'RIGHT' : 'LEFT');
            } else {
                if(Math.abs(yDiff) > 30) changeDirection(yDiff > 0 ? 'DOWN' : 'UP');
            }
        }, {passive: false});

        function draw() {
            if (isPaused) return; ctx.clearRect(0, 0, 280, 180);
            ctx.fillStyle = "#000"; ctx.fillRect(food.x + 1, food.y + 1, box - 2, box - 2);
            let skColor = getActiveSkin();
            
            snake.forEach((c, i) => { 
                ctx.fillStyle = (i === 0) ? "#000000" : skColor; 
                ctx.fillRect(c.x + 1, c.y + 1, box - 2, box - 2); 
                if(i === 0) { ctx.fillStyle = "#8c9f21"; ctx.fillRect(c.x + 3, c.y + 3, 2, 2); }
            });

            // تم تصحيح منطق حساب إحداثيات الرأس المتغير كعنصر مصفوفة كامل مصفوفاً بدقة من السلسلة البرمجية لمنع الاختفاء
            let hX = snake[0].x;
            let hY = snake[0].y;
            
            if(d === "LEFT") hX -= box; 
            else if(d === "UP") hY -= box; 
            else if(d === "RIGHT") hX += box; 
            else if(d === "DOWN") hY += box;
            
            let nH = {x: hX, y: hY};

            if(hX < 0 || hX >= 280 || hY < 0 || hY >= 180 || snake.some(c => c.x === nH.x && c.y === nH.y)) { endGame(); return; }

            if(hX === food.x && hY === food.y) {
                score += 10; document.getElementById('snakeScore').innerText = "النقاط: " + score; playSound('eat');
                document.getElementById('touchArea').classList.add('flash'); setTimeout(() => document.getElementById('touchArea').classList.remove('flash'), 60);
                genFood();
            } else { snake.pop(); }
            snake.unshift(nH);
        }

        function endGame() {
            clearInterval(gameInterval); stopMusic(); isGameOver = true; playSound('lose');
            document.getElementById('phoneWrapper').classList.add('shake'); setTimeout(() => document.getElementById('phoneWrapper').classList.remove('shake'), 300);
            
            let uData = JSON.parse(localStorage.getItem('snake_u_' + currentUser));
            let earnedApples = score / 10; uData.totalApples += earnedApples;
            localStorage.setItem('snake_u_' + currentUser, JSON.stringify(uData));
            loadUserData(currentUser);

            let l = JSON.parse(localStorage.getItem('responsive_nokia_scores')) || []; l.push({name: currentUser, score: score}); l.sort((a,b)=>b.score-a.score); l = l.slice(0,3);
            localStorage.setItem('responsive_nokia_scores', JSON.stringify(l)); loadLead();

            document.getElementById('goTitle').innerText = "انتهت اللعبة";
            document.getElementById('finalScoreText').innerText = "نقاط الجولة: " + score + " | ربحت: " + earnedApples + " 🍎";
            document.getElementById('playerName').value = currentUser;
            document.getElementById('gameOverScreen').style.display = 'block';
            
            if(l.length > 0 && l[0].name === currentUser && score > 0 && l[0].score === score) { 
                playSound('win'); 
                document.getElementById('recordOverlay').style.display = 'block'; 
                document.getElementById('nokiaScreen').classList.add('highscore-flash');
            }
        }

        function renderShop() {
            let uData = JSON.parse(localStorage.getItem('snake_u_' + currentUser));
            let h = ""; shopItems.forEach(i => {
                let btn = ""; if(i.equipped) btn = `<button class="item-buy-btn equipped">مفعل</button>`;
                else if(i.purchased) btn = `<button class="item-buy-btn" style="background:#000;color:#8c9f21;" onclick="equipItem('${i.id}')">تفعيل</button>`;
                else btn = `<button class="item-buy-btn" style="background:#000;color:#ff4d4d;" onclick="buyItem('${i.id}', ${i.price})">${i.price} 🍎</button>`;
                h += `<div class="shop-item"><span>${i.name}</span>${btn}</div>`;
            });
            document.getElementById('shopItemsContainer').innerHTML = h;
        }
        window.buyItem = function(id, pr) {
            let u = JSON.parse(localStorage.getItem('snake_u_' + currentUser)); if(u.totalApples < pr) { alert("رصيد تفاحك غير كافٍ! 🍎"); return; }
            u.totalApples -= pr; u.items.push(id); localStorage.setItem('snake_u_' + currentUser, JSON.stringify(u)); loadUserData(currentUser); renderShop();
        }
        window.equipItem = function(id) {
            let u = JSON.parse(localStorage.getItem('snake_u_' + currentUser)), it = shopItems.find(i=>i.id===id);
            u.equipped[it.type] = id; localStorage.setItem('snake_u_' + currentUser, JSON.stringify(u)); loadUserData(currentUser); renderShop(); stopMusic(); if(!isGameOver) startMusic();
        }

        function loadLead() {
            let l = JSON.parse(localStorage.getItem('responsive_nokia_scores')) || [{name:"المركز 1",score:0},{name:"المركز 2",score:0},{name:"المركز 3",score:0}], h = "";
            l.forEach((s, i) => { h += `<div class="score-row"><span>${i+1}. ${s.name}</span><span>${s.score}</span></div>`; });
            document.getElementById('leaderboardContent').innerHTML = h;
        }

        let lastUser = localStorage.getItem('snake_last_user');
        if(lastUser) { document.getElementById('playerName').value = lastUser; }
        loadLead();
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE)
