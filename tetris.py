from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

TETRIS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Albrawe - Tetris</title>
    <style>
        body { font-family: monospace; background: #121212; color: #8c9f21; text-align: center; padding: 20px; margin:0; display:flex; flex-direction:column; min-height:100vh; align-items:center; justify-content:center;}
        .back-btn { background: #111; color: #8c9f21; border: 2px solid #8c9f21; padding: 8px 16px; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold; margin-bottom: 15px; }
        canvas { background: #000; border: 4px solid #333; display: block; }
        .controls { margin-top: 15px; display: grid; grid-template-columns: repeat(3, 60px); gap: 10px; }
        .btn { background: #cbd3d8; border: 2px solid #a1aab0; padding: 15px; font-size: 18px; font-weight: bold; cursor: pointer; color:#000; border-radius:10px; text-align:center;}
    </style>
</head>
<body>
    <br><a href="/" class="back-btn">القائمة الرئيسية</a>
    <h2>🧱 لعبة التترس البكسلية</h2>
    <h3 id="tetrisScore">النقاط: 0</h3>
    <canvas id="tetrisCanvas" width="240" height="400"></canvas>
    <div class="controls">
        <div></div><div class="btn" onclick="moveUp()">▲</div><div></div>
        <div class="btn" onclick="moveLeft()">◀</div><div class="btn" onclick="drop()">▼</div><div class="btn" onclick="moveRight()">▶</div>
    </div>
    <script>
        const canvas = document.getElementById('tetrisCanvas'), ctx = canvas.getContext('2d');
        const ROW = 20, COL = 12, SQ = 20, VACANT = "#000";
        let score = 0;
        let board = [];
        for(r=0; r<ROW; r++){ board[r]=[]; for(c=0; c<COL; c++){ board[r][c]=VACANT; } }
        function drawSquare(x,y,color){ ctx.fillStyle = color; ctx.fillRect(x*SQ, y*SQ, SQ, SQ); ctx.strokeStyle = "#222"; ctx.strokeRect(x*SQ, y*SQ, SQ, SQ); }
        function drawBoard(){ for(r=0; r<ROW; r++){ for(c=0; c<COL; c++){ drawSquare(c,r,board[r][c]); } } }
        drawBoard();
        const PIECES = [
            [[[1,1,1,1]],[[1],[1],[1],[1]]],
            [[[1,1],[1,1]]],
            [[[0,1,0],[1,1,1]],[[1,0],[1,1],[1,0]],[[1,1,1],[0,1,0]],[[0,1],[1,1],[0,1]]]
        ];
        let p = PIECES[0][0], pCol = "#8c9f21", pX = 4, pY = 0;
        function drawPiece(){ for(r=0; r<p.length; r++){ for(c=0; c<p[r].length; c++){ if(p[r][c]){ drawSquare(pX+c, pY+r, pCol); } } } }
        function clearPiece(){ for(r=0; r<p.length; r++){ for(c=0; c<p[r].length; c++){ if(p[r][c]){ drawSquare(pX+c, pY+r, VACANT); } } } }
        function moveLeft(){ clearPiece(); pX--; if(collision()){ pX++; } drawPiece(); }
        function moveRight(){ clearPiece(); pX++; if(collision()){ pX--; } drawPiece(); }
        function moveUp(){ clearPiece(); pY--; if(collision()){ pY++; } drawPiece(); }
        function drop(){ clearPiece(); pY++; if(collision()){ pY--; lock(); } drawPiece(); }
        function collision(){ for(r=0; r<p.length; r++){ for(c=0; c<p[r].length; c++){ if(!p[r][c]) continue; let newX=pX+c, newY=pY+r; if(newX<0||newX>=COL||newY>=ROW){return true;} if(newY<0) continue; if(board[newY][newX]!==VACANT){return true;} } } return false; }
        function lock(){ for(r=0; r<p.length; r++){ for(c=0; c<p[r].length; c++){ if(!p[r][
