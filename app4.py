import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
# שינוי מפתח מוחק היסטוריה שבורה
app.secret_key = 'hacker_elite_working_v888'

# ==========================================
# 💎 נתונים (קבועים ויציבים)
# ==========================================

PROGRAMS = {
    # תקיפה (צבעים חמים)
    "ping": {"name": "הצפה מהירה ", "cost": 1, "dmg": 10, "risk": 1, "type": "atk"},
    "brute": {"name": "כוח גס", "cost": 3, "dmg": 30, "risk": 4, "type": "atk"},
    "inject": {"name": "הזרקת קוד ", "cost": 5, "dmg": 80, "risk": 10, "type": "atk"},
    "zero": {"name": "פרצת יום האפס", "cost": 10, "dmg": 300, "risk": 25, "type": "atk"},
    
    # הגנה (צבעים קרים)
    "proxy": {"name": "הסוואת IP", "cost": 3, "heal": 15, "type": "def"},
    "clean": {"name": "מחיקת עקבות", "cost": 6, "heal": 40, "type": "def"}
}

# הרשימה המלאה והסופית שביקשת
ALL_TARGETS = [
    {"name": "ראוטר של שכן", "hp": 20, "cash": 50},
    {"name": "קופה של פיצה", "hp": 40, "cash": 120},
    {"name": "מצלמת תנועה", "hp": 60, "cash": 200},
    {"name": "שרת בית ספר", "hp": 100, "cash": 400},
    {"name": "כספומט", "hp": 150, "cash": 800},
    {"name": "רשת חנות בגדים", "hp": 200, "cash": 1200},
    {"name": "אתר חדשות קטן", "hp": 300, "cash": 2000},
    {"name": "שרתי ספוטיפיי", "hp": 500, "cash": 4000},
    {"name": "בנק דיסקונט", "hp": 800, "cash": 8000},
    {"name": "חברת החשמל", "hp": 1200, "cash": 15000},
    {"name": "מגדל פיקוח נתב'ג", "hp": 2000, "cash": 30000},
    {"name": "מחשבי הבורסה", "hp": 3500, "cash": 50000},
    {"name": "כור גרעיני", "hp": 5000, "cash": 80000},
    {"name": "הפנטגון", "hp": 8000, "cash": 150000},
    {"name": "NASA Mainframe", "hp": 15000, "cash": 300000},
    {"name": "אילון מאסק", "hp": 30000, "cash": 1000000}
]

# ==========================================
# ⚙️ מנוע (Logic)
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state or "ram" not in state:
            self.reset()
        else:
            self.state = state

    def reset(self):
        # אתחול
        self.state = {
            "money": 0,
            "ram": 20, "max_ram": 20,
            "cpu": 1,
            "risk": 0,
            "connected_target_id": None, # ID של היעד הנוכחי
            "targets": [], # נשמור כאן את המצב החי של כל היעדים
            "game_over": False,
            "log": ["מערכת מוכנה. בחר יעד לתקיפה."]
        }
        
        # טעינת כל המטרות למשחק
        for t in ALL_TARGETS:
            new_t = t.copy()
            new_t["id"] = str(uuid.uuid4()) # מזהה ייחודי
            new_t["max_hp"] = t["hp"]
            self.state["targets"].append(new_t)

    def log(self, txt):
        self.state["log"].insert(0, txt)
        if len(self.state["log"]) > 10: self.state["log"].pop()

    # --- Actions ---

    def connect(self, target_id):
        if self.state["connected_target_id"]: return
        
        # חיפוש לפי ID
        found = next((t for t in self.state["targets"] if t["id"] == target_id), None)
        if found:
            self.state["connected_target_id"] = target_id
            self.log(f"התחברת ל-{found['name']}.")

    def disconnect(self):
        if not self.state["connected_target_id"]: return
        self.state["connected_target_id"] = None
        self.state["ram"] = self.state["max_ram"]
        self.log("התנתקת. RAM שוחזר.")

    def execute(self, key):
        if self.state["game_over"]: return

        # בדיקת יעד
        t_id = self.state["connected_target_id"]
        if not t_id:
            self.log("שגיאה: לא מחובר לשרת.")
            return

        target = next((t for t in self.state["targets"] if t["id"] == t_id), None)
        if not target: return # לא אמור לקרות

        prog = PROGRAMS[key]
        
        # בדיקת RAM
        if self.state["ram"] < prog["cost"]:
            self.log(f"חסר RAM! ({self.state['ram']}/{prog['cost']})")
            return

        self.state["ram"] -= prog["cost"]

        if prog["type"] == "atk":
            dmg = prog["dmg"] * self.state["cpu"]
            target["hp"] -= dmg
            self.state["risk"] += prog["risk"]
            
            self.log(f"הפעלת {prog['name']}. נזק: {dmg}")
            
            # ניצחון
            if target["hp"] <= 0:
                self.state["money"] += target["cash"]
                self.log(f"פריצה הושלמה! השגת ${target['cash']}")
                self.state["targets"].remove(target) # מוחק מהרשימה
                self.state["connected_target_id"] = None
                self.state["ram"] = self.state["max_ram"]
        
        elif prog["type"] == "def":
            self.state["risk"] = max(0, self.state["risk"] - prog["heal"])
            self.log("הורדת פרופיל. סיכון ירד.")

        # בדיקת הפסד
        if self.state["risk"] >= 100:
            self.state["game_over"] = True

    def buy(self, type):
        if type == "ram":
            cost = 200
            if self.state["money"] >= cost:
                self.state["money"] -= cost
                self.state["max_ram"] += 10
                self.state["ram"] = self.state["max_ram"]
                self.log("שדרוג RAM בוצע.")
        elif type == "cpu":
            cost = 500
            if self.state["money"] >= cost:
                self.state["money"] -= cost
                self.state["cpu"] += 1
                self.log("שדרוג CPU בוצע.")

