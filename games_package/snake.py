from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Snake - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #080c10; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #3fb950; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #3fb950; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #3fb950, 0 0 10px #3fb950; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #3fb950; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .snake-phone { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #3fb950; border-radius: 20px; width: 100%; max-width: 350px; padding: 20px 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 12px; color: #3fb950; align-items: center; }
        .speed-badge { color: #ffd700; font-weight: bold; font-size: 12px; }
        
        .game-area { position: relative; width: 100%; display: flex; justify-content: center; }
        canvas { background-color: #0b0e14; display: block; border: 2px solid #30363d; border-radius: 8px; box-shadow: 0 0 20px rgba(63, 185, 80, 0.15); }
        
        .overlay-txt { display: none; position: absolute; font-size: 20px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(13, 17, 23, 0.96); border: 2px solid #3fb950; padding: 20px; border-radius: 12px; text-align: center; width: 85%; box-shadow: 0 0 25px #3fb950; box-sizing: border-box; z-index: 5; }
        
        .control-pad { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 240px; margin-left: auto; margin-right: auto; }
        .ctrl-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; padding: 15px; font-size: 20px; color: #3fb950; cursor: pointer; user-select: none; -webkit-user-select: none; font-weight: bold; box-shadow: 0 4px #0d1117; transition: 0.1s; touch-action: none; }
        .ctrl-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
        
        .pause-action-btn { grid-column: span 3; background: #21262d; border: 1px solid #f85149; color: #f85149; font-size: 14px; font-weight: bold; border-radius: 8px; padding: 10px; cursor: pointer; box-shadow: 0 3px #0d1117; display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 5px; font-family: inherit; user-select: none; -webkit-user-select: none; touch-action: none; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#3fb950;">🐍 ثعبان النيون</span>
    </div>

    <div class="main-container">
        <div class="snake-phone">
            <div class="score-container">
                <span id="snakeScore">النقاط: 0</span>
                <span id="snakeSpeed" class="speed-badge">السرعة: 1.0x ⚡</span>
                <span>SNAKE</span>
            </div>
            <div class="game-area">
                <canvas id="snakeCanvas" width="240" height="300"></canvas>
                <div id="pauseOverlay" class="overlay-txt"><i class="fas fa-pause-circle"></i> اللعبة مؤقوتة ⏸️</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0; color:#3fb950;">محرك الثعبان المطور</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:8px 20px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="initGame()">بدء الزحف الفوري 🎮</button>
                </div>
            </div>
            
            <div class="control-pad">
                <div></div>
                <button class="ctrl-btn" ontouchstart="handleSnakeTouch(event, 'UP')" onmousedown="changeDirection('UP')">▲</button>
                <div></div>
                
                <button class="ctrl-btn" ontouchstart="handleSnakeTouch(event, 'LEFT')" onmousedown="changeDirection('LEFT')">◀</button>
                <button class="ctrl-btn" ontouchstart="handleSnakeTouch(event, 'DOWN')" onmousedown="changeDirection('DOWN')">▼</button>
                <button class="ctrl-btn" ontouchstart="handleSnakeTouch(event, 'RIGHT')" onmousedown="changeDirection('RIGHT')">▶</button>
                
                <button class="pause-action-btn" ontouchstart="handleSnakeTouch(event, 'PAUSE')" onmousedown="togglePause()"><i class="fas fa-pause"></i> إيقاف مؤقت / استئناف القتال</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('snakeCanvas'), ctx = canvas.getContext('2d');
        const box = 15;
        let snake = [], food = {}, score = 0, currentSpeed = 150, d = "RIGHT", nextD = "RIGHT", gameInterval = null;
        let isGameOver = true, isPaused = false;

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function handleSnakeTouch(e, action) {
            e.preventDefault();
            if(action === 'PAUSE') togglePause();
            else changeDirection(action);
        }

        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            if (type === 'eat') { o.type = 'sine'; o.frequency.setValueAtTime(523.25, audioCtx.currentTime); g.gain.setValueAtTime(0.03, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.05); }
            else if (type === 'lose') { o.type = 'sawtooth'; o.frequency.setValueAtTime(150, audioCtx.currentTime); o.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.4); g.gain.setValueAtTime(0.12, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.4); }
        }

        function changeDirection(dir) {
            if (isGameOver || isPaused) return;
            if (dir === "LEFT" && d !== "RIGHT") nextD = "LEFT";
            else if (dir === "UP" && d !== "DOWN") nextD = "UP";
            else if (dir === "RIGHT" && d !== "LEFT") nextD = "RIGHT";
            else if (dir === "DOWN" && d !== "UP") nextD = "DOWN";
        }

        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowLeft') changeDirection('LEFT');
            if (e.key === 'ArrowUp') changeDirection('UP');
            if (e.key === 'ArrowRight') changeDirection('RIGHT');
            if (e.key === 'ArrowDown') changeDirection('DOWN');
        });
        function spawnFood() {
            food = {
                x: Math.floor(Math.random() * (canvas.width / box)) * box,
                y: Math.floor(Math.random() * (canvas.height / box)) * box
            };
            for(let i=0; i<snake.length; i++) {
                if(snake[i].x === food.x && snake[i].y === food.y) spawnFood();
            }
        }

        // ✅ تم الإصلاح الجوهري: حقن المكونات البنائية القياسية بداخل المصفوفة المربعة القياسية [ ] لمنع كسر خادم بايثون
        function initGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            score = 0; currentSpeed = 150; d = "RIGHT"; nextD = "RIGHT"; isGameOver = false; isPaused = false;
            document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('snakeSpeed').innerText = "السرعة: 1.0x ⚡";
            
            snake = [];
            snake[0] = { x: 4 * box, y: 10 * box };
            snake[1] = { x: 3 * box, y: 10 * box };
            snake[2] = { x: 2 * box, y: 10 * box };
            
            spawnFood();
            runEngineInterval();
        }

        function runEngineInterval() {
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(drawLoop, currentSpeed);
        }

        function drawLoop() {
            if(isPaused || isGameOver) return;
            ctx.fillStyle = '#0b0e14'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            d = nextD; 
            
            for (let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i === 0) ? "#2ea44f" : "#3fb950";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeStyle = "#0b0e14"; ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }
            
            ctx.fillStyle = "#f85149"; ctx.fillRect(food.x, food.y, box, box);
            
            let snakeX = snake[0].x, snakeY = snake[0].y;
            if (d === "LEFT") snakeX -= box;
            if (d === "UP") snakeY -= box;
            if (d === "RIGHT") snakeX += box;
            if (d === "DOWN") snakeY += box;
            
            if (snakeX === food.x && snakeY === food.y) {
                score += 10; playSound('eat'); spawnFood();
                document.getElementById('snakeScore').innerText = "النقاط: " + score;
                
                currentSpeed = Math.max(60, 150 - (score * 0.8));
                let speedFactor = (150 / currentSpeed).toFixed(1);
                document.getElementById('snakeSpeed').innerText = "السرعة: " + speedFactor + "x ⚡";
                runEngineInterval();
            } else {
                snake.pop();
            }
            
            let newHead = { x: snakeX, y: snakeY };
            
            if (snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || collision(newHead, snake)) {
                endGame(); return;
            }
            
            snake.unshift(newHead);
        }

        function collision(head, array) { for (let i = 0; i < array.length; i++) { if (head.x === array[i].x && head.y === array[i].y) return true; } return false; }
        function togglePause() { if(isGameOver) return; isPaused = !isPaused; document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none'; }
        function endGame() { isGameOver = true; clearInterval(gameInterval); playSound('lose'); document.getElementById('goTitle').innerText = "انتهى الزحف! 💀"; document.getElementById('finalScoreText').innerText = "أحرزت: " + score + " نقطة تراكمية"; document.getElementById('gameOverScreen').style.display = 'block'; }
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_page():
    return render_template_string(SNAKE_TEMPLATE)
