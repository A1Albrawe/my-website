from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Snake Master</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #3fb950; position: relative; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #3fb950; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .header-brand-center { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-decoration: none; }
        .neon-text-style { font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #3fb950, 0 0 10px #3fb950; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .game-card { background: #161b22; border: 3px solid #30363d; border-top: 4px solid #3fb950; border-radius: 20px; width: 100%; max-width: 360px; padding: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.5); box-sizing: border-box; }
        .stats-bar { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 10px; color: #3fb950; }
        
        canvas { background-color: #0d1117; display: block; width: 100%; height: auto; border: 2px solid #30363d; border-radius: 8px; }
        .ctrl-pad { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 150px; margin-left: auto; margin-right: auto; }
        .arrow { background: #21262d; border: 1px solid #30363d; border-radius: 10px; padding: 12px; font-size: 18px; color: #3fb950; cursor: pointer; user-select: none; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة</a>
        <a href="/" class="header-brand-center"><span class="neon-text-style">Albrawe</span></a>
    </div>
    <div class="main-container">
        <div class="game-card">
            <div class="stats-bar">
                <span id="scoreDisplay">النقاط: 0</span>
                <span id="levelDisplay" style="color: #ffd700;">المرحلة: 1 / 10 👑</span>
            </div>
            <canvas id="snakeCanvas" width="300" height="200"></canvas>
            
            <div class="ctrl-pad">
                <div></div><button class="arrow" onclick="changeDir('UP')">▲</button><div></div>
                <button class="arrow" onclick="changeDir('LEFT')">◀</button>
                <button class="arrow" onclick="togglePause()"><i class="fas fa-pause"></i></button>
                <button class="arrow" onclick="changeDir('RIGHT')">▶</button>
                <div></div><button class="arrow" onclick="changeDir('DOWN')">▼</button><div></div>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('snakeCanvas'), ctx = canvas.getContext('2d');
        const box = 10; let snake = [], food = {}, score = 0, level = 1, d = 'RIGHT', interval = null, isPaused = false;
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playBeep(f) { const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination); o.frequency.value = f; g.gain.setValueAtTime(0.03, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.05); }

        function init() {
            snake = [{x: 50, y: 50}]; score = 0; d = 'RIGHT'; isPaused = false; spawnFood();
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            document.getElementById('levelDisplay').innerText = `المرحلة: ${level} / 10 👑`;
            if(interval) clearInterval(interval);
            // تسريع ميكانيكي وحساب التحدي بناءً على الـ 10 مراحل تصاعدياً
            interval = setInterval(draw, Math.max(40, 120 - (level * 8)));
        }
        function spawnFood() { food = { x: Math.floor(Math.random()*30)*box, y: Math.floor(Math.random()*20)*box }; }
        function changeDir(dir) { if(dir==='LEFT' && d!=='RIGHT') d='LEFT'; if(dir==='UP' && d!=='DOWN') d='UP'; if(dir==='RIGHT' && d!=='LEFT') d='RIGHT'; if(dir==='DOWN' && d!=='UP') d='DOWN'; }
        function togglePause() { isPaused = !isPaused; }

        function draw() {
            if(isPaused) return;
            ctx.fillStyle = '#0d1117'; ctx.fillRect(0,0,300,200);
            ctx.fillStyle = '#f85149'; ctx.fillRect(food.x, food.y, box, box);
            
            for(let i=0; i<snake.length; i++) { ctx.fillStyle = i===0?'#58a6ff':'#3fb950'; ctx.fillRect(snake[i].x, snake[i].y, box, box); }
            
            let hX = snake[0].x, hY = snake[0].y;
            if(d==='LEFT') hX -= box; if(d==='UP') hY -= box; if(d==='RIGHT') hX += box; if(d==='DOWN') hY += box;
            
            if(hX === food.x && hY === food.y) {
                score += 10; playBeep(600); spawnFood();
                document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
                // شرط الترقية للمرحلة التالية عند بلوغ 50 نقطة في كل شوط
                if(score >= 50 && level < 10) { level++; alert(`تهانينا! صعدت للمرحلة ${level} 🚀`); init(); return; }
            } else { snake.pop(); }
            
            let nH = {x: hX, y: hY};
            if(hX<0 || hX>=300 || hY<0 || hY>=200 || snake.some(s=>s.x===hX && s.y===hY)) { playBeep(150); alert('انتهت اللعبة! 💀'); level=1; init(); return; }
            snake.unshift(nH);
        }
        init();
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_page(): return render_template_string(SNAKE_HTML)
