import random
import uuid
from flask import Flask, render_template_string, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key = 'dm_pro_fixe_shop_v8'

# ==========================================
# 📘 מאגר נתונים (DATABASE)
# ==========================================
ITEMS_DB = {
    "שיקוי חיים": {"type": "heal", "val": 40, "desc": "מרפא 40 חיים", "price": 20},
    "תחבושת": {"type": "heal", "val": 15, "desc": "עוצר דימום"},
    "מנת קרב": {"type": "heal", "val": 10, "desc": "אוכל"},
    "רימון רעל": {"type": "dmg_item", "val": 30, "desc": "נזק אויב"},
    "שיקוי כוח": {"type": "buff", "val": 5, "desc": "נזק זמני"},
    "שיקוי חיים גדול": {"type": "heal", "val": 80, "desc": "מרפא 80", "price": 40},
    "שיקוי חיים אגדי": {"type": "heal", "val": 150, "desc": "מרפא 150"},
    "רימון אש": {"type": "dmg_item", "val": 50, "desc": "פיצוץ אש ענק", "price": 60},
    "רימון קרח": {"type": "dmg_item", "val": 35, "desc": "מקפיא מפלצת"},
    
    # === חפצים למכירה למקח ===
    "יהלום": {"type": "sell", "val": 100, "desc": "ימכר בחנות"},
    "אודם": {"type": "sell", "val": 60, "desc": "ימכר בחנות"},
    "ספיר": {"type": "sell", "val": 80, "desc": "ימכר בחנות"},
    "אזמרגד": {"type": "sell", "val": 90, "desc": "ימכר בחנות"},
    
    # === מפתחות ===
    "מפתח ברזל": {"type": "key", "val": 0, "desc": "פותח תיבות נפוצות"},
    "מפתח זהב": {"type": "key", "val": 0, "desc": "פותח תיבות מלכות"},
    "מפתח עתיק": {"type": "key", "val": 0, "desc": "פותח שערים מיוחדים"}
}

ENEMIES = [
    {"name": "גובלין ירוק", "hp": 30, "max": 30, "atk": 5, "xp": 10, "loot": ["מנת קרב", "תחבושת"]},
    {"name": "עכביש רעיל", "hp": 35, "max": 35, "atk": 7, "xp": 15, "loot": ["רימון רעל"]},
    {"name": "אורק שומר", "hp": 60, "max": 60, "atk": 12, "xp": 40, "loot": ["שיקוי חיים", "מפתח ברזל"]},
    {"name": "שלד כסוף", "hp": 45, "max": 45, "atk": 10, "xp": 30, "loot": ["אודם"]},
    {"name": "אביר פאנטום", "hp": 100, "max": 100, "atk": 18, "xp": 100, "loot": ["שיקוי חיים גדול", "ספיר"]},
    {"name": "קוסם שחור", "hp": 70, "max": 70, "atk": 25, "xp": 90, "loot": ["רימון אש", "מפתח עתיק"]},
    {"name": "בוס דרקון זהב", "hp": 250, "max": 250, "atk": 25, "xp": 500, "loot": ["יהלום", "אזמרגד", "מפתח זהב", "שיקוי חיים אגדי"]},
    {"name": "שומר המקוללים", "hp": 130, "max": 130, "atk": 20, "xp": 150, "loot": ["אזמרגד"]}
]

