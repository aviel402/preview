import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key = 'pokemon_master_ultimate_v3'

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
    "Poke Ball": {"type": "ball", "bonus": 1.0, "cost": 15},
    "Great Ball": {"type": "ball", "bonus": 1.5, "cost": 35},
    "Ultra Ball": {"type": "ball", "bonus": 2.0, "cost": 70},
    "Master Ball": {"type": "ball", "bonus": 255.0, "cost": 5000},
    "Potion": {"type": "heal", "val": 30, "cost": 20},
    "Super Potion": {"type": "heal", "val": 70, "cost": 50},
    "Hyper Potion": {"type": "heal", "val": 120, "cost": 100},
    "Max Potion": {"type": "heal", "val": 9999, "cost": 150},
    "Full Restore": {"type": "full_restore", "val": 9999, "cost": 300},
    "Revive": {"type": "revive", "percent": 0.5, "cost": 200},
    "Max Revive": {"type": "revive", "percent": 1.0, "cost": 400},
    "Rare Candy": {"type": "level_up", "val": 1, "cost": 4800},
    "Fire Stone": {"type": "evo_stone", "evolution": "fire", "cost": 2100},
    "Water Stone": {"type": "evo_stone", "evolution": "water", "cost": 2100},
    "Thunder Stone": {"type": "evo_stone", "evolution": "thunder", "cost": 2100},
    "Leaf Stone": {"type": "evo_stone", "evolution": "leaf", "cost": 2100},
    "Moon Stone": {"type": "evo_stone", "evolution": "moon", "cost": 2100},
    "Nugget": {"type": "sell", "val": 5000, "cost": 1000},
    "Stardust": {"type": "sell", "val": 2000, "cost": 1000}
}

# ==========================================
# 📍 HOENN ROUTES & LOCATIONS
# ==========================================
ROUTES = [
    {"name": "Littleroot Town", "icon": "🏡", "safe": True},
    {"name": "Oldale Town", "icon": "🏘️", "safe": True},
    {"name": "Petalburg City", "icon": "🏙️", "safe": True},
    {"name": "Rustboro City", "icon": "🏙️", "safe": True},
    {"name": "Route 101", "icon": "🌿", "safe": False},
    {"name": "Route 102", "icon": "🌿", "safe": False},
    {"name": "Route 103", "icon": "🌿", "safe": False},
    {"name": "Route 104", "icon": "🌿", "safe": False},
    {"name": "Petalburg Woods", "icon": "🌲", "safe": False},
    {"name": "Rusturf Tunnel", "icon": "⛰️", "safe": False},
    {"name": "Granite Cave", "icon": "🪨", "safe": False},
    {"name": "Route 110", "icon": "🌿", "safe": False},
    {"name": "Mauville City", "icon": "🏙️", "safe": True},
    {"name": "Victory Road", "icon": "🏔️", "safe": False}
]

