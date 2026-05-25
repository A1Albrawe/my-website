from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة الثعبان الملوكية - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background: linear-gradient(135deg, #111 0%, #1e1e24 100%);
            color: white; 
            padding: 20px; 
            margin: 0; 
        }
        .back-btn { 
            background: #1877f2; 
            color: white; 
            border: none; 
            padding: 12px 25px; 
            border-radius: 30px; 
            cursor: pointer; 
            text-decoration: none; 
            font-weight: bold; 
            display: inline-flex; 
            align-items: center;
            gap: 8px;
            margin-bottom: 20px; 
            box-shadow: 0 4px 15px rgba(24, 119, 242, 0.4);
            transition: 0.2s;
        }
        .back-btn:hover { transform: scale(1.05); background: #1565c0; }
        
        .game-layout {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 30px;
            max-width: 800px;
            margin: 0 auto;
            flex-wrap: wrap;
        }

        .canvas-area { position: relative; }
        
        canvas { 
            border: 5px solid #1877f2; 
            background-color: #0d0d11; 
            display: block; 
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.7); 
        }

        /* لوحة الصدارة المحسنة */
        .leaderboard {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 250px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .leaderboard h3 { color: #34b7f1; margin-top: 0; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .score-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 5px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 18px;
        }
        .rank-1 { color: #ffd700; font-weight: bold; }
        .rank-2 { color: #c0c0c0; font-weight: bold; }
        .rank-3 { color: #cd7f32; font-weight: bold; }

        .score-board { font-size: 26px; font-weight: bold; color: #34b7f1; margin-bottom: 15px; }

        /* شاشة انتهاء اللعبة */
        .game-over-overlay {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            border-radius: 12px;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
        }
        .game-over-overlay h2 { color: #ff4d4d; font-size: 32px; margin-bottom: 10px; }
        .input-name {
            padding: 10px; font-size: 16px; border-radius: 5px; border: none; 
            margin-bottom: 15px; text-align: center; width: 200px;
        }
        .restart-btn {
            background: #4caf50; color: white; border: none; padding: 12px 30px;
            font-size: 18px; font-weight: bold; border-radius: 25px; cursor: pointer;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4); transition: 0.2s;
        }
        .restart-btn:hover { background: #43a047; transform: scale(1.05); }
    </style>
</head>
<body>
    <br>
    <a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> العودة للرئيسية</a>
    <div id="snakeScore" class="score-board">النقاط الحالية: 0</div>

    <div class="game-layout">
        <div class="canvas-area">
            <canvas id="snakeCanvas" width="400" height="400"></canvas>
            <div id="gameOverScreen" class="game-over-overlay">
                <h2>انتهت اللعبة! 💀</h2>
                <p id="finalScoreText" style="font-size:20px; margin-top:0;"></p>
                <input type="text" id="playerName" class="input-name" placeholder="اكتب اسمك لتسجيل النتيجة" maxlength="12">
                <button class="restart-btn" onclick="resetGame()"><i class="fas fa-redo"></i> العب مجدداً</button>
            </div>
        </div>

        <div class="leaderboard">
            <h3><i class="fas fa-trophy"></i> لوحة الصدارة</h3>
            <div id="leaderboardContent"></div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('snakeCanvas');
        const ctx = canvas.getContext('2d');
        const box = 20;
        
        let score, snake, food, d, gameInterval;
        let isGameOver = false;

        function initGame() {
            score = 0;
            isGameOver = false;
            document.getElementById('snakeScore').innerText = "النقاط الحالية: " + score;
            document.getElementById('gameOverScreen').style.display = 'none';
            snake = [{x: 10 * box, y: 10 * box}];
            generateFood();
            d = "RIGHT";
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(draw, 100);
        }

        function generateFood() {
            food = { x: Math.floor(Math.random() * 20) * box, y: Math.floor(Math.random() * 20) * box };
            for(let cell of snake) { if(cell.x === food.x && cell.y === food.y) generateFood(); }
        }

        document.onkeydown = function(e) {
            if(isGameOver) return;
            if(e.keyCode == 37 && d != "RIGHT") d = "LEFT";
            else if(e.keyCode == 38 && d != "DOWN") d = "UP";
            else if(e.keyCode == 39 && d != "LEFT") d = "RIGHT";
            else if(e.keyCode == 40 && d != "UP") d = "DOWN";
        };

        function draw() {
            ctx.fillStyle = '#0d0d11'; ctx.fillRect(0, 0, 400, 400);
            ctx.shadowBlur = 15; ctx.shadowColor = "#ff4d4d"; ctx.fillStyle = "#ff4d4d";
            ctx.beginPath(); ctx.arc(food.x + box/2, food.y + box/2, box/2 - 2, 0, 2 * Math.PI); ctx.fill();
            ctx.shadowBlur = 0;

            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i === 0) ? "#1877f2" : `rgba(52, 183, 241, ${1 - (i / snake.length) * 0.6})`;
                ctx.beginPath(); ctx.roundRect(snake[i].x + 1, snake[i].y + 1, box - 2, box - 2, 5); ctx.fill();
            }

            let snakeX = snake.x, snakeY = snake.y;
            if(d == "LEFT") snakeX -= box; if(d == "UP") snakeY -= box; if(d == "RIGHT") snakeX += box; if(d == "DOWN") snakeY += box;

            let newHead = {x: snakeX, y: snakeY};
            if(snakeX < 0 || snakeX >= 400 || snakeY < 0 || snakeY >= 400 || collision(newHead, snake)) { endGame(); return; }

            if(snakeX == food.x && snakeY == food.y) { score += 10; document.getElementById('snakeScore').innerText = "النقاط الحالية: " + score; generateFood(); }
            else { snake.pop(); }
            snake.unshift(newHead);
        }

        function collision(head, array) { for(let i = 0; i < array.length; i++) { if(head.x == array[i].x && head.y == array[i].y) return true; } return false; }
        
        function endGame() { clearInterval(gameInterval); isGameOver = true; document.getElementById('finalScoreText').innerText = "مجموع نقاطك المحققة: " + score; document.getElementById('gameOverScreen').style.display = 'flex'; }
        
        function resetGame() {
            let nameInput = document.getElementById('playerName').value.trim();
            let finalName = nameInput ? nameInput : "لاعب مجهول";
            saveScore(finalName, score);
            document.getElementById('playerName').value = "";
            initGame();
        }

        function saveScore(name, score) {
            let scores = JSON.parse(localStorage.getItem('snake_scores')) || [];
            scores.push({name: name, score: score});
            scores.sort((a, b) => b.score - a.score);
            scores = scores.slice(0, 3);
            localStorage.setItem('snake_scores', JSON.stringify(scores));
            loadLeaderboard();
        }

        function loadLeaderboard() {
            let scores = JSON.parse(localStorage.getItem('snake_scores')) || [{name: "البطل الأول", score: 0}, {name: "المنافس الثاني", score: 0}, {name: "المتحدي الثالث", score: 0}];
            let content = "";
            scores.forEach((item, index) => { content += `<div class="score-row rank-${index + 1}"><span>${index + 1}. ${item.name}</span><span>${item.score} نقطة</span></div>`; });
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