BIOMES =[
    {"name": "צינוק טחוב", "icon": "⛓️"},
    {"name": "אולם אבן", "icon": "🏛️"},
    {"name": "מערה קפואה", "icon": "❄️"},
    {"name": "יער העד", "icon": "🌲"},
    {"name": "כלא אסורים", "icon": "🚪"},
    {"name": "מרתף מוצף", "icon": "💧"},
    {"name": "מגדל ארקיין", "icon": "🔮"},
    {"name": "ארמון רעפים", "icon": "🏰"},
    {"name": "ביצות ערפילים", "icon": "🌫️"},
    {"name": "מדבר חול", "icon": "🔥"},
    {"name": "הר געש פעיל", "icon": "🌋"},
    {"name": "שדה פרחים", "icon": "🌸"},
    {"name": "קרחת יער חשוכה", "icon": "🌑"},
    {"name": "חוף סלעי", "icon": "🏖️"},
    {"name": "מערת גבישים", "icon": "💎"},
    {"name": "ביצת קוצים", "icon": "🌿"},
    {"name": "טירת רוח קפואה", "icon": "🏯"},
    {"name": "גשר תלוי", "icon": "🌉"},
    {"name": "עמק האגדות", "icon": "📜"},
    {"name": "שדה קרב עתיק", "icon": "⚔️"},
    {"name": "מבוך עצים", "icon": "🌳"},
    {"name": "מגדל השעון", "icon": "⏰"},
    {"name": "מערבולת מים", "icon": "🌪️"},
    {"name": "חורבת האלים", "icon": "🏚️"},
    {"name": "פסגת השלג", "icon": "🏔️"}
]

MERCHANT_GREETINGS = [
    "סחורות טובות לאנשים שמחים! מה תיקח?",
    "זהירות, הבוסים בקומה הבאה משוגעים. תקנה שיקוי!",
    "אני קונה יהלומים, מוכר התקפות. דיל טוב.",
    "החיים קצרים. השקע בשדרוג הלהב שלך היום.",
    "רימוני קרח במלאי מוגבל – תזדרז!",
    "מפתח זהב? רק למי שממש רציני..."
]