# ==========================================
# 🐾 POKEMON SPECIES & EVOLUTIONS
# ==========================================
POKEMON_SPECIES = [
    # Starters (Mudkip Line)
    {"name": "Mudkip", "type": "Water", "hp": 50, "atk": 70, "catch_rate": 0.45, "icon": "💧", "evolves_at": 16, "evolves_to": "Marshtomp", "moves": [{"name": "Water Gun", "type": "Water", "pow": 40}, {"name": "Tackle", "type": "Normal", "pow": 35}, {"name": "Mud Slap", "type": "Ground", "pow": 30}]},
    {"name": "Marshtomp", "type": "Water/Ground", "hp": 70, "atk": 85, "catch_rate": 0.30, "icon": "💧", "evolves_at": 36, "evolves_to": "Swampert", "moves": [{"name": "Water Pulse", "type": "Water", "pow": 60}, {"name": "Mud Shot", "type": "Ground", "pow": 55}, {"name": "Tackle", "type": "Normal", "pow": 35}]},
    {"name": "Swampert", "type": "Water/Ground", "hp": 100, "atk": 110, "catch_rate": 0.20, "icon": "💧", "evolves_at": 999, "evolves_to": None, "moves": [{"name": "Surf", "type": "Water", "pow": 90}, {"name": "Earthquake", "type": "Ground", "pow": 100}, {"name": "Tackle", "type": "Normal", "pow": 35}]},

    # Other common encounters
    {"name": "Pidgey", "type": "Normal/Flying", "hp": 40, "atk": 45, "catch_rate": 0.60, "icon": "🐦", "evolves_at": 18, "evolves_to": "Pidgeotto", "moves": [{"name": "Gust", "type": "Flying", "pow": 40}, {"name": "Quick Attack", "type": "Normal", "pow": 40}]},
    {"name": "Pidgeotto", "type": "Normal/Flying", "hp": 63, "atk": 60, "catch_rate": 0.40, "icon": "🦅", "evolves_at": 36, "evolves_to": "Pidgeot", "moves": [{"name": "Wing Attack", "type": "Flying", "pow": 60}, {"name": "Quick Attack", "type": "Normal", "pow": 40}]},
    {"name": "Pidgeot", "type": "Normal/Flying", "hp": 83, "atk": 80, "catch_rate": 0.25, "icon": "🦅", "evolves_at": 999, "evolves_to": None, "moves": [{"name": "Air Slash", "type": "Flying", "pow": 75}, {"name": "Quick Attack", "type": "Normal", "pow": 40}]},

    {"name": "Pikachu", "type": "Electric", "hp": 35, "atk": 55, "catch_rate": 0.40, "icon": "⚡", "evolves_at": 999, "evolves_to": None, "moves": [{"name": "Thunder Shock", "type": "Electric", "pow": 40}, {"name": "Quick Attack", "type": "Normal", "pow": 40}]},
    {"name": "Zigzagoon", "type": "Normal", "hp": 38, "atk": 30, "catch_rate": 0.70, "icon": "🦝", "evolves_at": 20, "evolves_to": "Linoone", "moves": [{"name": "Tackle", "type": "Normal", "pow": 35}, {"name": "Headbutt", "type": "Normal", "pow": 70}]},
    {"name": "Linoone", "type": "Normal", "hp": 78, "atk": 70, "catch_rate": 0.35, "icon": "🦝", "evolves_at": 999, "evolves_to": None, "moves": [{"name": "Slash", "type": "Normal", "pow": 70}, {"name": "Headbutt", "type": "Normal", "pow": 70}]}
]

# Helper to find species template
def get_species_data(name):
    for spec in POKEMON_SPECIES:
        if spec["name"] == name:
            return spec
    # Fallback default
    return POKEMON_SPECIES[0]

