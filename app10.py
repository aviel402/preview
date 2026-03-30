import random
from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = "neon_rider_secret"

NEON_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEON SYNTHWAVE RIDER 2.1</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-pink: #ff00ff;
            --neon-blue: #00ffff;
            --neon-yellow: #ffff00;
            --bg-dark: #050510;
        }

        body {
            margin: 0; padding: 0; background: var(--bg-dark);
            color: white; font-family: 'Orbitron', sans-serif;
            overflow: hidden; display: flex; flex-direction: column;
            align-items: center; justify-content: center; height: 100vh;
            user-select: none;
        }

        .game-container {
            position: relative;
            width: 800px; height: 600px;
        }

        canvas {
            position: absolute; top: 0; left: 0;
            border: 4px solid var(--neon-blue);
            box-shadow: 0 0 30px var(--neon-blue), inset 0 0 30px var(--neon-blue);
            background: linear-gradient(to bottom, #110022 0%, #000000 40%);
            border-radius: 10px;
        }

        /* מניע מסך טלוויזיה ישן - אפקט מטורף בלי להכביד על הקנבס */
        .crt-overlay {
            position: absolute; top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 4px, 6px 100%;
            box-shadow: inset 0 0 100px rgba(0,0,0,0.9);
            pointer-events: none;
            z-index: 5;
            border-radius: 10px;
        }

        .ui-layer {
            position: absolute; top: 20px; left: 20px; right: 20px;
            display: flex; justify-content: space-between;
            font-size: 22px; font-weight: 700; letter-spacing: 2px;
            text-shadow: 0 0 10px var(--neon-pink), 0 0 20px var(--neon-pink);
            pointer-events: none; z-index: 10;
        }

        .level-up {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            font-size: 80px; color: var(--neon-yellow); font-weight: 900;
            text-shadow: 0 0 20px var(--neon-pink), 0 0 40px var(--neon-yellow);
            display: none;
            pointer-events: none; z-index: 20; white-space: nowrap;
        }

        @keyframes popUp {
            0% { opacity: 0; transform: translate(-50%, -20%) scale(0.5); }
            10% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
            20% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            100% { opacity: 0; transform: translate(-50%, -80%) scale(1.5); }
        }

        .start-screen {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(5, 5, 15, 0.85); display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 100;
            border-radius: 10px; text-align: center;
        }

        .start-screen h1 {
            color: var(--neon-blue); text-shadow: 0 0 20px var(--neon-blue), 0 0 40px var(--neon-pink);
            font-size: 64px; margin: 0 0 20px 0; font-style: italic; letter-spacing: 5px;
        }

        .btn {
            background: transparent; border: 3px solid var(--neon-pink);
            color: white; padding: 15px 50px; text-transform: uppercase;
            font-family: inherit; font-size: 28px; font-weight: bold;
            cursor: pointer; transition: 0.3s; margin-top: 30px;
            text-shadow: 0 0 10px var(--neon-pink); box-shadow: 0 0 15px rgba(255,0,255,0.4);
        }

        .btn:hover {
            background: var(--neon-pink); color: black; text-shadow: none;
            box-shadow: 0 0 40px var(--neon-pink), inset 0 0 20px white; transform: scale(1.05);
        }

        .controls-hint {
            position: absolute; bottom: 15px; width: 100%; text-align: center;
            color: rgba(255, 255, 255, 0.4); font-size: 14px; letter-spacing: 1px; z-index: 10;
        }
        
        .screen-shake {
            animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
        }

        @keyframes shake {
            10%, 90% { transform: translate3d(-3px, 0, 0); }
            20%, 80% { transform: translate3d(4px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-8px, 0, 0); }
            40%, 60% { transform: translate3d(8px, 0, 0); }
        }
    </style>
</head>
<body>
    <div class="game-container" id="container">
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div class="crt-overlay"></div>
        
        <div class="ui-layer">
            <div>SCORE: <span id="score" style="color: var(--neon-blue);">0000</span></div>
            <div>LEVEL: <span id="level" style="color: var(--neon-yellow);">1</span></div>
            <div>MULTIPLIER: <span id="bits" style="color: var(--neon-pink);">x1</span></div>
        </div>

        <div id="start-screen" class="start-screen">
            <h1>NEON OVERDRIVE</h1>
            <p style="font-size: 18px; color: #ddd; max-width: 500px; line-height: 1.8;">
                Welcome to 2084. Dodge the <span style="color:#f00; text-shadow:0 0 5px #f00">RED spikes</span>.<br>
                Collect the <span style="color:#0ff; text-shadow:0 0 5px #0ff">BLUE cores</span> to increase score multiplier.<br>
            </p>
            <button class="btn" onclick="startGame()">INITIATE SEQUENCE</button>
        </div>

        <div id="level-alert" class="level-up">LEVEL UP!</div>
        <div class="controls-hint">ARROWS / A & D TO STEER • SURVIVE</div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const container = document.getElementById('container');
        
        // --- WebAudio Synthesizer Engine (NO ASSETS NEEDED) ---
        let audioCtx;
        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function playSound(type) {
            if (!audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);

            const now = audioCtx.currentTime;
            if (type === 'collect') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(800, now);
                osc.frequency.exponentialRampToValueAtTime(1600, now + 0.1);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.start(now); osc.stop(now + 0.1);
            } else if (type === 'explode') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(100, now);
                osc.frequency.exponentialRampToValueAtTime(10, now + 0.5);
                gain.gain.setValueAtTime(0.5, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
                osc.start(now); osc.stop(now + 0.5);
            } else if (type === 'levelup') {
                osc.type = 'square';
                [400, 600, 800, 1200].forEach((freq, i) => {
                    setTimeout(() => {
                        if(audioCtx.state === 'closed') return;
                        const o = audioCtx.createOscillator();
                        const g = audioCtx.createGain();
                        o.connect(g); g.connect(audioCtx.destination);
                        o.type = 'square'; o.frequency.value = freq;
                        g.gain.setValueAtTime(0.1, audioCtx.currentTime);
                        g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                        o.start(); o.stop(audioCtx.currentTime + 0.1);
                    }, i * 100);
                });
            }
        }

        // --- Game State & Variables ---
        let gameRunning = false;
        let score = 0, level = 1, multiplier = 1, consecutiveBits = 0;
        let baseSpeed = 4; // <--- תיקון: הופחת מ-7 ל-4 להתחלה רגועה יותר
        let globalZOffset = 0; 
        
        let player = { 
            x: 400, y: 520, vx: 0, w: 30, h: 40, trail: [] 
        };
        
        let entities = [];
        let particles = [];
        let keys = {};

        window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
        window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

        function startGame() {
            initAudio(); 
            document.getElementById('start-screen').style.display = 'none';
            container.classList.remove('screen-shake');
            gameRunning = true;
            score = 0; level = 1; multiplier = 1; consecutiveBits = 0; 
            baseSpeed = 4; // תיקון מהירות התחלתית
            entities = []; particles = [];
            player.x = 400; player.vx = 0; player.trail = [];
            requestAnimationFrame(gameLoop);
        }

        function createExplosion(x, y, color, amount=20) {
            for(let i=0; i<amount; i++) {
                particles.push({
                    x, y,
                    vx: (Math.random() - 0.5) * 15, vy: (Math.random() - 0.5) * 15,
                    life: 1.0, decay: Math.random() * 0.03 + 0.01, color, size: Math.random() * 5 + 2
                });
            }
        }

        function spawnEntity() {
            let r = Math.random();
            // הגברנו מעט את הסיכוי להופעת מכשולים כדי שלא יהיה "ריק" מידי כשהמהירות נמוכה
            if(r < 0.06 + (level * 0.006)) { 
                entities.push({ type: 'obstacle', x: Math.random() * 700 + 50, y: -50, w: 35, h: 35, dead: false });
            }
            if(Math.random() < 0.05) { 
                entities.push({ type: 'bit', x: Math.random() * 700 + 50, y: -50, r: 12, dead: false });
            }
        }

        function updateUI() {
            document.getElementById('score').innerText = String(Math.floor(score)).padStart(5, '0');
            document.getElementById('level').innerText = level;
            document.getElementById('bits').innerText = 'x' + multiplier;
            if(multiplier > 1) document.getElementById('bits').style.textShadow = '0 0 20px var(--neon-yellow)';
            else document.getElementById('bits').style.textShadow = '0 0 10px var(--neon-pink)';
        }

        function gameLoop() {
            if(!gameRunning) return;

            // Physics & Movement 
            player.vx *= 0.80; // <--- תיקון: חיכוך מוגבר (80 במקום 85) לשליטה הדוקה ועצירה מהירה יותר
            if(keys['arrowleft'] || keys['a']) player.vx -= 1.6; // תיקון האצה
            if(keys['arrowright'] || keys['d']) player.vx += 1.6;
            player.x += player.vx;
            
            // Wall bounce
            if(player.x < 30) { player.x = 30; player.vx *= -0.5; }
            if(player.x > 770 - player.w) { player.x = 770 - player.w; player.vx *= -0.5; }

            // Player Trail
            player.trail.push({x: player.x, y: player.y});
            if(player.trail.length > 15) player.trail.shift();

            // Scrolling background Grid
            globalZOffset = (globalZOffset + baseSpeed) % 40;

            spawnEntity();

            // Entities update
            entities.forEach(ent => {
                // <--- תיקון: הקטנת מהירות הנפילה היחסית של המשולשים מ-1.2 ל-1.15 כדי לתת יותר זמן תגובה
                ent.y += baseSpeed * (ent.type === 'bit' ? 1 : 1.15); 
                
                // Out of bounds
                if(ent.y > 650) {
                    ent.dead = true;
                    if(ent.type === 'obstacle') score += 10 * multiplier;
                    if(ent.type === 'bit') { multiplier = 1; consecutiveBits = 0; }
                }

                // Collisions 
                let px = player.x + player.w/2; let py = player.y + player.h/2;
                if(!ent.dead) {
                    if(ent.type === 'obstacle') {
                        let dist = Math.hypot(px - (ent.x + ent.w/2), py - (ent.y + ent.h/2));
                        if(dist < 22) { // Hit
                            gameRunning = false;
                            playSound('explode');
                            createExplosion(px, py, '#ff0055', 50);
                            container.classList.add('screen-shake');
                            setTimeout(() => {
                                document.getElementById('start-screen').style.display = 'flex';
                                document.querySelector('.start-screen h1').innerText = 'SYSTEM FAILURE';
                                document.querySelector('.start-screen p').innerHTML = `FINAL SCORE: <b style="color:var(--neon-yellow); font-size:24px">${Math.floor(score)}</b>`;
                            }, 1500);
                        }
                    } else if(ent.type === 'bit') {
                        let dist = Math.hypot(px - ent.x, py - ent.y);
                        if(dist < 30) { // Collect
                            ent.dead = true;
                            consecutiveBits++;
                            if(consecutiveBits % 3 === 0 && multiplier < 10) multiplier++;
                            score += 50 * multiplier;
                            playSound('collect');
                            createExplosion(ent.x, ent.y, '#00ffff', 10);
                        }
                    }
                }
            });

            // Cleanup dead entities
            entities = entities.filter(ent => !ent.dead);

            // Particles update
            particles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                p.life -= p.decay;
                p.vx *= 0.95; p.vy *= 0.95;
            });
            particles = particles.filter(p => p.life > 0);

            // Level Up logic
            if(score > level * level * 600) { // תיקון: הורדנו קצת את יעד הניקוד לשלב כי הניקוד עולה לאט יותר
                level++;
                baseSpeed += 0.4; // <--- תיקון: המהירות עולה רק ב-0.4 (ולא 0.8) בכל שלב
                playSound('levelup');
                let alertEl = document.getElementById('level-alert');
                alertEl.style.display = 'block';
                alertEl.style.animation = 'none';
                void alertEl.offsetWidth; // trigger reflow
                alertEl.style.animation = 'popUp 1.5s ease-out forwards';
                setTimeout(() => { alertEl.style.display = 'none'; }, 1500);
            }

            score += 0.1 * multiplier; 
            updateUI();
            draw();
            requestAnimationFrame(gameLoop);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const sunY = 180;
            const gradient = ctx.createLinearGradient(0, sunY-120, 0, sunY+120);
            gradient.addColorStop(0, '#ffff00'); gradient.addColorStop(0.5, '#ff00ff'); gradient.addColorStop(1, '#aa00ff');
            ctx.fillStyle = gradient;
            ctx.beginPath(); ctx.arc(400, sunY, 120, 0, Math.PI * 2); ctx.fill();
            
            ctx.fillStyle = '#000'; 
            for(let i=0; i<6; i++) {
                let h = 3 + i*1.5;
                ctx.fillRect(250, sunY + 20 + i*16, 300, h);
            }

            ctx.strokeStyle = 'rgba(255, 0, 255, 0.3)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            const horizon = 300;
            ctx.moveTo(0, horizon); ctx.lineTo(800, horizon);
            
            for(let i=-20; i<=20; i++) {
                let xTop = 400 + i*15;
                let xBottom = 400 + i*60;
                ctx.moveTo(xTop, horizon); ctx.lineTo(xBottom, 600);
            }
            
            for(let y = horizon + (globalZOffset * 0.1); y < 600; y += (y - horizon) * 0.1 + 1) {
                ctx.moveTo(0, y); ctx.lineTo(800, y);
            }
            ctx.stroke();

            ctx.globalCompositeOperation = "lighter";

            if(gameRunning) {
                ctx.beginPath();
                for(let i=0; i<player.trail.length; i++) {
                    let pt = player.trail[i];
                    ctx.lineTo(pt.x + player.w/2, pt.y + player.h);
                }
                ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
                ctx.lineWidth = 10;
                ctx.shadowBlur = 15;
                ctx.shadowColor = '#00ffff';
                ctx.stroke();
            }

            ctx.shadowBlur = 20;

            entities.forEach(ent => {
                if(ent.type === 'obstacle') {
                    ctx.shadowColor = '#ff0055'; ctx.fillStyle = '#ff0055';
                    ctx.beginPath();
                    ctx.moveTo(ent.x + ent.w/2, ent.y); 
                    ctx.lineTo(ent.x + ent.w, ent.y + ent.h); 
                    ctx.lineTo(ent.x, ent.y + ent.h); 
                    ctx.closePath();
                    ctx.fill();
                    ctx.fillStyle = '#ffffff'; ctx.shadowBlur = 0;
                    ctx.beginPath();
                    ctx.moveTo(ent.x + ent.w/2, ent.y + 10);
                    ctx.lineTo(ent.x + ent.w - 8, ent.y + ent.h - 5);
                    ctx.lineTo(ent.x + 8, ent.y + ent.h - 5);
                    ctx.fill();
                    ctx.shadowBlur = 20; 
                } else if(ent.type === 'bit') {
                    ctx.shadowColor = '#00ffff'; ctx.fillStyle = '#00ffff';
                    ctx.beginPath();
                    ctx.arc(ent.x, ent.y, ent.r, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.arc(ent.x, ent.y, ent.r + (Math.sin(Date.now()*0.01)*5 + 5), 0, Math.PI*2);
                    ctx.stroke();
                }
            });

            particles.forEach(p => {
                ctx.globalAlpha = p.life;
                ctx.fillStyle = p.color;
                ctx.shadowColor = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
            });
            ctx.globalAlpha = 1.0;

            if (gameRunning || particles.length < 40) {
                ctx.shadowColor = '#fff'; ctx.fillStyle = '#eef';
                ctx.beginPath();
                ctx.moveTo(player.x + player.w/2, player.y);
                ctx.lineTo(player.x + player.w + (player.vx*2), player.y + player.h);
                ctx.lineTo(player.x + player.w/2, player.y + player.h - 10); 
                ctx.lineTo(player.x - (player.vx*2), player.y + player.h);
                ctx.closePath();
                ctx.fill();
                
                ctx.shadowColor = '#ff00ff'; ctx.fillStyle = '#ff00ff';
                ctx.beginPath();
                ctx.arc(player.x + player.w/2, player.y + player.h - 5, Math.random()*5+3, 0, Math.PI*2);
                ctx.fill();
            }
            
            ctx.globalCompositeOperation = "source-over"; 
            ctx.shadowBlur = 0; 
        }
        
        draw();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(NEON_HTML)

if __name__ == '__main__':
    app.run(port=5010, debug=True)
