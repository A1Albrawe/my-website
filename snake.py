from flask import Blueprint, render_template_string

snake_blueprint = Blueprint('snake', __name__)

SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Snake</title>
    <style>
        body { font-family: monospace; text-align: center; background: #121212; padding: 10px; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; box-sizing: border-box; }
        .back-btn { background: #111; color: #8c9f21; border: 2px solid #8c9f21; padding: 8px 16px; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold; margin-bottom: 15px; font-size: 13px; }
        .nokia-phone { background: #3a4d5c; border: 8px solid #25333d; border-radius: 40px; width: 100%; max-width: 370px; padding: 25px 20px; box-shadow: 0 20px 45px rgba(0,0,0,0.8); box-sizing: border-box; }
        .nokia-screen { background-color: #8c9f21; border: 12px solid #111; border-radius: 10px; padding: 10px; position: relative; box-sizing: border-box; }
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 2px solid #000; padding-bottom: 4px; margin-bottom: 6px; }
        canvas { background-color: transparent; display: block; max-width: 100%; height: auto; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #000; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(140, 159, 33, 0.95); padding: 8px 12px; border: 2px solid #000; text-align: center; width: 85%; box-sizing: border-box; }
        .nokia-dpad { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 170px; height: 170px; margin: auto; }
        .arrow-btn { background: #cbd3d8; border: 2px solid #a1aab0; border-radius: 15px; display: flex; justify-content: center; align-items: center; font-size: 22px; color: #222; cursor: pointer; box-shadow: 0 4px #78838a; user-select: none; }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">القائمة الرئيسية</a>
    <div class="nokia-phone">
        <div class="nokia-screen">
            <div class="score-container"><span id="snakeScore">النقاط: 0</span><span>NOKIA</span></div>
            <canvas id="snakeCanvas" width="240" height="160"></canvas>
            <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                <h4 style="margin:0 0 5px 0;">مرحباً بك</h4>
                <button style="background:#000; color:#8c9f21; border:none; padding:6px 15px; font-weight:bold; cursor:pointer;" onclick="startGame()">بدء اللعب</button>
            </div>
        </div>
        <div class="nokia-dpad">
            <div></div><div class="arrow-btn" onclick="changeDir('UP')">▲</div><div></div>
            <div class="arrow-btn" onclick="changeDir('LEFT')">◀</div><div></div><div class="arrow-btn" onclick="changeDir('RIGHT')">▶</div>
            <div></div><div class="arrow-btn" onclick="changeDir('DOWN')">▼</div><div></div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('snakeCanvas'), ctx = canvas.getContext('2d'), box = 10;
        let score=0, snake=[], food={}, d="RIGHT", interval=null, isGameOver=true;

        function startGame() {
            if(interval) clearInterval(interval);
            score=0; isGameOver=false; d="RIGHT";
            document.getElementById('snakeScore').innerText = "النقاط: " + score;
            document.getElementById('gameOverScreen').style.display = 'none';
            snake = [{x:100, y:80}, {x:90, y:80}, {x:80, y:80}];
            genFood();
            interval = setInterval(draw, 120);
        }
        function genFood() { food = { x: Math.floor(Math.random()*24)*box, y: Math.floor(Math.random()*16)*box }; }
        function changeDir(dir) { if(dir==="LEFT"&&d!=="RIGHT")d="LEFT"; if(dir==="UP"&&d!=="DOWN")d="UP"; if(dir==="RIGHT"&&d!=="LEFT")d="RIGHT"; if(dir==="DOWN"&&d!=="UP")d="DOWN"; }
        
        document.onkeydown = function(e) { 
            if(e.keyCode===37) changeDir('LEFT'); if(e.keyCode===38) changeDir('UP'); if(e.keyCode===39) changeDir('RIGHT'); if(e.keyCode===40) changeDir('DOWN'); 
        };

        function draw() {
            if(isGameOver) return;
            ctx.clearRect(0, 0, 240, 160);
            ctx.fillStyle = "#000"; ctx.fillRect(food.x, food.y, box, box);
            
            snake.forEach((c, i) => { ctx.fillStyle = "#000"; ctx.fillRect(c.x, c.y, box, box); });
            
            let hX = snake[0].x, hY = snake[0].y;
            if(d==="LEFT") hX -= box; if(d==="UP") hY -= box; if(d==="RIGHT") hX += box; if(d==="DOWN") hY += box;
            let nH = {x:hX, y:hY};

            if(hX<0 || hX>=240 || hY<0 || hY>=160 || snake.some(c=>c.x===nH.x && c.y===nH.y)) {
                clearInterval(interval); isGameOver=true;
                document.getElementById('gameOverScreen').style.display = 'block';
                return;
            }
            if(hX===food.x && hY===food.y) { score+=10; document.getElementById('snakeScore').innerText = "النقاط: "+score; genFood(); }
            else { snake.pop(); }
            snake.unshift(nH);
        }
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE)