# ==========================================
# SERVER
# ==========================================
@app.route("/")
def home():
    if "uid" not in session: session["uid"] = str(uuid.uuid4())
    return render_template_string(HTML, api=url_for("update"))

@app.route("/update", methods=["POST"])
def update():
    try: eng = Engine(session.get("game_v5"))
    except: eng = Engine(None)
    
    req = request.json or {}
    act = req.get("act")
    val = req.get("val")

    if act == "reset": eng.reset()
    elif act == "conn": eng.connect(val)
    elif act == "disc": eng.disconnect()
    elif act == "run": eng.execute(val)
    elif act == "buy": eng.buy(val)
    
    # שליפת היעד הנוכחי כדי לשלוח ללקוח
    curr_target = None
    tid = eng.state["connected_target_id"]
    if tid:
        curr_target = next((t for t in eng.state["targets"] if t["id"] == tid), None)
    
    session["game_v5"] = eng.state
    
    return jsonify({
        "s": eng.state,
        "target": curr_target,
        "progs": PROGRAMS
    })

# ==========================================
# UI (Dark & Neon)
# ==========================================
HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HACKER ELITE</title>
<style>
    body { background: #050505; color: #00ff88; font-family: monospace; margin: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
    
    /* Layout */
    .top { height: 50px; background: #111; border-bottom: 2px solid #00ff88; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; font-size: 20px;}
    .content { flex: 1; display: grid; grid-template-columns: 250px 1fr; }
    
    /* Side Panel */
    .side { background: #080808; border-left: 1px solid #333; padding: 15px; display: flex; flex-direction: column; gap: 15px;}
    .stat-row { margin-bottom: 5px; }
    .bar { height: 10px; background: #222; border-radius: 5px; overflow: hidden;}
    .fill { height: 100%; width: 100%; transition: width 0.3s; background: #00ff88;}
    
    /* Main Area */
    .main { padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;}
    
    /* Lists */
    .list-container { width: 100%; height: 100%; overflow-y: auto; padding: 10px;}
    .card { background: #111; border: 1px solid #333; padding: 15px; margin-bottom: 10px; border-radius: 8px; cursor: pointer; display:flex; justify-content:space-between;}
    .card:hover { border-color: #00ff88; background: #0a1a0a; }

    /* Hack Screen */
    .hack-screen { width: 100%; max-width: 600px; display: flex; flex-direction: column; gap: 20px;}
    .target-box { background: #111; padding: 20px; border: 2px solid #00ff88; border-radius: 10px; text-align: center;}
    
    .actions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .btn { padding: 15px; background: #002200; color: #afa; border: 1px solid #004400; cursor: pointer; border-radius: 5px; text-align: center; }
    .btn:hover { background: #003300; border-color: #0f0; }
    .btn small { display: block; font-size: 10px; color: #5a5; margin-top: 5px;}
    
    .btn-def { border-color: #004455; background: #001122; color: #aaf; }
    .btn-def:hover { border-color: #0088aa; background: #002244; }

    /* Modal */
    .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.9); display: none; flex-direction: column; justify-content: center; align-items: center; color: red; font-size: 40px; z-index: 99;}

    /* Shop */
    .shop-btn { width: 100%; padding: 10px; background: #222; border: 1px solid #444; color: #ccc; cursor: pointer; margin-top: 5px;}
    .shop-btn:hover { color: gold; border-color: gold; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #111; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px;}
</style>
</head>
<body>

<div id="game-over" class="modal">
    <div>SYSTEM FAILURE</div>
    <button onclick="api('reset')" style="margin-top:20px; padding:10px 30px; font-size:20px; background:red; border:none; cursor:pointer;">RESET</button>
</div>

<div class="top">
    <div>HACKER ELITE</div>
    <div style="color:gold">$<span id="ui-money">0</span></div>
</div>

<div class="content">
    <div class="side">
        <div class="stat-row">
            <div>סיכון (Trace) <span id="val-risk">0%</span></div>
            <div class="bar"><div id="bar-risk" class="fill" style="background:red"></div></div>
        </div>
        <div class="stat-row">
            <div>זיכרון (RAM) <span id="val-ram">20</span></div>
            <div class="bar"><div id="bar-ram" class="fill" style="background:cyan"></div></div>
        </div>
        
        <div style="background:black; padding:10px; height:150px; overflow-y:auto; border:1px solid #333; font-size:12px; color:#aaa;" id="log-box"></div>
        
        <div style="margin-top:auto">
            <button class="shop-btn" onclick="api('buy','ram')">+RAM ($200)</button>
            <button class="shop-btn" onclick="api('buy','cpu')">+CPU ($1000)</button>
        </div>
    </div>
    
    <div class="main">
        
        <!-- TARGET LIST -->
        <div id="view-list" class="list-container"></div>
        
        <!-- HACKING INTERFACE -->
        <div id="view-hack" class="hack-screen" style="display:none;">
            <div class="target-box">
                <h2 id="t-name" style="margin:0; color:yellow">...</h2>
                <div style="margin-top:10px;">HP SERVER</div>
                <div class="bar" style="border:1px solid yellow"><div id="bar-hp" class="fill" style="background:yellow"></div></div>
                <button onclick="api('disc')" style="margin-top:10px; background:none; border:1px solid red; color:red; cursor:pointer;">[ התנתק / טען RAM ]</button>
            </div>
            
            <div class="actions-grid" id="btns-area"></div>
        </div>

    </div>
</div>

<script>
const API = "{{ api }}";
window.onload = () => api('init');

async function api(a, v=null) {
    try {
        let res = await fetch(API, {
            method:'POST', headers:{'Content-Type':'application/json'},
            body:JSON.stringify({act:a, val:v})
        });
        let d = await res.json();
        render(d);
    } catch(e) { console.error(e); }
}

function render(d) {
    let s = d.s;
    
    // Game Over
    document.getElementById("game-over").style.display = s.game_over ? "flex" : "none";
    
    // Stats
    document.getElementById("ui-money").innerText = s.money;
    document.getElementById("val-risk").innerText = s.risk + "%";
    document.getElementById("bar-risk").style.width = s.risk + "%";
    document.getElementById("val-ram").innerText = s.ram + "/" + s.max_ram;
    document.getElementById("bar-ram").style.width = (s.ram / s.max_ram) * 100 + "%";

    // Log
    let l = document.getElementById("log-box");
    l.innerHTML = s.log.join("<br>");

    // Views
    if (d.target) {
        document.getElementById("view-list").style.display = "none";
        document.getElementById("view-hack").style.display = "flex";
        
        // Target Info
        document.getElementById("t-name").innerText = d.target.name;
        let hpPct = (d.target.hp / d.target.max_hp) * 100;
        document.getElementById("bar-hp").style.width = hpPct + "%";
        
        // Buttons
        let bHtml = "";
        for (let k in d.progs) {
            let p = d.progs[k];
            let cls = p.type === 'def' ? 'btn-def' : '';
            // כפתור חסום אם אין RAM
            let dis = s.ram < p.cost ? "opacity:0.3; pointer-events:none;" : "";
            
            bHtml += `<div class="btn ${cls}" style="${dis}" onclick="api('run','${k}')">
                <div>${p.name}</div>
                <small>${p.cost} RAM | ${p.dmg || 0} DMG | ${p.heal || 0}% HEAL</small>
            </div>`;
        }
        document.getElementById("btns-area").innerHTML = bHtml;
        
    } else {
        document.getElementById("view-list").style.display = "block";
        document.getElementById("view-hack").style.display = "none";
        
        let lHtml = "";
        if (s.targets.length === 0) lHtml = "<center>מחפש שרתים...</center>";
        s.targets.forEach(t => {
            lHtml += `<div class="card" onclick="api('conn','${t.id}')">
                <div style="font-weight:bold">${t.name}</div>
                <div style="font-size:12px; color:#aaa;">HP: ${t.max_hp} | Loot: $${t.cash}</div>
            </div>`;
        });
        document.getElementById("view-list").innerHTML = lHtml;
    }
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5006, debug=True)
