import random
import uuid
import time
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key = 'parasite_arena_enhanced_v2'

# ==========================================
# 🧬 מאגר גופים משופר
# ==========================================
HOSTS = {
    # Tier 1 - חלשים
    "blob":    {"name": "עיסה", "icon": "🦠", "hp": 25, "atk": 3, "tier": 1, "color": "#4a9"},
    "rat":     {"name": "עכברוש", "icon": "🐀", "hp": 35, "atk": 6, "tier": 1, "color": "#999"},
    "drone":   {"name": "רחפן", "icon": "🛸", "hp": 30, "atk": 5, "tier": 1, "color": "#69f"},
    
    # Tier 2 - בינוניים
    "wolf":    {"name": "זאב", "icon": "🐺", "hp": 65, "atk": 14, "tier": 2, "color": "#f93"},
    "soldier": {"name": "חייל", "icon": "👮", "hp": 85, "atk": 16, "tier": 2, "color": "#3af"},
    "alien":   {"name": "חייזר", "icon": "👽", "hp": 75, "atk": 19, "tier": 2, "color": "#9f3"},

    # Tier 3 - חזקים
    "robot":   {"name": "רובוט", "icon": "🤖", "hp": 160, "atk": 22, "tier": 3, "color": "#f6f"},
    "beast":   {"name": "מפלצת", "icon": "👹", "hp": 190, "atk": 27, "tier": 3, "color": "#f33"},
    "dragon":  {"name": "דרקון", "icon": "🐲", "hp": 320, "atk": 48, "tier": 3, "color": "#fa0"}
}
HOSTSN={
    't1':["blob", "rat", "drone"],
    't2':["wolf", "soldier", "alien"],
    't3':["robot", "beast"]
}
# תוספות ל-HOSTS

HOSTS.update({
    # Tier 1
    "snake":   {"name": "נחש",    "icon": "🐍", "hp": 28,  "atk": 4,  "tier": 1, "color": "#6a4"},
    "bug":     {"name": "חרק",    "icon": "🪲", "hp": 20,  "atk": 5,  "tier": 1, "color": "#7a7"},

    # Tier 2
    "bandit":  {"name": "שודד",   "icon": "🗡️", "hp": 90,  "atk": 18, "tier": 2, "color": "#a63"},
    "golem":   {"name": "גולם",   "icon": "🗿", "hp": 120, "atk": 15, "tier": 2, "color": "#888"},

    # Tier 3
    "giant":   {"name": "ענק",    "icon": "🦣", "hp": 260, "atk": 35, "tier": 3, "color": "#964"},
    "lich":    {"name": "אל-מת",  "icon": "☠️", "hp": 210, "atk": 40, "tier": 3, "color": "#556"},
})

HOSTSN["t1"] += ["snake", "bug"]
HOSTSN["t2"] += ["bandit", "golem"]
HOSTSN["t3"] += ["giant", "lich"]

