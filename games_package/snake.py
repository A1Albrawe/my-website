from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Snake Game - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #58a6ff; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .nokia-phone { background: #161b22; border: 3px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 20px; width: 100%; max-width: 370px; padding: 25px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .nokia-screen { background-color: #0d1117; border: 2px solid #30363d; border-radius: 10px; padding: 10px; position: relative; box-sizing: border-box; touch-action: none; }
        
        .score-container { display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 10px; color: #58a6ff; }
        .level-badge { color: #ffd700; font-weight: bold; }
        
        .canvas-container { width: 100%; display: flex; justify-content: center; position: relative; }
        canvas { background-color: #161b22; display: block; max-width: 100%; height: auto; border: 1px solid #30363d; border-radius: 4px; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #58a6ff; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        
        .nokia-dpad { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 160px; height: 160px; margin-left: auto; margin-right: auto; }
        .arrow-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; color: #58a6ff; cursor: pointer; box-shadow: 0 4px #0d1117; user-select: none; -webkit-user-select: none; }
        .arrow-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
        .dpad-empty { pointer-events: none; visibility: hidden; }
        .dpad-center-btn { background: #30363d; border: 1px solid #58a6ff; border-radius: 50%; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 14px; color: #fff; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#58a6ff;">🐍 لعبة الثعبان</span>
    </div>

    <div class="main-container">
        <div class="nokia-phone" id="phoneWrapper">
            <div class="nokia-screen" id="nokiaScreen">
                <div class="score-container">
                    <span id="snakeScore">النقاط: 0</span>
                    <span id="snakeLevel" class="level-badge">المرحلة: 1 / 10 👑</span>
                    <span>SNAKE</span>
                </div>
                
                <div class="canvas-container">
                    <canvas id="snakeCanvas" width="240" height="160"></canvas>
                    <div id="pauseOverlay" class="overlay-txt">مؤقت ⏸️</div>
                    
                    <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                        <h4 id="goTitle" style="margin:0 0 5px 0; color:#58a6ff;">مرحباً بك</h4>
                        <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                        <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:8px 20px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="initGame()">بدء اللعب الفوري 🎮</button>
                    </div>
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
        const canvas = document.getElementById('snakeCanvas');
        const ctx = canvas.getContext('2d');
        const box = 10;
        
        let snake = [];
        let food = {};
        let score = 0;
        let d = '';
        let gameLoopInterval;
        let isPaused = false;
        let gameActive = false;
        let currentLevel = 1;
        let baseSpeed = 120; 

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const baseNotes = [130.81, 146.83, 164.81, 196.00]; 

        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            
            if(type === 'eat') { osc.type='sine'; osc.frequency.setValueAtTime(523.25 + (score * 5), audioCtx.currentTime); gain.gain.setValueAtTime(0.04, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.05); }
            else if(type === 'levelUp') { osc.type='square'; osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(1174.66, audioCtx.currentTime + 0.25); gain.gain.setValueAtTime(0.06, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.25); }
            else if(type === 'lose') { osc.type='sawtooth'; osc.frequency.setValueAtTime(180, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(60, audioCtx.currentTime + 0.4); gain.gain.setValueAtTime(0.12, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        }

        function playStepMusic() {
            if(!gameActive || isPaused) return;
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.type = 'triangle';
            let currentNote = baseNotes[snake.length % baseNotes.length] + (currentLevel * 10);
            osc.frequency.setValueAtTime(currentNote, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.015, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.1);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.12);
        }

        function initGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            snake = [{x: 12 * box, y: 8 * box}];
            generateFood();
            score = 0;
            currentLevel = 1;
            d = 'RIGHT';
            isPaused = false;
            gameActive = true;
            document.getElementById('snakeScore').innerText = 'النقاط: ' + score;
            document.getElementById('snakeLevel').innerText = 'المرحلة: ' + currentLevel + ' / 10 👑';
            runEngineLoop();
        }

        function runEngineLoop() {
            if(gameLoopInterval) clearInterval(gameLoopInterval);
            let currentSpeed = baseSpeed - (currentLevel * 9);
            gameLoopInterval = setInterval(draw, currentSpeed);
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * (canvas.width / box)) * box,
                y: Math.floor(Math.random() * (canvas.height / box)) * box
            };
            for (let cell of snake) {
                if (cell.x === food.x && cell.y === food.y) generateFood();
            }
        }

        function changeDirection(dir) {
            if(!gameActive || isPaused) return;
            if(dir === 'LEFT' && d !== 'RIGHT') d = 'LEFT';
            if(dir === 'UP' && d !== 'DOWN') d = 'UP';
            if(dir === 'RIGHT' && d !== 'LEFT') d = 'RIGHT';
            if(dir === 'DOWN' && d !== 'UP') d = 'DOWN';
        }

        document.addEventListener('keydown', e => {
            if(e.key === 'ArrowLeft') changeDirection('LEFT');
            if(e.key === 'ArrowUp') changeDirection('UP');
            if(e.key === 'ArrowRight') changeDirection('RIGHT');
            if(e.key === 'ArrowDown') changeDirection('DOWN');
            if(e.code === 'Space') togglePause();
        });

        function togglePause() {
            if(!gameActive) return;
            isPaused = !isPaused;
            document.getElementById('pauseOverlay').style.display = isPaused ? 'block' : 'none';
        }

        function checkCollision(head, array) {
            for(let i = 0; i < array.length; i++) {
                if(head.x === array[i].x && head.y === array[i].y) return true;
            }
            return false;
        }

        function draw() {
            if(isPaused || !gameActive) return;
            
            if (Math.random() < 0.2) playStepMusic();

            ctx.fillStyle = '#161b22';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // رسم الثعبان
            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i === 0) ? '#58a6ff' : `hsl(${120 + (currentLevel * 10)}, 70%, 45%)`;
                ctx.strokeStyle = '#0d1117';
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }

            ctx.fillStyle = '#f85149';
            ctx.fillRect(food.x, food.y, box, box);

            // ✅ التعديل الهندسي الحاسم: سحب الإحداثيات من الخانة صفر للرأس مباشرة بدلاً من استدعاء المصفوفة ككل
            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if(d === 'LEFT') snakeX -= box;
            if(d === 'UP') snakeY -= box;
            if(d === 'RIGHT') snakeX += box;
            if(d === 'DOWN') snakeY += box;

            if(snakeX === food.x && snakeY === food.y) {
                score += 10;
                document.getElementById('snakeScore').innerText = 'النقاط: ' + score;
                playSound('eat');
                generateFood();
                
                if(score % 50 === 0 && currentLevel < 10) {
                    currentLevel++;
                    document.getElementById('snakeLevel').innerText = 'المرحلة: ' + currentLevel + ' / 10 👑';
                    playSound('levelUp');
                    runEngineLoop();
                }
            } else {
                snake.pop();
            }

            let newHead = { x: snakeX, y: snakeY };

            if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || checkCollision(newHead, snake)) {
                gameActive = false;
                clearInterval(gameLoopInterval);
                playSound('lose');
                handleGameOver();
                return;
            }

            snake.unshift(newHead);
        }

        function handleGameOver() {
            document.getElementById('goTitle').innerText = 'انتهت اللعبة! 💀';
            document.getElementById('finalScoreText').innerText = `أحرزت: ${score} نقطة في المرحلة ${currentLevel}`;
            document.getElementById('gameOverScreen').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_page():
    return render_template_string(SNAKE_TEMPLATE)