# ==========================================
# ⚙️ GAME ENGINE
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state:
            # Starter starter: Mudkip Level 5
            starter_spec = get_species_data("Mudkip")
            starter = {
                "name": starter_spec["name"],
                "type": starter_spec["type"],
                "level": 5,
                "xp": 0,
                "xp_to_next": 50,
                "hp": starter_spec["hp"],
                "max_hp": starter_spec["hp"],
                "atk": starter_spec["atk"],
                "icon": starter_spec["icon"],
                "moves": starter_spec["moves"],
                "evolves_at": starter_spec["evolves_at"],
                "evolves_to": starter_spec["evolves_to"]
            }
            self.state = {
                "x": 0, "y": 0,
                "gold": 100,
                "team": [starter],
                "active_idx": 0,
                "inv": ["Poke Ball", "Poke Ball", "Poke Ball", "Potion"],
                "map": {},
                "visited": ["0,0"],
                "last_center": {"x": 0, "y": 0, "name": "Littleroot Town"},
                "log": [{"text": "Welcome to the Hoenn Region! Your journey begins with Mudkip.", "type": "sys"}]
            }
            self.create_room(0, 0)
        else:
            self.state = state

    def pos(self): return f"{self.state['x']},{self.state['y']}"
    
    def log(self, txt, t="game"): self.state["log"].append({"text": txt, "type": t})

    def active_mon(self):
        if 0 <= self.state["active_idx"] < len(self.state["team"]):
            return self.state["team"][self.state["active_idx"]]
        return None

    def create_room(self, x, y):
        k = f"{x},{y}"
        if k in self.state["map"]: return

        # Pick a route/town from ROUTES based on coordinates or random
        route = random.choice(ROUTES)
        r_data = {
            "name": route["name"], 
            "icon": route["icon"], 
            "enemy": None, 
            "items": [], 
            "is_shop": route["safe"], 
            "is_center": route["safe"]
        }

        # If it's a safe town, update last_center checkpoint
        if route["safe"] and ("Town" in route["name"] or "City" in route["name"]):
            self.state["last_center"] = {"x": x, "y": y, "name": route["name"]}

        # If wild grass / dangerous route, chance for a wild Pokémon encounter
        if not r_data["is_shop"] and random.random() < 0.70:
            spec = random.choice(POKEMON_SPECIES)
            # scale level based on distance from start
            lvl = max(3, min(50, 4 + abs(x) + abs(y)))
            r_data["enemy"] = {
                "name": spec["name"],
                "type": spec["type"],
                "level": lvl,
                "hp": spec["hp"] + (lvl * 3),
                "max": spec["hp"] + (lvl * 3),
                "atk": spec["atk"] + lvl,
                "catch_rate": spec["catch_rate"],
                "icon": spec["icon"]
            }

        if random.random() < 0.25:
            r_data["items"].append(random.choice(["Poke Ball", "Potion"]))

        self.state["map"][k] = r_data

    def move(self, dx, dy):
        r_now = self.state["map"][self.pos()]
        if r_now.get("enemy"):
            self.log("A wild Pokémon blocks your path! You must fight or catch it before moving.", "danger")
            return

        self.state["x"] += dx
        self.state["y"] += dy
        k = self.pos()
        
        self.create_room(self.state["x"], self.state["y"])
        if k not in self.state["visited"]: self.state["visited"].append(k)
        
        r = self.state["map"][k]
        self.log(f"Arrived at {r['name']}.", "sys")
        if r.get("is_center"): self.log(f"🏥 {r['name']} Pokemon Center & Shop checkpoint!", "success")
        if r.get("enemy"): self.log(f"⚠️ Wild {r['enemy']['name']} (Lvl {r['enemy']['level']}, {r['enemy']['type']}) appeared!", "danger")
        if r["items"]: self.log(f"🔎 Found items on the ground: {', '.join(r['items'])}", "success")

    def check_evolution(self, mon):
        if mon["level"] >= mon.get("evolves_at", 999) and mon.get("evolves_to"):
            new_spec = get_species_data(mon["evolves_to"])
            old_name = mon["name"]
            mon["name"] = new_spec["name"]
            mon["type"] = new_spec["type"]
            mon["icon"] = new_spec["icon"]
            mon["moves"] = new_spec["moves"]
            mon["evolves_at"] = new_spec["evolves_at"]
            mon["evolves_to"] = new_spec["evolves_to"]
            # Boost stats on evolution
            mon["max_hp"] += 20
            mon["hp"] = mon["max_hp"]
            mon["atk"] += 15
            self.log(f"✨ What?! {old_name} evolved into {mon['name']}! 🎉", "gold")

    def add_xp(self, amount):
        mon = self.active_mon()
        if not mon: return
        mon["xp"] += amount
        self.log(f"{mon['name']} gained {amount} XP.", "sys")
        while mon["xp"] >= mon["xp_to_next"]:
            mon["xp"] -= mon["xp_to_next"]
            mon["level"] += 1
            mon["xp_to_next"] = int(mon["xp_to_next"] * 1.5)
            mon["max_hp"] += 8
            mon["hp"] = mon["max_hp"]
            mon["atk"] += 4
            self.log(f"📈 {mon['name']} grew to Level {mon['level']}! Stats increased!", "success")
            self.check_evolution(mon)

    def calculate_type_multiplier(self, atk_type, def_type_str):
        # Handle dual types separated by '/' e.g., "Water/Ground"
        def_types = def_type_str.split("/")
        total_mult = 1.0
        for dt in def_types:
            mult = TYPE_CHART.get(atk_type, {}).get(dt, 1.0)
            total_mult *= mult
        return total_mult

    def attack(self, move_idx=0):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        player_mon = self.active_mon()

        if not enemy: return self.log("No enemy Pokémon here.", "info")
        if not player_mon or player_mon["hp"] <= 0:
            return self.log("Your active Pokémon is fainted! Switch or heal.", "danger")

        moves = player_mon.get("moves", [{"name": "Tackle", "type": "Normal", "pow": 35}])
        move = moves[move_idx % len(moves)]

        p_type = move["type"]
        e_type_str = enemy["type"]
        
        mult = self.calculate_type_multiplier(p_type, e_type_str)

        base_dmg = player_mon["atk"] + move["pow"] // 2
        player_dmg = int(random.randint(base_dmg - 5, base_dmg + 5) * mult)
        player_dmg = max(1, player_dmg)
        
        enemy["hp"] -= player_dmg
        
        eff_msg = ""
        if mult > 1.0: eff_msg = " (It's super effective! ⚡)"
        elif mult == 0.0: eff_msg = " (It had no effect...)"
        elif mult < 1.0: eff_msg = " (It's not very effective...)"

        self.log(f"⚔️ {player_mon['name']} used {move['name']}! Dealt {player_dmg} damage.{eff_msg}", "sys")

        if enemy["hp"] <= 0:
            gold_drop = enemy["level"] * 10
            xp_drop = enemy["level"] * 15
            self.state["gold"] += gold_drop
            self.log(f"💀 Wild {enemy['name']} fainted! Earned {gold_drop} gold and {xp_drop} XP.", "gold")
            r["enemy"] = None
            self.add_xp(xp_drop)
        else:
            e_dmg = max(1, enemy["atk"] - random.randint(0, 4))
            player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
            self.log(f"💥 Wild {enemy['name']} counter-attacked for {e_dmg} damage!", "danger")
            if player_mon["hp"] <= 0:
                self.handle_player_defeat()

    def handle_player_defeat(self):
        mon = self.active_mon()
        self.log(f"😵 {mon['name']} fainted! All your Pokémon blacked out...", "danger")
        # Respawn at last visited Pokemon Center checkpoint
        center = self.state["last_center"]
        self.state["x"] = center["x"]
        self.state["y"] = center["y"]
        # Heal entire team fully on blackout
        for m in self.state["team"]:
            m["hp"] = m["max_hp"]
        self.log(f"🏥 Nurse Joy rushed you to {center['name']}. Your team is fully healed!", "success")

    def catch(self, ball_name):
        r = self.state["map"][self.pos()]
        enemy = r.get("enemy")
        if not enemy: return self.log("No wild Pokémon to catch here!", "info")

        if ball_name not in self.state["inv"]:
            return self.log(f"You don't have a {ball_name} in your bag!", "danger")

        self.state["inv"].remove(ball_name)
        ball_data = ITEMS_DB.get(ball_name, {"bonus": 1.0})

        hp_factor = 1.0 - (enemy["hp"] / enemy["max"])
        base_rate = enemy.get("catch_rate", 0.4)
        chance = (base_rate + (hp_factor * 0.5)) * ball_data["bonus"]

        if random.random() < chance or ball_name == "Master Ball":
            self.log(f"🎉 Gotcha! Caught {enemy['name']}!", "gold")
            new_mon = {
                "name": enemy["name"],
                "type": enemy["type"],
                "level": enemy["level"],
                "xp": 0,
                "xp_to_next": enemy["level"] * 30,
                "hp": enemy["max"],
                "max_hp": enemy["max"],
                "atk": enemy["atk"],
                "icon": enemy["icon"],
                "moves": get_species_data(enemy["name"]).get("moves", [{"name": "Tackle", "type": "Normal", "pow": 35}]),
                "evolves_at": get_species_data(enemy["name"]).get("evolves_at", 999),
                "evolves_to": get_species_data(enemy["name"]).get("evolves_to", None)
            }
            if len(self.state["team"]) < 6:
                self.state["team"].append(new_mon)
                self.log(f"{enemy['name']} was added to your active team!", "success")
            else:
                self.log(f"Team full (6/6). {enemy['name']} was sent to PC storage.", "sys")
            r["enemy"] = None
        else:
            self.log(f"🔴 Oh no! {enemy['name']} broke free from the {ball_name}!", "danger")
            player_mon = self.active_mon()
            if player_mon and player_mon["hp"] > 0:
                e_dmg = max(1, enemy["atk"] - random.randint(0, 3))
                player_mon["hp"] = max(0, player_mon["hp"] - e_dmg)
                self.log(f"💥 {enemy['name']} struck back for {e_dmg} damage!", "danger")
                if player_mon["hp"] <= 0:
                    self.handle_player_defeat()

    def heal_team(self):
        r = self.state["map"][self.pos()]
        if not r.get("is_center"):
            return self.log("You must be at a Pokémon Center town to heal your team!", "info")
        
        for mon in self.state["team"]:
            mon["hp"] = mon["max_hp"]
        self.log("💖 Nurse Joy healed your entire team to full health!", "success")

    def take(self):
        r = self.state["map"][self.pos()]
        if not r["items"]: return self.log("Nothing to pick up here.", "info")
        for item in r["items"]: self.state["inv"].append(item)
        self.log(f"Picked up: {', '.join(r['items'])}", "success")
        r["items"] = []

    def use_item(self, item_name):
        if item_name not in self.state["inv"]: return
        eff = ITEMS_DB.get(item_name, {})

        if eff.get("type") == "ball":
            self.catch(item_name)
        elif eff.get("type") == "heal" or eff.get("type") == "full_restore":
            mon = self.active_mon()
            if not mon: return
            if mon["hp"] >= mon["max_hp"]: return self.log(f"{mon['name']} is already at full HP.", "info")
            val = eff.get("val", 30)
            mon["hp"] = min(mon["max_hp"], mon["hp"] + val)
            self.log(f"Used {item_name} on {mon['name']} → Restored HP!", "success")
            self.state["inv"].remove(item_name)
        elif eff.get("type") == "level_up":
            mon = self.active_mon()
            if not mon: return
            self.state["inv"].remove(item_name)
            self.log(f"Used {item_name}!", "gold")
            self.add_xp(mon["xp_to_next"] - mon["xp"])
        else:
            self.log(f"Cannot use {item_name} right now.", "info")

    def buy(self, item_name):
        r = self.state["map"][self.pos()]
        if not r.get("is_shop"): return

        cost = ITEMS_DB.get(item_name, {}).get("cost", 999)
        if self.state["gold"] < cost:
            return self.log(f"Not enough gold! Need {cost} coins.", "danger")

        self.state["gold"] -= cost
        self.state["inv"].append(item_name)
        self.log(f"Bought {item_name} for {cost} gold!", "success")

    def switch_mon(self, idx):
        if 0 <= idx < len(self.state["team"]):
            self.state["active_idx"] = idx
            self.log(f"Go! {self.state['team'][idx]['name']}!", "sys")

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

        active_m = self.active_mon()
        return {
            "gold": self.state["gold"],
            "team": self.state["team"],
            "active_idx": self.state["active_idx"],
            "active_moves": active_m.get("moves", []) if active_m else [],
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
    elif act == "attack": eng.attack(val if val is not None else 0)
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
<title>Pokémon Hoenn Adventure Ultimate</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arimo:wght@400;700&display=swap');
    :root { --bg:#121820; --panel:#1e2638; --panel2: #2a354d; --acc:#ffcc00; --border:#3d4b68;}
    body { background: var(--bg); color: #dedde6; margin: 0; font-family: 'Arimo', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow:hidden;}
    header { background: #0b0f19; padding: 10px 16px; display: flex; justify-content: space-between; align-items:center; border-bottom: 3px solid var(--border);}
    .title {font-weight:900; color:var(--acc); letter-spacing:1px; margin:0; font-size:18px;}
    .stat-badge { background: #222d42; border:1px solid var(--border); padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: bold;}
    
    .viewport { flex: 1; display: grid; grid-template-columns: 2fr 1fr; gap: 8px; padding: 10px; overflow: hidden; background:radial-gradient(circle at center, #1a2333 0%, #0d121c 100%);}
    .side-panel { display: flex; flex-direction: column; gap: 8px; }
    
    .map-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; margin: 0 auto; width: 140px; }
    .map-cell { height: 42px; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; font-size: 20px; border-radius: 6px; border:1px solid rgba(255,255,255,0.05);}
    .map-cell.player { border: 2px solid #00ffcc; background: rgba(0,255,204, 0.2); }
    .map-cell.known { background: rgba(255,255,255, 0.08); }

    .room-card { background: var(--panel2); border-left: 5px solid var(--acc); border-radius: 6px; padding: 10px; text-align: center; display:flex; flex-direction:column; gap:6px;}
    .dynamic-interaction {display:none; background:#3b1818; padding:8px; border-radius:6px; border:2px dashed #a83232; flex-direction:column; gap:4px;}
    .hp-track { width: 100%; height: 10px; background: rgba(0,0,0,0.6); border-radius: 10px; overflow: hidden; }
    .hp-fill { height: 100%; background: linear-gradient(90deg, #42b883, #00ffcc); width: 100%; transition: 0.2s;}

    .shop-box, .center-box {display:none; background:#18281e; padding:8px; border-radius:6px; border:1px solid #32a869;}
    .btn-action { background:#2a5c3e; border:1px solid #42b883; border-radius:4px; padding:5px; margin:2px 0; width:100%; font-weight:bold; cursor:pointer; color:white; font-size:12px;}
    .btn-action:active {transform:scale(0.98);}

    .log-container { background: #0a0d14; border-radius: 6px; border: 1px solid var(--border); padding: 10px; overflow-y: auto; display:flex; flex-direction:column-reverse; gap:4px;}
    .msg { padding: 5px; border-radius: 4px; font-size: 12px; border-left: 3px solid transparent; background:rgba(255,255,255,0.02);}
    .sys { color: #7aa2f7; border-left-color:#3d59a1;}
    .danger { color: #f7768e; border-left-color:#db4b4b; background: rgba(255,0,0,0.1); }
    .success { color: #9ece6a; border-left-color:#73daca; background: rgba(0,255,0,0.05);}
    .gold { color: #e0af68; border-left-color:#ff9e3b; font-weight:bold;}

    .team-bar { display:flex; gap:6px; background:var(--panel); padding:6px; border-radius:6px; overflow-x:auto;}
    .mon-slot { background:#121820; border:1px solid var(--border); padding:5px; border-radius:4px; font-size:11px; cursor:pointer; min-width:70px; text-align:center;}
    .mon-slot.active { border-color:var(--acc); background:#28344d;}

    .controls { height: 155px; background: #151b26; border-top: 3px solid var(--border); padding: 10px; display: grid; grid-template-columns: 1.5fr 140px; gap: 10px; align-items: center;}
    .d-pad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; width: 140px; height:100%;}
    .btn-arr { background: #222d42; color: #fff; border:none; border-radius: 6px; font-size: 16px; cursor: pointer;}
    .btn-arr:active { background: #32415e; }
    .up { grid-column: 2; grid-row: 1; }
    .down { grid-column: 2; grid-row: 3; }
    .left { grid-column: 1; grid-row: 2; }
    .right { grid-column: 3; grid-row: 2; }

    .main-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; height: 100%; }
    .act-btn { font-weight: bold; font-size: 13px; border: none; border-radius: 6px; cursor: pointer; color:#fff; padding:6px;}
    .btn-atk { background: #a22929; grid-column: span 2; }
    .btn-inv { background: #3d59a1; grid-column: span 2; }
    .move-btn { background: #2d4a7a; font-size: 11px; }

    .modal { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); z-index:99; justify-content:center; align-items:center;}
    .modal-box { background:var(--panel2); width:85%; max-width:400px; padding:20px; border-radius:8px; border:1px solid var(--border); max-height:80vh; overflow-y:auto;}
</style>
</head>
<body>

<header>
    <div class="title">🔴 POKÉMON HOENN</div>
    <div style="display:flex; gap:8px;">
        <div class="stat-badge" style="color:gold;">💰 <span id="gold">100</span></div>
    </div>
</header>

<div class="viewport">
    <div class="side-panel">
        <div class="map-grid" id="map-target"></div>
        
        <div class="room-card">
            <div id="loc-name" style="font-weight:900; font-size:14px;">...</div>
            
            <div id="enemy-box" class="dynamic-interaction">
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <strong id="en-name" style="color:#ff8181;"></strong>
                    <span>HP: <span id="en-hp"></span>/<span id="en-max"></span></span>
                </div>
                <div class="hp-track"><div id="en-fill" class="hp-fill" style="width:100%"></div></div>
            </div>

            <div id="shop-box" class="shop-box">
                <div style="color:#ffcc00; font-size:13px; margin-bottom:4px;">🏪 PokéMart</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                    <button class="btn-action" onclick="send('buy','Poke Ball')">Poke Ball (15💰)</button>
                    <button class="btn-action" onclick="send('buy','Great Ball')">Great Ball (35💰)</button>
                    <button class="btn-action" onclick="send('buy','Ultra Ball')">Ultra Ball (70💰)</button>
                    <button class="btn-action" onclick="send('buy','Potion')">Potion (20💰)</button>
                </div>
            </div>

            <div id="center-box" class="center-box">
                <div style="color:#00ffcc; font-size:13px; margin-bottom:4px;">🏥 Pokémon Center</div>
                <button class="btn-action" style="background:#00a86b;" onclick="send('heal')">💖 Heal Team</button>
            </div>
        </div>

        <div class="team-bar" id="team-bar"></div>
    </div>

    <div class="log-container" id="log-box"></div>
</div>

<div class="modal" id="inv-modal" onclick="if(event.target==this) toggleModal('inv-modal')">
    <div class="modal-box">
        <h3 style="margin-top:0; color:var(--acc);">🎒 Bag Items</h3>
        <div id="inv-list" style="display:grid; gap:6px;"></div>
    </div>
</div>

<div class="controls">
    <div class="main-actions" id="action-panel">
        <!-- Dynamic moves & inventory buttons rendered via JS -->
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
                    <div>${m.icon} ${m.name}</div>
                    <div style="font-size:9px;">Lvl ${m.level}</div>
                    <div style="font-size:9px;">${m.hp}/${m.max_hp}</div>
                </div>`;
        });
        document.getElementById("team-bar").innerHTML = teamH;

        // Render Action buttons (Moves + Bag)
        let actHtml = "";
        if (d.active_moves && d.active_moves.length > 0) {
            d.active_moves.forEach((mv, mIdx) => {
                actHtml += `<button class="act-btn move-btn" onclick="send('attack', ${mIdx})">⚔️ ${mv.name}</button>`;
            });
        } else {
            actHtml += `<button class="act-btn btn-atk" onclick="send('attack', 0)">⚔️ Attack</button>`;
        }
        actHtml += `<button class="act-btn btn-inv" onclick="toggleModal('inv-modal')">🎒 Bag (${d.inv.length})</button>`;
        document.getElementById("action-panel").innerHTML = actHtml;

        document.getElementById("enemy-box").style.display = d.enemy ? "flex" : "none";
        if (d.enemy) {
            document.getElementById("en-name").innerText = `${d.enemy.icon} ${d.enemy.name} (Lvl ${d.enemy.level}) [${d.enemy.type}]`;
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
            // Group items or list them with click triggers
            d.inv.forEach(it => {
                invL.innerHTML += `<button class="btn-action" onclick="send('use','${it}'); toggleModal('inv-modal')">Use / Throw: ${it}</button>`;
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