# ==========================================
# ⚙️ מנוע המשחק
# ==========================================
class Engine:
    def __init__(self, state=None):
        if not state:
            self.state = {
                "x": 0, "y": 0,
                "stats": {"hp": 100, "max": 100, "gold": 20, "atk_base": 20, "atk_bonus": 0},
                "inv": ["שיקוי חיים", "תחבושת"],
                "map": {},
                "visited": ["0,0"],
                "log": [{"text": "דלת צינוק חורקת. אתה מתחיל מסע. אסוף כסף וחפש את הסוחר.", "type": "sys"}]
            }
            self.create_room(0, 0, safe=True)
        else:
            self.state = state

    def pos(self): return f"{self.state['x']},{self.state['y']}"
    
    def log(self, txt, t="game"): self.state["log"].append({"text": txt, "type": t})

    def create_room(self, x, y, safe=False):
        k = f"{x},{y}"
        if k in self.state["map"]: return

        r_data = {
            "name": "", "icon": "", "enemy": None, "items": [], 
            "is_shop": False, "chest": False
        }

        if safe:
            r_data["name"] = "מעגל ריפוי"
            r_data["icon"] = "🏠"
            self.state["map"][k] = r_data
            return

        rnd = random.random()
        if rnd < 0.12:
            r_data["name"] = "דוכן סוחר נודד"
            r_data["icon"] = "🏪"
            r_data["is_shop"] = True
            r_data["greeting"] = random.choice(MERCHANT_GREETINGS)
        else:
            biome = random.choice(BIOMES)
            r_data["name"] = biome["name"]
            r_data["icon"] = biome["icon"]
            
            if random.random() < 0.40:
                r_data["enemy"] = random.choice(ENEMIES).copy()
            elif random.random() < 0.15:
                r_data["chest"] = True
                r_data["name"] += " (כספת נסתרת)"
                
            if random.random() < 0.3:
                 r_data["items"].append(random.choice(["תחבושת", "מנת קרב", "אודם", "מפתח ברזל"]))

        self.state["map"][k] = r_data

    def move(self, dx, dy):
        r_now = self.state["map"][self.pos()]
        if r_now.get("enemy"):
            self.log("הדלת נעולה. האויב בחדר חוסם ממעבר!", "danger")
            return

        self.state["x"] += dx
        self.state["y"] += dy
        k = self.pos()
        
        self.create_room(self.state["x"], self.state["y"])
        if k not in self.state["visited"]: self.state["visited"].append(k)
        
        r = self.state["map"][k]
        self.log(f"הגעת ל-{r['name']}.", "sys")
        if r.get("is_shop"): self.log("🏪 יש פה סוחר – שווה לבדוק מה יש לו!", "gold")
        if r.get("chest"): self.log("🗝️ תיבה עתיקה נעולה בפינה...", "info")
        if r.get("enemy"): self.log(f"⚠️ {r['enemy']['name']} מחכה לך!", "danger")
        if r["items"]: self.log(f"🔎 מצאת על הרצפה: {', '.join(r['items'])}", "success")

    def attack(self):
        r = self.state["map"][self.pos()]
        if not r.get("enemy"): return self.log("אין כאן אויב לתקוף.", "info")
        
        enemy = r["enemy"]
        base = self.state["stats"]["atk_base"] + self.state["stats"]["atk_bonus"]
        player_dmg = random.randint(base - 3, base + 5)
        
        enemy["hp"] -= player_dmg
        self.log(f"⚔️ פגעת ב-{enemy['name']} ב-{player_dmg} נזק!", "sys")
        
        if enemy["hp"] <= 0:
            gold_drop = random.randint(8, 20)
            self.state["stats"]["gold"] += gold_drop
            self.log(f"💀 {enemy['name']} מת! +{gold_drop} זהב", "gold")
            if enemy.get("loot"): r["items"].extend(enemy["loot"])
            r["enemy"] = None 
        else:
            e_dmg = max(1, enemy["atk"] - random.randint(0, 3))
            self.state["stats"]["hp"] -= e_dmg
            self.log(f"🩸 האויב תקף בחזרה – {e_dmg} נזק!", "danger")

    def open_chest(self):
        r = self.state["map"][self.pos()]
        if not r.get("chest"): return
        
        key_held = None
        for it in self.state["inv"]:
            if ITEMS_DB.get(it, {}).get("type") == "key":
                key_held = it
                break
                
        if key_held:
            self.state["inv"].remove(key_held)
            r["chest"] = False
            gold = random.randint(50, 150)
            self.state["stats"]["gold"] += gold
            prize = random.choice(["יהלום", "שיקוי חיים אגדי", "רימון אש", "מפתח זהב"])
            self.state["inv"].append(prize)
            self.log(f"✨ פתחת את התיבה! קיבלת {prize} + {gold} זהב", "gold")
        else:
            self.log("🔒 אין לך מפתח מתאים...", "danger")

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
            st = self.state["stats"]
            if st["hp"] >= st["max"]: return self.log("אתה כבר בבריאות מלאה.", "info")
            st["hp"] = min(st["max"], st["hp"] + eff["val"])
            self.log(f"השתמשת ב-{item_name} → +{eff['val']} HP", "success")
            self.state["inv"].remove(item_name)
            
        elif eff["type"] == "buff":
            self.state["stats"]["atk_bonus"] += eff["val"]
            self.log(f"השתמשת ב-{item_name} → +{eff['val']} כוח זמני", "gold")
            self.state["inv"].remove(item_name)
            
        elif eff["type"] == "dmg_item":
            r = self.state["map"][self.pos()]
            if r.get("enemy"):
                r["enemy"]["hp"] -= eff["val"]
                self.log(f"💥 {item_name} פגע ב-{r['enemy']['name']} ב-{eff['val']} נזק!", "success")
                self.state["inv"].remove(item_name)
                if r["enemy"]["hp"] <= 0:
                    self.log("האויב הובס בעזרת החפץ!", "gold")
                    r["enemy"] = None
            else:
                self.log("אין אויב כאן לשימוש בזה.", "info")

    def sell_junk(self):
        r = self.state["map"][self.pos()]
        if not r.get("is_shop"): return
        
        profit = 0
        leftover = []
        sold_count = 0
        for item in self.state["inv"]:
            it_data = ITEMS_DB.get(item, {})
            if it_data.get("type") == "sell":
                profit += it_data.get("val", 0)
                sold_count += 1
            else:
                leftover.append(item)
                
        if sold_count > 0:
            self.state["inv"] = leftover
            self.state["stats"]["gold"] += profit
            self.log(f"מכרת {sold_count} חפצי אוצר → +{profit} זהב", "gold")
        else:
            self.log("אין לך חפצי מכירה כרגע...", "info")

    def buy(self, action_id):
        st = self.state["stats"]
        r = self.state["map"][self.pos()]
        if not r.get("is_shop"): return

        shop_items = {
            "upg_hp":       {"cost":  80, "name": "+20 מקס HP",           "effect": lambda: (st.__setitem__("max", st["max"]+20), st.__setitem__("hp", st["hp"]+20))},
            "upg_atk":      {"cost": 100, "name": "+5 כוח בסיס",         "effect": lambda: st.__setitem__("atk_base", st["atk_base"]+5)},
            "buy_heal":     {"cost":  35, "name": "שיקוי חיים גדול",     "effect": lambda: self.state["inv"].append("שיקוי חיים גדול")},
            "buy_mega":     {"cost":  90, "name": "שיקוי חיים אגדי",     "effect": lambda: self.state["inv"].append("שיקוי חיים אגדי")},
            "buy_poison":   {"cost":  45, "name": "רימון רעל",           "effect": lambda: self.state["inv"].append("רימון רעל")},
            "buy_ice":      {"cost":  65, "name": "רימון קרח",           "effect": lambda: self.state["inv"].append("רימון קרח")},
            "buy_key_iron": {"cost":  30, "name": "מפתח ברזל",            "effect": lambda: self.state["inv"].append("מפתח ברזל")},
            "buy_key_gold": {"cost": 120, "name": "מפתח זהב",             "effect": lambda: self.state["inv"].append("מפתח זהב")},
            "buy_buff":     {"cost":  70, "name": "שיקוי כוח (+5)",      "effect": lambda: self.state["inv"].append("שיקוי כוח")},
        }

        if action_id not in shop_items:
            return self.log("מוצר לא קיים בחנות", "danger")

        item = shop_items[action_id]
        if st["gold"] < item["cost"]:
            return self.log(f"צריך {item['cost']} זהב ל-{item['name']}", "danger")

        st["gold"] -= item["cost"]
        item["effect"]()
        self.log(f"קנית: {item['name']} !", "success")

    def get_ui_data(self):
        k = self.pos()
        r = self.state["map"][k]
        grid = []
        for dy in range(1, -2, -1):
            row = []
            for dx in range(-1, 2):
                p2 = f"{self.state['x']+dx},{self.state['y']+dy}"
                val, cls = "", "fog"
                if dx==0 and dy==0: val, cls = "🏃‍♂️", "player"
                elif p2 in self.state["visited"]:
                    val = "💀" if self.state["map"][p2].get("enemy") else self.state["map"][p2]["icon"]
                    cls = "known"
                row.append({"val":val, "cls":cls})
            grid.append(row)
            
        atk_visual = self.state["stats"]["atk_base"] + self.state["stats"]["atk_bonus"]

        return {
            "hp": self.state["stats"]["hp"], "max_hp": self.state["stats"]["max"],
            "gold": self.state["stats"]["gold"], "atk": atk_visual,
            "inv": self.state["inv"], "log": self.state["log"][-20:],
            
            "room_name": r["name"], "is_shop": r.get("is_shop", False), "shop_greet": r.get("greeting", ""),
            "items": r["items"], "enemy": r.get("enemy"), "chest": r.get("chest"),
            
            "map_grid": grid
        }

