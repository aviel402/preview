from flask import Flask, render_template_string, jsonify, request
import json
import maps9
import txt9

app = Flask(__name__)
app.secret_key = 'clover_fast_heroes_v10'

PLAYER_DATA = {"shards": 0, "max_stage_reached": 1}

@app.route('/')
def idx():
    game_maps = maps9.generate_maps()
    return render_template_string(GAME_HTML, 
                                  maps_json=json.dumps(game_maps),
                                  texts=json.dumps(txt9.TEXTS),
                                  heroes_texts=json.dumps(txt9.HERO_TEXTS))

@app.route('/save', methods=['POST'])
def save_progress():
    global PLAYER_DATA
    try:
        data = request.json
        PLAYER_DATA["shards"] += data.get("shards", 0)
        if data.get("stage", 1) > PLAYER_DATA["max_stage_reached"]:
            PLAYER_DATA["max_stage_reached"] = data.get("stage", 1)
        return jsonify(PLAYER_DATA)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

GAME_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NEON CLOVER - SPEED UPDATE</title>
    <link href="https://fonts.googleapis.com/css2?family=Righteous&family=Jura:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #00f3ff; --neon-red: #ff003c; --neon-green: #00ff66; --bg-dark: #0a0a0f; }
        * { box-sizing: border-box; touch-action: manipulation; }
        body { margin: 0; overflow: hidden; background: var(--bg-dark); font-family: 'Jura', sans-serif; color: white; user-select: none; }
        canvas { display: block; width: 100%; height: 100vh; image-rendering: pixelated; position: absolute; z-index: 1; }
        
        /* CRT Scanlines */
        body::before { content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0; 
                       background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%); z-index: 200; background-size: 100% 3px; pointer-events: none; }
        
        .screen { position: absolute; top:0; left:0; width:100%; height:100%; z-index: 300; 
            background: rgba(10, 10, 15, 0.95); display:flex; flex-direction:column; align-items:center; justify-content:center; overflow-y:auto; backdrop-filter: blur(5px);}
        .hidden { display: none !important; opacity:0; pointer-events:none;}
        
        h1.title { font-family: 'Righteous', cursive; font-size: clamp(40px, 8vw, 90px); margin:0; text-transform: uppercase; letter-spacing: 4px;
                   color: var(--gold); text-shadow: 0 0 20px var(--gold), 0 0 40px #00aaff;}
        
        #dev-panel { background: rgba(0,243,255,0.1); border: 1px solid var(--gold); padding: 15px; border-radius: 5px; margin-bottom: 20px; display: none; text-align:center;}
        #dev-panel select, #dev-panel button { padding: 8px; font-size: 14px; margin: 5px; font-family: 'Jura'; background:#111; color:var(--gold); border:1px solid var(--gold);}

        .info-chest { background: rgba(0,0,0,0.8); border-left: 4px solid var(--gold); padding: 20px; max-width: 800px; margin-top: 20px; text-align: right; box-shadow: -10px 0 20px rgba(0,243,255,0.1); }
        .info-chest h3 { color: var(--gold); margin-top: 0; font-family:'Righteous'; letter-spacing:1px;}
        .info-chest ul { list-style: none; padding: 0; margin:0;}
        .info-chest li { margin-bottom: 8px; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px; color:#ccc;}

        .char-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; width: 95%; max-width: 1200px; margin-top:30px; padding-bottom: 50px;}
        .char-card { background: rgba(20,20,30,0.8); border: 1px solid #333; padding: 20px; border-radius: 8px; cursor: pointer; text-align: center; transition: all 0.2s; position: relative; border-bottom: 3px solid var(--card-color);}
        .char-card:hover { transform: translateY(-5px); border-color: var(--card-color); box-shadow: 0 10px 20px rgba(0,0,0,0.8), 0 0 15px var(--card-color) inset;}
        .char-card h3 { margin: 0 0 10px 0; font-family: 'Righteous'; font-size: 26px; text-transform:uppercase; color:var(--card-color);}
        
        #ui-layer { position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:100; display:flex; flex-direction:column; padding:20px; justify-content:space-between; }
        
        /* Mobile System Override */
        .mobile-ui { position: absolute; bottom: 20px; width: 100%; left: 0; display: none; pointer-events: none; padding: 0 20px; justify-content: space-between; z-index: 150;}
        .mob-left, .mob-right { pointer-events: auto; opacity: 0.5; transform: scale(0.85); transform-origin: bottom; }
        
        .d-pad { display: grid; grid-template-columns: 60px 60px 60px; grid-template-rows: 60px 60px 60px; gap: 5px;}
        .action-btns { display: grid; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(3, 60px); gap: 5px; justify-content: end; }
        
        .btn-mob { background: rgba(0,0,0,0.6); border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; color: white; font-weight: 900; font-size: 18px; cursor: pointer; font-family:'Righteous'; transition:0.1s;}
        .btn-mob:active { background: rgba(0,243,255,0.8); color: black; border-color:var(--gold); transform: scale(0.9); }

        .top-right-controls { display: flex; flex-direction: column; gap: 10px; align-items: flex-end; pointer-events: auto;}
        .toggle-btn { padding: 8px 16px; font-family: 'Jura'; font-size: 14px; font-weight:bold; background: rgba(0,0,0,0.8); color: #fff; border: 1px solid var(--gold); border-radius: 4px; cursor: pointer; transition: 0.2s; text-shadow:0 0 5px var(--gold);}
        .toggle-btn:hover { background: var(--gold); color: #000;}

        .hud-top { display: flex; justify-content: space-between; align-items: flex-start; width: 100%; }
        .stats-panel { background: rgba(0,0,0,0.6); border: 1px solid #333; padding: 15px; border-radius: 8px; border-left: 3px solid var(--gold); backdrop-filter: blur(3px);}
        .stat-bar-container { display: flex; align-items: center; margin-bottom:8px; width:280px; }
        .stat-icon { font-weight:900; margin-left: 10px; width:40px; font-family:'Righteous'; font-size: 16px; letter-spacing: 1px;}
        .bar-out { background: rgba(0,0,0,0.8); flex-grow: 1; height: 14px; border: 1px solid #444; position:relative; overflow:hidden;}
        .bar-in { height:100%; transition: width 0.1s;}
        .hp-bar { background: var(--neon-green); box-shadow: 0 0 10px var(--neon-green); }
        .en-bar { background: var(--gold); box-shadow: 0 0 10px var(--gold); }
        
        .stage-title { position: absolute; left: 50%; transform: translateX(-50%); font-family: 'Righteous'; font-size:24px; color:#fff; text-shadow:0 0 10px var(--gold); background:rgba(0,0,0,0.6); padding:5px 20px; border:1px solid var(--gold); border-radius:4px;}
        
        .menu-btn { padding:15px 40px; border:1px solid var(--gold); border-radius:4px; color:var(--gold); font-size:20px; font-family:'Righteous'; font-weight:900; background:rgba(0,0,0,0.8); cursor:pointer; margin-top:20px; transition:0.2s; width: 350px; max-width: 90vw; letter-spacing:1px;}
        .menu-btn:hover { background:var(--gold); color:#000; box-shadow:0 0 20px var(--gold);}
        
        kbd { background: #222; color: var(--gold); padding: 2px 6px; border-radius: 4px; border: 1px solid #444; font-weight: bold; margin:0 3px;}
        #stage-alert { position: absolute; top:40%; left:50%; transform: translate(-50%, -50%); font-family:'Righteous'; font-size: 6vw; opacity:0; color:var(--gold); text-shadow: 0 0 20px var(--gold); text-align:center; z-index: 100; letter-spacing:5px;}
        #shard-hud { color: var(--gold); font-family: 'Righteous'; font-size: 18px; margin-top: 10px; text-align: left; text-shadow: 0 0 5px var(--gold);}
    </style>
</head>
<body>

<div id="select-screen" class="screen">
    <div id="dev-panel">
        <h2 id="t-dev-title"></h2>
        <select id="dev-stage"> <script>for(let i=1;i<=20;i++) document.write(`<option value="${i}">Warp -> Stage ${i}</option>`);</script> </select>
        <button id="t-dev-btn" onclick="startMission(HEROES[0], true)"></button>
    </div>

    <h1 class="title" id="t-main-title"></h1><h2 id="t-main-sub" style="margin-top:-5px; color:#fff; font-family:'Jura'; letter-spacing:2px; font-weight:300;"></h2>
    
    <div class="info-chest">
        <h3 id="t-htp-title"></h3><p id="t-htp-desc" style="white-space: pre-line; line-height:1.6;"></p>
        <h3 id="t-ctrl-title"></h3><ul id="t-ctrl-list" style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;"></ul>
    </div>
    <div class="char-grid" id="roster"></div>
</div>

<div id="pause-screen" class="screen hidden">
    <h1 class="title" id="t-pause" style="color:var(--gold); margin-bottom: 20px;"></h1>
    <button class="menu-btn" onclick="togglePause()" id="btn-resume"></button>
    <button class="menu-btn" onclick="location.reload()" id="btn-restart" style="color:var(--neon-red); border-color:var(--neon-red);"></button>
</div>

<div id="ui-layer" class="hidden">
    <div class="hud-top">
        <div class="stats-panel" style="direction: ltr;">
            <div class="stat-bar-container"><span class="stat-icon" style="color:var(--neon-green);">HP</span>
                <div class="bar-out"><div class="bar-in hp-bar" id="hp-bar"></div></div> <span id="hp-t" style="color:#aaa;font-size:12px;margin-left:5px; width:40px; text-align:right;"></span></div>
            <div class="stat-bar-container"><span class="stat-icon" style="color:var(--gold);">EN</span>
                <div class="bar-out"><div class="bar-in en-bar" id="en-bar"></div></div> <span id="en-t" style="color:#aaa;font-size:12px;margin-left:5px; width:40px; text-align:right;"></span></div>
            <div id="shard-hud">SHARDS: 0</div>
        </div>
        <div class="stage-title" id="stage-info">...</div>
        
        <div class="top-right-controls">
             <button class="toggle-btn" id="t-mobile-toggle" onclick="toggleMobileUI()"></button>
             <button class="toggle-btn" onclick="togglePause()">⏸ PAUSE <kbd>ESC</kbd></button>
        </div>
    </div>
    
    <div id="stage-alert"></div>
    
    <!-- Mobile UI Fixed -->
    <div class="mobile-ui" id="mob-ui">
        <div class="mob-left d-pad">
            <div></div><button class="btn-mob" ontouchstart="mk('KeyW')" ontouchend="rk('KeyW')">W</button><div></div>
            <button class="btn-mob" ontouchstart="mk('KeyA')" ontouchend="rk('KeyA')">A</button> 
            <button class="btn-mob" ontouchstart="mk('KeyS')" ontouchend="rk('KeyS')">S</button> 
            <button class="btn-mob" ontouchstart="mk('KeyD')" ontouchend="rk('KeyD')">D</button>
        </div>
        <div class="mob-right action-btns">
            <button class="btn-mob" ontouchstart="mk('KeyH')" ontouchend="rk('KeyH')">H</button> 
            <button class="btn-mob" ontouchstart="mk('KeyJ')" ontouchend="rk('KeyJ')">J</button> 
            <button class="btn-mob" ontouchstart="mk('KeyK')" ontouchend="rk('KeyK')">K</button> 
            <button class="btn-mob" style="color:var(--neon-green);" ontouchstart="mk('KeyE')" ontouchend="rk('KeyE')">E</button> 
            <button class="btn-mob" style="color:var(--gold);" ontouchstart="mk('KeyU')" ontouchend="rk('KeyU')">U</button> 
            <button class="btn-mob" ontouchstart="mk('KeyI')" ontouchend="rk('KeyI')">I</button> 
            <div></div>
            <button class="btn-mob" style="color:var(--neon-red);" ontouchstart="mk('KeyY')" ontouchend="rk('KeyY')">Y</button>
        </div>
    </div>
</div>

<div id="death-screen" class="screen hidden" style="z-index:400;">
    <h1 class="title" id="t-death" style="color:var(--neon-red); text-shadow: 0 0 20px var(--neon-red);"></h1>
    <h2 style="font-size:20px; font-weight:normal; color:#ccc;"><span id="t-death-sub"></span> <span id="final-lvl" style="color:white; font-family:'Righteous'; font-size:24px;"></span> </h2>
    <button class="menu-btn" onclick="location.reload()" id="btn-retry" style="color:var(--neon-red); border-color:var(--neon-red); margin-top: 40px;"></button>
</div>

<div id="victory-screen" class="screen hidden" style="z-index:500;">
    <h1 class="title" id="t-vic" style="color:var(--neon-green); text-shadow: 0 0 30px var(--neon-green);"></h1>
    <h2 id="t-vic-sub" style="font-size:18px; line-height:1.6; max-width: 600px; text-align:center; font-weight:normal; color:#ddd;"></h2>
    <button class="menu-btn" onclick="location.href='/'" id="btn-home" style="color:var(--neon-green); border-color:var(--neon-green); margin-top:50px;"></button>
</div>

<script>
const MAPS = {{ maps_json | safe }}; const TEXTS = {{ texts | safe }}; const HERO_TEXTS = {{ heroes_texts | safe }};

// Set DOM Texts
document.getElementById('t-main-title').innerText = TEXTS.title_main; document.getElementById('t-main-sub').innerText = TEXTS.subtitle_main; document.getElementById('t-htp-title').innerText = TEXTS.how_to_play_title; document.getElementById('t-htp-desc').innerText = TEXTS.how_to_play_desc; document.getElementById('t-ctrl-title').innerText = TEXTS.controls_title; document.getElementById('t-pause').innerText = TEXTS.pause_title; document.getElementById('btn-resume').innerText = TEXTS.btn_resume; document.getElementById('btn-restart').innerText = TEXTS.btn_restart; document.getElementById('t-death').innerText = TEXTS.death_title; document.getElementById('t-death-sub').innerText = TEXTS.death_sub; document.getElementById('btn-retry').innerText = TEXTS.btn_retry; document.getElementById('t-vic').innerText = TEXTS.victory_title; document.getElementById('t-vic-sub').innerText = TEXTS.victory_sub; document.getElementById('btn-home').innerText = TEXTS.btn_home; document.getElementById('t-mobile-toggle').innerText = TEXTS.mobile_toggle; document.getElementById('t-dev-title').innerText = TEXTS.dev_title; document.getElementById('t-dev-btn').innerText = TEXTS.dev_btn;
let clist = ""; TEXTS.controls_list.forEach(c => clist += `<li>${c}</li>`); document.getElementById('t-ctrl-list').innerHTML = clist;
if(new URLSearchParams(window.location.search).get('x') === 'v') { document.getElementById('dev-panel').style.display = 'block'; }

const activeKeys = {};
window.addEventListener('keydown', e => { 
    if(e.code==='Space') e.preventDefault(); 
    if(e.code === 'KeyP' || e.code === 'Escape') togglePause();
    activeKeys[e.code]=true;
}); window.addEventListener('keyup', e => { activeKeys[e.code]=false; });
function kd(c) { return activeKeys[c]===true; } function mk(c){activeKeys[c]=true;} function rk(c){activeKeys[c]=false;}
let isMobUI=false; function toggleMobileUI(){isMobUI=!isMobUI; document.getElementById('mob-ui').style.display=isMobUI?'flex':'none';}
function intersect(a,b){return!(b.x>a.x+a.w || b.x+b.w<a.x || b.y>a.y+a.h || b.y+b.h<a.y);}

// HEROES CONFIG - SPEEDS INCREASED SIGNIFICANTLY!
const HEROES =[
    { id: 'earth', col: '#2ecc71', maxHp: 180, hpRegen: 0.01, speed: 4.0, jump: 15, maxEn: 100, dmgMult: 1.2, enCostMult: 1, pCol: '#27ae60'},
    { id: 'fire', col: '#e74c3c', maxHp: 80, hpRegen: 0, speed: 6.5, jump: 17, maxEn: 120, dmgMult: 1.8, enCostMult: 1, pCol: '#ff7979'},
    { id: 'water', col: '#3498db', maxHp: 110, hpRegen: 0.15, speed: 5.0, jump: 16, maxEn: 110, dmgMult: 1.0, enCostMult: 1, pCol: '#7ed6df'},
    { id: 'air', col: '#ecf0f1', maxHp: 90, hpRegen: 0, speed: 7.0, jump: 20, maxEn: 100, dmgMult: 0.8, enCostMult: 0.7, pCol: '#c7ecee'},
    { id: 'lightning', col: '#f1c40f', maxHp: 90, hpRegen: 0, speed: 8.5, jump: 16, maxEn: 100, dmgMult: 1.5, enCostMult: 1.5, pCol: '#f9ca24'},
    { id: 'magma', col: '#d35400', maxHp: 160, hpRegen: 0.05, speed: 3.5, jump: 13, maxEn: 100, dmgMult: 1.6, enCostMult: 1.2, pCol: '#eb4d4b'},
    { id: 'light', col: '#ffffb3', maxHp: 100, hpRegen: 0.02, speed: 5.5, jump: 16, maxEn: 300, dmgMult: 0.9, enCostMult: 0.8, pCol: '#fff200'},
    { id: 'dark', col: '#8e44ad', maxHp: 85, hpRegen: 0, speed: 6.0, jump: 16, maxEn: 120, dmgMult: 1.0, enCostMult: 1.0, pCol: '#9b59b6'}
];

function createSelectMenu() {
    let box = document.getElementById('roster');
    HEROES.forEach(h => {
        let ht = HERO_TEXTS[h.id]; let d = document.createElement('div');
        d.className='char-card'; d.style.setProperty('--card-color', h.col);
        d.innerHTML = `<h3 style="color:${h.col};">${ht.name}</h3><div style="font-size:12px;color:#aaa;line-height:1.4;">${ht.desc}</div>`;
        d.onclick=()=>{startMission(h, false);}; box.appendChild(d);
    });
}

const canvas = document.createElement('canvas'); const ctx = canvas.getContext('2d'); document.body.appendChild(canvas);
window.addEventListener('resize',()=>{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; ctx.imageSmoothingEnabled=false; }); window.dispatchEvent(new Event('resize'));

// --- UNIQUE CHARACTER DESIGNS ---
function drawPlayerSprite(context, tx, ty, w, h, cId, pCol, isFaceRight, isCrouch, vx) {
    context.save(); context.translate(tx, ty); 
    if(!isFaceRight){ context.scale(-1, 1); context.translate(-w, 0); } 

    let bx = 0; let bw = w; 
    let walkBounce = Math.abs(vx) > 0.5 ? Math.sin(f/5)*3 : 0;
    
    // Shadow
    context.fillStyle = 'rgba(0,0,0,0.5)'; context.fillRect(bx+5, h-2, bw-10, 4);
    
    context.translate(0, walkBounce);

    if (cId === 'earth') { // TITAN
        context.fillStyle = '#4a5d23'; context.fillRect(bx-4, 10, bw+8, h-10); // Massive body
        context.fillStyle = '#27ae60'; context.fillRect(bx, 0, bw, 15); // Head
        context.fillStyle = '#2ecc71'; context.fillRect(bx-8, 15, 12, 20); // Pauldron
        context.fillStyle = '#fff'; context.fillRect(bx+bw-8, 5, 4, 4); // Eye
    } 
    else if (cId === 'fire') { // BLAZE
        context.fillStyle = '#c0392b'; context.fillRect(bx+4, 15, bw-8, h-15); // Slim body
        context.fillStyle = '#e74c3c'; context.beginPath(); context.arc(bx+bw/2, 10, 10, 0, Math.PI*2); context.fill(); // Round head
        // Flame hair
        context.fillStyle = '#f1c40f'; context.beginPath(); context.moveTo(bx+bw/2, 10); context.lineTo(bx+bw/2-5+Math.sin(f/2)*5, -10); context.lineTo(bx+bw/2+5, 5); context.fill();
        context.fillStyle = '#fff'; context.fillRect(bx+bw/2+2, 5, 4, 4);
    }
    else if (cId === 'water') { // AQUA
        context.fillStyle = '#2980b9'; context.fillRect(bx, 10, bw, h-10); // Robe
        context.fillStyle = '#3498db'; context.beginPath(); context.moveTo(bx, 15); context.lineTo(bx+bw/2, 0); context.lineTo(bx+bw, 15); context.fill(); // Hood
        context.fillStyle = '#111'; context.fillRect(bx+bw/2, 5, 10, 10); // Face hidden
        context.fillStyle = '#7ed6df'; context.fillRect(bx+bw/2+4, 8, 4, 4); // Glowing eye
    }
    else if (cId === 'air') { // ZEPHYR
        context.fillStyle = '#bdc3c7'; context.fillRect(bx+5, 10, bw-10, h-10); // Agile body
        context.fillStyle = '#ecf0f1'; context.beginPath(); context.arc(bx+bw/2, 8, 8, 0, Math.PI*2); context.fill(); // Head
        // Scarf
        context.fillStyle = '#fff'; context.fillRect(bx-15-Math.sin(f/3)*5, 10, 20, 5);
        context.fillStyle = '#3498db'; context.fillRect(bx+bw/2+2, 5, 4, 2); // Visor
    }
    else if (cId === 'lightning') { // VOLT
        context.fillStyle = '#111'; context.fillRect(bx+5, 10, bw-10, h-10); // Dark suit
        context.fillStyle = '#f1c40f'; context.fillRect(bx+5, 0, bw-10, 12); // Yellow helmet
        // Lightning horns
        context.beginPath(); context.moveTo(bx+5, 0); context.lineTo(bx-5, -10); context.lineTo(bx+10, -5); context.fill();
        context.beginPath(); context.moveTo(bx+bw-5, 0); context.lineTo(bx+bw+5, -10); context.lineTo(bx+bw-10, -5); context.fill();
        context.fillStyle = '#fff'; context.fillRect(bx+bw-8, 4, 6, 4); // Visor
    }
    else if (cId === 'magma') { // CORE
        context.fillStyle = '#8e44ad'; context.fillRect(bx, 5, bw, h-5); // Dark rock body
        context.fillStyle = '#d35400'; context.fillRect(bx+5, h/2-5, bw-10, 10); // Magma core
        context.fillStyle = '#eb4d4b'; context.fillRect(bx+bw-10, 10, 6, 6); // Eye
        if(f%10<5) { context.fillStyle = '#f1c40f'; context.fillRect(bx+10, h/2-2, 4, 4); } // Core pulse
    }
    else if (cId === 'light') { // PULSE
        context.fillStyle = '#fff'; context.fillRect(bx+5, 15, bw-10, h-15); // Bright body
        context.fillStyle = '#ffffb3'; context.beginPath(); context.arc(bx+bw/2, 10, 9, 0, Math.PI*2); context.fill(); // Head
        // Halo
        context.strokeStyle = '#f1c40f'; context.lineWidth=2; ctx.beginPath(); ctx.ellipse(bx+bw/2, -5+Math.sin(f/5)*3, 12, 4, 0, 0, Math.PI*2); ctx.stroke();
        context.fillStyle = '#f1c40f'; context.fillRect(bx+bw/2+2, 8, 4, 4);
    }
    else if (cId === 'dark') { // VOID
        context.fillStyle = '#2c3e50'; context.fillRect(bx, 10, bw, h-10); // Dark body
        context.fillStyle = '#8e44ad'; context.fillRect(bx, 15, bw, h-20); // Cloak
        context.fillStyle = '#111'; context.beginPath(); context.arc(bx+bw/2, 10, 10, 0, Math.PI*2); context.fill(); // Head
        context.fillStyle = '#ff003c'; context.fillRect(bx+bw/2+4, 8, 4, 4); // Red eye
    }
    else {
        // Fallback
        context.fillStyle = '#000'; context.fillRect(bx-2, -2, bw+4, h+4); 
        context.fillStyle = pCol; context.fillRect(bx, 0, bw, h); 
        context.fillStyle = '#fff'; context.fillRect(bx+bw-12, 10, 6, 6); 
    }

    context.restore();
}

function drawEnemySprite(context, tx, ty, w, h, primeCol, t_type, hpRatio, phaseFlag, isFaceRight) {
    context.save(); context.translate(tx, ty); 
    if(!isFaceRight){ context.scale(-1, 1); context.translate(-w, 0); } 

    let bx = 0; let bw = w; 
    context.fillStyle = '#000'; context.fillRect(bx-2, -2, bw+4, h+4); 
    context.fillStyle = primeCol; context.fillRect(bx, 0, bw, h); 

    if(t_type === 'bomber') {
        let inflate = 1.0 + (1-hpRatio)*0.6; context.scale(1, inflate); 
        context.fillStyle='#d35400'; context.fillRect(bx, h/3, bw, h*0.6); 
        context.fillStyle='#000'; context.fillRect(bx+bw/2, 5, 4, 15); 
        context.fillStyle='#e74c3c'; context.fillRect(bx+bw-12, h/2, 8, 6); 
    }
    else if(t_type === 'shield'){
        context.fillStyle = '#333'; context.fillRect(bx, 5, bw, h); 
        context.fillStyle = '#fff'; context.fillRect(bw-10, -5, 15, h+10); 
        context.fillStyle = '#00f3ff'; context.fillRect(bw-6, h/3, 7, 20); 
    }
    else if(t_type === 'ninja'){
        context.fillStyle = '#111'; context.fillRect(bx, 0, bw, h); 
        context.fillStyle = '#ff003c'; context.fillRect(bx-4, 12, bw+8, 6); 
        context.fillStyle = '#fff'; context.fillRect(bx+bw-8, 14, 4, 4); 
    }
    else if(t_type === 'flyer'){
        context.fillStyle = '#00f3ff'; context.beginPath(); context.arc(bw/2, h/2, w/2, 0, Math.PI*2); context.fill();
        context.fillStyle='#fff'; context.fillRect(bx-15, h/4, 20, 6); context.fillRect(bx-15, h/1.5, 20, 6); 
        context.fillStyle='#ff003c'; context.fillRect(bx+bw-12, h/2-4, 8, 8); 
    }
    else if(t_type === 'boss'){
        let c = phaseFlag===1 ? '#f39c12' : phaseFlag===2 ? '#8e44ad' : '#e74c3c';
        context.fillStyle = '#111'; context.fillRect(0,0, w, h);
        context.fillStyle = c; context.fillRect(4,4, w-8, h-8);
        context.fillStyle = '#000'; context.fillRect(w/2, 20, w/2, 20); 
        context.fillStyle = phaseFlag>2 ? '#fff':'red'; context.fillRect(w/2+10, 25, 10,8); 
        context.fillStyle='#f1c40f'; context.fillRect(-10, 0, 25, 25); 
        if(phaseFlag>=2) { context.fillStyle='#00f3ff'; context.fillRect(w/2, h/2, w+40, 6); } 
    }
    else {
        context.fillStyle = primeCol; context.fillRect(bx, 0, bw, h);
        context.fillStyle = '#000'; context.fillRect(bx+bw-12, 12, 6,6);
        if(t_type === 'shooter') { context.fillStyle='#fff'; context.fillRect(bx+bw-4, 25, 20, 4); } 
        if(t_type === 'tank') { context.fillStyle='#555'; context.fillRect(bx-5, h/3, bw+10, h/2); } 
    }
    context.restore();
}

const STAGE_WIDTH = 10000;
let pl, e_arr=[], pr_arr=[], p_pr=[], fx=[], drops=[];
let currentMap = MAPS[1]; let globalStage = 1; let f=0; let shakeV=0, camX=0;
let isPaused = false, pipe = null, cloverChest = null;
let collectedShards = 0; let shardNotif = ""; let shardNotifTimer = 0;

function doShake(amt){shakeV=amt*5;} 
function togglePause() {
    if(!pl || pl.hp<=0 || globalStage>20) return; 
    isPaused = !isPaused; document.getElementById('pause-screen').classList.toggle('hidden', !isPaused);
    if(!isPaused) for(let k in activeKeys) activeKeys[k] = false; 
}

class Pipe { 
    constructor(x) { this.w = 100; this.h = 120; this.x = x - this.w - 50; this.y = canvas.height - 80 - this.h; }
    draw() {
        ctx.fillStyle = '#111'; ctx.fillRect(this.x, this.y, this.w, this.h); 
        ctx.fillStyle = currentMap.neon; ctx.fillRect(this.x-10, this.y, this.w+20, 20);
        ctx.strokeStyle = currentMap.neon; ctx.lineWidth=2; 
        ctx.strokeRect(this.x, this.y, this.w, this.h); ctx.strokeRect(this.x-10, this.y, this.w+20, 20);
        ctx.fillStyle = '#fff'; ctx.font="24px Righteous"; ctx.fillText("⬇ S", this.x+30, this.y-20);
    }
}
class Drop {
    constructor(x,y, isB) { this.x=x; this.y=y; this.w=20; this.h=20; this.vy=-8; this.isB=isB;}
    upd() { this.vy+=0.5; this.y+=this.vy; if(this.y+this.h > canvas.height-80){this.y=canvas.height-80-this.h; this.vy=-this.vy*0.4;}
        if(intersect(this,pl)){
            if(this.isB){pl.maxHp+=20; pl.maxEn+=20; pl.hp=pl.maxHp; pl.en=pl.maxEn; makeFX(this.x,this.y, 25,'#00f3ff','boom');}
            else { pl.hp=Math.min(pl.hp+15, pl.maxHp); makeFX(this.x,this.y, 10,'#00ff66','spark'); } 
            
            collectedShards++; document.getElementById('shard-hud').innerText = "SHARDS: " + collectedShards;
            if(collectedShards % 20 === 0) { pl.maxHp+=10; pl.maxEn+=10; pl.hp=pl.maxHp; shardNotif="LEVEL UP! +MAX STATS"; shardNotifTimer=100; makeFX(pl.x,pl.y,30,'#00f3ff','boom');}
            return true;
        } return false;
    }
    draw() { ctx.fillStyle=this.isB?'#00f3ff':'#00ff66'; ctx.fillRect(this.x,this.y,this.w,this.h); ctx.strokeStyle='#fff'; ctx.lineWidth=1; ctx.strokeRect(this.x,this.y,this.w,this.h); }
}

class Player {
    constructor(c){
        this.w=36; this.h=64; this.x=100; this.y=0; this.vx=0; this.vy=0; this.c = c; this.maxHp=c.maxHp; this.hp=this.maxHp; this.maxEn=c.maxEn; this.en=this.maxEn;
        this.facing = 1; this.grounded = false; this.target = null; this.iFrames = 0; this.chargeI = 0; this.atkWait = {}; this.jCount=0;
    }
    upd() {
        if(this.hp<=0) return; this.hp = Math.min(this.hp+this.c.hpRegen, this.maxHp); if(this.iFrames>0) this.iFrames--;
        
        let crch=kd('KeyS'); let sprt=(kd('ShiftLeft')||kd('ShiftRight')); let chu=kd('KeyU'); let chi=kd('KeyI');
        if(crch && !chi){ if(this.h!==38) {this.y+=26; this.h=38; this.vx*=0.4;} } else { if(this.h!==64) {this.y-=26; this.h=64;} }

        if(chi){ this.chargeI=Math.min(this.chargeI+2, 200); makeFX(this.x+this.w/2, this.y+this.h/2,1,this.c.pCol,'spark'); if(Math.floor(this.chargeI)%10==0) doShake(0.5); 
        } else if(this.chargeI>0){
            let dmg = this.chargeI * 2.5 * this.c.dmgMult; let s = this.chargeI/3;
            p_pr.push({x:this.facing>0?this.x+this.w:this.x-s, y:this.y+20-s/2, dir:this.facing, s:25, dmg:dmg, size:s, color:this.c.pCol, tgt:this.target});
            this.vx-=(this.chargeI/8)*this.facing; this.chargeI=0; doShake(5);
        }

        // SPEED MULTIPLIERS!
        let speed = this.c.speed; 
        if(sprt) speed*=2.2; // Sprint is much faster now
        if(chu || chi || crch) speed*=0.4;
        
        if(sprt && this.grounded && f%3===0 && (kd('KeyA')||kd('KeyD'))) makeFX(this.x+10,this.y+this.h, 2, currentMap.neon,'spark');

        let nx = this.x;
        if(kd('KeyA')){nx-=speed; this.facing=-1;} if(kd('KeyD')){nx+=speed; this.facing=1;}
        
        let hitWall = false;
        currentMap.walls.forEach(w => {
            let wx = w.x; let wy = canvas.height - 80 - w.h;
            if(this.y + this.h > wy) {
                if(this.facing===1 && nx+this.w > wx && this.x+this.w <= wx) { nx = wx - this.w; hitWall=true; }
                else if(this.facing===-1 && nx < wx+w.w && this.x >= wx+w.w) { nx = wx + w.w; hitWall=true; }
            }
        });
        this.x = nx;
        
        if((kd('KeyW')||kd('Space')) && !crch){ if(!this.jHold && this.jCount<2){this.vy=-this.c.jump; this.jCount++; makeFX(this.x+15,this.y+this.h, 6, '#fff','spark'); this.jHold=true;} } else {this.jHold=false;}

        if(chu){ this.en = Math.min(this.en+1.5, this.maxEn); makeFX(this.x+this.w/2,this.y+this.h/2,1,currentMap.neon,'beam');} 
        else if(!chi) {
            this.shK('KeyH','1',8*this.c.enCostMult, 15*this.c.dmgMult, 10);
            this.shK('KeyJ','2',20*this.c.enCostMult, 35*this.c.dmgMult, 18);
            this.shK('KeyK','3',45*this.c.enCostMult, 80*this.c.dmgMult, 30);
            if(kd('KeyY')&&!this.atkWait['KeyY']) {
                if(this.en >= this.maxEn-2){
                    this.en=0; p_pr.push({x:this.facing>0?this.x+this.w:this.x-100, y:this.y-10, dir:this.facing, s:18, dmg:500*this.c.dmgMult, size:80, color:varColor('neon-red'), tgt:this.target});
                    this.vx -= 20*this.facing; doShake(12);
                } this.atkWait['KeyY']=true; 
            } else if(!kd('KeyY')) this.atkWait['KeyY']=false;
        }

        if(kd('KeyE')){if(!this.LTrig){this.swLck(); this.LTrig=true;}}else this.LTrig=false;
        if(this.target && this.target.hp<=0){this.target=null; this.getBestTrg();}

        this.vy+=0.6; this.y+=this.vy; 
        if(this.x < 50) {this.x=50;}
        if(this.x+this.w > STAGE_WIDTH) {this.x=STAGE_WIDTH-this.w;}
        
        let isG=false; let flY=canvas.height-80; 
        if(this.y+this.h>=flY){this.y=flY-this.h; this.vy=0; isG=true;} 
        else {
            currentMap.platforms.forEach(p => { 
                let pFY = canvas.height-p.y_offset;
                if(this.vy>=0 && this.y+this.h>=pFY-16 && this.y+this.h<=pFY+16 && this.x+this.w>p.x && this.x<p.x+p.w) {this.y=pFY-this.h; this.vy=0; isG=true;}
            });
            currentMap.walls.forEach(w => {
                let wY = canvas.height - 80 - w.h;
                if(this.vy>=0 && this.y+this.h>=wY-16 && this.y+this.h<=wY+16 && this.x+this.w>w.x && this.x<w.x+w.w) {this.y=wY-this.h; this.vy=0; isG=true;}
            });
        }
        if(isG){this.jCount=0; this.grounded=true;} else this.grounded=false;
        
        if(pipe && intersect(this,pipe) && crch && isG){
             pl.hp = Math.min(pl.hp+(pl.maxHp*0.3), pl.maxHp); 
             makeFX(this.x,this.y, 40,'#fff','boom'); globalStage++; loadStg(globalStage);
        }
    }

    shK(k, t, c, dmg, s){
        if(kd(k)){ if(!this.atkWait[k] && this.en>=c) {
            this.en-=c; p_pr.push({x:this.facing>0?this.x+this.w:this.x, y:this.y+this.h/3, dir:this.facing, s:(t==='1')?20:16, dmg:dmg, size:s, color:this.c.pCol, tgt:this.target});
            this.vx -= (c/8)*this.facing; this.atkWait[k]=true;
        } } else this.atkWait[k]=false;
    }

    swLck(){if(this.target) this.target=null; else this.getBestTrg();}
    getBestTrg() { let md=1500; let trg=null; e_arr.forEach(e=>{let d=Math.abs(e.x-this.x); if(d<md && e.x>this.x-500 && e.x<this.x+1000){md=d; trg=e;}}); if(trg){this.target=trg; doShake(1.5);} }

    draw() {
        if(this.iFrames>0 && Math.floor(f/4)%2===0) ctx.globalAlpha=0.3;
        
        drawPlayerSprite(ctx, this.x, this.y, this.w, this.h, this.c.id, this.c.col, this.facing>0, kd('KeyS'), this.vx);

        if(this.chargeI>0){ ctx.fillStyle=this.c.pCol; ctx.beginPath(); ctx.arc(this.x+this.w/2, this.y+this.h/2, this.chargeI/3, 0, Math.PI*2); ctx.fill(); }
        
        if(this.target) {
            let tx=this.target.x+this.target.w/2; let ty=this.target.y+this.target.h/2;
            ctx.strokeStyle=varColor('neon-red'); ctx.lineWidth=2; ctx.beginPath(); ctx.arc(tx,ty,35+Math.sin(f/4)*5, 0, Math.PI*2); ctx.stroke();
            ctx.setLineDash([5,5]); ctx.beginPath(); ctx.moveTo(this.x+this.w/2, this.y+this.h/2); ctx.lineTo(tx,ty); ctx.stroke(); ctx.setLineDash([]);
        }
        ctx.globalAlpha=1;
    }
}

class Enemy {
    constructor(x, ty) {
        this.ty=ty; this.w=45; this.h=55; this.isAggro=false;
        this.homeX = x; this.x = x; 
        this.vx=0; this.vy=0; 
        this.s = 3.0; this.stC=120; // BASE ENEMY SPEED INCREASED!
        this.maxHp = 60 + (globalStage*25);
        this.c = '#7f8c8d'; this.atkWait = 0; 
        
        if(ty==='boss'){ this.maxHp=1000+globalStage*200; this.w=90; this.h=110; this.s=2.0;}
        else if(ty==='tank'){ this.w=65; this.h=85; this.maxHp*=4; this.s=1.0; this.c='#34495e';}
        else if(ty==='shield'){ this.w=50; this.c='#95a5a6'; this.maxHp*=2; this.s=2.5;}
        else if(ty==='bomber'){ this.w=35; this.h=45; this.maxHp*=0.7; this.s=4.5;} // Fast!
        else if(ty==='flyer') { this.maxHp*=0.6; this.s=2.5; this.y = canvas.height - 350; } 
        else if(ty==='ninja') { this.maxHp*=0.8; this.s=4.0; } // Very fast
        else if(ty==='shooter'){ this.s=1.5; this.stC = 120 - Math.min(60, globalStage*2); }
        else { this.c = '#c0392b'; } 
        
        if(this.ty !== 'flyer') this.y = -100;
        this.hp = this.maxHp; this.phase = 1;
    }

    upd() {
        let dx = pl.x - this.x; let isFDir = (dx>0)?1:-1; let flY = canvas.height-80; 

        if(!this.isAggro){ if(Math.abs(dx)<900) this.isAggro=true; else if(this.ty!=='flyer') this.vx = Math.sin(f/60)*this.s*0.5;}
        else {
            if(this.ty==='boss') {
                if(this.hp/this.maxHp < 0.3) this.phase=3; else if(this.hp/this.maxHp < 0.6) this.phase=2;
                let curSp = (this.phase===3)? 4.5 : (this.phase===2)? 3.0 : 2.0;
                this.atkWait--;
                if(this.phase===1) { if(Math.abs(dx)>20) this.vx=isFDir*curSp; }
                else if (this.phase===2) { 
                    this.vx = isFDir * curSp; 
                    if(this.atkWait<=0 && Math.abs(dx)>150){ this.atkWait=90; pr_arr.push({x:this.x+this.w/2, y:this.y+30, dx:isFDir*12, dy:2, age:0}); }
                }
                else if(this.phase===3) { 
                    if(this.atkWait>0){ this.vx = isFDir*8; } else { this.vx = isFDir*curSp; }
                    if(f%180===0){ this.atkWait=30; this.vy=-8; makeFX(this.x,this.y,10,varColor('neon-red'),'boom');}
                }
            }
            else if (this.ty==='flyer'){ this.x += isFDir * this.s; this.y = pl.y - 120 + Math.sin(f/20)*60; }
            else if (this.ty==='bomber') { if(Math.abs(dx)<50) this.dieAndExplode(); this.vx = isFDir * this.s; }
            else if(this.ty==='shield' || this.ty==='tank') { this.vx = isFDir * this.s; }
            else if (this.ty==='ninja'){ this.atkWait--; if(this.atkWait>20) this.vx = isFDir*2.0; else if(this.atkWait>0){this.vx=isFDir*16; this.vy=-2; } else this.atkWait=100;}
            else if (this.ty==='shooter') { this.atkWait--; if(Math.abs(dx)>450) this.vx = isFDir*this.s; else this.vx*=0.8;
                 if(this.atkWait<=0) { this.atkWait = this.stC; pr_arr.push({x:this.x+20,y:this.y+20, dx:isFDir*12, dy:0, age:0});}
            }
            else if (this.ty==='summoner') {
                 if(Math.abs(dx)<600){this.vx = isFDir* -2.0;} else this.vx*=0.8; 
                 this.atkWait--; if(this.atkWait<=0){ this.atkWait=200; e_arr.push(new Enemy(this.x, 'jumper')); e_arr[e_arr.length-1].isAggro=true; }
            }
            else if(this.ty==='jumper') { this.vx=isFDir*2.5; this.atkWait--; if(this.atkWait<=0 && this.y+this.h>=flY-20) {this.vy=-14; this.atkWait=80;}}
            else { this.vx = isFDir*this.s; } 
        }

        let nx = this.x + this.vx;
        if(nx < 50) { nx = 50; this.vx*=-1; }
        
        if(this.ty !== 'flyer') {
            currentMap.walls.forEach(w => {
                let wx = w.x; let wy = canvas.height - 80 - w.h;
                if(this.y + this.h > wy) {
                    if(this.vx > 0 && nx+this.w > wx && this.x+this.w <= wx) { nx = wx - this.w; this.vx*=-1; }
                    else if(this.vx < 0 && nx < wx+w.w && this.x >= wx+w.w) { nx = wx + w.w; this.vx*=-1; }
                }
            });
        }
        this.x = nx;

        if(this.ty!=='flyer') {
            this.vy+=0.6; this.y+=this.vy; 
            let isGe=false; if(this.y+this.h>=flY){this.y=flY-this.h; this.vy=0; isGe=true;}
            if(!isGe && this.ty!=='jumper') {
                 currentMap.platforms.forEach(p=>{
                    let py = canvas.height-p.y_offset;
                    if(this.vy>=0 && this.y+this.h>=py-15 && this.y+this.h<=py+15 && this.x+this.w>p.x && this.x<p.x+p.w) {this.y=py-this.h; this.vy=0;}
                 });
                 currentMap.walls.forEach(w=>{
                    let wy = canvas.height - 80 - w.h;
                    if(this.vy>=0 && this.y+this.h>=wy-15 && this.y+this.h<=wy+15 && this.x+this.w>w.x && this.x<w.x+w.w) {this.y=wy-this.h; this.vy=0;}
                 });
            }
        }

        if(this.isAggro && pl.iFrames<=0 && intersect(this, pl)) {
            let dg = (this.ty==='boss')? 30: (this.ty==='tank')? 22 : 12; 
            pl.hp -= dg; pl.vx = dx<0?15:-15; pl.vy=-10; pl.iFrames=50; doShake(3);
        }
    }
    
    dieAndExplode() {
         makeFX(this.x+this.w/2, this.y+this.h/2, 60, '#ff5e00', 'boom'); 
         if(intersect({x:this.x-150, y:this.y-150, w:300, h:300}, pl) && pl.iFrames<=0) {
             pl.hp -= 40; pl.iFrames=40; pl.vx = pl.x<this.x?-20:20; pl.vy=-10; doShake(8);
         }
         this.hp = -999; 
    }

    draw() { 
        if(!this.isAggro && this.ty==='flyer' && this.y < 0) return; 
        drawEnemySprite(ctx, this.x, this.y, this.w, this.h, this.c, this.ty, this.hp/this.maxHp, this.phase, pl.x > this.x); 
        ctx.fillStyle='#000'; ctx.fillRect(this.x, this.y-10, this.w,4); ctx.fillStyle='red'; ctx.fillRect(this.x,this.y-10, this.w*(Math.max(0,this.hp)/this.maxHp), 4);
        if(!this.isAggro && this.ty!=='flyer') { ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.font="14px Jura"; ctx.fillText("Zzz", this.x+10, this.y-15); }
    }
}

class CloverChest {
    constructor(x) { this.x=x; this.y=canvas.height-180; this.w=100; this.h=100; this.hp=600; this.maxHp=600; }
    draw(){ ctx.fillStyle='#111'; ctx.fillRect(this.x,this.y,this.w,this.h); ctx.fillStyle=varColor('gold'); ctx.fillRect(this.x+this.w/2-5, this.y+30, 10,20);
            ctx.strokeStyle=varColor('gold'); ctx.lineWidth=4; ctx.strokeRect(this.x,this.y,this.w,this.h); 
            ctx.fillStyle=varColor('neon-red'); ctx.fillRect(this.x, this.y-20, this.w*(this.hp/this.maxHp),10);
            ctx.fillStyle='#fff'; ctx.font="bold 26px Righteous"; ctx.fillText("CLOVER", this.x+5, this.y-35);
    }
}

function makeFX(x,y,q,c,m) { for(let i=0;i<q;i++) fx.push({ x:x, y:y, vx:(Math.random()-0.5)*(m==='boom'?16:4), vy:(m==='beam')?-(Math.random()*8): (Math.random()-0.5)*(m==='boom'?16:4), col:c, l: (m==='spark')?12:20, s: (m==='boom')?Math.random()*10+5 : 4}); }
function varColor(n) { return getComputedStyle(document.documentElement).getPropertyValue('--'+n).trim(); }

function loadStg(s_N) {
    let tmap = MAPS[s_N > 20 ? 20 : s_N]; currentMap = tmap;
    document.getElementById('stage-info').innerText = tmap.name; document.getElementById('stage-info').style.color = tmap.neon;
    document.getElementById('stage-alert').innerText = tmap.is_boss ? "BOSS ARENA" : "SYSTEM ENGAGED"; 
    document.getElementById('stage-alert').style.color = tmap.neon;
    document.getElementById('stage-alert').style.opacity = 1; setTimeout(()=>{ document.getElementById('stage-alert').style.opacity=0 }, 2500);

    pl.x = 100; 
    e_arr=[]; pr_arr=[]; p_pr=[]; drops=[]; pipe=null; cloverChest=null; 

    if(tmap.is_boss) { e_arr.push(new Enemy(2000, 'boss')); } 
    else { 
        let ec = 15 + s_N * 3; // More enemies!
        for(let k=0; k<ec; k++){ 
            let ty=tmap.enemies[Math.floor(Math.random()*tmap.enemies.length)]; 
            e_arr.push(new Enemy(1500 + Math.random()*8000, ty)); 
        } 
    }
    
    if(s_N === 20) { cloverChest=new CloverChest(9500); }
    else { pipe = new Pipe(9800); }
}

function startMission(charData, devFlag) {
    p_class = charData;
    globalStage = devFlag ? parseInt(document.getElementById('dev-stage').value) : 1;
    document.getElementById('select-screen').classList.add('hidden'); document.getElementById('ui-layer').classList.remove('hidden');
    pl = new Player(charData); if(devFlag){pl.maxHp=5000; pl.hp=5000; pl.en=5000; pl.maxEn=5000;}
    loadStg(globalStage); requestAnimationFrame(sysLoop);
}

function sysLoop() {
    if(isPaused){requestAnimationFrame(sysLoop); return; }
    f++;
    if(pl.hp<=0){ document.getElementById('ui-layer').classList.add('hidden'); document.getElementById('death-screen').classList.remove('hidden'); document.getElementById('final-lvl').innerText="SECTOR " + globalStage; return;}

    pl.upd();

    for(let i=e_arr.length-1; i>=0; i--) { let e=e_arr[i]; e.upd(); 
        if(e.hp<=0) { if(e.ty==='bomber')e.dieAndExplode(); else {makeFX(e.x+20,e.y+20,30,currentMap.neon,'boom'); drops.push(new Drop(e.x,e.y, e.ty==='boss')); } e_arr.splice(i,1); }
    }
    
    if(cloverChest && cloverChest.hp<=0) { document.getElementById('ui-layer').classList.add('hidden'); document.getElementById('victory-screen').classList.remove('hidden'); return; }
    for(let i=drops.length-1; i>=0; i--) { if(drops[i].upd()) drops.splice(i,1); }

    for(let i=pr_arr.length-1; i>=0; i--){ let b=pr_arr[i]; 
         b.age++;
         if(b.age < 150) {
             let ta = Math.atan2((pl.y+pl.h/2)-b.y, (pl.x+pl.w/2)-b.x);
             b.dx += (Math.cos(ta)*12 - b.dx)*0.05;
             b.dy += (Math.sin(ta)*12 - b.dy)*0.05;
         }
         b.x+=b.dx; b.y+=b.dy; makeFX(b.x,b.y, 1, varColor('neon-red'), 'spark'); 
         
         if(intersect({x:b.x,y:b.y,w:8,h:8}, pl)) { if (pl.iFrames<=0) { pl.hp-=18; pl.iFrames=45; pl.vx += b.dx>0?8:-8; doShake(3); } pr_arr.splice(i,1); continue; }
         if(b.y>canvas.height || b.x<camX || b.x>camX+canvas.width) pr_arr.splice(i,1);
    }
    
    for(let i=p_pr.length-1; i>=0; i--){ let b = p_pr[i]; 
        if(b.tgt && b.tgt.hp>0){
             let ta = Math.atan2((b.tgt.y+b.tgt.h/2)-b.y, (b.tgt.x+b.tgt.w/2)-b.x); 
             b.x += Math.cos(ta)*b.s; b.y+=Math.sin(ta)*b.s; 
        } else { b.x += b.dir*b.s; }
        makeFX(b.x,b.y,1,b.color,'spark');

        let isDel = false; let projRecHit = {x:b.x-b.size/2, y:b.y-b.size/2, w:b.size, h:b.size};

        if(cloverChest && intersect(projRecHit, cloverChest)) { cloverChest.hp-=b.dmg; makeFX(b.x, b.y, 5, varColor('neon-green'), 'boom'); isDel=true; doShake(1.5); } 
        else {
             for(let j=e_arr.length-1; j>=0; j--){ let te = e_arr[j];
                  if(intersect(projRecHit, te)) {
                      let sameDirFacing = (te.x > pl.x) ? (b.dir===1) : (b.dir===-1); 
                      if (te.ty==='shield' && sameDirFacing && b.size < 40){ 
                           b.dir*=-1; pr_arr.push({x:b.x, y:b.y, dx:b.dir*15, dy:0, age:150}); isDel=true; makeFX(b.x, b.y, 15, '#fff', 'spark'); doShake(1); break;
                      } 
                      te.hp-=b.dmg; makeFX(b.x,b.y,8,b.color,'boom'); isDel=true; doShake((b.dmg)/25); te.vx += b.dir*12;
                      if(p_class.id==='dark'){pl.hp=Math.min(pl.maxHp,pl.hp+(b.dmg*0.035));} te.isAggro=true; break;
                  }
             }
        }
        if(isDel || b.y>canvas.height || Math.abs(b.x-pl.x)>1500) p_pr.splice(i,1);
    }

    for(let i=fx.length-1; i>=0; i--) { fx[i].x+=fx[i].vx; fx[i].vy+=0.1; fx[i].y+=fx[i].vy; fx[i].l--; if(fx[i].l<=0) fx.splice(i,1); }
    
    let cxT = pl.x - canvas.width/2 + 100; 
    if(cxT<0) cxT=0; if(cxT > STAGE_WIDTH - canvas.width) cxT = STAGE_WIDTH - canvas.width;
    camX += (cxT-camX)*0.08; 
    let S_X = camX, S_Y = 0; if(shakeV>0){ S_X+=(Math.random()-0.5)*shakeV; S_Y+=(Math.random()-0.5)*shakeV; shakeV*=0.8;} if(shakeV<0.4) shakeV=0;
    
    ctx.fillStyle = currentMap.bg; ctx.fillRect(0,0, canvas.width, canvas.height);
    ctx.fillStyle='rgba(255,255,255,0.05)'; for(let ds=0;ds<60;ds++) { let pX = ((ds*584)-(camX*0.06))%canvas.width; if(pX<0)pX+=canvas.width; ctx.fillRect(pX,(ds*4113)%canvas.height, 4+(ds%2)*2,4+(ds%2)*2); }
    
    ctx.save(); ctx.translate(-S_X, S_Y); 
    
    let baseFY = canvas.height-80;
    ctx.fillStyle = currentMap.floor; ctx.fillRect(S_X-200, baseFY, canvas.width+500, 300);
    ctx.strokeStyle=currentMap.neon; ctx.globalAlpha=0.2; for(let xk=S_X-(S_X%100); xk<S_X+canvas.width+400; xk+=100) { ctx.beginPath(); ctx.moveTo(xk, baseFY); ctx.lineTo(xk, canvas.height); ctx.stroke(); } ctx.globalAlpha=1;

    currentMap.platforms.forEach(p=>{
        let pY = canvas.height-p.y_offset;
        ctx.fillStyle = currentMap.floor; ctx.fillRect(p.x,pY,p.w,p.h);
        ctx.fillStyle=currentMap.neon; ctx.globalAlpha=0.3; ctx.fillRect(p.x,pY,p.w,2); ctx.globalAlpha=1;
    });

    currentMap.walls.forEach(w=>{
        let wY = canvas.height - 80 - w.h;
        ctx.fillStyle = currentMap.floor; ctx.fillRect(w.x, wY, w.w, w.h);
        ctx.fillStyle=currentMap.neon; ctx.globalAlpha=0.5; ctx.fillRect(w.x, wY, w.w, 2); ctx.fillRect(w.x, wY, 2, w.h); ctx.fillRect(w.x+w.w-2, wY, 2, w.h); ctx.globalAlpha=1;
    });

    if(pipe) pipe.draw(); if(cloverChest) cloverChest.draw(); drops.forEach(d=>d.draw());
    pl.draw(); e_arr.forEach(e=>e.draw()); 
    ctx.fillStyle=varColor('neon-red'); pr_arr.forEach(b=>{ctx.beginPath(); ctx.arc(b.x,b.y,6,0,Math.PI*2); ctx.fill();});
    
    p_pr.forEach(b=>{ctx.fillStyle=b.color; ctx.shadowBlur=15; ctx.shadowColor=b.color; ctx.beginPath(); ctx.arc(b.x,b.y,b.size,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;});
    fx.forEach(x => {ctx.fillStyle=x.col; ctx.globalAlpha=(x.l/25); ctx.fillRect(x.x,x.y,x.s,x.s);}); ctx.globalAlpha=1;
    
    ctx.restore();
    
    document.getElementById('hp-bar').style.width=Math.max(0,(pl.hp/pl.maxHp)*100)+'%'; document.getElementById('hp-t').innerText=Math.floor(pl.hp)+"/"+pl.maxHp;
    document.getElementById('en-bar').style.width=Math.max(0,(pl.en/pl.maxEn)*100)+'%'; document.getElementById('en-t').innerText=Math.floor(pl.en)+"/"+pl.maxEn;
    
    if(shardNotifTimer > 0) { shardNotifTimer--; document.getElementById('stage-alert').innerText = shardNotif; document.getElementById('stage-alert').style.opacity = shardNotifTimer/100; }
    
    requestAnimationFrame(sysLoop);
}

createSelectMenu();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5009, debug=True)
