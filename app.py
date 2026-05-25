from flask import Flask, render_template_string

app = Flask(__name__)

# 1. تصميم الصفحة الرئيسية (لوحة التحكم المركزية)
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع Albrawe - الرئيسية</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #f0f2f5; padding: 50px; margin: 0; }
        .menu-btn { position: fixed; top: 20px; right: 20px; font-size: 20px; background: #1877f2; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; z-index: 1000; font-weight: bold; display: flex; align-items: center; gap: 8px; }
        .sidebar { height: 100%; width: 0; position: fixed; z-index: 999; top: 0; right: 0; background-color: #1a1a1a; overflow-x: hidden; transition: 0.3s; padding-top: 80px; text-align: right; box-shadow: -4px 0 15px rgba(0,0,0,0.4); }
        .sidebar a, .sidebar .dropdown-btn { padding: 15px 25px; text-decoration: none; font-size: 18px; color: #b3b3b3; display: flex; align-items: center; gap: 12px; transition: 0.2s; border-bottom: 1px solid #2d2d2d; background: none; border-top: none; border-left: none; border-right: none; width: 100%; text-align: right; cursor: pointer; font-family: inherit; box-sizing: border-box; }
        .sidebar a:hover, .sidebar .dropdown-btn:hover { color: white; background-color: #1877f2; }
        .dropdown-container { display: none; background-color: #242424; padding-right: 20px; }
        .dropdown-container a { font-size: 16px; border-bottom: 1px solid #333; }
        .sidebar .close-btn { position: absolute; top: 20px; left: 20px; font-size: 28px; color: #bbb; cursor: pointer; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; max-width: 500px; margin-top: 60px; }
        h1 { color: #1877f2; margin-top: 0; }
        .telegram-btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; background-color: #0088cc; color: white; text-decoration: none; padding: 14px 30px; border-radius: 30px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 12px rgba(0, 136, 204, 0.3); transition: 0.3s; }
        .telegram-btn:hover { background-color: #0077b3; transform: translateY(-2px); }
        .footer { margin-top: 30px; color: #888; font-size: 14px; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
</head>
<body>
    <button class="menu-btn" onclick="toggleNav()"><i class="fas fa-bars"></i> القائمة</button>
    <div id="mySidebar" class="sidebar">
        <span class="close-btn" onclick="toggleNav()">&times;</span>
        <a href="/"><i class="fas fa-home"></i> الصفحة الرئيسية</a>
        <a href="#"><i class="fas fa-code"></i> المشاريع</a>
        <button class="dropdown-btn" onclick="toggleDropdown()"><i class="fas fa-link"></i> روابط أخرى <i class="fas fa-caret-down" style="margin-right: auto;"></i></button>
        <div id="gamesDropdown" class="dropdown-container">
            <a href="/snake"><i class="fas fa-gamepad"></i> لعبة الثعبان</a>
            <a href="/tetris"><i class="fas fa-cubes"></i> لعبة التترس</a>
        </div>
        <a href="#"><i class="fas fa-info-circle"></i> حول هذا</a>
    </div>
    <div class="container">
        <h1>مرحباً بك في موقع albrawe</h1>
        <p>تم تشغيل الموقع بنجاح وهو الآن متاح للجميع على الإنترنت!</p>
        <a href="https://t.me" target="_blank" class="telegram-btn"><i class="fab fa-telegram-plane"></i> تليجرام @a1albrawe</a>
        <div class="footer">يعمل بواسطة Python & Flask</div>
    </div>
    <script>
        let sidebarOpen = false;
        function toggleNav() { const sidebar = document.getElementById("mySidebar"); sidebar.style.width = sidebarOpen ? "0" : "250px"; sidebarOpen = !sidebarOpen; }
        function toggleDropdown() { const dropdown = document.getElementById("gamesDropdown"); dropdown.style.display = dropdown.style.display === "block" ? "none" : "block"; }
    </script>
</body>
</html>
"""
# 2. تصميم صفحة لعبة الثعبان (رابط منفرد)
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
        const canvas = document.getElementById('snakeCanvas');
        const ctx = canvas.getContext('2d');
        let score = 0, box = 20;
        let snake = [{x: 10 * box, y: 10 * box}];
        let food = {x: Math.floor(Math.random()*20)*box, y: Math.floor(Math.random()*20)*box};
        let d = "RIGHT";
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
# 3. تصميم صفحة لعبة التترس وتوجيه المسارات السحابية
TETRIS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة التترس - Albrawe</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #1a1a1a; color: white; padding: 20px; margin: 0; }
        .back-btn { background: #1877f2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 20px; }
        .score-board { font-size: 24px; font-weight: bold; color: #34b7f1; margin-bottom: 10px; }
        canvas { border: 4px solid #1877f2; background-color: #000; display: block; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">⬅️ العودة للرئيسية</a>
    <h2>لعبة التترس (⬇️ إسقاط، ⬆️ تدوير، ⬅️ ➡️ توجيه)</h2>
    <div id="tetrisScore" class="score-board">النقاط: 0</div>
    <canvas id="tetrisCanvas" width="240" height="400"></canvas>
    <script>
        const canvas = document.getElementById('tetrisCanvas'); const context = canvas.getContext('2d'); context.scale(20, 20);
        let score = 0; const arena = Array(20).fill().map(() => Array(12).fill(0));
        const pieces = [[[0,0,0],[1,1,1],[0,1,0]], [[2,2],[2,2]], [[0,3,3],[3,3,0]], [[4,4,0],[0,4,4]], [[0,5,0,0],[0,5,0,0],[0,5,0,0],[0,5,0,0]]];
        const player = { pos: {x: 4, y: 0}, matrix: pieces[Math.floor(Math.random() * pieces.length)] };
        function drawMatrix(matrix, offset, color = '#1877f2') { matrix.forEach((row, y) => { row.forEach((value, x) => { if (value !== 0) { context.fillStyle = color; context.fillRect(x + offset.x, y + offset.y, 1, 1); } }); }); }
        function draw() { context.fillStyle = '#000'; context.fillRect(0, 0, canvas.width, canvas.height); drawMatrix(arena, {x:0, y:0}, '#333'); drawMatrix(player.matrix, player.pos, '#1877f2'); }
        function merge(arena, player) { player.matrix.forEach((row, y) => { row.forEach((value, x) => { if (value !== 0) arena[y + player.pos.y][x + player.pos.x] = value; }); }); }
        function playerDrop() { player.pos.y++; if (collide(arena, player)) { player.pos.y--; merge(arena, player); player.matrix = pieces[Math.floor(Math.random() * pieces.length)]; player.pos.y = 0; player.pos.x = 4; if (collide(arena, player)) { alert("انتهت اللعبة! نقاطك: " + score); window.location.href = "/"; } arenaSweep(); } dropCounter = 0; }
        function arenaSweep() { outer: for (let y = arena.length - 1; y > 0; --y) { for (let x = 0; x < arena[y].length; ++x) { if (arena[y][x] === 0) continue outer; } const row = arena.splice(y, 1)[0].fill(0); arena.unshift(row); ++y; score += 10; document.getElementById('tetrisScore').innerText = "النقاط: " + score; } }
        function collide(arena, player) { const [m, o] = [player.matrix, player.pos]; for (let y = 0; y < m.length; ++y) { for (let x = 0; x < m[y].length; ++x) { if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) return true; } } return false; }
        function rotate(matrix) { for (let y = 0; y < matrix.length; ++y) { for (let x = 0; x < y; ++x) [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]]; } matrix.forEach(row => row.reverse()); }
        let dropCounter = 0, dropInterval = 1000, lastTime = 0;
        function update(time = 0) { const deltaTime = time - lastTime; lastTime = time; dropCounter += deltaTime; if (dropCounter > dropInterval) playerDrop(); draw(); requestAnimationFrame(update); }
        window.addEventListener('keydown', event => {
            if ([37, 38, 39, 40].includes(event.keyCode)) event.preventDefault();
            if (event.keyCode === 37) { player.pos.x--; if (collide(arena, player)) player.pos.x++; }
            else if (event.keyCode === 39) { player.pos.x++; if (collide(arena, player)) player.pos.x--; }
            else if (event.keyCode === 40) playerDrop();
            else if (event.keyCode === 38) { rotate(player.matrix); if (collide(arena, player)) rotate(player.matrix); }
        });
        update();
    </script>
</body>
</html>
"""

# --- قسم التوجيه الرئيسي (Flask Routes) ---

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/snake')
def snake_game():
    return render_template_string(SNAKE_TEMPLATE)

@app.route('/tetris')
def tetris_game():
    return render_template_string(TETRIS_TEMPLATE)

if __name__ == '__main__':
    app.run()
