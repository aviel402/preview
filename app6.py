import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key = 'pokemon_master_secret_key_v1'

# ==========================================
# 📘 יחסי סוגים (TYPE MATCHUPS)
# ==========================================
TYPE_CHART = {
    "אש":    {"עשב": 2.0, "מים": 0.5, "אש": 0.5},
    "מים":   {"אש": 2.0, "עשב": 0.5, "מים": 0.5},
    "עשב":  {"מים": 2.0, "אש": 0.5, "עשב": 0.5},
    "חשמל": {"מים": 2.0, "עשב": 0.5, "חשמל": 0.5},
    "רגיל":  {}
}

# ==========================================
# 🎒 חפצים (ITEMS DB)
# ==========================================
ITEMS_DB = {
    "פוקדור":     {"type": "ball", "bonus": 1.0, "desc": "לכדידת פוקימונים בסיסית"},
    "סופר-דור":   {"type": "ball", "bonus": 1.5, "desc": "סיכוי תפיסה מוגבר"},
    "אולטרה-דור": {"type": "ball", "bonus": 2.0, "desc": "תפיסה באיכות גבוהה"},
    "שיקוי חיים": {"type": "heal", "val": 30,   "desc": "מרפא 30 HP לפוקימון הפעיל"},
    "שיקוי על":   {"type": "heal", "val": 70,   "desc": "מרפא 70 HP לפוקימון הפעיל"}
}

# ==========================================
# 🐾 פוקימונים (POKEMON SPECIES)
# ==========================================
POKEMON_SPECIES = [
    {"name": "פידג'י",   "type": "רגיל", "hp": 35, "max": 35, "atk": 8,  "catch_rate": 0.6,  "icon": "🐦"},
    {"name": "קטרפי",   "type": "עשב",  "hp": 30, "max": 30, "atk": 6,  "catch_rate": 0.7,  "icon": "🐛"},
    {"name": "פיקאצ'ו",  "type": "חשמל", "hp": 45, "max": 45, "atk": 14, "catch_rate": 0.4,  "icon": "⚡"},
    {"name": "צ'רמנדר",  "type": "אש",   "hp": 50, "max": 50, "atk": 15, "catch_rate": 0.35, "icon": "🔥"},
    {"name": "בלבזאור",  "type": "עשב",  "hp": 55, "max": 55, "atk": 12, "catch_rate": 0.35, "icon": "🍃"},
    {"name": "סקוורטל",  "type": "מים",  "hp": 52, "max": 52, "atk": 13, "catch_rate": 0.35, "icon": "💧"},
    {"name": "ג'יגליפאף", "type": "רגיל", "hp": 60, "max": 60, "atk": 9,  "catch_rate": 0.5,  "icon": "רוז"},
    {"name": "סנורלקס",  "type": "רגיל", "hp": 110,"max": 110,"atk": 20, "catch_rate": 0.15, "icon": "🐻"},
    {"name": "מיוטו",    "type": "חשמל", "hp": 150,"max": 150,"atk": 28, "catch_rate": 0.05, "icon": "🔮"}
]

ROUTES = [
    {"name": "דרך 1 - דשא נמוך", "icon": "🌿"},
    {"name": "דרך 2 - יער עבות",   "icon": "🌲"},
    {"name": "דרך 3 - מערת סלעים", "icon": "⛰️"},
    {"name": "אגם המים הצלולים", "icon": "🌊"}
]

