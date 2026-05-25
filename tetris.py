from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

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
        const pieces = [[[1,1,1],[0,1,0]], [[0,2,2],[2,2,0]], [[3,3,0],[0,3,3]], [[4,4],[4,4]], [[0,0,5],[5,5,5]]];
        const player = { pos: {x: 4, y: 0}, matrix: pieces[Math.floor(Math.random() * pieces.length)] };
        function drawMatrix(matrix, offset, color = '#1877f2') { matrix.forEach((row, y) => { row.forEach((value, x) => { if (value !== 0) { context.fillStyle = color; context.fillRect(x + offset.x, y + offset.y, 1, 1); } }); }); }
        function draw() { context.fillStyle = '#000'; context.fillRect(0, 0, canvas.width, canvas.height); drawMatrix(arena, {x:0, y:0}, '#333'); drawMatrix(player.matrix, player.pos, '#1877f2'); }
        function merge(arena, player) { player.matrix.forEach((row, y) => { row.forEach((value, x) => { if (value !== 0) arena[y + player.pos.y][x + player.pos.x] = value; }); }); }
        function playerDrop() { player.pos.y++; if (collide(arena, player)) { player.pos.y--; merge(arena, player); player.matrix = pieces[Math.floor(Math.random() * pieces.length)]; player.pos.y = 0; player.pos.x = 4; if (collide(arena, player)) { alert("انتهت اللعبة! نقاطك: " + score); window.location.href = "/"; } arenaSweep(); } dropCounter = 0; }
        function arenaSweep() { outer: for (let y = arena.length - 1; y > 0; --y) { for (let x = 0; x < arena[y].length; ++x) { if (arena[y][x] === 0) continue outer; } const row = arena.splice(y, 1).fill(0); arena.unshift(row); ++y; score += 10; document.getElementById('tetrisScore').innerText = "النقاط: " + score; } }
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

@tetris_blueprint.route('/tetris')
def tetris_game():
    return render_template_string(TETRIS_TEMPLATE)