class Engine:
    def __init__(self, state=None):
        if not state or "rivals" not in state:
            self.state = {
                "x": 0, "y": 0,
                "host": "blob",
                "hp": 25, "max_hp": 25,
                "is_dead": False,
                "map_size": 10,
                "rivals": [], 
                "map_content": {},
                "visited": ["0,0"],
                "log": [{"text": "🎮 ברוך הבא לזירת הטפיל! השמד את כל המתחרים.", "type": "sys"}],
                # Stats
                "kills": 0,
                "possessions": 0,
                "start_time": time.time(),
                "turn_count": 0
            }
            self.init_arena()
        else:
            self.state = state

    def log(self, t, type="game"): 
        self.state["log"].append({"text": t, "type": type})
        if len(self.state["log"]) > 50: self.state["log"].pop(0)

    def init_arena(self):
        names = ["אלפא", "בטא", "גמא", "דלתא", "נמסיס", "צללית", "רוח", "זעם"]
        for i in range(1,8):
            for n in names:
                bot = {
                    "name": n+f'{i}',
                    "host": "rat",
                    "hp": 35, "max_hp": 35,
                    "x": random.randint(-10, 11),
                    "y": random.randint(-10, 11),
                    "dead": False
                }
                self.state["rivals"].append(bot)
        
        # מילוי הזירה במפלצות
        for x in range(-10, 11):
            for y in range(-10, 11):
                if x==0 and y==0: continue
                
                if random.random() < 0.55:  # 55% סיכוי למפלצת
                    rng = random.random()
                    tier = "rat"
                    if rng < 0.5: tier = random.choice(HOSTSN['t1'])
                    elif rng < 0.8: tier = random.choice(HOSTSN['t2'])
                    elif rng < 0.96: tier = random.choice(HOSTSN['t3'])
                    else: tier = "dragon"
                    
                    self.state["map_content"][f"{x},{y}"] = {
                        "type": tier,
                        "hp": HOSTS[tier]["hp"],
                        "alive": True
                    }

    def pos(self): return f"{self.state['x']},{self.state['y']}"

    def process_ai(self):
        self.state["turn_count"] += 1
        px, py = self.state["x"], self.state["y"]
        pos_key = self.pos()

        # 1. תור הבוטים - AI משופר
        for bot in self.state["rivals"]:
            if bot["dead"]: continue
            
            if bot["x"] == px and bot["y"] == py:
                if not self.state["is_dead"]:
                    dmg = HOSTS[bot["host"]]["atk"] + random.randint(0, 3)
                    self.state["hp"] -= dmg
                    self.log(f"⚔️ {bot['name']} תוקף! -{dmg} HP", "danger")
            else:
                # AI מתקדם יותר
                bot_pos = f"{bot['x']},{bot['y']}"
                local_mon = self.state["map_content"].get(bot_pos)
                
                if local_mon and local_mon["alive"]:
                    mon_dmg = HOSTS[local_mon["type"]]["atk"]
                    bot_dmg = HOSTS[bot["host"]]["atk"]
                    
                    bot["hp"] -= mon_dmg
                    
                    # סיכוי יותר גבוה לבוט לנצח
                    if bot["hp"] > 0 and (bot_dmg > mon_dmg or random.random() < 0.4):
                        local_mon["alive"] = False
                        # שדרוג חכם - רק אם הגוף יותר טוב
                        if HOSTS[local_mon["type"]]["hp"] > bot["max_hp"]:
                            bot["host"] = local_mon["type"]
                            bot["max_hp"] = HOSTS[local_mon["type"]]["hp"]
                            bot["hp"] = bot["max_hp"]
                            if abs(bot['x']-px) < 4 and abs(bot['y']-py) < 4:
                                self.log(f"⚠️ {bot['name']} שדרג ל-{HOSTS[local_mon['type']]['name']}!", "warning")
                    
                    if bot["hp"] <= 0:
                        bot["dead"] = True
                else:
                    # תנועה חכמה יותר
                    dx, dy = 0, 0
                    dist = abs(bot["x"] - px) + abs(bot["y"] - py)
                    
                    # בוטים חזקים רודפים ממרחק רחוק יותר
                    chase_dist = 4 if HOSTS[bot["host"]]["tier"] == 1 else 6
                    
                    if dist <= chase_dist and not self.state["is_dead"]:
                        dx = 1 if bot["x"] < px else (-1 if bot["x"] > px else 0)
                        dy = 1 if bot["y"] < py else (-1 if bot["y"] > py else 0)
                    else:
                        dx = random.choice([-1, 0, 1])
                        dy = random.choice([-1, 0, 1])
                    
                    bot["x"] = max(-10, min(10, bot["x"] + dx))
                    bot["y"] = max(-10, min(10, bot["y"] + dy))

        # 2. מפלצות בחדר שלי
        my_room_mon = self.state["map_content"].get(pos_key)
        if my_room_mon and my_room_mon["alive"] and not self.state["is_dead"]:
            m_atk = HOSTS[my_room_mon["type"]]["atk"] + random.randint(0, 2)
            self.state["hp"] -= m_atk
            self.log(f"🩸 {HOSTS[my_room_mon['type']]['name']} תוקף! -{m_atk}", "danger")

        # 3. בדיקת מוות
        if self.state["hp"] <= 0 and not self.state["is_dead"]:
            self.state["hp"] = 0
            self.state["is_dead"] = True
            self.log("💀 הגוף נהרס! השתלט על מישהו כדי להמשיך.", "critical")

    def move(self, dx, dy):
        if self.state["is_dead"]:
            self.log("⛔ רוחות לא יכולות לזוז. השתלט על גוף!", "sys")
            return

        nx = self.state["x"] + dx
        ny = self.state["y"] + dy
        
        if nx < -10 or nx > 10 or ny < -10 or ny > 10:
            self.log("🚧 קיר! לא ניתן לחצות.", "sys")
            return

        self.state["x"] = nx
        self.state["y"] = ny
        
        pos = self.pos()
        if pos not in self.state["visited"]: 
            self.state["visited"].append(pos)
            self.log(f"🗺️ אזור חדש: ({nx}, {ny})", "info")
        
        self.process_ai()

    def attack(self, target_type, idx):
        if self.state["is_dead"]: return

        pos = self.pos()
        my_dmg = HOSTS[self.state["host"]]["atk"] + random.randint(1, 5)

        if target_type == "monster":
            mon = self.state["map_content"].get(pos)
            if mon and mon["alive"]:
                mon["hp"] -= my_dmg
                self.log(f"⚔️ פגעת במפלצת (-{my_dmg})", "success")
                if mon["hp"] <= 0:
                    mon["alive"] = False
                    mon["hp"] = 0
                    self.state["kills"] += 1
                    self.log("💀 המפלצת מתה! הגופה כאן.", "gold")
                self.process_ai()

        elif target_type == "bot":
            active_bots = [b for b in self.state["rivals"] if f"{b['x']},{b['y']}"==pos and not b["dead"]]
            if idx < len(active_bots):
                bot = active_bots[idx]
                bot["hp"] -= my_dmg
                self.log(f"⚔️ תקפת את {bot['name']} (-{my_dmg})", "success")
                if bot["hp"] <= 0:
                    bot["dead"] = True
                    self.state["map_content"][pos] = {"type": bot["host"], "hp": 0, "alive": False}
                    self.state["kills"] += 1
                    self.log(f"🎯 חיסלת את {bot['name']}!", "gold")
                self.process_ai()

    def infect(self, target_type, idx):
        if not self.state["is_dead"]:
            self.log("⛔ רק רוחות יכולות להשתלט!", "sys")
            return

        pos = self.pos()
        new_type = None
        
        if target_type == "monster":
            mon = self.state["map_content"].get(pos)
            if mon:
                new_type = mon["type"]
                del self.state["map_content"][pos]

        elif target_type == "bot":
            active_bots = [b for b in self.state["rivals"] if f"{b['x']},{b['y']}"==pos and not b["dead"]]
            if idx < len(active_bots):
                bot = active_bots[idx]
                new_type = bot["host"]
                bot["dead"] = True
                self.log(f"👻 גנבת את גופו של {bot['name']}!", "gold")

        if new_type:
            self.state["host"] = new_type
            self.state["max_hp"] = HOSTS[new_type]["hp"]
            self.state["hp"] = self.state["max_hp"]
            self.state["is_dead"] = False
            self.state["possessions"] += 1
            self.log(f"🧬 קמת לתחייה כ-{HOSTS[new_type]['name']}!", "success")

    def get_ui(self):
        pos = self.pos()
        
        # מפה רדאר
        grid = []
        radius = 4
        cx, cy = self.state["x"], self.state["y"]
        
        for dy in range(radius, -radius-1, -1):
            row = []
            for dx in range(-radius, radius+1):
                tx, ty = cx + dx, cy + dy
                k = f"{tx},{ty}"
                cell = {"txt":"⬛", "cls":"fog"}
                
                if tx < -10 or tx > 10 or ty < -10 or ty > 10:
                    cell = {"txt":"🚫", "cls":"wall"}
                elif dx==0 and dy==0:
                    cell = {"txt": "●", "cls":"me"}
                elif k in self.state["visited"] or (abs(dx)<=2 and abs(dy)<=2):
                    cont = self.state["map_content"].get(k)
                    bots_here = [b for b in self.state["rivals"] if b["x"]==tx and b["y"]==ty and not b["dead"]]
                    
                    if bots_here: cell = {"txt":"◉", "cls":"rival"}
                    elif cont: 
                        icon = HOSTS[cont["type"]]["icon"]
                        cls = "alive" if cont["alive"] else "corpse"
                        cell = {"txt": icon, "cls": cls}
                    else: cell = {"txt":"·", "cls":"empty"}
                        
                row.append(cell)
            grid.append(row)

        # אויבים בחדר
        room_mon = self.state["map_content"].get(pos)
        room_bots = [b for b in self.state["rivals"] if f"{b['x']},{b['y']}"==pos and not b["dead"]]
        
        live_bots = len([b for b in self.state["rivals"] if not b["dead"]])
        victory = (live_bots == 0)

        scene_objects = []
        
        if room_mon:
            scene_objects.append({
                "type": "monster", "idx": 0, 
                "name": HOSTS[room_mon["type"]]["name"],
                "icon": HOSTS[room_mon["type"]]["icon"],
                "hp": room_mon["hp"],
                "max_hp": HOSTS[room_mon["type"]]["hp"],
                "is_corpse": not room_mon["alive"],
                "color": HOSTS[room_mon["type"]]["color"],
                "tier": HOSTS[room_mon["type"]]["tier"]
            })
            
        for i, b in enumerate(room_bots):
            scene_objects.append({
                "type": "bot", "idx": i,
                "name": b['name'],
                "host_name": HOSTS[b['host']]['name'],
                "icon": HOSTS[b["host"]]["icon"],
                "hp": b["hp"],
                "max_hp": b["max_hp"],
                "is_corpse": False,
                "color": HOSTS[b["host"]]["color"],
                "tier": HOSTS[b["host"]]["tier"]
            })

        # חישוב זמן
        survival_time = int(time.time() - self.state.get("start_time", time.time()))

        return {
            "map": grid,
            "log": self.state["log"],
            "scene": scene_objects,
            "player": {
                "name": HOSTS[self.state["host"]]["name"],
                "icon": HOSTS[self.state["host"]]["icon"],
                "hp": self.state["hp"],
                "max": self.state["max_hp"],
                "dead": self.state["is_dead"],
                "bots_left": live_bots,
                "won": victory,
                "color": HOSTS[self.state["host"]]["color"]
            },
            "stats": {
                "kills": self.state["kills"],
                "possessions": self.state["possessions"],
                "time": survival_time,
                "turns": self.state["turn_count"],
                "explored": len(self.state["visited"])
            }
        }

