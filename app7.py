import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'fantasy_castle_defender_v2' 

# ==========================================
# 🏰 נתוני המבצר וחדרי ההגנה
# ==========================================
SECTORS = {
    "N": {"name": "השער הצפוני", "defense": 100, "max_def": 100},
    "S": {"name": "החפיר הדרומי", "defense": 100, "max_def": 100},
    "E": {"name": "צריח הקוסמים", "defense": 100, "max_def": 100},
    "W": {"name": "חומת הפלדה", "defense": 100, "max_def": 100},
    "CORE": {"name": "כס המלכות (הליבה)", "defense": 1000, "max_def": 1000} 
}

ALIENS = [
    {"name": "שלד לוחם", "dmg": 4, "hp_base": 15, "icon": "💀", "min_day": 1},
    {"name": "עדר זומבים", "dmg": 8, "hp_base": 30, "icon": "🧟", "min_day": 1},
    {"name": "כלב-גיהינום", "dmg": 15, "hp_base": 25, "icon": "🐺", "min_day": 2},
    {"name": "רוח רפאים", "dmg": 22, "hp_base": 20, "icon": "👻", "min_day": 3},
    {"name": "נקרומנסר (מזמן מתים)", "dmg": 18, "hp_base": 60, "icon": "🧙‍♂️", "min_day": 4},
    {"name": "דרקון העצמות (בוס!)", "dmg": 40, "hp_base": 120, "icon": "🐉", "min_day": 6}
]

