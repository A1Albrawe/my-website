from flask import Blueprint, render_template_string

clicker_blueprint = Blueprint('clicker', __name__)

CLICKER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Speed Clicker - Albrawe</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: 'Courier New', Courier, monospace; text-align: center; background: #0d1117; color: #c9d1d9; padding: 0; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .header-nav { background-color: #161b22; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ff7b72; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .back-btn { background: #21262d; border: 1px solid #30363d; color: #ff7b72; padding: 6px 15px; border-radius: 6px; cursor: pointer; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        /* ✨ تأثير النيون لاسم المهندس البراوي في المنتصف للتوجيه للرئيسية */
        .brand-center-link { text-decoration: none; font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; color: #fff; text-shadow: 0 0 5px #ff7b72, 0 0 10px #ff7b72; transition: 0.2s; }
        .brand-center-link:hover { text-shadow: 0 0 10px #fff, 0 0 20px #ff7b72; }
        
        .main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .click-box { background: #161b22; border: 1px solid #30363d; border-top: 4px solid #ff7b72; border-radius: 12px; padding: 30px 20px; width: 100%; max-width: 340px; box-shadow: 0 10px 20px rgba(0,0,0,0.4); text-align: center; box-sizing: border-box; position: relative; overflow: hidden; }
        
        .score-container { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 15px; color: #ff7b72; align-items: center; }
        .level-badge { color: #ffd700; font-weight: bold; }
        
        /* ⚡ تأثيرات النيون والتحجيم التفاعلي البصري للهدف */
        .circle-target { width: 110px; height: 110px; background: #ff7b72; border-radius: 50%; margin: 25px auto; display: flex; justify-content: center; align-items: center; font-size: 14px; font-weight: bold; color: #000; cursor: pointer; user-select: none; -webkit-user-select: none; transition: transform 0.05s ease, background-color 0.2s, width 0.3s, height 0.3s; box-shadow: 0 0 15px #ff7b72; position: relative; z-index: 2; }
        .circle-target:active { transform: scale(0.9) rotate(5deg); }
        
        .overlay-txt { display: none; position: absolute; font-size: 18px; font-weight: bold; color: #fff; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(22, 27, 34, 0.95); border: 2px solid #ff7b72; padding: 12px; border-radius: 8px; text-align: center; width: 85%; box-sizing: border-box; z-index: 5; }
        
        /* جزيئات الانفجار الحركي المتوهجة */
        .particle { position: absolute; width: 6px; height: 6px; background: #ff7b72; border-radius: 50%; pointer-events: none; animation: explode 0.4s ease-out forwards; z-index: 3; }
        @keyframes explode { 0% { transform: scale(1); opacity: 1; } 100% { transform: translate(var(--x), var(--y)) scale(0); opacity: 0; } }
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="/" class="back-btn">◀ الرئيسة</a>
        <!-- حقن رابط المطور المركزي في منتصف شريط التنقل -->
        <a href="/" class="brand-center-link">Albrawe</a>
        <span style="font-weight:bold; color:#ff7b72;">⚡ نيون</span>
    </div>
    <div class="main-container">
        <div class="click-box" id="clickCard">
            <div class="score-container">
                <span id="timerDisplay">الوقت: 10.0ث</span>
                <span id="levelDisplay" class="level-badge">المرحلة: 1 / 10 👑</span>
                <span id="scoreDisplay">النقاط: 0</span>
            </div>
            
            <div style="position:relative; min-height:180px; display:flex; align-items:center; justify-content:center;">
                <div class="circle-target" id="target" onclick="clickEngineTarget(event)">انقر للبدء!</div>
                
                <div id="gameOverScreen" class="overlay-txt" style="display:block;">
                    <h4 id="goTitle" style="margin:0 0 5px 0; color:#ff7b72;">تحدي النقر السريع</h4>
                    <p id="finalScoreText" style="margin:0 0 8px 0; font-size:12px; font-weight:bold;"></p>
                    <button style="background:#238636; color:#fff; border:1px solid #2ea44f; padding:8px 20px; font-size:13px; font-weight:bold; cursor:pointer; border-radius:6px;" onclick="startGame()">تنشيط المحرك ⚡</button>
                </div>
            </div>
            <div style="font-size:11px; color:#8b949e; font-weight:bold; margin-top:10px;">اكسر حاجز السرعة؛ كل مرحلة يتقلص الهدف ويزداد التسارع!</div>
        </div>
    </div>
    <script>
        let score = 0, timeLeft = 10.0, currentLevel = 1, gameActive = false, countdownInterval;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const colors = ["#ff7b72", "#58a6ff", "#3fb950", "#d29922", "#a371f7"];

        function playClickSound() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = 'sine'; 
            // تصعيد التردد الصوتي حدةً مع تزايد النقرات
            o.frequency.setValueAtTime(400 + (score * 8) + (currentLevel * 30), audioCtx.currentTime); 
            g.gain.setValueAtTime(0.05, audioCtx.currentTime);
            o.start(); o.stop(audioCtx.currentTime + 0.04);
        }

        function playLevelUpSound() {
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = 'triangle'; o.frequency.setValueAtTime(523.25, audioCtx.currentTime);
            o.frequency.exponentialRampToValueAtTime(1318.51, audioCtx.currentTime + 0.25);
            g.gain.setValueAtTime(0.08, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.25);
        }

        function playLoseSound() {
            const o = audioCtx.createOscillator(), g = audioCtx.createGain(); o.connect(g); g.connect(audioCtx.destination);
            o.type = 'sawtooth'; o.frequency.setValueAtTime(150, audioCtx.currentTime);
            o.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.4);
            g.gain.setValueAtTime(0.15, audioCtx.currentTime); o.start(); o.stop(audioCtx.currentTime + 0.4);
        }

        function startGame() {
            document.getElementById('gameOverScreen').style.display = 'none';
            score = 0; timeLeft = 10.0; currentLevel = 1; gameActive = true;
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            document.getElementById('levelDisplay').innerText = "المرحلة: " + currentLevel + " / 10 👑";
            document.getElementById('timerDisplay').innerText = "الوقت: " + timeLeft.toFixed(1) + "ث";
            
            const t = document.getElementById('target');
            t.innerText = "اضغط!"; t.style.width = "110px"; t.style.height = "110px";
            t.style.backgroundColor = colors[0]; t.style.boxShadow = `0 0 15px ${colors[0]}`;
            
            if(countdownInterval) clearInterval(countdownInterval);
            countdownInterval = setInterval(updateTimer, 100); // تحديث كل جزء من الثانية لتسجيل دقة الوقت
        }

        function clickEngineTarget(e) {
            if(!gameActive || timeLeft <= 0) return;
            score++;
            document.getElementById('scoreDisplay').innerText = "النقاط: " + score;
            playClickSound(); createParticles(e);
            
            // تصعيد الصعوبة بـ 10 مراحل: يتقلص قطر الهدف عند كل مرحلة (كل 15 نقرة)
            if(score % 15 === 0 && currentLevel < 10) {
                currentLevel++;
                playLevelUpSound();
                document.getElementById('levelDisplay').innerText = "المرحلة: " + currentLevel + " / 10 👑";
                
                // تقليد القطر تدريجياً لزيادة صعوبة التصويب والنقر
                let newSize = 110 - (currentLevel * 6);
                const t = document.getElementById('target');
                t.style.width = newSize + "px"; t.style.height = newSize + "px";
                
                // إضافة وقت مكافأة للمرحلة الجديدة
                timeLeft += 2.0;
            }

            // تبديل وتوهج لون النيون عشوائياً عند النقرة الناجحة
            let randColor = colors[Math.floor(Math.random() * colors.length)];
            e.target.style.backgroundColor = randColor;
            e.target.style.boxShadow = `0 0 22px ${randColor}`;
        }

        function createParticles(e) {
            const card = document.getElementById('clickCard'), rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left, y = e.clientY - rect.top;
            const targetColor = document.getElementById('target').style.backgroundColor || "#ff7b72";
            
            for(let i=0; i<10; i++) {
                const p = document.createElement('div'); p.className = 'particle';
                p.style.left = x + 'px'; p.style.top = y + 'px';
                let mx = (Math.random() - 0.5) * 140 + 'px', my = (Math.random() - 0.5) * 140 + 'px';
                p.style.setProperty('--x', mx); p.style.setProperty('--y', my);
                p.style.backgroundColor = targetColor;
                card.appendChild(p); setTimeout(() => p.remove(), 400);
            }
        }

        function updateTimer() {
            if (!gameActive) return;
            timeLeft -= 0.1;
            if (timeLeft <= 0) {
                timeLeft = 0; gameActive = false; clearInterval(countdownInterval); playLoseSound();
                document.getElementById('timerDisplay').innerText = "الوقت: 0.0ث";
                document.getElementById('goTitle').innerText = "انتهى الوقت! 💀";
                document.getElementById('finalScoreText').innerText = `نقراتك الإجمالية: ${score} نقرة في المرحلة ${currentLevel}`;
                document.getElementById('gameOverScreen').style.display = 'block';
                document.getElementById('target').innerText = "انتهى";
            } else {
                document.getElementById('timerDisplay').innerText = "الوقت: " + timeLeft.toFixed(1) + "ث";
            }
        }
    </script>
</body>
</html>
"""

@clicker_blueprint.route('/clicker')
def clicker_page():
    return render_template_string(CLICKER_TEMPLATE)