# ==========================================
# ⚙️ מנוע המשחק
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state:
            # פוקימון התחלתי - פיקאצ'ו
            starter = {"name": "פיקאצ'ו", "type": "חשמל", "hp": 45, "max": 45, "atk": 14, "icon": "⚡"}
            self.state = {
                "x": 0, "y": 0,
                "gold": 50,
                "team": [starter],
                "active_idx": 0,
                "inv": ["פוקדור", "פוקדור", "שיקוי חיים"],
                "map": {},
                "visited": ["0,0"],
                "log": [{"text": "ברוך הבא לעולם הפוקימונים! יצאת לדרך עם פיקאצ'ו.", "type": "sys"}]
            }
            self.create_room(0, 0, safe=True)
        else:
            self.state = state

    def pos(self): return f"{self.state['x']},{self.state['y']}"
    
    def log(self, txt, t="game"): self.state["log"].append({"text": txt, "type": t})

    def active_mon(self):
        if 0 <= self.state["active_idx"] < len(self.state["team"]):
            return self.state["team"][self.state["active_idx"]]
        return None

    def create_room(self, x, y, safe=False):
        k = f"{x},{y}"
        if k in self.state["map"]: return

        r_data = {
            "name": "", "icon": "", "enemy": None, "items": [], 
            "is_shop": False, "is_center": False
        }

        if safe:
            r_data["name"] = "מרכז פוקימונים ראשי"
            r_data["icon"] = "🏥"
            r_data["is_center"] = True
            self.state["map"][k] = r_data
            return

        rnd = random.random()
        if rnd < 0.15:
            r_data["name"] = "חנות פוקדורים (PokéMart)"
            r_data["icon"] = "🏪"
            r_data["is_shop"] = True
        elif rnd < 0.25:
            r_data["name"] = "מרכז פוקימונים"
            r_data["icon"] = "🏥"
            r_data["is_center"] = True
        else:
            route = random.choice(ROUTES)
            r_data["name"] = route["name"]
            r_data["icon"] = route["icon"]
            
            # מפגש עם פוקימון פראי (60% סיכוי)
            if random.random() < 0.60:
                spec = random.choice(POKEMON_SPECIES).copy()
                r_data["enemy"] = spec

            if random.random() < 0.20:
                r_data["items"].append(random.choice(["פוקדור", "שיקוי חיים"]))

        self.state["map"][k] = r_data

    def move(self, dx, dy):
        r_now = self.state["map"][self.pos()]
        if r_now.get("enemy"):
            self.log("פוקימון פראי חוסם אותך! עליך לתקוף, לתפוס או לברוח.", "danger")
            return

        self.state["x"] += dx
        self.state["y"] += dy
        k = self.pos()
        
        self.create_room(self.state["x"], self.state["y"])
        if k not in self.state["visited"]: self.state["visited"].append(k)
        
        r = self.state["map"][k]
        self.log(f"הגעת ל-{r['name']}.", "sys")
        if r.get("is_center"): self.log("🏥 מרכז פוקימונים! לחץ על כפתור הריפוי כדי לרפא את כל הצוות.", "success")
        if r.get("is_shop"): self.log("🏪 חנות פוקדורים וציוד פתוחה!", "gold")
        if r.get("enemy"): self.log(f"⚠️ פוקימון פראי הופיע: {r['enemy']['name']} ({r['enemy']['type']})!", "danger")
        if r["items"]: self.log(f"🔎 מצאת על הרצפה: {', '.join(r['items'])}", "success")

    def attack(self):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        player_mon = self.active_mon()

        if not enemy: return self.log("אין פוקימון לתקוף.", "info")
        if not player_mon or player_mon["hp"] <= 0:
            return self.log("הפוקימון הפעיל שלך מעולף! החלף פוקימון.", "danger")

        # חישוב יחסי סוגים
        p_type = player_mon.get("type", "רגיל")
        e_type = enemy.get("type", "רגיל")
        mult = TYPE_CHART.get(p_type, {}).get(e_type, 1.0)

        base_dmg = player_mon["atk"]
        player_dmg = int(random.randint(base_dmg - 2, base_dmg + 4) * mult)
        
        enemy["hp"] -= player_dmg
        
        eff_msg = ""
        if mult > 1.0: eff_msg = " (סופר אפקטיבי! ⚡)"
        elif mult < 1.0: eff_msg = " (לא מאוד אפקטיבי...)"

        self.log(f"⚔️ {player_mon['name']} תקף את {enemy['name']} והסב {player_dmg} נזק!{eff_msg}", "sys")

        if enemy["hp"] <= 0:
            gold_drop = random.randint(15, 35)
            self.state["gold"] += gold_drop
            self.log(f"💀 {enemy['name']} התעלף! קיבלת {gold_drop} מטבעות.", "gold")
            r["enemy"] = None
        else:
            # התקפת נגד של האויב
            e_mult = TYPE_CHART.get(e_type, {}).get(p_type, 1.0)
            e_dmg = int(max(1, enemy["atk"] - random.randint(0, 3)) * e_mult)
            player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
            self.log(f"💥 {enemy['name']} החזיר התקפה וגרם ל-{e_dmg} נזק!", "danger")
            if player_mon["hp"] <= 0:
                self.log(f"😵 {player_mon['name']} התעלף!", "danger")

    def catch(self, ball_name):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        if not enemy: return self.log("אין פוקימון פראי לתפוס!", "info")

        if ball_name not in self.state["inv"]:
            return self.log(f"אין לך {ball_name} בתיק!", "danger")

        self.state["inv"].remove(ball_name)
        ball_data = ITEMS_DB.get(ball_name, {"bonus": 1.0})

        # נוסחת תפיסה: HP נמוך = סיכוי גבוה
        hp_factor = 1.0 - (enemy["hp"] / enemy["max"])
        base_rate = enemy.get("catch_rate", 0.4)
        chance = (base_rate + (hp_factor * 0.45)) * ball_data["bonus"]

        if random.random() < chance:
            self.log(f"🎉 תפסת את {enemy['name']}!", "gold")
            if len(self.state["team"]) < 6:
                self.state["team"].append(enemy.copy())
                self.log(f"{enemy['name']} הוסף לצוות שלך!", "success")
            else:
                self.log(f"הצוות מלא (6/6). {enemy['name']} נשלח לבית הגידול.", "sys")
            r["enemy"] = None
        else:
            self.log(f"🔴 {enemy['name']} השתחרר מ{ball_name}!", "danger")
            # הפוקימון תוקף
            player_mon = self.active_mon()
            if player_mon and player_mon["hp"] > 0:
                e_dmg = max(1, enemy["atk"] - random.randint(0, 2))
                player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
                self.log(f"💥 {enemy['name']} התרגז ותקף ב-{e_dmg} נזק!", "danger")

    def heal_team(self):
        r = self.state["map"][self.pos()]
        if not r.get("is_center"):
            return self.log("אתה חייב להיות במרכז פוקימונים כדי לרפא!", "info")
        
        for mon in self.state["team"]:
            mon["hp"] = mon["max"]
        self.log("💖 כל הפוקימונים בצוות חזרו לבריאות מלאה!", "success")

    def take(self):
        r = self.state["map"][self.pos()]
        if not r["items"]: return self.log("אין מה לאסוף כאן.", "info")
        for item in r["items"]: self.state["inv"].append(item)
        self.log(f"אספת: {', '.join(r['items'])}", "success")
        r["items"] = []

    def use_item(self, item_name):
        if item_name not in self.state["inv"]: return
        eff = ITEMS_DB.get(item_name)
        if not eff: return

        if eff["type"] == "heal":
            mon = self.active_mon()
            if not mon: return
            if mon["hp"] >= mon["max"]: return self.log(f"{mon['name']} כבר בבריאות מלאה.", "info")
            mon["hp"] = min(mon["max"], mon["hp"] + eff["val"])
            self.log(f"השתמשת ב-{item_name} על {mon['name']} → +{eff['val']} HP", "success")
            self.state["inv"].remove(item_name)
        elif eff["type"] == "ball":
            self.catch(item_name)

    def buy(self, item_name):
        r = self.state["map"][self.pos()]
        if not r.get("is_shop"): return

        prices = {"פוקדור": 15, "סופר-דור": 35, "אולטרה-דור": 70, "שיקוי חיים": 20, "שיקוי על": 50}
        cost = prices.get(item_name, 999)

        if self.state["gold"] < cost:
            return self.log(f"אין לך מספיק זהב! צריך {cost} מטבעות.", "danger")

        self.state["gold"] -= cost
        self.state["inv"].append(item_name)
        self.log(f"קנית {item_name} ב-{cost} זהב!", "success")

    def switch_mon(self, idx):
        if 0 <= idx < len(self.state["team"]):
            self.state["active_idx"] = idx
            self.log(f"שלחת לקרב את {self.state['team'][idx]['name']}!", "sys")

    def get_ui_data(self):
        k = self.pos()
        r = self.state["map"][k]
        grid = []
        for dy in range(1, -2, -1):
            row = []
            for dx in range(-1, 2):
                p2 = f"{self.state['x']+dx},{self.state['y']+dy}"
                val, cls = "", "fog"
                if dx==0 and dy==0: val, cls = "🚶", "player"
                elif p2 in self.state["visited"]:
                    val = "⚠️" if self.state["map"][p2].get("enemy") else self.state["map"][p2]["icon"]
                    cls = "known"
                row.append({"val":val, "cls":cls})
            grid.append(row)

        return {
            "gold": self.state["gold"],
            "team": self.state["team"],
            "active_idx": self.state["active_idx"],
            "inv": self.state["inv"], 
            "log": self.state["log"][-20:],
            "room_name": r["name"], 
            "is_shop": r.get("is_shop", False), 
            "is_center": r.get("is_center", False),
            "items": r["items"], 
            "enemy": r.get("enemy"),
            "map_grid": grid
        }