# ==========================================
# ⚙️ מנוע כישוף המשחק
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state:
            self.state = {
                "energy": 100, "max_energy": 250, # המאנה הכחולה
                "oxygen": 100, "max_oxygen": 100, # מורל הצבא
                "day": 1,
                "sectors": SECTORS.copy(),
                "enemies": [],
                "log": [{"text": "התפלצויות באופק. כוננות מבצר עליונה החלה!", "type": "info"}],
                "events": []
            }
        else:
            self.state = state

    def log(self, t, type="sys"): 
        self.state["log"].append({"text": t, "type": type})

    def add_event(self, t, room=None):
        self.state["events"].append({"type": t, "room": room})

    def spawn_wave(self):
        available_monsters = [m for m in ALIENS if m["min_day"] <= self.state["day"]]
        count = random.randint(1, min(self.state["day"] // 2 + 1, 4)) 
        
        for _ in range(count):
            loc = random.choice(["N", "S", "E", "W"])
            base = random.choice(available_monsters)
            
            if base["name"] == "דרקון העצמות (בוס!)" and random.random() > 0.2:
                 base = available_monsters[1] 

            enemy = {
                "id": str(uuid.uuid4())[:8],
                "name": base["name"],
                "dmg": base["dmg"] + (self.state["day"] * 1), 
                "hp": base["hp_base"] + (self.state["day"] * 4), 
                "loc": loc,
                "icon": base["icon"]
            }
            self.state["enemies"].append(enemy)
            self.log(f"⚔️ תצפית חומות: {enemy['name']} תוקף מ{SECTORS[loc]['name']}.", "danger")
            self.add_event("alarm", loc)

    def next_turn(self):
        s = self.state
        s["events"] = [] 
        
        s["energy"] = min(s["energy"] + 15, s["max_energy"]) 
        s["oxygen"] -= 1 
        
        if s["oxygen"] <= 0:
            return "dead"

        alive = []
        for e in s["enemies"]:
            loc = e["loc"]
            sec = s["sectors"][loc]
            
            # פריצת חומות וכניסה לאולם הראשי
            if sec["defense"] <= 0 and loc != "CORE":
                self.log(f"🚨 חומה נשברה! מפלצת צועדת אל כס המלכות.", "danger")
                e["loc"] = "CORE"
                sec["defense"] = 0
                self.add_event("breach", "CORE")
            
            s["sectors"][e["loc"]]["defense"] -= e["dmg"]
            
            if s["sectors"]["CORE"]["defense"] <= 0:
                return "dead"
            
            if s["sectors"][e["loc"]]["defense"] > 0 and e["loc"] != "CORE":
                e["hp"] -= 12
                if e["hp"] <= 0:
                     self.add_event("kill", e["loc"])
                     s["energy"] = min(s["energy"] + 15, s["max_energy"])
            
            if e["hp"] > 0:
                alive.append(e)

        s["enemies"] = alive
        
        if random.random() < 0.25 + (s["day"] * 0.02):
            self.spawn_wave()

        return "ok"

    def action_fire(self, loc): 
        if self.state["energy"] >= 20:
            self.state["energy"] -= 20
            hits = False
            survivors = []
            base_damage = 50 
            is_crit = random.random() < 0.3 
            final_dmg = base_damage * 2.5 if is_crit else base_damage
            
            if is_crit:
                self.add_event("crit_shoot", loc)
            else:
                self.add_event("shoot", loc)

            for e in self.state["enemies"]:
                if e["loc"] == loc:
                    e["hp"] -= final_dmg
                    hits = True
                    if e["hp"] > 0: 
                        survivors.append(e)
                    else: 
                        self.log(f"💥 בום! חיסלת בעזרת כישוף את {e['name']}.", "success")
                        self.state["energy"] = min(self.state["energy"] + 10, self.state["max_energy"])
                        self.add_event("kill", loc)
                else:
                    survivors.append(e)
            
            self.state["enemies"] = survivors
            if not hits:
                self.log("כישוף מבוזבז באזור ריק.", "sys")
        else:
            self.add_event("error")

    def action_emp(self): 
        if self.state["energy"] >= 80:
            self.state["energy"] -= 80
            self.add_event("emp")
            alive = []
            for e in self.state["enemies"]:
                e["hp"] -= 120 
                if e["hp"] > 0: alive.append(e)
            
            earned = (len(self.state["enemies"]) - len(alive)) * 10
            if earned > 0:
                self.state["energy"] = min(self.state["energy"] + earned, self.state["max_energy"])
                self.log(f"סופת מטאורים ריסקה שדות צורפים! +{earned} מאנה.", "success")
            self.state["enemies"] = alive
        else:
             self.add_event("error")

    def action_repair(self, loc):
        if self.state["energy"] >= 20:
            self.state["energy"] -= 20
            self.add_event("heal", loc)
            self.state["sectors"][loc]["defense"] = self.state["sectors"][loc]["max_def"] 
            self.log("בנאים וקוסמים הקימו את החומה מחדש.", "sys")
        else:
             self.add_event("error")

    def action_wait(self):
        self.state["energy"] = min(self.state["energy"] + 45, self.state["max_energy"]) 
        self.add_event("charge")
        self.log("מדיטציה עמוקה משקמת את רוח הקרב (+45 קריסטלים).", "sys")

    def action_ventilate(self):  
        if self.state["energy"] >= 15:
            self.state["energy"] -= 15
            self.state["oxygen"] = min(self.state["oxygen"] + 50, 100) 
            self.add_event("air")
            self.log("קריאת תקיפה! המורל בצבא זינק בחזרה.", "sys")
        else:
             self.add_event("error")

# ==========================================
# SERVER API
# ==========================================
@app.route("/")
def index():
    if "uid" not in session: session["uid"] = str(uuid.uuid4())
    return render_template_string(HTML)

@app.route("/update", methods=["POST"])
def update_game():
    d = request.json
    try: 
        eng = Engine(session.get("game_cmd_fntasy"))
    except: 
        eng = Engine(None)

    act = d.get("action")
    target = d.get("target") 

    status = "ok"

    if act == "reset": eng = Engine(None)
    elif act == "fire":
        eng.action_fire(target)
        status = eng.next_turn()
    elif act == "repair":
        eng.action_repair(target)
        status = eng.next_turn()
    elif act == "vent":
        eng.action_ventilate()
        status = eng.next_turn()
    elif act == "wait":
        eng.action_wait()
        status = eng.next_turn()
    elif act == "emp":
        eng.action_emp()
        status = eng.next_turn()

    if status == "dead":
        session["game_cmd_fntasy"] = None 
        return jsonify({"dead": True, "day": eng.state["day"]})

    if random.random() < 0.15: 
        eng.state["day"] += 1
        eng.log(f"השמיים קודרים... השרצנו אל לגל קושי: מפלצות רמה {eng.state['day']} !", "info")

    session["game_cmd_fntasy"] = eng.state
    
    return jsonify({
        "stats": {
            "energy": eng.state["energy"],
            "oxy": eng.state["oxygen"],
            "day": eng.state["day"],
            "core": eng.state["sectors"]["CORE"]["defense"]
        },
        "sectors": eng.state["sectors"],
        "enemies": eng.state["enemies"], 
        "events": eng.state["events"],  
        "log": eng.state["log"][-10:] 
    })


# ==========================================
# FRONTEND - Dark Fantasy UI
# ==========================================
HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SHADOW KINGDOM</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Secular+One&display=swap');
    
    :root { 
        --mana: #00d4ff; 
        --mana-dark: #005a7f;
        --blood: #e74c3c;
        --bg: #0d0614; 
        --stone: #2a2533;
        --border-glow: rgba(142, 68, 173, 0.6);
    }
    
    body { background: var(--bg); color: #ecf0f1; font-family: 'Secular One', sans-serif; margin: 0; height: 100vh; display: flex; flex-direction: column; overflow:hidden;}
    
    .emp-blast { animation: flash_emp 0.6s ease-out; }
    @keyframes flash_emp { 0% {background: white;} 50%{background: #8e44ad;} 100%{background: var(--bg);} }

    /* התיקון שלנו לרעידות: הוסר הinfinite כך שהיא תתרחש רק לחצי שנייה כשנקרא לה! */
    .screen-shake { animation: shake 0.4s cubic-bezier(.36,.07,.19,.97); }
    @keyframes shake {
      10%, 90% { transform: translate3d(-1px, 0, 0); }
      20%, 80% { transform: translate3d(2px, 0, 0); }
      30%, 50%, 70% { transform: translate3d(-4px, -1px, 0); }
      40%, 60% { transform: translate3d(4px, 1px, 0); }
    }
    
    /* Top Menu HUD */
    .hud { 
        background: #140924; padding: 10px 15px; border-bottom: 3px solid #8e44ad; 
        display: flex; justify-content: space-between; align-items: center; z-index: 10;
        box-shadow: 0 5px 20px rgba(142,68,173,0.3);
    }
    
    .bar-box { width: 140px; text-align: center; font-size: 15px; }
    .bar { height: 16px; background: #1a1a1a; margin-top: 5px; border:2px solid #555; border-radius:5px; position:relative;}
    .fill { height: 100%; transition: width 0.3s; width: 100%; border-radius:3px; }
    .hud-title h2 {margin:0; font-size: 32px; background: -webkit-linear-gradient(#d2b4de, #8e44ad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform:uppercase;}
    .hud-title div { background:#1a0822; padding:3px 10px; border-radius:20px; font-size:14px; margin-top:5px; border:1px solid #4a235a;}

    /* THE CASTLE BOARD */
    .station { 
        flex: 1; display: grid; position: relative;
        grid-template-areas: 
            ". N ."
            "W C E"
            ". S .";
        gap: 25px; align-items: center; justify-content: center;
        background: radial-gradient(circle at center, #1e0d33 0%, var(--bg) 95%);
    }
    
    .room {
        width: 175px; height: 140px;
        background: var(--stone); border: 2px solid #5d4037; border-radius: 4px;
        display: flex; flex-direction: column; justify-content: space-between; padding: 8px;
        text-align: center; position: relative; box-shadow: 5px 5px 10px rgba(0,0,0,0.8);
        background-image: linear-gradient(to bottom, #2d2633 0%, #1e1921 100%);
    }
    
    .hit-flash { animation: strike 0.4s forwards; }
    .hit-crit { animation: crit_strike 0.5s forwards; }
    @keyframes strike { 0% { background: #00d4ff; box-shadow: 0 0 30px #00d4ff;} 100% { background:var(--stone);} }
    @keyframes crit_strike { 0% { background: #f1c40f; box-shadow: 0 0 50px white; transform:scale(1.1);} 100% { background:var(--stone); transform:scale(1);} }
    
    .r-n { grid-area: N; }  .r-s { grid-area: S; }  
    .r-e { grid-area: E; }  .r-w { grid-area: W; } 
    
    .r-c { grid-area: C; border-color: #f39c12; border-width: 4px; height: 155px; width: 195px; background: rgba(50,20,0,0.8); display:flex; flex-direction:column; justify-content:center; box-shadow: inset 0 0 40px rgba(0,0,0,0.8);}
    .king-icon {font-size:40px; text-shadow:0 0 20px #f1c40f; z-index:1; opacity: 0.9;}

    .alien-layer {
        position: absolute; top: 35px; left: 0; right: 0; bottom: 35px;
        display: flex; flex-wrap: wrap; justify-content: center; align-content: center;
        gap: 6px; font-size: 28px; filter: drop-shadow(4px 4px 6px rgba(0,0,0,1));
        pointer-events: none;
    }
    .enemy-pop { animation: floatEnemy 0.6s infinite alternate; }
    @keyframes floatEnemy {from{transform:translateY(0)}to{transform:translateY(4px)}}

    .hp-strip { height: 10px; background: #000; margin-top: auto; margin-bottom: 5px; border-radius:3px; border:1px solid #444;}
    .hp-val { height: 100%; background: #2ecc71; width: 100%; transition: 0.3s;}
    
    .action-row {display:flex; gap: 5px; z-index:2;}
    .btn { 
        flex: 1; border: 2px solid transparent; padding: 6px 0; border-radius:4px;
        font-family: inherit; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.1s;
    }
    .btn-fire { background: #8e44ad; color:#fff; border-bottom:3px solid #4a235a;} 
    .btn-fire:hover { background: #9b59b6;} 
    .btn-fire:active { transform: translateY(3px); border-bottom-width:0px;}

    .btn-fix { background: #34495e; color:#fff; border-bottom:3px solid #2c3e50;}
    .btn-fix:hover { background: #7f8c8d; }
    .btn-fix:active { transform: translateY(3px); border-bottom-width:0px;}

    .danger-glow { animation: blink_danger 1s infinite; border-color: var(--blood); }
    @keyframes blink_danger { 50% { box-shadow: inset 0 0 20px var(--blood); } }
    
    .float-text { position: absolute; font-size: 24px; font-family:'sans-serif'; font-weight:900; animation: floatUp 1.2s forwards; pointer-events: none; text-shadow:2px 2px 2px #000; z-index: 100; left:40%;}
    @keyframes floatUp { 0%{ transform:translateY(0) scale(1.5); opacity:1;} 100%{transform:translateY(-60px) scale(1); opacity:0;} }

    .bottom-panel { height: 180px; background: #0b0710; border-top: 3px solid #5a3070; display: grid; grid-template-columns: 2fr 1.5fr;}
    
    .logs { padding: 15px; overflow-y: auto; font-size: 14px; border-left: 2px solid #5a3070; background:rgba(0,0,0,0.5); display:flex; flex-direction: column-reverse; }
    .log-line { margin-bottom: 5px; padding-bottom: 5px; border-bottom: 1px dotted rgba(255,255,255,0.05); color:#a9a1af;}
    .log-line:first-child { color:#e5c468; font-weight:bold; }
    
    .sys-controls { padding: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; align-items:center; }
    
    .big-btn { padding: 15px; border: 2px solid; border-radius:6px; font-family: inherit; font-size:14px; cursor: pointer; font-weight:bold;}
    
    .charge-btn { background:#1f1326; color: var(--mana); border-color:var(--mana); grid-column:span 2;}
    .charge-btn:hover { background:var(--mana); color:#000; box-shadow:0 0 20px var(--mana);}

    .vent-btn {background: #27ae60; border-color: #1e8449; color:white; box-shadow: inset 0 -3px #1e8449;} 
    .vent-btn:hover{filter:brightness(1.1); transform:translateY(2px);}
    
    .emp-btn {background: #e74c3c; border-color: #c0392b; color:white; box-shadow: inset 0 -3px #c0392b;} 
    .emp-btn:hover{filter:brightness(1.1); transform:translateY(2px);}

    .back-btn {position: absolute; top:12px; left:12px; color:#ccc; text-decoration:none; font-size:12px; border:1px solid #555; border-radius:4px; padding:6px 12px; z-index: 100;}
</style>
</head>
<body>
<a href="/" class="back-btn">למסך משחקים אקייד</a>

<div class="hud">
    <div class="bar-box">
        <span style="font-size:22px;">💎</span> מאנה / קסם 
        <div class="bar"><div id="bar-en" class="fill" style="background:var(--mana); box-shadow:0 0 10px var(--mana);"></div></div>
        <div style="font-size:12px; margin-top:2px;" id="txt-en">250/250</div>
    </div>
    
    <div class="hud-title">
        <h2>CASTLE DEFENDER</h2>
        <div>יום מתקפה <span id="day-val" style="color:#e74c3c; font-weight:bold; font-size:18px;">1</span> | חסינות הכס: <span id="txt-core" style="color:#f1c40f;">1000</span></div>
    </div>
    
    <div class="bar-box">
        <span style="font-size:22px;">🛡️</span> מורל צבאי
        <div class="bar"><div id="bar-ox" class="fill" style="background:#e74c3c"></div></div>
        <div style="font-size:12px; margin-top:2px;" id="txt-ox">100%</div>
    </div>
</div>

<div class="station">
    <div class="room r-n" id="room-N">
        <div style="color:#aab7b8; font-size:15px; border-bottom:1px solid #555; padding-bottom:4px;">השער הצפוני (N)</div>
        <div class="alien-layer" id="aliens-N"></div>
        <div class="hp-strip"><div class="hp-val" id="hp-N"></div></div>
        <div class="action-row">
            <button class="btn btn-fire" onclick="act('fire', 'N')">הכה!⚡</button>
            <button class="btn btn-fix" onclick="act('repair', 'N')">בנה!🧱</button>
        </div>
    </div>

    <div class="room r-w" id="room-W">
        <div style="color:#aab7b8; font-size:15px; border-bottom:1px solid #555; padding-bottom:4px;">חומה המערב (W)</div>
        <div class="alien-layer" id="aliens-W"></div>
        <div class="hp-strip"><div class="hp-val" id="hp-W"></div></div>
        <div class="action-row">
            <button class="btn btn-fire" onclick="act('fire', 'W')">הכה!⚡</button>
            <button class="btn btn-fix" onclick="act('repair', 'W')">בנה!🧱</button>
        </div>
    </div>

    <!-- המלך שלנו -->
    <div class="room r-c" id="room-CORE">
        <div style="color:#f1c40f; font-size:17px; text-shadow:2px 2px 0 #000;">כס המלכות 🏰</div>
        <div class="alien-layer" id="aliens-CORE" style="font-size:40px;"></div> 
        <div class="king-icon">🧙‍♂️👑</div>
        <div class="hp-strip" style="background:#3e2723; margin:0 auto; width:80%;"><div class="hp-val" id="hp-CORE" style="background:#f1c40f;"></div></div>
    </div>

    <div class="room r-e" id="room-E">
        <div style="color:#aab7b8; font-size:15px; border-bottom:1px solid #555; padding-bottom:4px;">מגדל המזרח (E)</div>
        <div class="alien-layer" id="aliens-E"></div>
        <div class="hp-strip"><div class="hp-val" id="hp-E"></div></div>
         <div class="action-row">
             <button class="btn btn-fire" onclick="act('fire', 'E')">הכה!⚡</button>
            <button class="btn btn-fix" onclick="act('repair', 'E')">בנה!🧱</button>
        </div>
    </div>

    <div class="room r-s" id="room-S">
        <div style="color:#aab7b8; font-size:15px; border-bottom:1px solid #555; padding-bottom:4px;">ביצות הדרום (S)</div>
        <div class="alien-layer" id="aliens-S"></div>
        <div class="hp-strip"><div class="hp-val" id="hp-S"></div></div>
        <div class="action-row">
             <button class="btn btn-fire" onclick="act('fire', 'S')">הכה!⚡</button>
            <button class="btn btn-fix" onclick="act('repair', 'S')">בנה!🧱</button>
        </div>
    </div>
</div>

<div class="bottom-panel">
    <div class="logs" id="logbox"></div>
    <div class="sys-controls">
        <button class="big-btn charge-btn" onclick="act('wait')">🌌 מדיטצית חצות הליל (45+ מאנה) </button>
        
        <button class="big-btn vent-btn" onclick="act('vent')" title="להפיח אש בלוחמים (+50% מורל צבא)">🎺 קריאה להסתער! (15💧)</button>
        <button class="big-btn emp-btn" onclick="act('emp')" title="להטיל גל כישוף שהופך כל רשע לעפר בכל האגפים">☄️ פקודת יום הדין! (80💧)</button>
    </div>
</div>

<script>
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioCtx();
    
    function beep(type, freq, time, pitchShift=false) {
        if(ctx.state === 'suspended') ctx.resume();
        let osc = ctx.createOscillator(); let gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        if (pitchShift) osc.frequency.exponentialRampToValueAtTime(freq*0.2, ctx.currentTime+time); 
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + time);
        
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + time);
    }
    
    const SFX = {
        magic_hit: () => beep('triangle', 600, 0.4, true),         
        crit: () => beep('sawtooth', 300, 0.7, true),              
        build: () => {beep('square', 100, 0.2); setTimeout(()=>beep('square',150,0.1),100)}, 
        heal_morale: () => beep('sine', 400, 0.6),    
        win_mana: () => beep('sine', 1200, 0.2) 
    };

    const API = "update"; 
    let previousCoreDefense = 1000;

    async function act(action, target=null) {
        if(ctx.state === 'suspended') ctx.resume();
        try {
            let res = await fetch(API, {
                method: 'POST', 
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action:action, target:target})
            });
            let d = await res.json();

            if (d.dead) {
                // הרעד בזמן פטירה מוסיף טיפת אלמנט אפוקליפטי
                document.body.classList.add("screen-shake"); 
                beep('sawtooth', 80, 2, true);
                setTimeout(() => { alert("🏰 הכסא נפל! חיל הזומבים הפך את עצמותייך לכסא הבא! מתת ביום ה- " + d.day); location.reload();}, 800);
                return;
            }

            // === התיקון השני: עדכון החלק העליון המבריק (הכס והיום) ====== 
            document.getElementById('txt-en').innerText = d.stats.energy;
            document.getElementById('bar-en').style.width = Math.min((d.stats.energy / 250)*100,100) + "%"; 
            document.getElementById('bar-ox').style.width = d.stats.oxy + "%"; 
            document.getElementById('txt-ox').innerText = d.stats.oxy + "%"; 
            
            // תיוג תיבת הימים בנתונים העדכניים:
            document.getElementById('day-val').innerText = d.stats.day;
            document.getElementById('txt-core').innerText = d.stats.core;
            
            // התיקון הראשון: רעידת הליבה קצרצרה בלבד כאשר מתבצע שינוי במינוס המלך 
            if (d.stats.core < previousCoreDefense) {
                document.body.classList.remove("screen-shake"); 
                void document.body.offsetWidth; 
                document.body.classList.add("screen-shake");
            }
            previousCoreDefense = d.stats.core; 
            
            
            if (d.events && d.events.length > 0) {
                d.events.forEach(ev => {
                    let roomEl = document.getElementById("room-" + ev.room);
                    if (ev.type === "emp") { document.body.classList.add("emp-blast"); setTimeout(()=>document.body.classList.remove("emp-blast"),600); beep('square',200, 1.2, true);}
                    if (ev.type === "charge") beep('sine',300, 0.8);
                    if (ev.type === "air") SFX.heal_morale(); 
                    if (ev.room) {
                        if (ev.type === "shoot") { SFX.magic_hit(); roomEl.classList.remove("hit-flash"); void roomEl.offsetWidth; roomEl.classList.add("hit-flash"); spawnTextFloat("-50💥", ev.room, "cyan"); }
                        if (ev.type === "crit_shoot") { SFX.crit(); roomEl.classList.remove("hit-crit"); void roomEl.offsetWidth; roomEl.classList.add("hit-crit"); spawnTextFloat("-CRIT-", ev.room, "gold"); }
                        if (ev.type === "heal") { SFX.build(); spawnTextFloat("+מגן אבנים", ev.room, "gray"); }
                        if (ev.type === "kill") { SFX.win_mana(); spawnTextFloat("+💎", ev.room, "cyan"); }
                        if (ev.type === "alarm" || ev.type==="breach") { beep('sawtooth', 150, 0.3); } 
                    }
                });
            }

            const dirs = ['N','S','E','W', 'CORE'];
            dirs.forEach(k => document.getElementById(`aliens-${k}`).innerHTML = ''); 

            d.enemies.forEach(e => {
                let theDiv = document.getElementById(`aliens-${e.loc}`);
                if (theDiv) {  theDiv.innerHTML += `<span class="enemy-pop" title="מופל חיים: ${e.hp} !">${e.icon}</span>`; }
            });

            for (let k in d.sectors) {
                let sec = d.sectors[k];
                let elHp = document.getElementById("hp-"+k);
                let pct = (sec.defense / sec.max_def) * 100;
                
                if(elHp) elHp.style.width = pct + "%";
                let roomEl = document.getElementById("room-"+k);
                
                // שימו לב! כשמשפצים חומה ההופכי יעבוד בזכות השורות האלה (יוריד השקפה ומחלה מהחלונות!)
                if (pct < 30 && pct > 0) {
                     if(k!=="CORE") elHp.style.backgroundColor = "var(--blood)"; else elHp.style.backgroundColor = "orange";
                     roomEl.classList.add("danger-glow");
                     roomEl.style.opacity = "1";
                     roomEl.style.filter = "none";
                } 
                else if(pct <= 0) { 
                    elHp.style.backgroundColor = "transparent"; 
                    roomEl.style.opacity = "0.4"; 
                    roomEl.style.filter = "grayscale(100%)"; 
                    roomEl.classList.remove("danger-glow");
                }
                else {
                    elHp.style.backgroundColor = "#2ecc71";
                    roomEl.style.opacity = "1"; 
                    roomEl.style.filter = "none"; 
                    roomEl.classList.remove("danger-glow");
                }
            }

            let lb = document.getElementById("logbox");
            lb.innerHTML = "";
            let latests = d.log.reverse(); 
            latests.forEach(l => {
                lb.innerHTML += `<div class="log-line ${l.type}"> * ${l.text}</div>`;
            });

        } catch(e) {}
    }


    function spawnTextFloat(txt, roomId, color) {
        let theDiv = document.getElementById("room-" + roomId);
        if(!theDiv) return;
        let floater = document.createElement('div');
        floater.className = 'float-text';
        floater.style.color = color;
        floater.innerText = txt;
        theDiv.appendChild(floater);
        setTimeout(() => floater.remove(), 1200);
    }
    
    window.onload = () => { act('init'); };
</script>
</body>
</html>"""

if __name__ == "__main__":
    # כמובן, אם זה מאחורי הלאונצ'ר, הוא לא ישתמש ב-5007 אלא בניתוב הראשי,
    # אבל לשם הפעלה בודדת לבדיקה:
    app.run(port=5007, debug=True)
