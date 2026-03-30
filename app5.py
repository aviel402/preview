import random
import time
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = "iron_legion_commander"

# --- נתוני יחידות ומדינה ---

UNIT_TYPES = {
    "grunt": {"name": "לוחם חי\"ר", "cost": 50, "dmg": 2, "hp": 10, "icon": "🔫"},
    "sniper": {"name": "צלף עלית", "cost": 150, "dmg": 15, "hp": 5, "icon": "🔭"},
    "tank": {"name": "טנק כבד", "cost": 500, "dmg": 50, "hp": 100, "icon": "🚜"},
    "mech": {"name": "רובוט קרב", "cost": 2000, "dmg": 150, "hp": 300, "icon": "🤖"},
}

UPGRADES = {
    "weapons": {"name": "שדרוג נשק (+20% נזק)", "cost": 1000, "factor": 1.2, "type": "dmg"},
    "armor": {"name": "שדרוג שריון (+20% בריאות)", "cost": 1000, "factor": 1.2, "type": "hp"},
}

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.gold = 300
        self.wave = 1
        # הצבא הנוכחי שלך (כמות מכל סוג)
        self.army = {"grunt": 0, "sniper": 0, "tank": 0, "mech": 0}
        
        # רמות שדרוגים
        self.tech = {"weapons": 1, "armor": 1}
        self.upgrade_costs = {"weapons": 1000, "armor": 1000}
        
        self.last_battle_log = ["ברוך הבא למפקדה, גנרל. גייס כוחות וצא לקרב."]
        self.battle_result = None # 'win', 'lose', or None

    def get_army_stats(self):
        # חישוב כוח כולל
        total_dmg = 0
        total_hp = 0
        count = 0
        for u_key, amount in self.army.items():
            if amount > 0:
                stats = UNIT_TYPES[u_key]
                # נוסחת הכוח: בסיס * כמות * טכנולוגיה
                total_dmg += (stats["dmg"] * amount) * self.tech["weapons"]
                total_hp += (stats["hp"] * amount) * self.tech["armor"]
                count += amount
        return int(total_dmg), int(total_hp), count

    def fight(self):
        # 1. חישוב כוח האויב (גדל אקספוננציאלית עם כל גל)
        enemy_hp = 20 * (self.wave ** 1.5)
        enemy_dmg = 5 * (self.wave ** 1.3)
        enemy_name = f"גלי תקיפה #{self.wave}"
        
        # 2. נתונים התחלתיים
        my_dmg, my_hp, my_count = self.get_army_stats()
        
        if my_count == 0:
            self.last_battle_log = ["❌ אין לך צבא! גייס חיילים לפני הקרב."]
            return

        combat_log = [f"⚔️ הקרב מול {enemy_name} החל!"]
        combat_log.append(f"כוח שלך: {my_dmg} נזק | {my_hp} חיים")
        combat_log.append(f"כוח אויב: {int(enemy_dmg)} נזק | {int(enemy_hp)} חיים")
        
        # 3. סימולציית הקרב (בסיבובים אוטומטיים)
        rounds = 0
        victory = False
        
        while my_hp > 0 and enemy_hp > 0:
            rounds += 1
            # תור השחקן
            enemy_hp -= my_dmg
            
            # תור האויב (אם הוא שרד)
            if enemy_hp > 0:
                damage_taken = enemy_dmg
                my_hp -= damage_taken
                
                # האויב הורג יחידות תוך כדי קרב!
                # אובדן יחידות הוא יחסי לנזק שספגת (אחוזים)
                units_lost_percent = min(0.1, damage_taken / (my_hp + damage_taken))
                # בכל סיבוב, יש סיכוי שחיילים מתים
                self.kill_units(units_lost_percent) 
                
                # עדכון מחדש של כוח אחרי שאנשים מתו
                my_dmg, real_current_hp, _ = self.get_army_stats() 
                if real_current_hp <= 0: my_hp = 0 # מוודאים סנכרון

        # 4. תוצאות
        if my_hp > 0:
            victory = True
            reward = int(100 * (self.wave ** 1.2))
            self.gold += reward
            self.wave += 1
            self.battle_result = 'win'
            combat_log.append(f"🏆 ניצחון ב-{rounds} סבבים! השלל: {reward} זהב.")
        else:
            self.battle_result = 'lose'
            # בהפסד מאבדים חצי מהצבא שנשאר
            self.kill_units(0.5)
            consolation = int(20 * self.wave)
            self.gold += consolation
            combat_log.append(f"💀 התבוסה צורבת... הצבא נמחק. פיצוי קטן: {consolation} זהב.")

        self.last_battle_log = combat_log

    def kill_units(self, percentage):
        # הורג אחוז מסוים מכל סוג יחידה (מעגל למטה)
        # זה קריטי - קרבות עולים בחיי אדם!
        for u_key in self.army:
            if self.army[u_key] > 0:
                dead = int(self.army[u_key] * percentage)
                # תמיד יש סיכוי שלפחות חייל אחד ימות אם נפגענו
                if dead == 0 and random.random() < 0.3: dead = 1
                self.army[u_key] = max(0, self.army[u_key] - dead)

