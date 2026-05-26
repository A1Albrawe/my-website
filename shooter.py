from flask import Blueprint, render_template_string

shooter_blueprint = Blueprint('shooter', __name__)

SHOOTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Albrawe - Space Shooter</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #388bfd; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #388bfd; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; }
        canvas { background: #000; border: 2px solid #30363d; border-radius: 8px; max-width: 100%; height: auto; }
        .controls { display: flex; gap: 15px; margin-top: 10px; width: 100%; max-width: 300px; }
        .btn { flex: 1; background: #21262d; border: 1px solid #30363d; color: #388bfd; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 18px; user-select: none; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="font-weight:bold; color:#fff;">🚀 غازي الفضاء الكلاسيكي 👾</span>
    </div>
    <div class="main-container">
        <canvas id="gameCanvas" width="300" height="400"></canvas>
        <div class="controls">
            <button class="btn" onmousedown="move(-20)" ontouchstart="move(-20)">◀</button>
            <button class="btn" onclick="shoot()">🚀 إطلاق</button>
            <button class="btn" onmousedown="move(20)" ontouchstart="move(20)">▶</button>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas'), ctx = canvas.getContext('2d');
        let player = { x: 135, y: 360, w: 30, h: 20 }, lasers = [], enemies = [], score = 0, gameOver = false;

        function spawnEnemy() { if(!gameOver) enemies.push({ x: Math.random()*280, y: 0, w: 20, h: 20 }); }
        setInterval(spawnEnemy, 1000);

        function move(dir) { if(!gameOver) { player.x = Math.max(0, Math.min(270, player.x + dir)); } }
        function shoot() { if(!gameOver) lasers.push({ x: player.x + 13, y: player.y, w: 4, h: 10 }); }

        document.addEventListener('keydown', e => {
            if(e.key === 'ArrowLeft') move(-15); if(e.key === 'ArrowRight') move(15); if(e.key === ' ') shoot();
        });

        function update() {
            if (gameOver) return;
            lasers.forEach((l, li) => { l.y -= 5; if(l.y < 0) lasers.splice(li, 1); });
            enemies.forEach((e, ei) => {
                e.y += 2;
                if(e.y > 400) { gameOver = true; alert(`انتهت اللعبة! نتيجتك: ${score}`); window.location.reload(); }
                lasers.forEach((l, li) => {
                    if(l.x < e.x + e.w && l.x + l.w > e.x && l.y < e.y + e.h && l.y + l.h > e.y) {
                        enemies.splice(ei, 1); lasers.splice(li, 1); score += 10;
                    }
                });
            });
        }

        function draw() {
            ctx.fillStyle = '#000'; ctx.fillRect(0,0,300,400);
            ctx.fillStyle = '#388bfd'; ctx.fillRect(player.x, player.y, player.w, player.h);
            ctx.fillStyle = '#ffd700'; lasers.forEach(l => ctx.fillRect(l.x, l.y, l.w, l.h));
            ctx.fillStyle = '#f85149'; enemies.forEach(e => ctx.fillRect(e.x, e.y, e.w, e.h));
            ctx.fillStyle = '#fff'; ctx.font = '14px monospace'; ctx.fillText(`النقاط: ${score}`, 10, 20);
        }

        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
</body>
</html>
"""

@shooter_blueprint.route('/shooter')
def shooter_page():
    return render_template_string(SHOOTER_TEMPLATE)
