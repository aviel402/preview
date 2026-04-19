import random
import uuid
from flask import Flask, redirect, session
from jinja2 import Environment, BaseLoader

app = Flask(__name__)
app.secret_key = "rpg_legend_secret_super_key_123"
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 30

# ====================== HTML TEMPLATE ======================
HTML_TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPG Legends: Golden Forest</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --gold: #FFD700;
            --dark-bg: #0d1117;
            --panel-bg: rgba(30, 34, 42, 0.85);
            --danger: #ff4d4d;
            --safe: #4CAF50;
        }
        body {
            background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.8)), url('/static/background.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: #0d0d0f;
            color: #c5c6c7; font-family: 'Assistant', sans-serif;
            margin: 0; padding: 20px 10px; display: flex; flex-direction: column;
            align-items: center; min-height: 100vh; overflow-x: hidden;
        }
        .game-card {
            background: var(--panel-bg); width: 100%; max-width: 520px;
            padding: 20px; border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.8), 0 0 20px rgba(255, 215, 0, 0.1);
            border: 2px solid #332f1b; position: relative; backdrop-filter: blur(8px);
        }
        h2 {
            margin: 0 0 15px 0; color: var(--gold); text-align: center;
            font-family: 'Cinzel', serif; font-size: 28px; text-shadow: 0 2px 10px rgba(255, 215, 0, 0.4);
            letter-spacing: 2px;
        }
        .stats-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;
            background: rgba(0,0,0,0.6); padding: 12px; border-radius: 10px;
            margin-bottom: 20px; text-align: center; border: 1px solid #444;
            font-weight: bold; color: #fff; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
        }
        .stat-box { display: flex; flex-direction: column; align-items: center; justify-content: center; font-size:14px; }
        .stat-icon { font-size: 20px; margin-bottom: 3px; }
        .hp-wrapper { width: 100%; grid-column: span 4; margin-top: 5px; }
        .hp-container {
            background: #222; height: 14px; border-radius: 10px;
            overflow: hidden; box-shadow: inset 0 2px 5px rgba(0,0,0,0.9); border: 1px solid #555;
        }
        .hp-fill {
            height: 100%; transition: width 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
            box-shadow: 0 0 10px var(--safe); background-image: linear-gradient(90deg, #1f6b21, #4CAF50);
        }
        @keyframes pulse-danger { 0% { opacity: 0.8; } 100% { opacity: 1; filter: brightness(1.5); } }
        .scene {
            background: linear-gradient(to bottom, {{ bg_color }} 0%, rgba(0,0,0,0.8) 100%);
            height: 180px; border-radius: 12px; margin-bottom: 20px;
            position: relative; display: flex; flex-direction: column; justify-content: center; align-items: center;
            font-size: 65px; text-shadow: 0 5px 15px black; border: 2px solid #524724;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.9); overflow: hidden;
        }
        .scene-icon { animation: float 3s ease-in-out infinite; transition: transform 0.2s; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
        .shake-impact { animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both; color: red; }
        @keyframes shake { 10%, 90% { transform: translate3d(-4px, 0, 0) scale(1.1); } 20%, 80% { transform: translate3d(6px, 0, 0) scale(1.1); } 30%, 50%, 70% { transform: translate3d(-10px, 0, 0) scale(1.1); } 40%, 60% { transform: translate3d(10px, 0, 0) scale(1.1); } }
        .scene-badge {
            position: absolute; bottom: 10px; font-size: 15px; background: rgba(0,0,0,0.7);
            padding: 5px 15px; border-radius: 20px; color: var(--gold); border: 1px solid var(--gold); font-weight: bold;
        }
        .enemy-hp { position:absolute; top: 10px; width: 80%; }
        .logs-wrapper {
            background: rgba(0,0,0,0.75); padding: 15px; height: 110px; overflow-y: hidden;
            border-radius: 8px; margin-bottom: 20px; border: 1px solid #333;
            display:flex; flex-direction:column-reverse; position: relative;
        }
        .logs-wrapper::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 30px; background: linear-gradient(rgba(0,0,0,1), transparent); pointer-events: none; }
        .log-line { margin-bottom: 6px; padding-bottom: 4px; border-bottom: 1px dashed #222; font-size: 15px; opacity: 0.8; transition: 0.3s; }
        .log-line:first-child { opacity: 1; font-weight: bold; font-size: 16px; border: none; }
        .log-good { color: #5ce65c; } .log-bad { color: #ff4d4d; } .log-alert { color: var(--gold); } .log-gold { color: #ffeb3b; }
        .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        button {
            background: linear-gradient(to bottom, #2b3344, #181d28); border: 2px solid #4a5c7c;
            color: #d1d8e0; padding: 15px; font-size: 16px; cursor: pointer; border-radius: 10px;
            font-weight: 800; text-shadow: 0 1px 3px black; box-shadow: 0 4px 6px rgba(0,0,0,0.5);
            transition: all 0.15s; position: relative; overflow: hidden; font-family: 'Assistant', sans-serif;
        }
        button::before { content:''; position: absolute; top:0;left:-100%; width:50%; height:100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); transform: skewX(-20deg); transition: 0s; }
        button:hover { filter: brightness(1.2); transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.6); }
        button:hover::before { left: 150%; transition: 0.6s ease; }
        button:active { transform: translateY(2px); box-shadow: 0 2px 4px rgba(0,0,0,0.6); }
        .combat-btn { background: linear-gradient(to bottom, #591919, #360b0b); border-color: #ff4d4d; color: #ffb3b3;}
        .heal-btn { background: linear-gradient(to bottom, #1d4d1d, #0b2b0b); border-color: #4CAF50; color: #b3ffb3;}
        .shop-btn { background: linear-gradient(to bottom, #4d4013, #2b2308); border-color: var(--gold); color: #fffde0;}
        .travel-btn { background: linear-gradient(to bottom, #1a3b40, #0a1f22); border-color: #4df;}
        .boss-btn { background: linear-gradient(to bottom, #6b5c00, #362a00); border-color: var(--gold); color: #fff; box-shadow: 0 0 20px rgba(255,215,0,0.4); text-shadow: 0 0 10px var(--gold); animation: pulse-danger 1.5s infinite alternate; }
        .victory-screen { text-align: center; background: rgba(0,0,0,0.8); padding: 30px; border-radius: 15px; border: 2px solid var(--gold); margin-bottom: 20px;}
        .victory-screen h1 { color: var(--gold); font-size: 45px; text-shadow: 0 0 20px var(--gold); margin:0 0 10px 0;}
        a.back-menu { display:block; margin-top: 20px; color: #bbb; font-size: 14px; text-decoration:none; text-align: center; background: rgba(0,0,0,0.5); padding: 5px 15px; border-radius: 10px;}
        a.back-menu:hover { color: var(--gold); text-shadow: 0 0 10px var(--gold); background: rgba(0,0,0,0.8); }
        .flash-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: red; opacity: 0; pointer-events: none; z-index: 100; transition: opacity 0.5s; }
        .flash-active { animation: hit-flash 0.3s forwards; }
        @keyframes hit-flash { 0% {opacity:0.4;} 100% {opacity:0;} }
    </style>
</head>
<body data-won="{{ 'true' if p.game_won else 'false' }}">
    <div class="flash-overlay" id="flash-screen"></div>
    <div class="game-card">
        <h2>יער הזהב וממלכת הצללים</h2>
        <div class="stats-grid">
            <div class="stat-box"><span class="stat-icon">⭐</span> {{ p.level }} רמה</div>
            <div class="stat-box"><span class="stat-icon">💰</span> {{ p.gold }}ג</div>
            <div class="stat-box"><span class="stat-icon">⚔️</span> {{ p.damage }} כוח</div>
            <div class="stat-box"><span class="stat-icon">🧪</span> {{ p.potions }} ש"ח</div>
           
            <div class="hp-wrapper">
                <div style="font-size:12px; margin-bottom:3px; display:flex; justify-content:space-between">
                    <span style="color:#ff6666">❤️ {{ p.hp }}/{{ p.max_hp }} ({{ p.xp }}/{{ p.next_level_xp }} XP)</span>
                </div>
                <div class="hp-container">
                    <div class="hp-fill" style="width: {{ ((p.hp / p.max_hp) * 100) }}%;"></div>
                </div>
            </div>
        </div>
        <div class="scene">
            <div class="scene-icon" id="target-icon" style="{{ 'font-size:80px; text-shadow:0 0 30px gold;' if 'בוס' in location_name else '' }}">{{ emoji_icon }}</div>
            {% if p.in_combat and p.current_enemy %}
            <div class="hp-container enemy-hp"><div class="hp-fill" style="background-image:linear-gradient(90deg, #aa0000, #ff4d4d); width:{{ ((p.current_enemy.hp / p.current_enemy.max_hp)*100) }}%;"></div></div>
            {% endif %}
            <div class="scene-badge">{{ location_name }}</div>
        </div>
        <div class="logs-wrapper" id="logs-box">
            {% for log in p.logs %}
                {% set log_class = "" %}
                {% if "נפגעת" in log or "איבדת" in log or "חסר" in log or "מכה אנושה" in log %}{% set log_class = "log-bad" %}
                {% elif "זהב" in log and ("גרם" in log or "+" in log) %}{% set log_class = "log-gold" %}
                {% elif "שיקוי" in log or "שודרג" in log or "ניצחון" in log or "רמה" in log or "הצלחת" in log %}{% set log_class = "log-good" %}
                {% elif "מארב פתע" in log or "רעדה" in log %}{% set log_class = "log-alert" %}
                {% endif %}
                <div class="log-line {{ log_class }}">{{ log }}</div>
            {% endfor %}
        </div>

        {% if p.game_won %}
        <div class="victory-screen">
            <h1>🏆 נצחון אגדי! 🏆</h1>
            <p style="font-size: 18px;">הבסת את שד הזהב העתיק ושחררת את ממלכת הצללים!</p>
            <p style="color:var(--gold); font-weight:bold; font-size: 20px;">זהב סופי: {{ p.gold }}ג | רמה: {{ p.level }}</p>
            <button type="button" data-act="coin" data-url="/game2/restart" style="margin-top: 15px; width:100%;" class="shop-btn">🔄 התחל אגדה חדשה</button>
        </div>
        {% else %}
        <div class="actions">
            {% if p.hp <= 0 %}
                <button type="button" data-act="death" data-url="/game2/restart" style="grid-column: span 2; background: #660000; border-color: red;">☠️ מסעך הסתיים. לחץ להתחלה חדשה</button>
            {% elif p.in_combat %}
                <button type="button" class="combat-btn" data-act="attack" data-url="/game2/action/attack">⚔️ תקיפת חרב</button>
                <button type="button" class="heal-btn" data-act="heal" data-url="/game2/action/heal">🧪 שתיית שיקוי</button>
                <button type="button" style="grid-column: span 2;" data-act="run" data-url="/game2/action/flee">🏃 נסיגה פחדנית חזרה (-זהב)</button>
            {% elif p.location == 'town' %}
                <button type="button" class="travel-btn" data-act="travel" data-url="/game2/travel/forest">🌲 היכנס ליער הזהב</button>
                <button type="button" class="travel-btn" style="border-color: #aa00ff" data-act="travel" data-url="/game2/travel/cave">🦇 מערת אופל הצללים</button>
                <button type="button" class="shop-btn" data-act="coin" data-url="/game2/shop/buy_potion">🧪 שיקוי חיים (30ג)</button>
                <button type="button" class="shop-btn" data-act="upgrade" data-url="/game2/shop/upgrade_weapon">⚔️ רכישת כוח ({{ p.weapon_level * 60 }}ג)</button>
                <button type="button" class="heal-btn" style="grid-column: span 2;" data-act="heal" data-url="/game2/action/inn">🏨 שינה מלאה בפונדק (20ג)</button>
            {% elif p.location == 'forest' or p.location == 'cave' %}
                <button type="button" class="combat-btn" data-act="search" data-url="/game2/action/explore" style="grid-column: span 2;">🔍 סייר במעמקים</button>
                {% if p.location == 'cave' and p.level >= 10 %}
                    <button type="button" class="boss-btn" data-act="boss" data-url="/game2/action/boss" style="grid-column: span 2;">👑 אתגר את שד הזהב העתיק (בוס סופי) 👑</button>
                {% endif %}
                <button type="button" data-act="travel" data-url="/game2/travel/town" style="grid-column: span 2;">🏠 חזור אל העיר</button>
            {% endif %}
        </div>
        {% endif %}
    </div>
    <a href="/" class="back-menu">⮜ חזרה לארקייד הראשי </a>

    <script>
        const AContext = window.AudioContext || window.webkitAudioContext;
        let ctx = null;

        function initAudio() {
            if (!ctx) ctx = new AContext();
            if (ctx.state === 'suspended') ctx.resume();
        }

        function playSfx(type) {
            initAudio();
            const now = ctx.currentTime;
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.connect(g); g.connect(ctx.destination);

            if (type === 'slash') {
                o.type = 'sawtooth'; o.frequency.setValueAtTime(150, now);
                o.frequency.exponentialRampToValueAtTime(10, now + 0.1);
                g.gain.setValueAtTime(0.5, now); g.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                o.start(now); o.stop(now + 0.1);
            } else if (type === 'hit') {
                o.type = 'square'; o.frequency.setValueAtTime(60, now);
                o.frequency.exponentialRampToValueAtTime(20, now + 0.3);
                g.gain.setValueAtTime(0.6, now); g.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                o.start(now); o.stop(now + 0.3);
            } else if (type === 'heal' || type === 'upgrade') {
                o.type = 'sine'; o.frequency.setValueAtTime(400, now);
                o.frequency.linearRampToValueAtTime(800, now + 0.2);
                g.gain.setValueAtTime(0.3, now); g.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                o.start(now); o.stop(now + 0.3);
            } else if (type === 'coin') {
                o.type = 'sine'; o.frequency.setValueAtTime(1000, now);
                g.gain.setValueAtTime(0.3, now); g.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                o.start(now); o.stop(now + 0.1);
            } else if (type === 'boss') {
                o.type = 'sawtooth'; o.frequency.setValueAtTime(50, now);
                o.frequency.linearRampToValueAtTime(200, now + 0.5);
                g.gain.setValueAtTime(0.5, now); g.gain.linearRampToValueAtTime(0.01, now + 0.8);
                o.start(now); o.stop(now + 0.8);
            } else if (type === 'victory') {
                [300, 400, 500, 600, 800].forEach((freq, i) => {
                    setTimeout(() => {
                        if (ctx.state === 'closed') return;
                        const oo = ctx.createOscillator();
                        const gg = ctx.createGain();
                        oo.connect(gg); gg.connect(ctx.destination);
                        oo.type = 'square'; oo.frequency.value = freq;
                        gg.gain.setValueAtTime(0.2, ctx.currentTime);
                        gg.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                        oo.start(); oo.stop(ctx.currentTime + 0.3);
                    }, i * 150);
                });
            } else {
                o.type = 'triangle'; o.frequency.setValueAtTime(800, now);
                g.gain.setValueAtTime(0.1, now); g.gain.linearRampToValueAtTime(0.01, now + 0.05);
                o.start(now); o.stop(now + 0.05);
            }
        }

        // ====================== EVENT DELEGATION ======================
        document.addEventListener('click', function(e) {
            const btn = e.target.closest('button[data-url]');
            if (!btn) return;

            e.preventDefault();

            const url = btn.getAttribute('data-url');
            const actionName = btn.getAttribute('data-act') || 'default';

            playSfx(actionName);

            if (actionName === 'attack' || actionName === 'boss') {
                const sceneIcon = document.getElementById("target-icon");
                if (sceneIcon) sceneIcon.classList.add("shake-impact");
            }

            if (actionName === 'death' || actionName === 'coin') {
                sessionStorage.removeItem("victory_played");
            }

            sessionStorage.setItem("trigger_action", actionName);

            setTimeout(() => {
                window.location.href = url;
            }, 180);
        });

        // ====================== ON LOAD ======================
        window.onload = () => {
            const actTriggered = sessionStorage.getItem("trigger_action");
            const sceneIcon = document.getElementById("target-icon");
            const lastLog = `{{ p.logs[0] if p.logs else '' }}`;
            const gameWon = document.body.getAttribute('data-won') === 'true';

            if (gameWon && !sessionStorage.getItem("victory_played")) {
                playSfx('victory');
                sessionStorage.setItem("victory_played", "true");
            } else if (actTriggered) {
                if (actTriggered === "attack" || actTriggered === "boss") {
                    if (sceneIcon) sceneIcon.classList.add("shake-impact");
                } else if (actTriggered === "heal") {
                    playSfx('heal');
                } else if (actTriggered === "coin" || actTriggered === "upgrade") {
                    playSfx('coin');
                }
                sessionStorage.removeItem("trigger_action");
            }

            if (lastLog.includes("נפגעת") && lastLog.includes("חיים") && !gameWon) {
                setTimeout(() => {
                    playSfx('hit');
                    const flash = document.getElementById("flash-screen");
                    if (flash) flash.classList.add("flash-active");
                }, 100);
            }
        };
    </script>
</body>
</html>
"""

jinja_env = Environment(loader=BaseLoader())
game_template = jinja_env.from_string(HTML_TEMPLATE_STR)

# ====================== MODELS ======================
class Enemy:
    def __init__(self, name, level, hp=None):
        self.name = name
        self.level = level
        self.max_hp = hp if hp is not None else 25 + (level * 15)
        self.hp = self.max_hp
        self.damage = 5 + (level * 4)
        self.xp_reward = 25 * level
        self.gold_reward = random.randint(15, 40) * level

    def to_dict(self):
        return {"name": self.name, "level": self.level, "max_hp": self.max_hp, "hp": self.hp, "damage": self.damage}

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        enemy = cls(data["name"], data["level"], data.get("max_hp"))
        enemy.hp = data.get("hp", enemy.max_hp)
        enemy.damage = data.get("damage", enemy.damage)
        return enemy


class Player:
    def __init__(self, data=None):
        if data:
            self.id = data.get("id", str(uuid.uuid4()))
            self.hp = data.get("hp", 100)
            self.max_hp = data.get("max_hp", 100)
            self.level = data.get("level", 1)
            self.xp = data.get("xp", 0)
            self.next_level_xp = data.get("next_level_xp", 100)
            self.gold = data.get("gold", 50)
            self.damage = data.get("damage", 20)
            self.potions = data.get("potions", 3)
            self.location = data.get("location", "town")
            self.in_combat = data.get("in_combat", False)
            self.current_enemy = Enemy.from_dict(data.get("current_enemy"))
            self.weapon_level = data.get("weapon_level", 1)
            self.game_won = data.get("game_won", False)
            self.logs = data.get("logs", ["🛡️ ברוכים הבאים. האגדה של 'יער הזהב' חוזרת לחיים."])
        else:
            self.id = str(uuid.uuid4())
            self.hp = 100
            self.max_hp = 100
            self.level = 1
            self.xp = 0
            self.next_level_xp = 100
            self.gold = 50
            self.damage = 20
            self.potions = 3
            self.location = "town"
            self.in_combat = False
            self.current_enemy = None
            self.game_won = False
            self.weapon_level = 1
            self.logs = ["🛡️ אגדת יער הזהב המקורית חוזרת... התחמש והכן עצמך!"]

    def to_dict(self):
        return {
            "id": self.id, "hp": self.hp, "max_hp": self.max_hp, "level": self.level,
            "xp": self.xp, "next_level_xp": self.next_level_xp, "gold": self.gold,
            "damage": self.damage, "potions": self.potions, "location": self.location,
            "in_combat": self.in_combat, "weapon_level": self.weapon_level,
            "game_won": self.game_won, "logs": self.logs,
            "current_enemy": self.current_enemy.to_dict() if self.current_enemy else None
        }

    def add_log(self, text):
        self.logs.insert(0, text)
        if len(self.logs) > 6:
            self.logs.pop()

    def heal(self):
        if self.potions > 0:
            if self.hp >= self.max_hp:
                return self.add_log("אין צורך, החיים שלך מלאים לחלוטין!")
            heal_amount = 40 + (self.level * 10)
            self.hp = min(self.max_hp, self.hp + heal_amount)
            self.potions -= 1
            self.add_log(f"קיבלת {heal_amount} חיים משיקוי! (נותרו: {self.potions} 🧪)")
        else:
            self.add_log("אין לך שיקויים... חזור לחנות!")

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.next_level_xp:
            self.level += 1
            self.xp -= self.next_level_xp
            self.next_level_xp = int(self.next_level_xp * 1.5)
            self.max_hp += 20
            self.hp = self.max_hp
            self.damage += 8
            self.add_log(f"⭐ השתדרגת! רמה חדשה ({self.level}). החיים והכוח שוקמו.")
        else:
            self.add_log(f"+ צברת {amount} ניסיון.")


def load_player():
    data = session.get('rpg_legend_v3')
    return Player(data) if data else None


def save_player(player):
    session.permanent = True
    session['rpg_legend_v3'] = player.to_dict()


# ====================== ROUTES ======================
@app.route('/')
def home():
    p = load_player()
    if not p:
        p = Player()
        save_player(p)

    # הגדרת רקע ואייקון
    if p.game_won:
        bg_color = "rgba(255, 215, 0, 0.2)"
        icon = "👑"
        loc_name = "יער הזהב חופשי (משחק נגמר!)"
    elif p.in_combat and p.current_enemy:
        bg_color = "rgba(54, 22, 22, 0.5)"
        if "בוס עליון" in p.current_enemy.name:
            icon = "👺"
            bg_color = "rgba(100, 0, 0, 0.8)"
        else:
            icon = "🐕" if "כלב" in p.current_enemy.name else "🐻" if "דוב" in p.current_enemy.name else "🐅" if "נמר" in p.current_enemy.name else "🦁" if "אריה" in p.current_enemy.name else "🐘" if "פיל" in p.current_enemy.name else "👿"
        loc_name = f"{p.current_enemy.name} - רמה {p.current_enemy.level}"
    elif p.location == "forest":
        bg_color = "rgba(22, 53, 32, 0.5)"
        icon = "🍂🌳"
        loc_name = "אמצע היער של קדם"
    elif p.location == "cave":
        bg_color = "rgba(23, 15, 46, 0.5)"
        icon = "🌫️⛰️"
        loc_name = "מערת אופל הצללים"
    else:
        bg_color = "rgba(61, 45, 11, 0.4)"
        icon = "🏰"
        loc_name = "העיר המרכזית"

    return game_template.render(p=p, bg_color=bg_color, emoji_icon=icon, location_name=loc_name)


@app.route('/restart')
def restart():
    session.pop('rpg_legend_v3', None)
    return redirect('/game2/')


@app.route('/travel/<destination>')
def travel(destination):
    p = load_player()
    if not p or p.hp <= 0 or p.in_combat or p.game_won:
        return redirect('/game2/')

    if destination in {"town", "forest", "cave"}:
        if destination == "cave" and p.level < 4:
            p.add_log("שומר המערה: חזור! נדרשת רמה 4+ ⛔")
        else:
            p.location = destination
            p.add_log(f"הגעת אל {destination}.")
    save_player(p)
    return redirect('/game2/')


@app.route('/shop/<action>')
def shop(action):
    p = load_player()
    if not p or p.location != "town" or p.game_won:
        return redirect('/game2/')

    if action == "buy_potion":
        if p.gold >= 30:
            p.gold -= 30
            p.potions += 1
            p.add_log("רכשת שיקוי חיים 🧪")
        else:
            p.add_log("חסר לך זהב (30ג)")
    elif action == "upgrade_weapon":
        cost = p.weapon_level * 60
        if p.gold >= cost:
            p.gold -= cost
            p.damage += 15
            p.weapon_level += 1
            p.add_log(f"שודרג הכוח! כוח התקפה: {p.damage}")
        else:
            p.add_log(f"חסר זהב (עולה {cost}ג)")
    save_player(p)
    return redirect('/game2/')


@app.route('/action/<act>')
def perform_action(act):
    p = load_player()
    if not p or p.hp <= 0 or p.game_won:
        return redirect('/game2/')

    if act == "explore" and not p.in_combat:
        if random.random() > 0.60:
            p.add_log("הלכת בזהירות... הכל שקט.")
        else:
            start_combat(p)
    elif act == "boss" and p.location == "cave" and p.level >= 10 and not p.in_combat:
        p.current_enemy = Enemy("שד הזהב העתיק (בוס עליון)", 15, hp=800)
        p.current_enemy.damage = 60
        p.current_enemy.xp_reward = 10000
        p.current_enemy.gold_reward = 5000
        p.in_combat = True
        p.add_log("⚡ שד הזהב העתיק התעורר! ⚡")
    elif act == "attack" and p.in_combat:
        handle_combat_round(p)
    elif act == "heal":
        if p.potions > 0:
            p.heal()
        if p.in_combat:
            enemy_turn(p)
    elif act == "flee" and p.in_combat:
        loss = int(p.gold * 0.20)
        p.gold -= loss
        p.in_combat = False
        p.current_enemy = None
        p.location = "town"
        p.add_log(f"ברחת! איבדת {-loss} זהב.")
    elif act == "inn" and p.location == "town":
        if p.gold >= 20:
            p.gold -= 20
            p.hp = p.max_hp
            p.add_log("שינה בפונדק - חיים מלאים! 💤")
        else:
            p.add_log("חסר 20ג לפונדק.")

    save_player(p)
    return redirect('/game2/')


def start_combat(p):
    forest = [("כלב טועה נושך", 1), ("דוב היער האכזרי", 2), ("נמר מסוות", 3)]
    cave = [("אריה הרים מטורף", 4), ("פיל מוזהב", 6), ("שד מערות אכזרי", 8)]
    animals = forest if p.location == "forest" else cave
    choice = random.choice(animals)
    if choice[1] >= 6 and p.level < 5:
        choice = ("עטלף קרנבל ענקי", 5)
    p.current_enemy = Enemy(choice[0], choice[1])
    p.in_combat = True
    p.add_log(f"⚠️ {p.current_enemy.name} תוקף אותך!")


def handle_combat_round(p):
    e = p.current_enemy
    if random.random() > 0.90:
        p.add_log(f"{e.name} התחמק מהמכה!")
    else:
        is_crit = random.random() > 0.70
        dmg = int(p.damage * 1.5) if is_crit else p.damage
        e.hp -= dmg
        p.add_log(f"{'מכה קריטית! ' if is_crit else ''}גרמת {dmg} נזק.")

    if e.hp <= 0:
        if "בוס עליון" in e.name:
            p.game_won = True
            p.gold += 5000
            p.add_log("👑 ניצחת את שד הזהב! אתה השליט החדש! 👑")
        else:
            p.gold += e.gold_reward
            p.add_log(f"ניצחת את {e.name}! +{e.gold_reward} זהב.")
            p.gain_xp(e.xp_reward)
        p.in_combat = False
        p.current_enemy = None
    else:
        enemy_turn(p)


def enemy_turn(p):
    if random.random() > 0.85:
        p.add_log("התחמקת יפה מהתקפה!")
    else:
        dmg = max(1, p.current_enemy.damage - p.level * 2 + random.randint(-2, 3))
        p.hp -= dmg
        p.add_log(f"נפגעת! איבדת {dmg} חיים.")
    if p.hp <= 0:
        p.hp = 0
        p.in_combat = False
        p.add_log("☠️ מסעך הסתיים...")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