# ==========================================
# ROUTES
# ==========================================
@app.route("/")
def index():
    if "uid" not in session: session["uid"] = str(uuid.uuid4())
    return render_template_string(HTML, api=url_for("process"))

@app.route("/game/process", methods=["POST"])
def process():
    d = request.json
    try: eng = Engine(session.get("poke_game"))
    except: eng = Engine(None)

    act = d.get("action")
    val = d.get("val")

    if act == "move": eng.move(*val)
    elif act == "attack": eng.attack()
    elif act == "take": eng.take()
    elif act == "use": eng.use_item(val)
    elif act == "catch": eng.catch(val)
    elif act == "buy": eng.buy(val)
    elif act == "heal": eng.heal_team()
    elif act == "switch": eng.switch_mon(val)
    elif act == "reset": eng = Engine(None)

    session["poke_game"] = eng.state
    return jsonify(eng.get_ui_data())


# ==========================================
# HTML + GUI
# ==========================================
HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>פוקימון - מסע המאמנים</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arimo:wght@400;700&display=swap');
    :root { --bg:#121820; --panel:#1e2638; --panel2: #2a354d; --acc:#ffcc00; --border:#3d4b68;}
    body { background: var(--bg); color: #dedde6; margin: 0; font-family: 'Arimo', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow:hidden;}
    header { background: #0b0f19; padding: 10px 16px; display: flex; justify-content: space-between; align-items:center; border-bottom: 3px solid var(--border);}
    .title {font-weight:900; color:var(--acc); letter-spacing:1px; margin:0; font-size:18px;}
    .stat-badge { background: #222d42; border:1px solid var(--border); padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: bold;}
    
    .viewport { flex: 1; display: grid; grid-template-columns: 2fr 1fr; gap: 8px; padding: 10px; overflow: hidden; background:radial-gradient(circle at center, #1a2333 0%, #0d121c 100%);}
    .side-panel { display: flex; flex-direction: column; gap: 10px; }
    
    .map-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; margin: 0 auto; width: 150px; }
    .map-cell { height: 45px; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 6px; border:1px solid rgba(255,255,255,0.05);}
    .map-cell.player { border: 2px solid #00ffcc; background: rgba(0,255,204, 0.2); }
    .map-cell.known { background: rgba(255,255,255, 0.08); }

    .room-card { background: var(--panel2); border-left: 5px solid var(--acc); border-radius: 6px; padding: 10px; text-align: center; display:flex; flex-direction:column; gap:8px;}
    .dynamic-interaction {display:none; background:#3b1818; padding:10px; border-radius:6px; border:2px dashed #a83232; flex-direction:column; gap:6px;}
    .hp-track { width: 100%; height: 12px; background: rgba(0,0,0,0.6); border-radius: 10px; overflow: hidden; }
    .hp-fill { height: 100%; background: linear-gradient(90deg, #42b883, #00ffcc); width: 100%; transition: 0.2s;}

    .shop-box, .center-box {display:none; background:#18281e; padding:10px; border-radius:6px; border:1px solid #32a869;}
    .btn-action { background:#2a5c3e; border:1px solid #42b883; border-radius:4px; padding:6px; margin:3px 0; width:100%; font-weight:bold; cursor:pointer; color:white;}
    .btn-action:active {transform:scale(0.98);}

    .log-container { background: #0a0d14; border-radius: 6px; border: 1px solid var(--border); padding: 10px; overflow-y: auto; display:flex; flex-direction:column-reverse; gap:4px;}
    .msg { padding: 6px; border-radius: 4px; font-size: 13px; border-right: 3px solid transparent; background:rgba(255,255,255,0.02);}
    .sys { color: #7aa2f7; border-right-color:#3d59a1;}
    .danger { color: #f7768e; border-right-color:#db4b4b; background: rgba(255,0,0,0.1); }
    .success { color: #9ece6a; border-right-color:#73daca; background: rgba(0,255,0,0.05);}
    .gold { color: #e0af68; border-right-color:#ff9e3b; font-weight:bold;}

    .team-bar { display:flex; gap:6px; background:var(--panel); padding:6px; border-radius:6px; overflow-x:auto;}
    .mon-slot { background:#121820; border:1px solid var(--border); padding:6px; border-radius:4px; font-size:12px; cursor:pointer; min-width:70px; text-align:center;}
    .mon-slot.active { border-color:var(--acc); background:#28344d;}

    .controls { height: 150px; background: #151b26; border-top: 3px solid var(--border); padding: 10px; display: grid; grid-template-columns: 1fr 140px; gap: 15px; align-items: center;}
    .d-pad { direction: ltr; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; width: 140px; height:100%;}
    .btn-arr { background: #222d42; color: #fff; border:none; border-radius: 6px; font-size: 18px; cursor: pointer;}
    .btn-arr:active { background: #32415e; }
    .up { grid-column: 2; grid-row: 1; }
    .down { grid-column: 2; grid-row: 2; }
    .left { grid-column: 1; grid-row: 2; }
    .right { grid-column: 3; grid-row: 2; }

    .main-actions { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; height: 100%; }
    .act-btn { height: 100%; font-weight: bold; font-size: 14px; border: none; border-radius: 6px; cursor: pointer; color:#fff;}
    .btn-atk { background: #a22929; }
    .btn-catch { background: #e0af68; color:black; }
    .btn-inv { background: #3d59a1; }

    .modal { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); z-index:99; justify-content:center; align-items:center;}
    .modal-box { background:var(--panel2); width:85%; max-width:400px; padding:20px; border-radius:8px; border:1px solid var(--border);}
</style>
</head>
<body>

<header>
    <div class="title">🔴 POKEMON ADVENTURE</div>
    <div style="display:flex; gap:8px;">
        <div class="stat-badge" style="color:gold;">💰 <span id="gold">50</span></div>
    </div>
</header>

<div class="viewport">
    <div class="side-panel">
        <div class="map-grid" id="map-target"></div>
        
        <div class="room-card">
            <div id="loc-name" style="font-weight:900; font-size:15px;">...</div>
            
            <!-- פוקימון פראי -->
            <div id="enemy-box" class="dynamic-interaction">
                <div style="display:flex; justify-content:space-between;">
                    <strong id="en-name" style="color:#ff8181;"></strong>
                    <span><span id="en-hp"></span>/<span id="en-max"></span> HP</span>
                </div>
                <div class="hp-track"><div id="en-fill" class="hp-fill" style="width:100%"></div></div>
            </div>

            <!-- חנות -->
            <div id="shop-box" class="shop-box">
                <div style="color:#ffcc00; font-size:14px; margin-bottom:6px;">🏪 חנות פוקדורים</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                    <button class="btn-action" onclick="send('buy','פוקדור')">פוקדור (15💰)</button>
                    <button class="btn-action" onclick="send('buy','סופר-דור')">סופר-דור (35💰)</button>
                    <button class="btn-action" onclick="send('buy','אולטרה-דור')">אולטרה (70💰)</button>
                    <button class="btn-action" onclick="send('buy','שיקוי חיים')">שיקוי (20💰)</button>
                </div>
            </div>

            <!-- מרכז פוקימונים -->
            <div id="center-box" class="center-box">
                <div style="color:#00ffcc; font-size:14px; margin-bottom:6px;">🏥 מרכז פוקימונים</div>
                <button class="btn-action" style="background:#00a86b;" onclick="send('heal')">💖 רפא את כל הצוות</button>
            </div>
        </div>

        <!-- צוות הפוקימונים -->
        <div class="team-bar" id="team-bar"></div>
    </div>

    <div class="log-container" id="log-box"></div>
</div>

<!-- מודל תיק -->
<div class="modal" id="inv-modal" onclick="if(event.target==this) toggleModal('inv-modal')">
    <div class="modal-box">
        <h3 style="margin-top:0; color:var(--acc);">🎒 התיק שלי</h3>
        <div id="inv-list" style="display:grid; gap:6px;"></div>
    </div>
</div>

<div class="controls">
    <div class="main-actions">
        <button class="act-btn btn-atk" onclick="send('attack')">⚔️ התקף</button>
        <button class="act-btn btn-catch" onclick="send('catch', 'פוקדור')">🔴 זרוק פוקדור</button>
        <button class="act-btn btn-inv" onclick="toggleModal('inv-modal')">🎒 תיק</button>
    </div>

    <div class="d-pad">
        <button class="btn-arr up" onclick="send('move', [0,1])">⬆</button>
        <button class="btn-arr left" onclick="send('move', [1,0])">⬅</button>
        <button class="btn-arr down" onclick="send('move', [0,-1])">⬇</button>
        <button class="btn-arr right" onclick="send('move', [-1,0])">➡</button>
    </div>
</div>

<script>
const API = "{{ api }}";

window.onload = () => send('init');

async function send(act, val=null) {
    try {
        let res = await fetch(API, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: act, val: val})
        });
        let d = await res.json();

        // הלוגים
        let logBox = document.getElementById("log-box");
        logBox.innerHTML = "";
        d.log.slice().reverse().forEach(msg => {
            logBox.innerHTML += `<div class="msg ${msg.type}">${msg.text}</div>`;
        });

        // מיני מפה
        let mapH = "";
        d.map_grid.forEach(row => {
            row.forEach(c => mapH += `<div class='map-cell ${c.cls}'>${c.val}</div>`);
        });
        document.getElementById("map-target").innerHTML = mapH;

        // סטטוסים
        document.getElementById("gold").innerText = d.gold;
        document.getElementById("loc-name").innerText = d.room_name;

        // צוות פוקימונים
        let teamH = "";
        d.team.forEach((m, idx) => {
            let activeCls = (idx === d.active_idx) ? "active" : "";
            teamH += `
                <div class="mon-slot ${activeCls}" onclick="send('switch', ${idx})">
                    <div>${m.icon || '🐾'} ${m.name}</div>
                    <div style="font-size:10px;">${m.hp}/${m.max} HP</div>
                </div>`;
        });
        document.getElementById("team-bar").innerHTML = teamH;

        // אויב
        document.getElementById("enemy-box").style.display = d.enemy ? "flex" : "none";
        if (d.enemy) {
            document.getElementById("en-name").innerText = `${d.enemy.icon || ''} ${d.enemy.name} (${d.enemy.type})`;
            document.getElementById("en-hp").innerText = d.enemy.hp;
            document.getElementById("en-max").innerText = d.enemy.max;
            document.getElementById("en-fill").style.width = (d.enemy.hp / d.enemy.max * 100) + "%";
        }

        // חנות ומרכז
        document.getElementById("shop-box").style.display = d.is_shop ? "block" : "none";
        document.getElementById("center-box").style.display = d.is_center ? "block" : "none";

        // תיק
        let invL = document.getElementById("inv-list");
        invL.innerHTML = "";
        if (d.inv.length === 0) {
            invL.innerHTML = "<div style='text-align:center;'>התיק ריק...</div>";
        } else {
            d.inv.forEach(it => {
                invL.innerHTML += `<button class="btn-action" onclick="send('use','${it}'); toggleModal('inv-modal')">${it}</button>`;
            });
        }

    } catch(e) { console.error(e); }
}

function toggleModal(id) {
    let el = document.getElementById(id);
    el.style.display = (el.style.display === "flex") ? "none" : "flex";
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5007, debug=True)
