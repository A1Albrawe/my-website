from flask import Blueprint, render_template_string, request, jsonify

# إنشاء البلوبرينت القياسي للعبة الثعبان
snake_blueprint = Blueprint('snake', __name__)

# مصفوفة سحابية مركزية مؤمنة داخل السيرفر لحفظ توب 3 لاعبين على مستوى العالم
GLOBAL_LEADERBOARD = [
    {"name": "البروي 👑", "score": 150},
    {"name": "لاعب 2", "score": 0},
    {"name": "لاعب 3", "score": 0}
]

# مسار سحابي لاستدعاء لوحة الصدارة الموحدة لكل المستخدمين
@snake_blueprint.route('/api/get_leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify(GLOBAL_LEADERBOARD)

# مسار سحابي لاستقبال النتيجة الجديدة وتدقيقها وترتيبها عالمياً في السيرفر
@snake_blueprint.route('/api/submit_score', methods=['POST'])
def submit_score():
    global GLOBAL_LEADERBOARD
    data = request.get_json() or {}
    name = data.get('name', 'لاعب مجهول').strip() or 'لاعب مجهول'
    score = int(data.get('score', 0))
    
    if score > 0:
        GLOBAL_LEADERBOARD.append({"name": name, "score": score})
        GLOBAL_LEADERBOARD.sort(key=lambda x: x['score'], reverse=True)
        GLOBAL_LEADERBOARD = GLOBAL_LEADERBOARD[:3]
        
    return jsonify({"status": "success", "leaderboard": GLOBAL_LEADERBOARD})


SNAKE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Snake</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .nokia-phone { background: #161b22; border: 3px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 20px; width: 100%; max-width: 370px; padding: 25px 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; position: relative; }
        .nokia-screen { background-color: #0d1117; border: 2px solid #30363d; border-radius: 10px; padding: 10px; position: relative; box-sizing: border-box; touch-action: none; }
        .highscore-flash { animation: rf 0.15s ease infinite alternate; }
        @keyframes rf { 0% { background-color: #0d1117; } 100% { background-color: #21262d; border-color: #ffd700; } }
        .score-container { display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 10px; color: #58a6ff; }
        .audio-controls { display: flex; align-items: center; gap: 4px; }
        .mute-btn { background: none; border: none; font-size: 14px; cursor: pointer; color: #58a6ff; padding: 0; }
        .volume-bar { width: 55px; accent-color: #58a6ff; height: 3px; cursor: pointer; }
        .canvas-container { width: 100%; display: flex; justify-content: center; position: relative; }
        canvas { background-color: #161b22; display: block; max-width: 100%; height: auto; border: 1px solid #30363d; border-radius: 4px; }
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #58a6ff; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        .leaderboard { margin-top: 10px; background: rgba(0, 0, 0, 0.2); padding: 8px; border-radius: 6px; font-size: 11px; text-align: right; border: 1px solid #30363d; }
        .leaderboard h4 { margin: 0 0 6px 0; text-align: center; font-size: 12px; color: #79c0ff; }
        .score-row { display: flex; justify-content: space-between; padding: 2px 0; font-weight: bold; color: #c9d1d9; }
        .nokia-dpad { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 160px; height: 160px; margin-left: auto; margin-right: auto; }
        .arrow-btn { background: #21262d; border: 1px solid #30363d; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; color: #58a6ff; cursor: pointer; box-shadow: 0 4px #0d1117; user-select: none; -webkit-user-select: none; }
        .arrow-btn:active { transform: translateY(2px); box-shadow: 0 1px #0d1117; }
        .dpad-empty { pointer-events: none; visibility: hidden; }
        .dpad-center-btn { background: #30363d; border: 1px solid #58a6ff; border-radius: 50%; cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 14px; color: #fff; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="font-weight:bold; color:#fff;">🐍 لعبة الثعبان السحابية </span>
    </div>
"""
SNAKE_BODY_TEMPLATE = """
    <div class="main-container">
        <div class="nokia-phone" id="phoneWrapper">
            <div class="nokia-screen" id="nokiaScreen">
                <div class="score-container">
                    <span id="snakeScore">النقاط: 0</span>
                    <div class="audio-controls">
                        <button class="mute-btn" id="muteToggle" onclick="toggleMute()"><i class="fas fa-volume-up"></i></button>
                        <input type="range" id="volumeSlider" class="volume-bar" min="0" max="1" step="0.1" value="0.5" oninput="updateVolume(this.value)">
                    </div>
                    <span>ALBRAWE</span>
                </div>
                
                <div class="canvas-container">
                    <canvas id="snakeCanvas" width="240" height="160"></canvas>
                    <div id="pauseOverlay" class="overlay-txt">مؤقت ⏸️</div>
                    
                    <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                        <h4 id="goTitle" style="margin:0 0 5px 0; color:#58a6ff;">مرحباً بك</h4>
                        <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                        <input type="text" id="playerName" style="padding:6px; font-size:12px; border:1px solid #30363d; background:#0d1117; color:#fff; margin-bottom:8px; text-align:center; width:85%; font-family:inherit; font-weight:bold; box-sizing:border-box;" placeholder="اسم المستخدم" maxlength="10">
                        <br><button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:6px 15px; font-size:12px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="submitPlayer()">بدء اللعب السحابي</button>
                    </div>
                </div>

                <div class="leaderboard">
                    <h4>🏆 لوحة صدارة أفضل نتائج اللاعبين عالمياً</h4>
                    <div id="leaderboardContent"></div>
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
"""
SNAKE_JS_TEMPLATE = """
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
        let isMuted = false;
        let gameActive = false;
        let currentHighScore = 0;

        fetchLeaderboard();

        function fetchLeaderboard() {
            fetch('/api/get_leaderboard')
            .then(res => res.json())
            .then(data => {
                let html = '';
                if(data && data.length > 0) {
                    currentHighScore = data[0].score;
                    data.forEach((item, index) => {
                        html += `<div class="score-row"><span>${index+1}. ${item.name}</span><strong>${item.score} ن</strong></div>`;
                    });
                }
                document.getElementById('leaderboardContent').innerHTML = html;
            });
        }

        function submitPlayer() {
            const nameInput = document.getElementById('playerName').value.trim();
            if(!nameInput && !gameActive) {
                alert('الرجاء كتابة اسم مستخدم لبدء حفظ نتيجتك سحابياً!');
                return;
            }
            document.getElementById('gameOverScreen').style.display = 'none';
            initGame();
        }

        function initGame() {
            snake = [{x: 12 * box, y: 8 * box}];
            generateFood();
            score = 0;
            d = 'RIGHT';
            isPaused = false;
            gameActive = true;
            document.getElementById('snakeScore').innerText = 'النقاط: ' + score;
            document.getElementById('phoneWrapper').classList.remove('highscore-flash');
            if(gameLoopInterval) clearInterval(gameLoopInterval);
            gameLoopInterval = setInterval(draw, 100);
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * (canvas.width / box)) * box,
                y: Math.floor(Math.random() * (canvas.height / box)) * box
            };
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
            if(isPaused) { clearInterval(gameLoopInterval); } else { gameLoopInterval = setInterval(draw, 100); }
        }

        function toggleMute() {}
        function updateVolume(val) {}

        function checkCollision(head, array) {
            for(let i = 0; i < array.length; i++) {
                if(head.x === array[i].x && head.y === array[i].y) return true;
            }
            return false;
        }

        function draw() {
            ctx.fillStyle = '#161b22';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            for(let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i === 0) ? '#58a6ff' : '#3fb950';
                ctx.strokeStyle = '#0d1117';
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }

            ctx.fillStyle = '#f85149';
            ctx.fillRect(food.x, food.y, box, box);

            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if(d === 'LEFT') snakeX -= box;
            if(d === 'UP') snakeY -= box;
            if(d === 'RIGHT') snakeX += box;
            if(d === 'DOWN') snakeY -= box;

            if(snakeX === food.x && snakeY === food.y) {
                score += 10;
                document.getElementById('snakeScore').innerText = 'النقاط: ' + score;
                generateFood();
                if(score > currentHighScore && currentHighScore > 0) {
                    document.getElementById('phoneWrapper').classList.add('highscore-flash');
                }
            } else {
                snake.pop();
            }

            let newHead = { x: snakeX, y: snakeY };

            if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || checkCollision(newHead, snake)) {
                clearInterval(gameLoopInterval);
                gameActive = false;
                handleGameOver();
                return;
            }

            snake.unshift(newHead);
        }

        function handleGameOver() {
            const pName = document.getElementById('playerName').value.trim() || 'لاعب مجهول';
            document.getElementById('goTitle').innerText = 'انتهت اللعبة! 💀';
            document.getElementById('finalScoreText').innerText = `أحرزت: ${score} نقطة`;
            document.getElementById('gameOverScreen').style.display = 'block';

            fetch('/api/submit_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: pName, score: score })
            })
            .then(res => res.json())
            .then(data => { fetchLeaderboard(); });
        }
    </script>
</body>
</html>
"""

@snake_blueprint.route('/snake')
def snake_page():
    # دمج الأجزاء الثلاثة ديناميكياً داخل دالة الـ Flask للاستجابة السريعة
    FULL_PAGE = SNAKE_TEMPLATE + SNAKE_BODY_TEMPLATE + SNAKE_JS_TEMPLATE
    return render_template_string(FULL_PAGE)