# ==========================================
# ROUTES
# ==========================================
@app.route("/")
def index():
    if "uid" not in session: session["uid"] = str(uuid.uuid4())
    return render_template_string(HTML, api=url_for("process"), home="/")

@app.route("/game/process", methods=["POST"])
def process():
    d = request.json
    try: eng = Engine(session.get("game_dmp"))
    except: eng = Engine(None)

    act = d.get("action")
    val = d.get("val")

    if eng.state["stats"]["hp"] <= 0 and act != "reset": return jsonify({"dead": True})

    if act == "move": eng.move(*val)
    elif act == "attack": eng.attack()
    elif act == "take": eng.take()
    elif act == "use": eng.use_item(val)
    elif act == "sell": eng.sell_junk()
    elif act == "buy": eng.buy(val)
    elif act == "open_chest": eng.open_chest()
    elif act == "reset": eng = Engine(None)

    session["game_dmp"] = eng.state
    return jsonify(eng.get_ui_data())


# ==========================================
# HTML + CSS + JS
# ==========================================
HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>חיפוש הקבר – Dungeon Pro</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arimo:wght@400;700&display=swap');
    
    :root { --bg:#1a1921; --panel:#282631; --panel2: #3a3746; --acc:#e6c433; --border:#4a4659;}
    body { background: var(--bg); color: #dedde6; margin: 0; font-family: 'Arimo', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow:hidden;}
    
    header { background: #131217; padding: 12px; display: flex; justify-content: space-between; align-items:center; border-bottom: 3px solid var(--border);}
    .title {font-weight:900; color:var(--acc); letter-spacing:2px; margin:0;}
    .stat-badge { background: #32303c; border:1px solid #666; padding: 4px 8px; border-radius: 4px; font-size: 13px; font-weight: bold;}
    
    .viewport { flex: 1; display: grid; grid-template-columns: 2fr 1fr; gap: 8px; padding: 10px; overflow: hidden; background:radial-gradient(circle at center, #262331 0%, #151419 100%);}
    
    .side-panel { display: flex; flex-direction: column; gap: 10px; }
    .map-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; margin: 0 auto; width: 140px; }
    .map-cell { height: 44px; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 4px; box-shadow:inset 0 0 10px rgba(0,0,0,1);}
    .map-cell.player { border: 2px solid lime; background: rgba(10,100,20, 0.4); }
    .map-cell.known { background: rgba(255,255,255, 0.1); border:1px solid rgba(255,255,255, 0.2); }

    .room-card { background: var(--panel2); border-left: 5px solid var(--acc); border-radius: 4px; padding: 10px; text-align: center; display:flex; flex-direction:column; gap:8px;}
    
    .dynamic-interaction {display:none; background:#2b0e0e; padding:10px; border-radius:5px; border:2px dashed #923a3a; flex-direction:column; gap:5px; box-shadow:0 0 10px #000 inset;}
    .hp-track { width: 100%; height: 12px; background: rgba(0,0,0,0.8); border-radius: 10px; overflow: hidden; border:1px inset #444; }
    .hp-fill { height: 100%; background: linear-gradient(90deg, #aa0000, #ff4040); width: 100%; transition: 0.2s cubic-bezier(0,1,1,1);}

    .shop-box {display:none; background:#181c19; padding:10px; border-radius:5px; border:1px solid #4a946b; box-shadow: inset 0 0 30px rgba(46,163,89, 0.2);}
    .shop-btn { background:#304e3b; border:1px solid #2ecc71; border-radius:4px; padding:6px; margin:3px 0; width:100%; font-weight:bold; cursor:pointer; color:white;}
    .shop-btn:active {transform:scale(0.97); background: #2ecc71;}
    .shop-btn.sell {background:#4a2c00; border-color:#ffaa00;}

    .chest-box {display:none; background:#1f1906; border: 2px dashed #d4af37; padding:10px; border-radius:6px; color:gold;}

    .log-container { background: #0c0b10; border-radius: 5px; border: 1px inset #222; padding: 10px; overflow-y: auto; display:flex; flex-direction:column-reverse; gap:4px; box-shadow: -10px 0 20px rgba(0,0,0,0.3);}
    .msg { padding: 6px; border-radius: 2px; font-size: 12px; line-height: 1.5; color:#a6a1bd; border-right: 3px solid transparent; background:rgba(255,255,255,0.015);}
    .sys { text-align: right; color: #5880a6; border-right-color:#2a5075; font-style:italic;}
    .danger { color: #f28b82; border-right-color:#c5221f; background: rgba(255,0,0,0.1); }
    .success { color: #81c995; border-right-color:#1e8e3e; background: rgba(0,255,0,0.05);}
    .gold { color: #fce8b2; border-right-color:#f29900; font-weight:bold;}

    .inv-modal { display:none; position:fixed; inset:0; background:rgba(10,5,15,0.85); z-index:99; justify-content:center; align-items:center; backdrop-filter: blur(2px);}
    .inv-box { background:var(--panel2); width:85%; max-width:420px; padding:20px; border-radius:8px; border:2px solid var(--border); box-shadow:0 0 40px #000; max-height:80vh; overflow-y:auto;}
    .use-btn { background: #23222a; color: white; font-weight:bold; padding: 10px; border: 1px solid #5a546e; border-radius:4px; width: 100%; cursor: pointer; margin:4px 0;}
    .use-btn:active { background: #454056; }
    
    .controls { height: 165px; background: #1f1d27; border-top: 3px solid #131217; padding: 15px 10px; display: grid; grid-template-columns: 1fr 150px; gap: 20px; align-items: center;}
    .d-pad { direction: ltr; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; width: 150px; height:100%;}
    .btn-arr { background: #2f2d39; color: #b7b3ce; border:none; box-shadow: inset 0 -3px #18161d; border-radius: 6px; font-size: 20px; cursor: pointer;}
    .btn-arr:active { background: #3b3947; box-shadow: none; transform:translateY(3px); }
    .up { grid-column: 2; grid-row: 1; }
    .down { grid-column: 2; grid-row: 2; }
    .left { grid-column: 1; grid-row: 2; }
    .right { grid-column: 3; grid-row: 2; }

    .main-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; height: 100%; }
    .act-btn { height: 100%; min-height:55px; font-weight: bold; font-size: 15px; border: none; border-radius: 6px; cursor: pointer; color:#e0e0e0; box-shadow: inset 0 -4px rgba(0,0,0,0.5);}
    .act-btn:active{transform:translateY(3px); box-shadow:none;}
    .btn-atk { background: #a22929; border: 1px solid #ff4e4e; }
    .btn-take { background: #267a3a; border: 1px solid #5bff81;}
    .btn-inv  { background: #886716; border:1px solid #ffc841; grid-column: span 2; min-height:45px;}
</style>
</head>
<body>

<header>
    <div class="title">TOMB SEEKER</div>
    <div style="display:flex; gap:6px;">
        <div class="stat-badge">⚔️ <span id="atk">10</span></div>
        <div class="stat-badge">❤️ <span id="hp">100/100</span></div>
        <div class="stat-badge" style="color:gold;">💰 <span id="gold">20</span></div>
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
                    <span><span id="en-hp"></span>/<span id="en-max"></span></span>
                </div>
                <div class="hp-track"><div id="en-fill" class="hp-fill" style="width:100%"></div></div>
            </div>
            
            <div id="shop-box" class="shop-box">
                <div style="color:lime; font-size:16px; margin-bottom:8px;">🏪 סוחר נודד</div>
                <div id="shop-txt" style="font-style:italic; color:#a2cfba; margin-bottom:12px;"></div>
                
                <button class="shop-btn sell" onclick="send('sell')">💰 למכור הכל (אבנים + יהלומים)</button>
                
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:12px;">
                    <button class="shop-btn" onclick="send('buy','upg_hp')">+20 HP (80)</button>
                    <button class="shop-btn" onclick="send('buy','upg_atk')">+5 ATK (100)</button>
                    <button class="shop-btn" onclick="send('buy','buy_heal')">שיקוי גדול (35)</button>
                    <button class="shop-btn" onclick="send('buy','buy_mega')">שיקוי אגדי (90)</button>
                    <button class="shop-btn" onclick="send('buy','buy_poison')">רימון רעל (45)</button>
                    <button class="shop-btn" onclick="send('buy','buy_ice')">רימון קרח (65)</button>
                    <button class="shop-btn" onclick="send('buy','buy_key_iron')">מפתח ברזל (30)</button>
                    <button class="shop-btn" onclick="send('buy','buy_key_gold')">מפתח זהב (120)</button>
                    <button class="shop-btn" style="grid-column:span 2;" onclick="send('buy','buy_buff')">שיקוי כוח (70)</button>
                </div>
            </div>

            <div id="chest-box" class="chest-box">
                <div>תיבה נעולה 🔒</div>
                <button onclick="send('open_chest')" style="width:100%; margin-top:8px; background:gold; color:black; font-weight:bold; padding:8px; border:none; border-radius:4px; cursor:pointer;">
                    לפתוח (צריך מפתח)
                </button>
            </div>
        </div>
    </div>

    <div class="log-container" id="log-box"></div>
</div>

<div class="inv-modal" id="inv-modal" onclick="if(event.target==this) toggleInv()">
    <div class="inv-box">
        <h2 style="margin:0 0 12px 0; text-align:center; color:var(--acc);">תיק</h2>
        <div id="inv-list" style="display:grid; gap:6px;"></div>
    </div>
</div>

<div class="controls">
    <div class="main-actions">
        <button class="act-btn btn-atk" onclick="send('attack')">⚔️ תקוף</button>
        <button class="act-btn btn-take" onclick="send('take')">✋ לאסוף</button>
        <button class="act-btn btn-inv" onclick="toggleInv()">🎒 תיק</button>
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
    if(act==='use') toggleInv();

    try {
        let res = await fetch(API, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: act, val: val})
        });
        let d = await res.json();

        if (d.dead) {
            alert("נפלת... המשחק יתאפס");
            send('reset');
            return;
        }

        // Log
        let logBox = document.getElementById("log-box");
        logBox.innerHTML = "";
        d.log.slice().reverse().forEach(msg => {
            logBox.innerHTML += `<div class="msg ${msg.type}">${msg.text}</div>`;
        });

        // Mini-map
        let mapH = "";
        d.map_grid.forEach(row => {
            row.forEach(c => mapH += `<div class='map-cell ${c.cls}'>${c.val}</div>`);
        });
        document.getElementById("map-target").innerHTML = mapH;

        // Stats
        document.getElementById("hp").innerText = `${d.hp}/${d.max_hp}`;
        document.getElementById("gold").innerText = d.gold;
        document.getElementById("atk").innerText = d.atk;
        document.getElementById("loc-name").innerText = d.room_name;

        // Contexts
        document.getElementById("enemy-box").style.display = d.enemy ? "flex" : "none";
        if (d.enemy) {
            document.getElementById("en-name").innerText = d.enemy.name;
            document.getElementById("en-hp").innerText = d.enemy.hp;
            document.getElementById("en-max").innerText = d.enemy.max;
            document.getElementById("en-fill").style.width = (d.enemy.hp / d.enemy.max * 100) + "%";
        }

        document.getElementById("shop-box").style.display = d.is_shop ? "block" : "none";
        if (d.is_shop) document.getElementById("shop-txt").innerText = d.shop_greet;

        document.getElementById("chest-box").style.display = d.chest ? "block" : "none";

        // Inventory modal
        let invL = document.getElementById("inv-list");
        invL.innerHTML = "";
        if (d.inv.length === 0) {
            invL.innerHTML = "<div style='text-align:center; color:#777;'>התיק ריק...</div>";
        } else {
            d.inv.sort().forEach(it => {
                invL.innerHTML += `<button class="use-btn" onclick="send('use','${it.replace(/'/g,"\\'")}')">${it}</button>`;
            });
        }

    } catch(e) { console.error(e); }
}

function toggleInv() {
    let el = document.getElementById("inv-modal");
    el.style.display = (el.style.display === "flex") ? "none" : "flex";
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5007, debug=True)