state = Game()

# --- עיצוב גרפי (Cyber-Military) ---
# הערה: כל הלינקים עודכנו להתחיל ב- /game5/

HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iron Legion</title>
    <style>
        body { 
            background-color: #0f111a; color: #aab2c0; font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 0; padding: 10px; text-align: center;
        }
        h1 { margin: 5px; color: #eab308; text-transform: uppercase; letter-spacing: 3px; font-size: 24px; }
        
        .container { max-width: 500px; margin: 0 auto; padding-bottom: 50px; }
        
        /* Stats Dashboard */
        .dashboard {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
            background: #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 20px;
            border-bottom: 4px solid #3b82f6; box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        .stat-val { display: block; font-size: 22px; color: white; font-weight: bold; }
        .stat-label { font-size: 12px; text-transform: uppercase; color: #64748b; }

        /* Unit Recruitment */
        .units-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .unit-card {
            background: #1e293b; padding: 10px; border-radius: 10px; text-align: right;
            border: 1px solid #334155; position: relative; transition: 0.2s;
        }
        .unit-card:hover { border-color: #eab308; transform: translateY(-2px); }
        .unit-icon { float: left; font-size: 30px; }
        .unit-name { color: #f8fafc; font-weight: bold; display: block; }
        .unit-cost { color: #eab308; font-size: 13px; }
        .unit-owned { font-size: 12px; color: #94a3b8; margin-top: 5px; }
        
        .btn-buy {
            width: 100%; margin-top: 8px; padding: 8px; border: none; background: #2563eb; 
            color: white; border-radius: 5px; cursor: pointer; font-weight: bold;
        }
        .btn-buy:hover { background: #1d4ed8; }
        
        /* Battle Section */
        .battle-section { background: #331515; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #7f1d1d; }
        .btn-fight {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white; border: none; font-size: 20px; font-weight: bold; border-radius: 8px;
            cursor: pointer; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }

        /* Tech */
        .tech-section { background: #172033; padding: 15px; border-radius: 12px; }
        .tech-row { display: flex; justify-content: space-between; margin-bottom: 10px; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 8px; }
        .btn-upgrade { background: #059669; padding: 5px 15px; color: white; border:none; border-radius: 4px; cursor: pointer; }

        /* Log */
        .log-box { 
            background: #000; color: #10b981; font-family: monospace; padding: 15px; 
            border-radius: 8px; text-align: right; min-height: 100px; max-height: 200px; 
            overflow-y: auto; margin-top: 20px; font-size: 13px; line-height: 1.5; border: 1px solid #1e293b;
        }
        .log-lose { color: #ef4444; }
        .log-title { color: white; border-bottom: 1px dashed #333; margin-bottom: 5px; }

        /* Back button */
        .back-link { margin-top:20px; display:inline-block; color:#aaa; font-size:12px; text-decoration:none; }
        .back-link:hover { text-decoration: underline; color: #fff; }

    </style>
</head>
<body>

<div class="container">
    <h1>⚔️ IRON LEGION ⚔️</h1>
    
    <div class="dashboard">
        <div><span class="stat-label">זהב</span><span class="stat-val" style="color:#eab308">{{ game.gold }}</span></div>
        <div><span class="stat-label">גל נוכחי</span><span class="stat-val">{{ game.wave }}</span></div>
        <div><span class="stat-label">גודל צבא</span><span class="stat-val">{{ total_units }}</span></div>
    </div>

    <!-- Battle Log -->
    <div class="log-box">
        {% for line in game.last_battle_log %}
            <div class="{{ 'log-lose' if '❌' in line or '💀' in line else '' }}">{{ line }}</div>
        {% endfor %}
    </div>

    <div class="battle-section">
        <a href="/game5/fight"><button class="btn-fight">🔥 שלח צבא לקרב 🔥</button></a>
        <div style="margin-top:10px; font-size:12px; color:#ef4444;">אזהרה: יחידות ימותו בקרב!</div>
    </div>

    <h3>💰 גיוס יחידות</h3>
    <div class="units-grid">
        {% for key, unit in units.items() %}
        <div class="unit-card">
            <span class="unit-icon">{{ unit.icon }}</span>
            <span class="unit-name">{{ unit.name }}</span>
            <div class="unit-cost">{{ unit.cost }}$ </div>
            <div class="unit-owned">יש ברשותך: <b>{{ game.army[key] }}</b></div>
            <a href="/game5/buy/{{ key }}"><button class="btn-buy">גייס (+1)</button></a>
        </div>
        {% endfor %}
    </div>

    <h3>🔧 שדרוגים (Tech)</h3>
    <div class="tech-section">
        {% for key, upg in upgrades.items() %}
        <div class="tech-row">
            <div style="text-align:right">
                <div style="font-weight:bold; color: white">{{ upg.name }}</div>
                <div style="font-size:12px">רמה נוכחית: {{ game.tech[key] }}</div>
            </div>
            <a href="/game5/upgrade/{{ key }}">
                <button class="btn-upgrade">{{ game.upgrade_costs[key] }}$ ▲</button>
            </a>
        </div>
        {% endfor %}
    </div>
    
    <br>
    <a href="/game5/reset" style="color: #64748b; font-size:12px; margin-left: 10px;">אפס משחק</a>
    <a href="/" class="back-link">יציאה ללובי</a>

</div>

</body>
</html>
"""

@app.route('/')
def home():
    # חישוב סה"כ חיילים לתצוגה
    _, _, total = state.get_army_stats()
    return render_template_string(HTML, game=state, units=UNIT_TYPES, upgrades=UPGRADES, total_units=total)

@app.route('/buy/<unit_key>')
def buy(unit_key):
    cost = UNIT_TYPES[unit_key]['cost']
    if state.gold >= cost:
        state.gold -= cost
        state.army[unit_key] += 1
    return redirect('/game5/')

@app.route('/upgrade/<upg_key>')
def upgrade(upg_key):
    cost = state.upgrade_costs[upg_key]
    if state.gold >= cost:
        state.gold -= cost
        state.tech[upg_key] = round(state.tech[upg_key] * UPGRADES[upg_key]['factor'], 2)
        # המחיר עולה פי 2 בכל שדרוג
        state.upgrade_costs[upg_key] = int(cost * 1.8)
    return redirect('/game5/')

@app.route('/fight')
def battle():
    state.fight()
    return redirect('/game5/')

@app.route('/reset')
def reset():
    state.reset()
    return redirect('/game5/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
