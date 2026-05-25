from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة الثعبان - Albrawe</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #1a1a1a; color: white; padding: 20px; margin: 0; }
        .back-btn { background: #1877f2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 20px; }
        .score-board { font-size: 24px; font-weight: bold; color: #34b7f1; margin-bottom: 10px; }
        canvas { border: 4px solid #1877f2; background-color: #000; display: block; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">⬅️ العودة للرئيسية</a>
    <h2>لعبة الثعبان (الأسهم ⬆️ ⬇️ ⬅️ ➡️)</h2>
    <div id="snakeScore" class="score-board">النقاط: 0</div>
    <canvas id="snakeCanvas" width="400" height="400"></canvas>
    <script>
        const canvas = document.getElementById('snakeCanvas'); const ctx = canvas.getContext('2d');
        let score = 0, box = 20; let snake = [{x: 10 * box, y: 10 * box}];
        let food = {x: Math.floor(Math.random()*20)*box, y: Math.floor(Math.random()*20)*box}; let d = "RIGHT";
        document.onkeydown = function(e) {
            if(e.keyCode == 37 && d != "RIGHT") d = "LEFT";
            else if(e.keyCode == 38 && d != "DOWN") d = "UP";
            else if(e.keyCode == 39 && d != "LEFT") d = "RIGHT";
            else if(e.keyCode == 40 && d != "UP") d = "DOWN";
        };
        function draw() {
            ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 400, 400);
            for(let i=0; i<snake.length; i++) { ctx.fillStyle = (i == 0)? "#1877f2" : "#fff"; ctx.fillRect(snake[i].x, snake[i].y, box, box); }
            ctx.fillStyle = "#ff4d4d"; ctx.fillRect(food.x, food.y, box, box);
            let snakeX = snake[0].x, snakeY = snake[0].y;
            if(d == "LEFT") snakeX -= box; if(d == "UP") snakeY -= box; if(d == "RIGHT") snakeX += box; if(d == "DOWN") snakeY += box;
            if(snakeX == food.x && snakeY == food.y) { score += 10; document.getElementById('snakeScore').innerText = "النقاط: " + score; food = {x: Math.floor(Math.random()*20)*box, y: Math.floor(Math.random()*20)*box}; }
            else { snake.pop(); }
            let newHead = {x: snakeX, y: snakeY};
            if(snakeX < 0 || snakeX >= 400 || snakeY < 0 || snakeY >= 400 || collision(newHead, snake)) { alert("انتهت اللعبة! نقاطك: " + score); window.location.href = "/"; return; }
            snake.unshift(newHead);
        }
        function collision(head, array) { for(let i=0; i<array.length; i++) { if(head.x == array[i].x && head.y == array[i].y) return true; } return false; }
        setInterval(draw, 100);
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE)
