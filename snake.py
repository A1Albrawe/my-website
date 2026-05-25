from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>لعبة ثعبان نوكيا الشاملة - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #1a1a1a;
            color: #000; 
            padding: 10px; 
            margin: 0; 
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
            overscroll-behavior-y: contain;
        }
        .back-btn { 
            background: #111; 
            color: #8c9f21; 
            border: 2px solid #8c9f21; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            font-weight: bold; 
            display: inline-flex; 
            align-items: center;
            gap: 8px;
            margin-bottom: 15px; 
            font-size: 14px;
        }
        
        .nokia-phone {
            background: #3a4d5c;
            border: 6px solid #25333d;
            border-radius: 30px;
            width: 100%;
            max-width: 420px;
            padding: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            box-sizing: border-box;
            transition: all 0.3s ease;
        }

        .nokia-screen {
            background-color: #8c9f21;
            border: 10px solid #111;
            border-radius: 8px;
            padding: 12px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
            position: relative;
            box-sizing: border-box;
            touch-action: none;
        }

        .score-container {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 15px;
            border-bottom: 2px solid #000;
            padding-bottom: 5px;
            margin-bottom: 8px;
        }

        .canvas-container {
            width: 100%;
            overflow: hidden;
            display: flex;
            justify-content: center;
        }

        canvas { 
            background-color: #8c9f21; 
            display: block; 
            max-width: 100%;
            height: auto;
        }

        .nokia-keypad {
            margin-top: 15px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding: 0 10px;
        }
        .key-btn {
            background: #cbd3d8;
            border: 2px solid #a1aab0;
            border-radius: 15px;
            height: 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 3px #78838a, inset 0 1px rgba(255,255,255,0.5);
            color: #333;
            font-size: 16px;
            user-select: none;
            -webkit-user-select: none;
        }
        .key-btn:active {
            box-shadow: 0 1px #78838a;
            transform: translateY(2px);
        }
        .key-btn span { font-size: 9px; color: #666; font-family: sans-serif; }

        .leaderboard {
            margin-top: 12px;
            background: rgba(0, 0, 0, 0.06);
            padding: 8px;
            border-radius: 4px;
            font-size: 13px;
            text-align: right;
            border-top: 1px dashed #000;
        }
        .leaderboard h4 { margin: 0 0 6px 0; text-align: center; font-size: 14px; }
        .score-row { display: flex; justify-content: space-between; padding: 2px 0; font-weight: bold; }

        .game-over-overlay {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #8c9f21;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
            border-radius: 4px;
            padding: 10px;
            box-sizing: border-box;
        }
        .input-name {
            padding: 6px; font-size: 14px; border: 2px solid #000; background: #8c9f21;
            margin-bottom: 8px; text-align: center; width: 80%; font-family: inherit; font-weight: bold;
            box-sizing: border-box;
        }
        .restart-btn {
            background: #000; color: #8c9f21; border: none; padding: 8px 20px;
            font-size: 14px; font-weight: bold; cursor: pointer; font-family: inherit;
            border-radius: 3px;
        }

        @media (max-width: 480px) {
            body { padding: 5px; }
            .nokia-phone {
                background: transparent;
                border: none;
                box-shadow: none;
                padding: 5px;
            }
            .nokia-screen {
                border-width: 6px;
                padding: 8px;
            }
            .key-btn {
                height: 55px;
                background: #e0e5e8;
            }
        }
    </style>
</head>
<body>
    <br>
    <a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> القائمة الرئيسية</a>

    <div class="nokia-phone">
        <div class="nokia-screen" id="touchArea">
            <div class="score-container">
                <span id="snakeScore">النقاط: 0</span>
                <span>NOKIA</span>
            </div>
            
            <div class="canvas-container">
                <canvas id="snakeCanvas" width="300" height="200"></canvas>
            </div>
            
            <div id="gameOverScreen" class="game-over-overlay">
                <h3 style="margin: 0 0 5px 0;">حاول مرة أخرى</h3>
                <p id="finalScoreText" style="margin: 0 0 8px 0; font-weight: bold; font-size:14px;"></p>
                <input type="text" id="playerName" class="input-name" placeholder="اكتب اسمك هنا" maxlength="10">
                <button class="restart-btn" onclick="resetGame()">إعادة تشغيل</button>
            </div>

            <div class="leaderboard">
                <h4>🏆 أفضل النتائج المسجلة</h4>
                <div id="leaderboardContent"></div>
            </div>
        </div>

        <div class="nokia-keypad">
            <div class="key-btn">1 <span>.,-</span></div>
            <div class="key-btn" onclick="changeDirection('UP')">2 <span>▲ فوق</span></div>
            <div class="key-btn">3 <span>def</span></div>
            <div class="key-btn" onclick="changeDirection('LEFT')">4 <span>◀ يسار</span></div>
            <div class="key-btn">5 <span>jkl</span></div>
            <div class="key-btn" onclick="changeDirection('RIGHT')">6 <span>يمين ▶</span></div>
            <div class="key-btn">7 <span>pqrs</span></div>
            <div class="key-btn" onclick="changeDirection('DOWN')">8 <span>▼ تحت</span></div>
            <div class="key-btn">9 <span>wxyz</span></div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('snakeCanvas');
        const ctx = canvas.getContext('2d');
        const box = 10;
        
        let score, snake, food, d, gameInterval;
        let isGameOver = false;

        function initGame() {
            score = 0;
            isGameOver = false;
            document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('gameOverScreen').style.display = 'none';
            
            // تهيئة السلسلة الحركية للثعبان من 3 بكسلات متتالية بشكل صحيح
            snake = [
                {x: 10 * box, y: 10 * box},
                {x: 9 * box, y: 10 * box},
                {x: 8 * box, y: 10 * box}
            ];
            generateFood();
            d = "RIGHT";
            
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(draw, 110);
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * 30) * box,
                y: Math.floor(Math.random() * 20) * box
            };
            for(let cell of snake) {
                if(cell.x === food.x && cell.y === food.y) generateFood();
            }
        }

        // تم إصلاح التداخل البرمجي هنا لضمان قراءة الأزرار (WASD، الأسهم، والآلة الحاسبة الجانبية) بشكل صحيح 100%
        document.onkeydown = function(e) {
            if(isGameOver) return;
            
            const key = e.keyCode;
            const keyChar = e.key ? e.key.toLowerCase() : "";

            if ((key === 37 || keyChar === 'a' || key === 100 || key === 52) && d !== "RIGHT") d = "LEFT";
            else if ((key === 38 || keyChar === 'w' || key === 104 || key === 56) && d !== "DOWN") d = "UP";
            else if ((key === 39 || keyChar === 'd' || key === 102 || key === 54) && d !== "LEFT") d = "RIGHT";
            else if ((key === 40 || keyChar === 's' || key === 98 || key === 50) && d !== "UP") d = "DOWN";
        };

        function changeDirection(dir) {
            if(isGameOver) return;
            if(dir === "LEFT" && d !== "RIGHT") d = "LEFT";
            if(dir === "UP" && d !== "DOWN") d = "UP";
            if(dir === "RIGHT" && d !== "LEFT") d = "RIGHT";
            if(dir === "DOWN" && d !== "UP") d = "DOWN";
        }

        // محرك اللمس السحابي (Swipe Gestures) للهواتف الذكية
        const touchArea = document.getElementById('touchArea');
        let touchStartX = 0, touchStartY = 0, touchEndX = 0, touchEndY = 0;

        touchArea.addEventListener('touchstart', function(event) {
            touchStartX = event.changedTouches[0].screenX;
            touchStartY = event.changedTouches[0].screenY;
        }, {passive: true});

        touchArea.addEventListener('touchend', function(event) {
            touchEndX = event.changedTouches[0].screenX;
            touchEndY = event.changedTouches[0].screenY;
            handleSwipe();
        }, {passive: true});

        function handleSwipe() {
            const xDiff = touchEndX - touchStartX;
            const yDiff = touchEndY - touchStartY;
            if (Math.abs(xDiff) > Math.abs(yDiff)) {
                if (Math.abs(xDiff) > 30) {
                    if (xDiff > 0) { changeDirection('RIGHT'); } else { changeDirection('LEFT'); }
                }
            } else {
                if (Math.abs(yDiff) > 30) {
                    if (yDiff > 0) { changeDirection('DOWN'); } else { changeDirection('UP'); }
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, 300, 200);
            
            // رسم نقطة الطعام
            ctx.fillStyle = "#000";
            ctx.fillRect(food.x + 1, food.y + 1, box - 2, box - 2);

            // إصلاح محاذاة رسم بكسلات الأفعى بالاعتماد على مصفوفة الجسم المحدثة
            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = "#000";
                ctx.fillRect(snake[i].x + 1, snake[i].y + 1, box - 2, box - 2);
                if(i === 0) {
                    ctx.fillStyle = "#8c9f21";
                    ctx.fillRect(snake[i].x + 3, snake[i].y + 3, 2, 2);
                }
            }

            // تم إصلاح تحديد موقع الرأس (snake[0].x) لمنع اختفاء الأفعى نهائياً
            let snakeX = snake[0].x;
            let snakeY = snake[0].y;
            
            if(d === "LEFT") snakeX -= box;
            if(d === "UP") snakeY -= box;
            if(d === "RIGHT") snakeX += box;
            if(d === "DOWN") snakeY += box;

            let newHead = {x: snakeX, y: snakeY};
            
            if(snakeX < 0 || snakeX >= 300 || snakeY < 0 || snakeY >= 200 || collision(newHead, snake)) {
                endGame();
                return;
            }

            if(snakeX === food.x && snakeY === food.y) {
                score += 10;
                document.getElementById('snakeScore').innerText = "النقاط: " + score;
                generateFood();
            } else {
                snake.pop();
            }
            snake.unshift(newHead);
        }

        function collision(head, array) {
            for(let i = 0; i < array.length; i++) { if(head.x === array[i].x && head.y === array[i].y) return true; }
            return false;
        }

        function endGame() {
            clearInterval(gameInterval);
            isGameOver = true;
            document.getElementById('finalScoreText').innerText = "النقاط الحالية: " + score;
            document.getElementById('gameOverScreen').style.display = 'flex';
        }

        function resetGame() {
            let nameInput = document.getElementById('playerName').value.trim();
            let finalName = nameInput ? nameInput : "لاعب نوكيا";
            saveScore(finalName, score);
            document.getElementById('playerName').value = "";
            initGame();
        }

        function saveScore(name, score) {
            let scores = JSON.parse(localStorage.getItem('responsive_nokia_scores')) || [];
            scores.push({name: name, score: score});
            scores.sort((a, b) => b.score - a.score);
            scores = scores.slice(0, 3);
            localStorage.setItem('responsive_nokia_scores', JSON.stringify(scores));
            loadLeaderboard();
        }

        function loadLeaderboard() {
            let scores = JSON.parse(localStorage.getItem('responsive_nokia_scores')) || [{name: "المرتبة 1", score: 0}, {name: "المرتبة 2", score: 0}, {name: "المرتبة 3", score: 0}];
            let content = "";
            scores.forEach((item, index) => { content += `<div class="score-row"><span>${index + 1}. ${item.name}</span><span>${item.score}</span></div>`; });
            document.getElementById('leaderboardContent').innerHTML = content;
        }

        loadLeaderboard();
        initGame();
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE)
