from flask import Blueprint, render_template_string

card_game_blueprint = Blueprint('card_game', __name__)

CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Memory Cards - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #080c10; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #58a6ff; }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #58a6ff; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #58a6ff, 0 0 10px #58a6ff; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; }
        .game-box { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 20px; width: 100%; max-width: 360px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); box-sizing: border-box; }
        
        .info-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 13.5px; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px; color: #58a6ff; font-family: monospace; }
        
        /* 🎴 شبكة البطاقات الذكية رباعية الأعمدة متناسقة التوزيع للموبايل */
        .card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 15px; }
        .card-item { aspect-ratio: 0.8; background: #21262d; border: 1px solid #30363d; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 22px; color: transparent; position: relative; transform-style: preserve-3d; transition: transform 0.25s ease, border-color 0.15s ease; user-select: none; -webkit-user-select: none; }
        .card-item:hover { border-color: #58a6ff; }
        .card-item.flipped { transform: rotateY(180deg); background: #0d1117; border-color: #58a6ff; color: #58a6ff; text-shadow: 0 0 8px rgba(88,166,255,0.4); }
        .card-item.matched { background: #0d1117; border-color: #3fb950; color: #3fb950; cursor: default; pointer-events: none; text-shadow: 0 0 8px rgba(63,185,80,0.4); }
        
        .reset-btn { background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 8px 20px; font-size: 13px; font-weight: bold; cursor: pointer; border-radius: 6px; font-family: inherit; width: 100%; }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#58a6ff;">🃏 تحدي البطاقات</span>
    </div>

    <div class="main-container">
        <div class="game-box">
            <div class="info-container">
                <span id="moveCounter">الحركات: 0</span>
                <span id="matchCounter">المطابقات: 0/8</span>
            </div>
            <div class="card-grid" id="gridBox"></div>
            <button class="reset-btn" onclick="initCardGame()">إعادة ترتيب البطاقات 🔄</button>
        </div>
    </div>

    <script>
        const icons = ["💎", "🚀", "⚡", "🎮", "🔑", "🛡️", "🛸", "👾", "💎", "🚀", "⚡", "🎮", "🔑", "🛡️", "🛸", "👾"];
        let flippedCards = [], matchedCount = 0, moves = 0, lockBoard = false;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playTone(freq, type='sine', duration=0.06) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = type; o.frequency.setValueAtTime(freq, audioCtx.currentTime);
            g.gain.setValueAtTime(0.02, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + duration);
        }

        function initCardGame() {
            const grid = document.getElementById('gridBox');
            grid.innerHTML = ""; flippedCards = []; matchedCount = 0; moves = 0; lockBoard = false;
            document.getElementById('moveCounter').innerText = "الحركات: 0";
            document.getElementById('matchCounter').innerText = "المطابقات: 0/8";
            
            // خوارزمية الخلط العشوائي الكلاسيكية (Fisher-Yates Shuffle)
            let shuffled = [...icons];
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }

            shuffled.forEach((icon, idx) => {
                const card = document.createElement('div');
                card.classList.add('card-item');
                card.dataset.icon = icon;
                card.dataset.index = idx;
                card.onclick = () => flipCard(card);
                grid.appendChild(card);
            });
            playTone(400, 'triangle', 0.1);
        }

        function flipCard(card) {
            if (lockBoard || card.classList.contains('flipped') || card.classList.contains('matched')) return;
            
            card.classList.add('flipped');
            card.innerText = card.dataset.icon;
            playTone(550);
            flippedCards.push(card);

            if (flippedCards.length === 2) {
                moves++;
                document.getElementById('moveCounter').innerText = "الحركات: " + moves;
                checkMatch();
            }
        }

        function checkMatch() {
            let [card1, card2] = flippedCards;
            if (card1.dataset.icon === card2.dataset.icon) {
                card1.classList.add('matched');
                card2.classList.add('matched');
                matchedCount++;
                document.getElementById('matchCounter').innerText = "المطابقات: " + matchedCount + "/8";
                playTone(783.99, 'sine', 0.12);
                flippedCards = [];
                if (matchedCount === 8) {
                    setTimeout(() => { playTone(987.77, 'sine', 0.2); alert("🏁 تهانينا يا هندسة! تم حل لغز البطاقات بنجاح!"); }, 300);
                }
            } else {
                lockBoard = true;
                setTimeout(() => {
                    card1.classList.remove('flipped'); card1.innerText = "";
                    card2.classList.remove('flipped'); card2.innerText = "";
                    playTone(250, 'sawtooth', 0.08);
                    flippedCards = []; lockBoard = false;
                }, 800);
            }
        }

        initCardGame();
    </script>
</body>
</html>
"""

@card_game_blueprint.route('/card_game')
def card_game_page():
    return render_template_string(CARD_TEMPLATE)
