from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة ثعبان نوكيا الكلاسيكية - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            background: #222;
            color: #000; 
            padding: 20px; 
            margin: 0; 
        }
        .back-btn { 
            background: #111; 
            color: #859a1d; 
            border: 2px solid #859a1d; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            font-weight: bold; 
            display: inline-flex; 
            align-items: center;
            gap: 8px;
            margin-bottom: 20px; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        
        /* هيكل هاتف نوكيا 3310 */
        .nokia-phone {
            background: #3a4d5c;
            border: 8px solid #25333d;
            border-radius: 40px;
            width: 430px;
            margin: 0 auto;
            padding: 30px 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.8);
            box-sizing: border-box;
        }

        /* شاشة النوكيا الفسفورية القديمة */
        .nokia-screen {
            background-color: #859a1d;
            border: 15px solid #111;
            border-radius: 10px;
            padding: 15px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
            position: relative;
        }

        .score-container {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 16px;
            border-bottom: 2px solid #000;
            padding-bottom: 5px;
            margin-bottom: 10px;
        }

        canvas { 
            background-color: #859a1d; 
            display: block; 
            margin: 0 auto; 
        }

        /* أزرار الهاتف الفعلية للتحكم */
        .nokia-keypad {
            margin-top: 25px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            padding: 0 30px;
        }
        .key-btn {
            background: #cbd3d8;
            border: 2px solid #a1aab0;
            border-radius: 50%;
            height: 60px;
            width: 60px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px #78838a, inset 0 2px rgba(255,255,255,0.5);
            color: #333;
        }
        .key-btn:active {
            box-shadow: 0 1px #78838a;
            transform: translateY(3px);
        }
        .key-btn span { font-size: 11px; color: #666; }

        /* لوحة الصدارة الكلاسيكية */
        .leaderboard {
            margin-top: 15px;
            background: rgba(0, 0, 0, 0.08);
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            text-align: right;
        }
        .leaderboard h4 { margin: 0 0 8px 0; text-align: center; border-bottom: 1px solid #000; padding-bottom: 3px; }
        .score-row { display: flex; justify-content: space-between; padding: 3px 0; }

        /* شاشة Game Over داخل النوكيا */
        .game-over-overlay {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #859a1d;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
            border-radius: 5px;
        }
        .input-name {
            padding: 5px; font-size: 14px; border: 2px solid #000; background: #859a1d;
            margin-bottom: 10px; text-align: center; width: 160px; font-family: inherit; font-weight: bold;
        }
        .restart-btn {
            background: #000; color: #859a1d; border: none; padding: 8px 20px;
            font-size: 14px; font-weight: bold; cursor: pointer; font-family: inherit;
        }
    </style>
</head>
<body>
    <br>
    <a href="/" class="back-btn"><i class="fas fa-arrow-right"></i> القائمة الرئيسية</a>

    <div class="nokia-phone">
        <div class="nokia-screen">
            <div class="score-container">
                <span id="snakeScore">النقاط: 0</span>
                <span>NOKIA</span>
            </div>
            
            <canvas id="snakeCanvas" width="360" height="240"></canvas>
            
            <div id="gameOverScreen" class="game-over-overlay">
                <h2 style="margin: 0 0 5px 0;">حاول مرة أخرى</h2>
                <p id="finalScoreText" style="margin: 0 0 10px 0; font-weight: bold;"></p>
                <input type="text" id="playerName" class="input-name" placeholder="اكتب اسمك هنا" maxlength="10">
                <button class="restart-btn" onclick="resetGame()">إعادة تشغيل</button>
            </div>

            <div class="leaderboard">
                <h4>🏆 لوحة أفضل النتائج</h4>
                <div id="leaderboardContent"></div>
            </div>
        </div>

        <!-- أزرار النوكيا الحقيقية للتحكم بالثعبان -->
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
        const box = 15; // حجم المربع الصغير البكسلي
        
        let score, snake, food, d, gameInterval;
        let isGameOver = false;

        function initGame() {
            score = 0;
            isGameOver = false;
            document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('gameOverScreen').style.display = 'none';
            
            // إصلاح الخطأ: مصفوفة إحداثيات رأس الأفعى والبدء من المنتصف
            snake = [
                {x: 12 * box, y: 8 * box},
                {x: 11 * box, y: 8 * box},
                {x: 10 * box, y: 8 * box}
            ];
            generateFood();
            d = "RIGHT";
            
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(draw, 120); // سرعة النوكيا الكلاسيكية الافتراضية
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * 24) * box,
                y: Math.floor(Math.random() * 16) * box
            };
            for(let cell of snake) {
                if(cell.x === food.x && cell.y === food.y) generateFood();
            }
        }

        // توجيه الأفعى عن طريق لوحة المفاتيح والأسهم
        document.onkeydown = function(e) {
            if(isGameOver) return;
            if(e.keyCode == 37 && d != "RIGHT") d = "LEFT";
            else if(e.keyCode == 38 && d != "DOWN") d = "UP";
            else if(e.keyCode == 39 && d != "LEFT") d = "RIGHT";
            else if(e.keyCode == 40 && d != "UP") d = "DOWN";
        };

        // توجيه الأفعى عن طريق أزرار هاتف نوكيا المدمجة على الشاشة
        function changeDirection(dir) {
            if(isGameOver) return;
            if(dir == "LEFT" && d != "RIGHT") d = "LEFT";
            if(dir == "UP" && d != "DOWN") d = "UP";
            if(dir == "RIGHT" && d != "LEFT") d = "RIGHT";
            if(dir == "DOWN" && d != "UP") d = "DOWN";
        }

        function draw() {
            ctx.clearRect(0, 0, 360, 240);

            // رسم طعام الأفعى (على شكل بكسل نوكيا مربع أسود تقليدي)
            ctx.fillStyle = "#000";
            ctx.fillRect(food.x + 1, food.y + 1, box - 2, box - 2);

            // رسم جسم الثعبان بكسل خلف بكسل بلون أسود داكن كلاسيكي
            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = "#000";
                ctx.fillRect(snake[i].x + 1, snake[i].y + 1, box - 2, box - 2);
                
                // ترك نقطة فارغة صغيرة داخل بكسل الرأس لتمثيل عين الأفعى التقليدية
                if(i === 0) {
                    ctx.fillStyle = "#859a1d";
                    ctx.fillRect(snake[i].x + 4, snake[i].y + 4, 3, 3);
                }
            }

            // تحديد إحداثيات موقع الرأس الجديد بدقة [0] بدلاً من الخطأ السابق
            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if(d == "LEFT") snakeX -= box;
            if(d == "UP") snakeY -= box;
            if(d == "RIGHT") snakeX += box;
            if(d == "DOWN") snakeY += box;

            let newHead = {x: snakeX, y: snakeY};

            // قوانين نوكيا الاصطدام بالحواف أو اصطدام الأفعى بنفسها يسبب الخسارة فوراً
            if(snakeX < 0 || snakeX >= 360 || snakeY < 0 || snakeY >= 240 || collision(newHead, snake)) {
                endGame();
                return;
            }

            if(snakeX == food.x && snakeY == food.y) {
                score += 10;
                document.getElementById('snakeScore').innerText = "النقاط: " + score;
                generateFood();
            } else {
                snake.pop();
            }

            snake.unshift(newHead);
        }

        function collision(head, array) {
            for(let i = 0; i < array.length; i++) {
                if(head.x == array[i].x && head.y == array[i].y) return true;
            }
            return false;
        }

        function endGame() {
            clearInterval(gameInterval);
            isGameOver = true;
            document.getElementById('finalScoreText').innerText = "النقاط المحققة: " + score;
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
            let scores = JSON.parse(localStorage.getItem('nokia_scores')) || [];
            scores.push({name: name, score: score});
            scores.sort((a, b) => b.score - a.score);
            scores = scores.slice(0, 3);
            localStorage.setItem('nokia_scores', JSON.stringify(scores));
            loadLeaderboard();
        }

        function loadLeaderboard() {
            let scores = JSON.parse(localStorage.getItem('nokia_scores')) || [
                {name: "المرتبة 1", score: 0},
                {name: "المرتبة 2", score: 0},
                {name: "المرتبة 3", score: 0}
            ];
            
            let content = "";
            scores.forEach((item, index) => {
                content += `
                    <div class="score-row">
                        <span>${index + 1}. ${item.name}</span>
                        <span>${item.score}</span>
                    </div>
                `;
            });
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
