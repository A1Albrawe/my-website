from flask import Blueprint, render_template_string

tetris_blueprint = Blueprint('tetris', __name__)

TETRIS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Albrawe - Tetris Pro</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #d29922; position: relative; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #d29922; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        .header-brand-center { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-decoration: none; }
        .neon-text-style { font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #d29922, 0 0 10px #d29922; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .game-card { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #d29922; border-radius: 20px; width: 100%; max-width: 320px; padding: 15px; box-shadow: 0 15px 30px rgba(0,0,0,0.5); box-sizing: border-box; }
        canvas { background-color: #0d1117; display: block; width: 100%; height: auto; border: 2px solid #30363d; border-radius: 6px; }
        .ctrl-pad { margin-top: 10px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        .btn { background: #21262d; border: 1px solid #30363d; color: #d29922; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ العودة</a>
        <a href="/" class="header-brand-center"><span class="neon-text-style">Albrawe</span></a>
    </div>
    <div class="main-container">
        <div class="game-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-weight:bold; font-size:12px; color:#d29922;">
                <span id="score">النقاط: 0</span>
                <span id="lvl">المرحلة: 1 / 10 👑</span>
            </div>
            <canvas id="tetris" width="200" height="400"></canvas>
            <div class="ctrl-pad">
                <button class="btn" onclick="mv(-1)">◀</button>
                <button class="btn" onclick="rot()">🔄</button>
                <button class="btn" onclick="mv(1)">▶</button>
                <div></div><button class="btn" onclick="drop()">▼</button><div></div>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('tetris'), ctx = canvas.getContext('2d');
        const ROW=20, COL=10, SQ=20, VACANT="#0d1117"; let board=[], score=0, level=1, timer=null;
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function snd(f) { const o=audioCtx.createOscillator(), g=audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination); o.frequency.value=f; g.gain.setValueAtTime(0.02, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime+0.05); }

        for(r=0; r<ROW; r++){ board[r]=[]; for(c=0; c<COL; c++){ board[r][c]=VACANT; } }
        function drawBoard(){ for(r=0; r<ROW; r++){ for(c=0; c<COL; c++){ fSq(c, r, board[r]); } } }
        function fSq(x, y, color){ ctx.fillStyle=color; ctx.fillRect(x*SQ, y*SQ, SQ, SQ); ctx.strokeStyle="#161b22"; ctx.strokeRect(x*SQ, y*SQ, SQ, SQ); }
        
        const PIECES=[ [[1,1,1,1]], [[1,1,1],[0,1,0]], [[1,1,0],[0,1,1]], [[1,1],[1,1]] ];
        const COLORS=["#388bfd", "#a371f7", "#d29922", "#3fb950"];
        let pLayout, pColor, pX=3, pY=-1;

        function newP() { let r=Math.floor(Math.random()*PIECES.length); pLayout=PIECES[r]; pColor=COLORS[r]; pX=3; pY=-pLayout.length; }
        function drawP(color){ for(r=0; r<pLayout.length; r++){ for(c=0; c<pLayout[r].length; c++){ if(pLayout[r][c] && pY+r>=0){ fSq(pX+c, pY+r, color); } } } }
        
        function drop() {
            if(!coll(0,1,pLayout)){ drawP(VACANT); pY++; drawP(pColor); }
            else { lock(); }
        }
        function coll(x,y,l) {
            for(r=0; r<l.length; r++){ for(c=0; c<l[r].length; c++){ if(!l[r][c])continue; let nX=pX+c+x, nY=pY+r+y; if(nX<0||nX>=COL||nY>=ROW)return true; if(nY<0)continue; if(board[nY][nX]!==VACANT)return true; } }
            return false;
        }
        function mv(d){ if(!coll(d,0,pLayout)){ drawP(VACANT); pX+=d; drawP(pColor); snd(300); } }
        function rot(){ let nL=pLayout[0].map((_,i)=>pLayout.map(row=>row[i]).reverse()); if(!coll(0,0,nL)){ drawP(VACANT); pLayout=nL; drawP(pColor); snd(400); } }
        
        function lock() {
            for(r=0; r<pLayout.length; r++){ for(c=0; c<pLayout[r].length; c++){ if(!pLayout[r][c])continue; if(pY+r<0){ alert('انتهت اللعبة! 💀'); score=0; level=1; window.location.reload(); return; } board[pY+r][pX+c]=pColor; } }
            for(r=0; r<ROW; r++){ let f=true; for(c=0; c<COL; c++){ if(board[r][c]===VACANT)f=false; } if(f){ board.splice(r,1); board.unshift(new Array(COL).fill(VACANT)); score+=100; snd(800); } }
            drawBoard(); document.getElementById('score').innerText="النقاط: "+score;
            if(score>=500 && level<10){ level++; alert(`تقدمت للمرحلة ${level} 🚀`); score=0; clearInterval(timer); timer=setInterval(drop, Math.max(100, 600 - (level*50))); }
            document.getElementById('lvl').innerText=`المرحلة: ${level} / 10 👑`; newP();
        }
        newP(); drawBoard(); timer=setInterval(drop, 600);
    </script>
</body>
</html>
"""

@tetris_blueprint.route('/tetris')
def tetris_page(): return render_template_string(TETRIS_HTML)
