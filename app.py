from flask import Flask, render_template_string

app = Flask(__name__)

# تصميم الموقع المتكامل مع القوائم والألعاب في قالب نصي واحد
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع Albrawe</title>
    <!-- استدعاء المكتبات الخارجية للأيقونات الخطية -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background-color: #f0f2f5; 
            padding: 50px; 
            margin: 0;
            transition: margin-right 0.3s ease;
        }
        
        /* تصميم زر التحكم في القائمة الجانبية */
        .menu-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            font-size: 20px;
            background: #1877f2;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* تنسيق الهيكل العام للقائمة الجانبية */
        .sidebar {
            height: 100%;
            width: 0;
            position: fixed;
            z-index: 999;
            top: 0;
            right: 0;
            background-color: #1a1a1a;
            overflow-x: hidden;
            transition: 0.3s ease;
            padding-top: 80px;
            text-align: right;
            box-shadow: -4px 0 15px rgba(0,0,0,0.4);
        }

        .sidebar a, .sidebar .dropdown-btn {
            padding: 15px 25px;
            text-decoration: none;
            font-size: 18px;
            color: #b3b3b3;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: 0.2s;
            border-bottom: 1px solid #2d2d2d;
            background: none;
            border-top: none; border-left: none; border-right: none;
            width: 100%;
            text-align: right;
            cursor: pointer;
            font-family: inherit;
            box-sizing: border-box;
        }

        .sidebar a:hover, .sidebar .dropdown-btn:hover {
            color: white;
            background-color: #1877f2;
        }

        /* حاوية الألعاب المنسدلة */
        .dropdown-container {
            display: none;
            background-color: #242424;
            padding-right: 20px;
        }

        .dropdown-container a {
            font-size: 16px;
            border-bottom: 1px solid #333;
        }

        .sidebar .close-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 28px;
            color: #bbb;
            cursor: pointer;
        }
        .sidebar .close-btn:hover { color: white; }

        /* الكارت المركزي لعرض البيانات الحالية */
        .container { 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            display: inline-block; 
            max-width: 500px;
            margin-top: 60px;
        }
        h1 { color: #1877f2; margin-top: 0; margin-bottom: 15px; }
        p { color: #555; font-size: 18px; line-height: 1.6; margin-bottom: 25px; }
        
        /* مظهر أيقونة التليجرام المحسنة */
        .telegram-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background-color: #0088cc;
            color: white;
            text-decoration: none;
            padding: 14px 30px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0, 136, 204, 0.3);
            transition: all 0.3s ease;
        }
        .telegram-btn:hover {
            background-color: #0077b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(0, 136, 204, 0.4);
        }

        .footer { margin-top: 30px; color: #888; font-size: 14px; border-top: 1px solid #eee; padding-top: 15px; }

        /* الشاشات المنبثقة للألعاب المدمجة */
        .game-modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0; top: 0;
            width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.85);
            justify-content: center;
            align-items: center;
        }

        .game-content {
            background-color: #1e1e1e;
            padding: 25px;
            border-radius: 12px;
            position: relative;
            color: white;
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
            text-align: center;
        }

        .game-close {
            position: absolute;
            top: 10px;
            left: 15px;
            color: #fff;
            font-size: 30px;
            cursor: pointer;
            transition: color 0.2s;
        }
        .game-close:hover { color: #ff4d4d; }

        .score-board {
            font-size: 20px;
            font-weight: bold;
            color: #34b7f1;
            margin-bottom: 10px;
        }

        canvas {
            border: 4px solid #1877f2;
            background-color: #000;
            display: block;
            margin: 0 auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

    <!-- زر القائمة الجانبية -->
    <button class="menu-btn" onclick="toggleNav()"><i class="fas fa-bars"></i> القائمة</button>

    <!-- الهيكل الخاص بالقوائم المطلوبة بالترتيب -->
    <div id="mySidebar" class="sidebar">
        <span class="close-btn" onclick="toggleNav()"><i class="fas fa-times"></i></span>
        <a href="#"><i class="fas fa-home"></i> الصفحة الرئيسية</a>
        <a href="#"><i class="fas fa-code"></i> المشاريع</a>
        
        <!-- روابط أخرى تتضمن ألعاب المتصفح -->
        <button class="dropdown-btn" onclick="toggleDropdown()">
            <i class="fas fa-link"></i> روابط أخرى <i class="fas fa-caret-down" style="margin-right: auto; margin-left: 0;"></i>
        </button>
        <div id="gamesDropdown" class="dropdown-container">
            <a href="#" onclick="openGame('snake')"><i class="fas fa-gamepad"></i> لعبة الثعبان</a>
            <a href="#" onclick="openGame('tetris')"><i class="fas fa-cubes"></i> لعبة التترس</a>
        </div>

        <a href="#"><i class="fas fa-info-circle"></i> حول هذا</a>
    </div>

    <!-- كارت المحتوى الأساسي والبيانات دون تغيير -->
    <div class="container">
        <h1>مرحباً بك في موقع albrawe</h1>
        <p>تم تشغيل الموقع بنجاح وهو الآن متاح للجميع على الإنترنت!</p>
        
        <!-- التوجيه الدقيق المباشر إلى حسابك بالتليجرام -->
        <a href="https://t.me" target="_blank" class="telegram-btn">
            <i class="fab fa-telegram-plane"></i> تليجرام @a1albrawe
        </a>

        <div class="footer">يعمل بواسطة Python & Flask</div>
    </div>
    <!-- نافذة منبثقة تفاعلية: لعبة الثعبان -->
    <div id="snakeModal" class="game-modal">
        <div class="game-content">
            <span class="game-close" onclick="closeGame('snake')">&times;</span>
            <h3 style="margin-top:0;">لعبة الثعبان (الأسهم ⬆️ ⬇️ ⬅️ ➡️)</h3>
            <div id="snakeScore" class="score-board">النقاط: 0</div>
            <canvas id="snakeCanvas" width="400" height="400"></canvas>
        </div>
    </div>

    <!-- نافذة منبثقة تفاعلية: لعبة التترس -->
    <div id="tetrisModal" class="game-modal">
        <div class="game-content">
            <span class="game-close" onclick="closeGame('tetris')">&times;</span>
            <h3 style="margin-top:0;">لعبة التترس (⬇️ إسقاط، ⬆️ تدوير، ⬅️ ➡️ توجيه)</h3>
            <div id="tetrisScore" class="score-board">النقاط: 0</div>
            <canvas id="tetrisCanvas" width="240" height="400"></canvas>
        </div>
    </div>

    <!-- المتحكمات البرمجية الذكية للواجهات والألعاب (JavaScript) -->
    <script>
        let sidebarOpen = false;
        function toggleNav() {
            const sidebar = document.getElementById("mySidebar");
            sidebar.style.width = sidebarOpen ? "0" : "250px";
            sidebarOpen = !sidebarOpen;
        }

        function toggleDropdown() {
            const dropdown = document.getElementById("gamesDropdown");
            dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
        }

        let snakeInterval, tetrisAnimationId;
        
        function openGame(game) {
            toggleNav();
            document.getElementById(game + 'Modal').style.display = 'flex';
            if (game === 'snake') startSnake();
            if (game === 'tetris') startTetris();
        }

        function closeGame(game) {
            document.getElementById(game + 'Modal').style.display = 'none';
            if (game === 'snake') clearInterval(snakeInterval);
            if (game === 'tetris') cancelAnimationFrame(tetrisAnimationId);
        }

        // --- محرك لعبة الثعبان ---
        function startSnake() {
            const canvas = document.getElementById('snakeCanvas');
            const ctx = canvas.getContext('2d');
            let score = 0;
            const box = 20;
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
                ctx.fillStyle = '#000';
                ctx.fillRect(0, 0, 400, 400);

                for(let i=0; i<snake.length; i++) {
                    ctx.fillStyle = (i == 0)? "#1877f2" : "#fff";
                    ctx.fillRect(snake[i].x, snake[i].y, box, box);
                }

                ctx.fillStyle = "#ff4d4d";
                ctx.fillRect(food.x, food.y, box, box);

                let snakeX = snake[0].x;
                let snakeY = snake[0].y;

                if(d == "LEFT") snakeX -= box;
                if(d == "UP") snakeY -= box;
                if(d == "RIGHT") snakeX += box;
                if(d == "DOWN") snakeY += box;

                if(snakeX == food.x && snakeY == food.y) {
                    score += 10;
                    document.getElementById('snakeScore').innerText = "النقاط: " + score;
                    food = {x: Math.floor(Math.random()*20)*box, y: Math.floor(Math.random()*20)*box};
                } else {
                    snake.pop();
                }

                let newHead = {x: snakeX, y: snakeY};

                if(snakeX < 0 || snakeX >= 400 || snakeY < 0 || snakeY >= 400 || collision(newHead, snake)) {
                    clearInterval(snakeInterval);
                    alert("انتهت اللعبة! مجموع نقاطك: " + score);
                    closeGame('snake');
                    return;
                }

                snake.unshift(newHead);
            }

            function collision(head, array) {
                for(let i=0; i<array.length; i++) {
                    if(head.x == array[i].x && head.y == array[i].y) return true;
                }
                return false;
            }
            clearInterval(snakeInterval);
            snakeInterval = setInterval(draw, 100);
        }
        // --- محرك لعبة التترس ---
        function startTetris() {
            const canvas = document.getElementById('tetrisCanvas');
            const context = canvas.getContext('2d');
            context.clearRect(0, 0, canvas.width, canvas.height);
            
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.scale(20, 20);
            
            let score = 0;
            document.getElementById('tetrisScore').innerText = "النقاط: 0";

            const pieces = [
                [[1, 1, 1, 1]],
                [[1, 1, 1], [0, 1, 0]],
                [[1, 1, 1], [1, 0, 0]],
                [[1, 1, 1], [0, 0, 1]],
                [[1, 1], [1, 1]],
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1, 1], [1, 1, 0]]
            ];

            function createMatrix(w, h) {
                const matrix = [];
                while (h--) { matrix.push(new Array(w).fill(0)); }
                return matrix;
            }

            const arena = createMatrix(12, 20);
            
            function getRandomPiece() {
                return pieces[Math.floor(Math.random() * pieces.length)];
            }

            const player = {
                pos: {x: 4, y: 0},
                matrix: getRandomPiece()
            };

            function drawMatrix(matrix, offset, color = '#1877f2') {
                matrix.forEach((row, y) => {
                    row.forEach((value, x) => {
                        if (value !== 0) {
                            context.fillStyle = color;
                            context.fillRect(x + offset.x, y + offset.y, 1, 1);
                        }
                    });
                });
            }

            function merge(arena, player) {
                player.matrix.forEach((row, y) => {
                    row.forEach((value, x) => {
                        if (value !== 0) { arena[y + player.pos.y][x + player.pos.x] = value; }
                    });
                });
            }

            function playerDrop() {
                player.pos.y++;
                if (collide(arena, player)) {
                    player.pos.y--;
                    merge(arena, player);
                    player.matrix = getRandomPiece();
                    player.pos.y = 0;
                    player.pos.x = 4;
                    if (collide(arena, player)) {
                        cancelAnimationFrame(tetrisAnimationId);
                        alert("انتهت اللعبة! مجموع نقاطك: " + score);
                        closeGame('tetris');
                        return;
                    }
                    arenaSweep();
                }
                dropCounter = 0;
            }

            function arenaSweep() {
                outer: for (let y = arena.length - 1; y > 0; --y) {
                    for (let x = 0; x < arena[y].length; ++x) {
                        if (arena[y][x] === 0) { continue outer; }
                    }
                    const row = arena.splice(y, 1).fill(0);
                    arena.unshift(row);
                    ++y;
                    score += 10;
                    document.getElementById('tetrisScore').innerText = "النقاط: " + score;
                }
            }

            function collide(arena, player) {
                const [m, o] = [player.matrix, player.pos];
                for (let y = 0; y < m.length; ++y) {
                    for (let x = 0; x < m[y].length; ++x) {
                        if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) { return true; }
                    }
                }
                return false;
            }

            let dropCounter = 0;
            let dropInterval = 1000;
            let lastTime = 0;

            function update(time = 0) {
                const deltaTime = time - lastTime;
                lastTime = time;
                dropCounter += deltaTime;
                if (dropCounter > dropInterval) { playerDrop(); }
                
                context.fillStyle = '#000';
                context.fillRect(0, 0, canvas.width, canvas.height);
                
                drawMatrix(arena, {x: 0, y: 0}, '#333');
                drawMatrix(player.matrix, player.pos, '#1877f2');
            }

            function rotate(matrix) {
                for (let y = 0; y < matrix.length; ++y) {
                    for (let x = 0; x < y; ++x) { [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]]; }
                }
                matrix.forEach(row => row.reverse());
            }

            window.addEventListener('keydown', function(event) {
                if([32, 37, 38, 39, 40].indexOf(event.keyCode) > -1) {
                    event.preventDefault();
                }
                if (document.getElementById('tetrisModal').style.display === 'flex') {
                    if (event.keyCode === 37) { player.pos.x--; if (collide(arena, player)) player.pos.x++; }
                    else if (event.keyCode === 39) { player.pos.x++; if (collide(arena, player)) player.pos.x--; }
                    else if (event.keyCode === 40) { playerDrop(); }
                    else if (event.keyCode === 38) { 
                        rotate(player.matrix); 
                        if (collide(arena, player)) { rotate(player.matrix); rotate(player.matrix); rotate(player.matrix); }
                    }
                }
            }, {passive: false});

            function loop(time) { 
                update(time); 
                tetrisAnimationId = requestAnimationFrame(loop); 
            }
            if(tetrisAnimationId) cancelAnimationFrame(tetrisAnimationId);
            loop();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
