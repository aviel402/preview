import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key = 'pokemon_master_secret_key_v2'

# ==========================================
# 📘 FULL 18-TYPE MATCHUP CHART
# ==========================================
TYPE_CHART = {
    "Normal":   {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire":     {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water":    {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Grass":    {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Electric": {"Water": 2.0, "Grass": 0.5, "Electric": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Ice":      {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5},
    "Poison":   {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
    "Ground":   {"Fire": 2.0, "Grass": 0.5, "Electric": 2.0, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying":   {"Grass": 2.0, "Electric": 0.5, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic":  {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Steel": 0.5, "Dark": 0.0},
    "Bug":      {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
    "Rock":     {"Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost":    {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Dragon":   {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Steel":    {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
    "Dark":     {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5},
    "Fairy":    {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5}
}

# ==========================================
# 🎒 ITEMS DB
# ==========================================
ITEMS_DB = {
    "Poke Ball":   {"type": "ball", "bonus": 1.0, "cost": 15},
    "Great Ball":  {"type": "ball", "bonus": 1.5, "cost": 35},
    "Ultra Ball":  {"type": "ball", "bonus": 2.0, "cost": 70},
    "Potion":      {"type": "heal", "val": 30,   "cost": 20},
    "Super Potion":{"type": "heal", "val": 70,   "cost": 50}
}

# ==========================================
# 🐾 POKEMON SPECIES
# ==========================================
POKEMON_SPECIES = [
    {"name": "Pidgey",     "type": "Normal",   "hp": 35, "max": 35, "atk": 8,  "catch_rate": 0.6,  "icon": "🐦"},
    {"name": "Caterpie",   "type": "Bug",      "hp": 30, "max": 30, "atk": 6,  "catch_rate": 0.7,  "icon": "🐛"},
    {"name": "Pikachu",    "type": "Electric", "hp": 45, "max": 45, "atk": 14, "catch_rate": 0.4,  "icon": "⚡"},
    {"name": "Charmander", "type": "Fire",     "hp": 50, "max": 50, "atk": 15, "catch_rate": 0.35, "icon": "🔥"},
    {"name": "Bulbasaur",  "type": "Grass",    "hp": 55, "max": 55, "atk": 12, "catch_rate": 0.35, "icon": "🍃"},
    {"name": "Squirtle",   "type": "Water",    "hp": 52, "max": 52, "atk": 13, "catch_rate": 0.35, "icon": "💧"},
    {"name": "Geodude",    "type": "Rock",     "hp": 40, "max": 40, "atk": 10, "catch_rate": 0.5,  "icon": "🪨"},
    {"name": "Gastly",     "type": "Ghost",    "hp": 30, "max": 30, "atk": 16, "catch_rate": 0.4,  "icon": "👻"},
    {"name": "Mewtwo",     "type": "Psychic",  "hp": 150,"max": 150,"atk": 28, "catch_rate": 0.05, "icon": "🔮"}
]

ROUTES = [
    {"name": "Route 1 - Tall Grass", "icon": "🌿"},
    {"name": "Route 2 - Viridian Forest", "icon": "🌲"},
    {"name": "Route 3 - Rock Cave", "icon": "⛰️"},
    {"name": "Cerulean Lake", "icon": "🌊"}
]

# ==========================================
# ⚙️ GAME ENGINE
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state:
            starter = {"name": "Pikachu", "type": "Electric", "hp": 45, "max": 45, "atk": 14, "icon": "⚡"}
            self.state = {
                "x": 0, "y": 0,
                "gold": 50,
                "team": [starter],
                "active_idx": 0,
                "inv": ["Poke Ball", "Poke Ball", "Potion"],
                "map": {},
                "visited": ["0,0"],
                "log": [{"text": "Welcome to Pokemon World! You set off with Pikachu.", "type": "sys"}]
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
            r_data["name"] = "Main Pokemon Center"
            r_data["icon"] = "🏥"
            r_data["is_center"] = True
            self.state["map"][k] = r_data
            return

        rnd = random.random()
        if rnd < 0.15:
            r_data["name"] = "PokéMart"
            r_data["icon"] = "🏪"
            r_data["is_shop"] = True
        elif rnd < 0.25:
            r_data["name"] = "Pokemon Center"
            r_data["icon"] = "🏥"
            r_data["is_center"] = True
        else:
            route = random.choice(ROUTES)
            r_data["name"] = route["name"]
            r_data["icon"] = route["icon"]
            
            if random.random() < 0.60:
                spec = random.choice(POKEMON_SPECIES).copy()
                r_data["enemy"] = spec

            if random.random() < 0.20:
                r_data["items"].append(random.choice(["Poke Ball", "Potion"]))

        self.state["map"][k] = r_data

    def move(self, dx, dy):
        r_now = self.state["map"][self.pos()]
        if r_now.get("enemy"):
            self.log("A wild Pokemon blocks your way! Attack, catch, or run.", "danger")
            return

        self.state["x"] += dx
        self.state["y"] += dy
        k = self.pos()
        
        self.create_room(self.state["x"], self.state["y"])
        if k not in self.state["visited"]: self.state["visited"].append(k)
        
        r = self.state["map"][k]
        self.log(f"Arrived at {r['name']}.", "sys")
        if r.get("is_center"): self.log("🏥 Pokemon Center! Click heal to restore your team.", "success")
        if r.get("is_shop"): self.log("🏪 PokéMart is open for items!", "gold")
        if r.get("enemy"): self.log(f"⚠️ Wild Pokemon appeared: {r['enemy']['name']} ({r['enemy']['type']})!", "danger")
        if r["items"]: self.log(f"🔎 Found on the ground: {', '.join(r['items'])}", "success")

    def attack(self):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        player_mon = self.active_mon()

        if not enemy: return self.log("No enemy Pokemon to attack.", "info")
        if not player_mon or player_mon["hp"] <= 0:
            return self.log("Your active Pokemon is fainted! Switch Pokemon.", "danger")

        p_type = player_mon.get("type", "Normal")
        e_type = enemy.get("type", "Normal")
        
        # Type matchup multiplier
        mult = TYPE_CHART.get(p_type, {}).get(e_type, 1.0)

        base_dmg = player_mon["atk"]
        player_dmg = int(random.randint(base_dmg - 2, base_dmg + 4) * mult)
        
        enemy["hp"] -= player_dmg
        
        eff_msg = ""
        if mult > 1.0: eff_msg = " (It's super effective! ⚡)"
        elif mult == 0.0: eff_msg = " (It had no effect...)"
        elif mult < 1.0: eff_msg = " (It's not very effective...)"

        self.log(f"⚔️ {player_mon['name']} attacked {enemy['name']} for {player_dmg} damage!{eff_msg}", "sys")

        if enemy["hp"] <= 0:
            gold_drop = random.randint(15, 35)
            self.state["gold"] += gold_drop
            self.log(f"💀 Wild {enemy['name']} fainted! Earned {gold_drop} gold.", "gold")
            r["enemy"] = None
        else:
            e_mult = TYPE_CHART.get(e_type, {}).get(p_type, 1.0)
            e_dmg = int(max(1, enemy["atk"] - random.randint(0, 3)) * e_mult)
            player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
            self.log(f"💥 {enemy['name']} counter-attacked for {e_dmg} damage!", "danger")
            if player_mon["hp"] <= 0:
                self.log(f"😵 {player_mon['name']} fainted!", "danger")

    def catch(self, ball_name):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        if not enemy: return self.log("No wild Pokemon to catch!", "info")

        if ball_name not in self.state["inv"]:
            return self.log(f"You don't have a {ball_name}!", "danger")

        self.state["inv"].remove(ball_name)
        ball_data = ITEMS_DB.get(ball_name, {"bonus": 1.0})

        hp_factor = 1.0 - (enemy["hp"] / enemy["max"])
        base_rate = enemy.get("catch_rate", 0.4)
        chance = (base_rate + (hp_factor * 0.45)) * ball_data["bonus"]

        if random.random() < chance:
            self.log(f"🎉 Caught {enemy['name']}!", "gold")
            if len(self.state["team"]) < 6:
                self.state["team"].append(enemy.copy())
                self.log(f"{enemy['name']} joined your team!", "success")
            else:
                self.log(f"Team full (6/6). {enemy['name']} was sent to PC.", "sys")
            r["enemy"] = None
        else:
            self.log(f"🔴 {enemy['name']} broke free from {ball_name}!", "danger")
            player_mon = self.active_mon()
            if player_mon and player_mon["hp"] > 0:
                e_dmg = max(1, enemy["atk"] - random.randint(0, 2))
                player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
                self.log(f"💥 {enemy['name']} attacked back for {e_dmg} damage!", "danger")

    def heal_team(self):
        r = self.state["map"][self.pos()]
        if not r.get("is_center"):
            return self.log("You must be at a Pokemon Center to heal!", "info")
        
        for mon in self.state["team"]:
            mon["hp"] = mon["max"]
        self.log("💖 Your entire team is restored to full health!", "success")

    def take(self):
        r = self.state["map"][self.pos()]
        if not r["items"]: return self.log("Nothing to pick up here.", "info")
        for item in r["items"]: self.state["inv"].append(item)
        self.log(f"Picked up: {', '.join(r['items'])}", "success")
        r["items"] = []

    def use_item(self, item_name):
        if item_name not in self.state["inv"]: return
        eff = ITEMS_DB.get(item_name)
        if not eff: return

        if eff["type"] == "heal":
            mon = self.active_mon()
            if not mon: return
            if mon["hp"] >= mon["max"]: return self.log(f"{mon['name']} is already full HP.", "info")
            mon["hp"] = min(mon["max"], mon["hp"] + eff["val"])
            self.log(f"Used {item_name} on {mon['name']} → +{eff['val']} HP", "success")
            self.state["inv"].remove(item_name)
        elif eff["type"] == "ball":
            self.catch(item_name)

    def buy(self, item_name):
        r = self.state["map"][self.pos()]
        if not r.get("is_shop"): return

        cost = ITEMS_DB.get(item_name, {}).get("cost", 999)
        if self.state["gold"] < cost:
            return self.log(f"Not enough gold! Need {cost}.", "danger")

        self.state["gold"] -= cost
        self.state["inv"].append(item_name)
        self.log(f"Bought {item_name} for {cost} gold!", "success")

    def switch_mon(self, idx):
        if 0 <= idx < len(self.state["team"]):
            self.state["active_idx"] = idx
            self.log(f"Sent out {self.state['team'][idx]['name']}!", "sys")

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
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pokemon Game Engine</title>
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
    .msg { padding: 6px; border-radius: 4px; font-size: 13px; border-left: 3px solid transparent; background:rgba(255,255,255,0.02);}
    .sys { color: #7aa2f7; border-left-color:#3d59a1;}
    .danger { color: #f7768e; border-left-color:#db4b4b; background: rgba(255,0,0,0.1); }
    .success { color: #9ece6a; border-left-color:#73daca; background: rgba(0,255,0,0.05);}
    .gold { color: #e0af68; border-left-color:#ff9e3b; font-weight:bold;}

    .team-bar { display:flex; gap:6px; background:var(--panel); padding:6px; border-radius:6px; overflow-x:auto;}
    .mon-slot { background:#121820; border:1px solid var(--border); padding:6px; border-radius:4px; font-size:12px; cursor:pointer; min-width:70px; text-align:center;}
    .mon-slot.active { border-color:var(--acc); background:#28344d;}

    .controls { height: 150px; background: #151b26; border-top: 3px solid var(--border); padding: 10px; display: grid; grid-template-columns: 1fr 140px; gap: 15px; align-items: center;}
    .d-pad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; width: 140px; height:100%;}
    .btn-arr { background: #222d42; color: #fff; border:none; border-radius: 6px; font-size: 18px; cursor: pointer;}
    .btn-arr:active { background: #32415e; }
    .up { grid-column: 2; grid-row: 1; }
    .down { grid-column: 2; grid-row: 3; }
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
            
            <div id="enemy-box" class="dynamic-interaction">
                <div style="display:flex; justify-content:space-between;">
                    <strong id="en-name" style="color:#ff8181;"></strong>
                    <span><span id="en-hp"></span>/<span id="en-max"></span> HP</span>
                </div>
                <div class="hp-track"><div id="en-fill" class="hp-fill" style="width:100%"></div></div>
            </div>

            <div id="shop-box" class="shop-box">
                <div style="color:#ffcc00; font-size:14px; margin-bottom:6px;">🏪 PokéMart</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                    <button class="btn-action" onclick="send('buy','Poke Ball')">Poke Ball (15💰)</button>
                    <button class="btn-action" onclick="send('buy','Great Ball')">Great Ball (35💰)</button>
                    <button class="btn-action" onclick="send('buy','Ultra Ball')">Ultra Ball (70💰)</button>
                    <button class="btn-action" onclick="send('buy','Potion')">Potion (20💰)</button>
                </div>
            </div>

            <div id="center-box" class="center-box">
                <div style="color:#00ffcc; font-size:14px; margin-bottom:6px;">🏥 Pokemon Center</div>
                <button class="btn-action" style="background:#00a86b;" onclick="send('heal')">💖 Heal Entire Team</button>
            </div>
        </div>

        <div class="team-bar" id="team-bar"></div>
    </div>

    <div class="log-container" id="log-box"></div>
</div>

<div class="modal" id="inv-modal" onclick="if(event.target==this) toggleModal('inv-modal')">
    <div class="modal-box">
        <h3 style="margin-top:0; color:var(--acc);">🎒 My Bag</h3>
        <div id="inv-list" style="display:grid; gap:6px;"></div>
    </div>
</div>

<div class="controls">
    <div class="main-actions">
        <button class="act-btn btn-atk" onclick="send('attack')">⚔️ Attack</button>
        <button class="act-btn btn-catch" onclick="send('catch', 'Poke Ball')">🔴 Throw Ball</button>
        <button class="act-btn btn-inv" onclick="toggleModal('inv-modal')">🎒 Bag</button>
    </div>

    <div class="d-pad">
        <button class="btn-arr up" onclick="send('move', [0,1])">▲</button>
        <button class="btn-arr left" onclick="send('move', [-1,0])">◄</button>
        <button class="btn-arr down" onclick="send('move', [0,-1])">▼</button>
        <button class="btn-arr right" onclick="send('move', [1,0])">►</button>
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

        let logBox = document.getElementById("log-box");
        logBox.innerHTML = "";
        d.log.slice().reverse().forEach(msg => {
            logBox.innerHTML += `<div class="msg ${msg.type}">${msg.text}</div>`;
        });

        let mapH = "";
        d.map_grid.forEach(row => {
            row.forEach(c => mapH += `<div class='map-cell ${c.cls}'>${c.val}</div>`);
        });
        document.getElementById("map-target").innerHTML = mapH;

        document.getElementById("gold").innerText = d.gold;
        document.getElementById("loc-name").innerText = d.room_name;

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

        document.getElementById("enemy-box").style.display = d.enemy ? "flex" : "none";
        if (d.enemy) {
            document.getElementById("en-name").innerText = `${d.enemy.icon || ''} ${d.enemy.name} (${d.enemy.type})`;
            document.getElementById("en-hp").innerText = d.enemy.hp;
            document.getElementById("en-max").innerText = d.enemy.max;
            document.getElementById("en-fill").style.width = (d.enemy.hp / d.enemy.max * 100) + "%";
        }

        document.getElementById("shop-box").style.display = d.is_shop ? "block" : "none";
        document.getElementById("center-box").style.display = d.is_center ? "block" : "none";

        let invL = document.getElementById("inv-list");
        invL.innerHTML = "";
        if (d.inv.length === 0) {
            invL.innerHTML = "<div style='text-align:center;'>Bag is empty...</div>";
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
