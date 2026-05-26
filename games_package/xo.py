from flask import Blueprint, render_template_string

xo_blueprint = Blueprint('xo', __name__)

XO_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Albrawe - X-O Game</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #a371f7; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #a371f7; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .game-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #a371f7; border-radius: 12px; padding: 25px; width: 100%; max-width: 340px; box-shadow: 0 10px 20px rgba(0,0,0,0.4); box-sizing: border-box; }
        .status { font-size: 16px; font-weight: bold; margin-bottom: 15px; color: #58a6ff; }
        .board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 15px; }
        .cell { background: #0d1117; border: 1px solid #30363d; height: 80px; border-radius: 8px; display: flex; justify-content: center; align-items: center; font-size: 32px; font-weight: bold; cursor: pointer; user-select: none; }
        .cell:hover { background: #21262d; }
        .cell.X { color: #f85149; } .cell.O { color: #58a6ff; }
        .reset-btn { background: #238636; color: #fff; border: none; padding: 8px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; font-family: inherit; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة للرئيسية</a>
        <span style="font-weight:bold; color:#fff;">❌ لعبة X-O الذكية ⭕</span>
    </div>
    <div class="main-container">
        <div class="game-card">
            <div class="status" id="status">دور اللاعب: X</div>
            <div class="board">
                <div class="cell" onclick="makeMove(this, 0)"></div>
                <div class="cell" onclick="makeMove(this, 1)"></div>
                <div class="cell" onclick="makeMove(this, 2)"></div>
                <div class="cell" onclick="makeMove(this, 3)"></div>
                <div class="cell" onclick="makeMove(this, 4)"></div>
                <div class="cell" onclick="makeMove(this, 5)"></div>
                <div class="cell" onclick="makeMove(this, 6)"></div>
                <div class="cell" onclick="makeMove(this, 7)"></div>
                <div class="cell" onclick="makeMove(this, 8)"></div>
            </div>
            <button class="reset-btn" onclick="resetGame()">إعادة اللعب</button>
        </div>
    </div>
    <script>
        let board = ["", "", "", "", "", "", "", "", ""];
        let currentPlayer = "X";
        let gameActive = true;
        const winConditions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]];

        function makeMove(cell, index) {
            if (board[index] !== "" || !gameActive) return;
            board[index] = currentPlayer;
            cell.innerText = currentPlayer;
            cell.classList.add(currentPlayer);
            checkResult();
        }

        function checkResult() {
            let roundWon = false;
            for (let i = 0; i < winConditions.length; i++) {
                const [a, b, c] = winConditions[i];
                if (board[a] && board[a] === board[b] && board[a] === board[c]) { roundWon = true; break; }
            }
            if (roundWon) { document.getElementById('status').innerText = `الفائز هو اللاعب: ${currentPlayer} 🎉`; gameActive = false; return; }
            if (!board.includes("")) { document.getElementById('status').innerText = "التعادل! 🤝"; gameActive = false; return; }
            currentPlayer = currentPlayer === "X" ? "O" : "X";
            document.getElementById('status').innerText = `دور اللاعب: ${currentPlayer}`;
        }

        function resetGame() {
            board = ["", "", "", "", "", "", "", "", ""];
            currentPlayer = "X"; gameActive = true;
            document.getElementById('status').innerText = "دور اللاعب: X";
            document.querySelectorAll('.cell').forEach(c => { c.innerText = ""; c.className = "cell"; });
        }
    </script>
</body>
</html>
"""

@xo_blueprint.route('/xo')
def xo_page():
    return render_template_string(XO_TEMPLATE)