# ==========================================
#  SERVER
# ==========================================
@app.route("/")
def index():
    if "uid" not in session: session["uid"] = str(uuid.uuid4())
    return render_template_string(HTML, api=url_for("update"))

@app.route("/api", methods=["POST"])
def update():
    try: eng = Engine(session.get("game_state"))
    except: eng = Engine(None)
    
    d = request.json or {}
    act = d.get("a")
    val = d.get("v")
    
    if act=="reset": eng = Engine(None)
    elif act=="move": eng.move(*val)
    elif act=="attack": eng.attack(*val)
    elif act=="infect": eng.infect(*val)
    
    session["game_state"] = eng.state
    return jsonify(eng.get_ui())

# ==========================================
# HTML UI משופר
# ==========================================
HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦠 PARASITE ARENA</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { 
        background: linear-gradient(135deg, #0a0015 0%, #1a0a2e 50%, #0f0520 100%); 
        color:#eee; 
        font-family:'Orbitron', monospace; 
        height:100vh; 
        display:flex; 
        flex-direction:column; 
        overflow:hidden;
    }
    
    @keyframes pulse { 0%, 100% { opacity:1; } 50% { opacity:0.5; } }
    @keyframes glow { 0%, 100% { box-shadow: 0 0 10px #0ff; } 50% { box-shadow: 0 0 25px #0ff, 0 0 50px #0ff; } }
    @keyframes fadeIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
    @keyframes rotate { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
    
    /* Header */
    .header { 
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); 
        padding:15px 20px; 
        display:flex; 
        justify-content:space-between; 
        align-items:center; 
        border-bottom:3px solid #0ff;
        box-shadow: 0 4px 20px rgba(0,255,255,0.3);
    }
    .player-stats {
        display:flex;
        gap:15px;
        align-items:center;
    }
    .stat-box { 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%); 
        padding:8px 15px; 
        border-radius:10px; 
        border:1px solid #0ff;
        font-size:13px;
        box-shadow: 0 0 10px rgba(0,255,255,0.2);
    }
    .stat-value { color:#0ff; font-weight:bold; margin-left:5px; }
    .icon-big { font-size:40px; filter:drop-shadow(0 0 10px #fff); }
    
    /* HP Bar */
    .hp-container {
        width:150px;
        height:10px;
        background:#222;
        border-radius:5px;
        overflow:hidden;
        border:1px solid #555;
    }
    .hp-bar {
        height:100%;
        background: linear-gradient(90deg, #f33 0%, #fa0 50%, #0f0 100%);
        transition: width 0.3s;
    }
    
    /* Main Content */
    .content { flex:1; display:flex; overflow:hidden; }
    
    /* Radar */
    .radar-section { 
        width:45%; 
        background: linear-gradient(135deg, #0a0a15 0%, #1a0a1f 100%); 
        display:flex; 
        flex-direction:column; 
        justify-content:center; 
        align-items:center; 
        padding:20px;
        border-right:2px solid #0ff;
    }
    .radar-title { 
        color:#0ff; 
        margin-bottom:15px; 
        font-size:16px; 
        font-weight:700;
        text-shadow: 0 0 10px #0ff;
        letter-spacing:3px;
    }
    .radar-grid { 
        display:grid; 
        gap:2px; 
        background:#000; 
        padding:5px;
        border:3px solid #0ff; 
        border-radius:10px;
        box-shadow: 0 0 30px rgba(0,255,255,0.5);
        animation: glow 3s infinite;
    }
    .cell { 
        width:32px; 
        height:32px; 
        display:flex; 
        align-items:center; 
        justify-content:center; 
        font-size:16px;
        border-radius:3px;
        transition: all 0.2s;
    }
    .fog { background:#0a0a0a; }
    .wall { background:#300; color:#f33; }
    .empty { background:#111; opacity:0.5; }
    .me { 
        background: radial-gradient(circle, #0ff 0%, #0aa 100%); 
        animation: pulse 2s infinite;
        box-shadow: 0 0 20px #0ff;
    }
    .rival { 
        background: radial-gradient(circle, #f33 0%, #a00 100%); 
        color:#fff;
        animation: pulse 1.5s infinite;
    }
    .alive { background:#1a1a1a; }
    .corpse { background:#0a0a0a; opacity:0.4; }
    
    /* Scene */
    .scene-section { 
        flex:1; 
        padding:20px; 
        overflow-y:auto;
        background: linear-gradient(135deg, #0f0520 0%, #1a0a2e 100%);
    }
    .scene-title {
        text-align:center;
        color:#0ff;
        margin-bottom:15px;
        font-size:14px;
        letter-spacing:2px;
    }
    .scene-grid {
        display:flex;
        flex-wrap:wrap;
        gap:15px;
        justify-content:center;
    }
    .entity-card {
        width:140px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border:2px solid #444;
        border-radius:12px;
        padding:12px;
        text-align:center;
        transition: all 0.3s;
        animation: fadeIn 0.4s;
        position:relative;
        overflow:hidden;
    }
    .entity-card::before {
        content:'';
        position:absolute;
        top:0; left:0; right:0;
        height:4px;
        background: linear-gradient(90deg, #0ff, #f0f);
        opacity:0;
        transition:0.3s;
    }
    .entity-card:hover::before { opacity:1; }
    .entity-card:hover {
        transform:translateY(-5px) scale(1.03);
        box-shadow: 0 10px 30px rgba(0,255,255,0.4);
        border-color:#0ff;
    }
    .corpse-card {
        opacity:0.6;
        filter:grayscale(50%);
        border-color:#666;
    }
    .tier-badge {
        position:absolute;
        top:8px;
        right:8px;
        background:#000;
        color:#0ff;
        border:1px solid #0ff;
        padding:3px 8px;
        border-radius:8px;
        font-size:10px;
        font-weight:700;
    }
    .entity-icon { font-size:45px; margin:10px 0; }
    .entity-name { font-size:13px; font-weight:700; margin:5px 0; }
    .entity-hp {
        font-size:12px;
        color:#0ff;
        margin:5px 0;
    }
    .hp-mini-bar {
        width:100%;
        height:6px;
        background:#222;
        border-radius:3px;
        overflow:hidden;
        margin:5px 0;
    }
    .hp-mini-fill {
        height:100%;
        background: linear-gradient(90deg, #f33, #0f0);
        transition: width 0.3s;
    }
    .action-btn {
        width:100%;
        padding:8px;
        border:none;
        border-radius:8px;
        font-family:inherit;
        font-weight:700;
        cursor:pointer;
        transition: all 0.2s;
        margin-top:8px;
        font-size:11px;
    }
    .btn-attack {
        background: linear-gradient(135deg, #f33 0%, #a00 100%);
        color:#fff;
    }
    .btn-attack:hover {
        background: linear-gradient(135deg, #f55 0%, #f00 100%);
        transform:scale(1.05);
    }
    .btn-infect {
        background: linear-gradient(135deg, #0f0 0%, #0a0 100%);
        color:#000;
    }
    .btn-infect:hover {
        background: linear-gradient(135deg, #3f3 0%, #0f0 100%);
        transform:scale(1.05);
    }
    
    /* Stats Panel */
    .stats-panel {
        position:fixed;
        top:80px;
        left:20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding:15px;
        border-radius:10px;
        border:2px solid #0ff;
        box-shadow: 0 0 20px rgba(0,255,255,0.3);
        z-index:10;
    }
    .stats-title {
        text-align:center;
        color:#0ff;
        margin-bottom:10px;
        font-size:14px;
        font-weight:700;
    }
    .stat-line {
        display:flex;
        justify-content:space-between;
        padding:5px 0;
        border-bottom:1px solid #333;
        font-size:12px;
    }
    .stat-line:last-child { border:none; }
    .stat-label { color:#aaa; }
    .stat-num { color:#0ff; font-weight:700; }
    
    /* Log */
    .log-section {
        height:100px;
        background: linear-gradient(135deg, #000 0%, #0a0a1a 100%);
        border-top:2px solid #0ff;
        padding:10px;
        overflow-y:auto;
        font-size:12px;
        box-shadow: 0 -4px 20px rgba(0,255,255,0.2);
    }
    .log-msg {
        padding:3px 0;
        animation: fadeIn 0.3s;
    }
    .sys { color:#aaa; }
    .info { color:#69f; }
    .success { color:#0f0; }
    .gold { color:#fa0; font-weight:700; }
    .danger { color:#f33; }
    .warning { color:#f90; }
    .critical { color:#f00; font-weight:700; text-shadow: 0 0 5px #f00; }
    
    /* Controls */
    .controls {
        height:130px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-top:2px solid #0ff;
        display:flex;
        align-items:center;
        justify-content:center;
        gap:30px;
        padding:0 20px;
    }
    .dpad {
        display:grid;
        grid-template-columns:repeat(3, 1fr);
        gap:8px;
        direction:ltr;
    }
    .move-btn {
        width:50px;
        height:50px;
        background: linear-gradient(135deg, #333 0%, #555 100%);
        border:2px solid #0ff;
        border-radius:10px;
        color:#0ff;
        font-size:24px;
        cursor:pointer;
        transition: all 0.2s;
        display:flex;
        align-items:center;
        justify-content:center;
        font-family:inherit;
    }
    .move-btn:hover {
        background: linear-gradient(135deg, #555 0%, #777 100%);
        box-shadow: 0 0 20px rgba(0,255,255,0.6);
        transform:scale(1.1);
    }
    .move-btn:active { transform:scale(0.95); }
    .u { grid-column:2; }
    .l { grid-row:2; }
    .d { grid-column:2; grid-row:2; }
    .r { grid-column:3; grid-row:2; }
    
    .reset-btn {
        padding:12px 24px;
        background: linear-gradient(135deg, #a00 0%, #600 100%);
        border:2px solid #f33;
        border-radius:10px;
        color:#fff;
        font-family:inherit;
        font-weight:700;
        cursor:pointer;
        transition: all 0.2s;
    }
    .reset-btn:hover {
        background: linear-gradient(135deg, #f33 0%, #a00 100%);
        box-shadow: 0 0 20px rgba(255,51,51,0.6);
    }
    
    /* Victory Screen */
    .victory-screen {
        position:fixed;
        inset:0;
        background:rgba(0,0,0,0.95);
        display:none;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        z-index:100;
    }
    .victory-title {
        font-size:80px;
        color:#fa0;
        text-shadow: 0 0 40px #fa0;
        animation: pulse 2s infinite;
        margin-bottom:20px;
    }
    .victory-btn {
        padding:20px 40px;
        font-size:24px;
        background: linear-gradient(135deg, #fa0 0%, #f60 100%);
        border:none;
        border-radius:15px;
        color:#000;
        font-family:inherit;
        font-weight:700;
        cursor:pointer;
        margin-top:30px;
        transition: all 0.3s;
    }
    .victory-btn:hover {
        transform:scale(1.1);
        box-shadow: 0 0 40px rgba(255,170,0,0.8);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width:8px; }
    ::-webkit-scrollbar-track { background:#111; }
    ::-webkit-scrollbar-thumb { background:#0ff; border-radius:4px; }
    ::-webkit-scrollbar-thumb:hover { background:#3ff; }
</style>
</head>
<body>

<div id="victory" class="victory-screen">
    <div class="victory-title">🏆 ניצחון! 🏆</div>
    <div style="color:#0ff; font-size:24px;">כל היריבים הושמדו</div>
    <button class="victory-btn" onclick="send('reset')">משחק חדש</button>
</div>

<div class="stats-panel">
    <div class="stats-title">📊 סטטיסטיקות</div>
    <div class="stat-line">
        <span class="stat-label">חיסולים</span>
        <span class="stat-num" id="stat-kills">0</span>
    </div>
    <div class="stat-line">
        <span class="stat-label">גופים</span>
        <span class="stat-num" id="stat-poss">0</span>
    </div>
    <div class="stat-line">
        <span class="stat-label">זמן</span>
        <span class="stat-num" id="stat-time">0s</span>
    </div>
    <div class="stat-line">
        <span class="stat-label">תורות</span>
        <span class="stat-num" id="stat-turns">0</span>
    </div>
    <div class="stat-line">
        <span class="stat-label">נחקר</span>
        <span class="stat-num" id="stat-explored">0</span>
    </div>
</div>

<div class="header">
    <div class="player-stats">
        <span class="icon-big" id="p-icon">🦠</span>
        <div>
            <div id="p-name" style="font-weight:700; font-size:18px; color:#0ff;">טוען...</div>
            <div class="hp-container">
                <div class="hp-bar" id="p-hp-bar"></div>
            </div>
            <div style="font-size:11px; margin-top:3px;">
                <span id="p-hp-text">0/0</span> HP
            </div>
        </div>
    </div>
    <div class="stat-box">
        🎯 יריבים: <span class="stat-value" id="rivals-count">8</span>
    </div>
</div>

<div class="content">
    <div class="radar-section">
        <div class="radar-title">⚡ מכ״ם ⚡</div>
        <div class="radar-grid" id="map"></div>
    </div>
    <div class="scene-section">
        <div class="scene-title">🔍 ניתוח זירה</div>
        <div class="scene-grid" id="scene"></div>
    </div>
</div>

<div class="log-section" id="log"></div>

<div class="controls">
    <button class="reset-btn" onclick="send('reset')">🔄 RESET</button>
    <div class="dpad">
        <button class="move-btn u" onclick="send('move',[0,1])">⬆</button>
        <button class="move-btn l" onclick="send('move',[1,0])">⬅</button>
        <button class="move-btn d" onclick="send('move',[0,-1])">⬇</button>
        <button class="move-btn r" onclick="send('move',[-1,0])">➡</button>
    </div>
    <div style="font-size:11px; color:#666;">חיצים / WASD</div>
</div>

<script>
const API = "{{ api }}";
window.onload = () => send('init');

async function send(act, val=null) {
    try {
        let res = await fetch(API, {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({a:act, v:val})
        });
        let d = await res.json();
        
        // Victory
        document.getElementById("victory").style.display = d.player.won ? "flex" : "none";
        
        // Player
        let p = d.player;
        document.getElementById("p-icon").innerText = p.icon;
        document.getElementById("p-name").innerText = p.dead ? "💀 GHOST MODE" : p.name;
       document.getElementById("p-hp-text").innerText = p.hp + "/" + p.max;
        document.getElementById("rivals-count").innerText = p.bots_left;
        
        let hpPct = (p.hp / p.max) * 100;
        document.getElementById("p-hp-bar").style.width = hpPct + "%";
        
        if(p.dead) document.body.style.filter = "hue-rotate(180deg)";
        else document.body.style.filter = "none";
        
        // Stats
        document.getElementById("stat-kills").innerText = d.stats.kills;
        document.getElementById("stat-poss").innerText = d.stats.possessions;
        document.getElementById("stat-time").innerText = d.stats.time + "s";
        document.getElementById("stat-turns").innerText = d.stats.turns;
        document.getElementById("stat-explored").innerText = d.stats.explored;
        
        // Map
        let mh = "";
        d.map.forEach(row => {
            row.forEach(c => mh += `<div class="cell ${c.cls}">${c.txt}</div>`);
        });
        let mapEl = document.getElementById("map");
        mapEl.innerHTML = mh;
        mapEl.style.gridTemplateRows = `repeat(${d.map.length}, 1fr)`;
        mapEl.style.gridTemplateColumns = `repeat(${d.map[0].length}, 1fr)`;
        
        // Scene
        let sh = "";
        if(d.scene.length === 0) {
            sh = "<div style='color:#555; padding:50px;'>אזור נקי</div>";
        } else {
            d.scene.forEach(obj => {
                let btn = "";
                let cardClass = obj.is_corpse ? "corpse-card" : "";
                
                if (p.dead) {
                    btn = `<button class="action-btn btn-infect" onclick="send('infect',['${obj.type}',${obj.idx}])">🧬 INFECT</button>`;
                } else if (!obj.is_corpse) {
                    btn = `<button class="action-btn btn-attack" onclick="send('attack',['${obj.type}',${obj.idx}])">⚔️ ATTACK</button>`;
                } else {
                    btn = "<div style='font-size:10px; color:#555; margin-top:8px;'>(גופה)</div>";
                }
                
                let hpPercent = (obj.hp / obj.max_hp) * 100;
                let tierText = "T" + obj.tier;
                
                sh += `<div class="entity-card ${cardClass}">
                    <div class="tier-badge" style="border-color:${obj.color}; color:${obj.color}">${tierText}</div>
                    <div class="entity-icon">${obj.icon}</div>
                    <div class="entity-name">${obj.name}</div>
                    ${obj.host_name ? `<div style="font-size:10px; color:#888;">${obj.host_name}</div>` : ''}
                    <div class="entity-hp">${obj.hp}/${obj.max_hp} HP</div>
                    <div class="hp-mini-bar">
                        <div class="hp-mini-fill" style="width:${hpPercent}%"></div>
                    </div>
                    ${btn}
                </div>`;
            });
        }
        document.getElementById("scene").innerHTML = sh;
        
        // Log
        let lh = "";
        d.log.slice().reverse().forEach(l => {
            lh += `<div class="log-msg ${l.type}">› ${l.text}</div>`;
        });
        document.getElementById("log").innerHTML = lh;
        
    } catch(e) {
        console.error(e);
    }
}

// Keyboard
window.addEventListener("keydown", e => {
    if(e.key == "ArrowUp" || e.key == "w" || e.key == "W") send('move',[0,1]);
    if(e.key == "ArrowDown" || e.key == "s" || e.key == "S") send('move',[0,-1]);
    if(e.key == "ArrowLeft" || e.key == "a" || e.key == "A") send('move',[1,0]);
    if(e.key == "ArrowRight" || e.key == "d" || e.key == "D") send('move',[-1,0]);
    if(e.key == "r" || e.key == "R") send('reset');
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("🦠 Parasite Arena Enhanced - http://localhost:5006")
    app.run(port=5006)
