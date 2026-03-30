import random
from flask import Flask, render_template_string, redirect

app = Flask(__name__)
app.secret_key = "space_odyssey"

# משתני המשחק גלובליים (לפשטות בקוד הזה)
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.week = 1
        self.max_weeks = 20
        self.crew = 100        # בני אדם (אסור שיגיע ל-0)
        self.food = 100        # אוכל (יורד כל שבוע)
        self.energy = 100      # דלק/חשמל
        self.hull = 100        # חוזק הספינה (0 = פיצוץ)
        self.credits = 500     # כסף למסחר
        self.log = "החללית ג'נסיס יצאה לדרך. היעד: מאדים."
        self.game_over = False
        self.victory = False
        self.current_event = None
        self.generate_event()

    def consume_resources(self):
        # צריכה טבעית בכל שבוע
        food_consumption = int(self.crew * 0.2) # אנשים רעבים
        energy_consumption = 5
        
        self.food -= food_consumption
        self.energy -= energy_consumption
        
        # השפעות לוואי
        if self.food < 0:
            starved = abs(self.food)
            self.crew -= starved # אנשים מתים מרעב
            self.food = 0
            self.log += f" <br>☠️ המזון נגמר! {starved} אנשי צוות גוועו ברעב."
        
        if self.energy <= 0:
            self.energy = 0
            self.hull -= 10
            self.log += " <br>⚡ אין אנרגיה למגנים! נזק למעטפת הספינה."

    def check_status(self):
        if self.hull <= 0:
            self.game_over = True
            self.log = "💥 הספינה התפרקה בחלל. אין ניצולים."
        elif self.crew <= 0:
            self.game_over = True
            self.log = "👻 כל הצוות מת. הספינה ממשיכה כספינת רפאים."
        elif self.week > self.max_weeks:
            self.victory = True
            self.log = "🚀 הגעתם למאדים! המושבה ניצלה. כל הכבוד, קפטן."

    def generate_event(self):
        # בנק האירועים
        events = [
            {
                "title": "מטר מטאורים",
                "desc": "שדה אסטרואידים לפנינו. איך נגיב?",
                "choices": [
                    {"txt": "הפעל מגני אנרגיה (20- אנרגיה)", "effect": {"nrg": -20}},
                    {"txt": "ספוג את הפגיעה (15- נזק לגוף הספינה)", "effect": {"hull": -15}},
                ]
            },
            {
                "title": "סוחר חלל מפוקפק",
                "desc": "חללית קטנה מציעה עסקת חליפין.",
                "choices": [
                    {"txt": "קנה מזון ב-100 קרדיטים", "effect": {"cred": -100, "food": 30}},
                    {"txt": "מכור אנרגיה תמורת 100 קרדיטים", "effect": {"cred": 100, "nrg": -20}},
                    {"txt": "התעלם והמשך", "effect": {}}
                ]
            },
            {
                "title": "דליפה בכור הגרעיני",
                "desc": "רמת הקרינה עולה במדור הנדסה.",
                "choices": [
                    {"txt": "שלח צוות לתקן (סיכון לחיי אדם)", "effect": {"crew": -random.randint(2, 8), "hull": 5}},
                    {"txt": "אטום את האגף (איבוד קבוע של 10% אנרגיה)", "effect": {"nrg": -10, "hull": -5}}, # כאן הקוד פשוט מוריד חד פעמי
                ]
            },
            {
                "title": "מוטציה באוכל",
                "desc": "חלק מהאספקה במחסן קיבלה עובש סגול ומוזר.",
                "choices": [
                    {"txt": "זרוק את האוכל הנגוע (20- מזון)", "effect": {"food": -20}},
                    {"txt": "הצוות יאכל את זה בכל זאת (סיכון למחלה)", "effect": {"crew": -random.randint(0, 15)}},
                ]
            },
            {
                "title": "אות מצוקה",
                "desc": "נקלט אות מחללית תקועה.",
                "choices": [
                    {"txt": "שגר חילוץ (בזבוז אנרגיה, אולי נקבל קרדיט)", "effect": {"nrg": -15, "cred": 50}},
                    {"txt": "התעלם (המורל יירד, אך בטוח)", "effect": {}} # כאן אפשר להוסיף מכניקת מורל בעתיד
                ]
            },
            {
                "title": "שקט בחלל",
                "desc": "שבוע רגוע. הזדמנות לתחזוקה.",
                "choices": [
                    {"txt": "בצע תיקונים (100- קרדיט, +10 לגוף)", "effect": {"cred": -100, "hull": 10}},
                    {"txt": "תן לצוות לנוח (חוסך אוכל השבוע)", "effect": {"food": 10}}, 
                ]
            }
        ]
        self.current_event = random.choice(events)

state = GameState()

# --- CSS & HTML ---
# נוספה שורת "חזור לתפריט" בתחתית ה-body, ועדכנתי את הלינקים שיתחילו ב-/game3
STYLE = """
<style>
    body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; text-align: center; direction: rtl; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    h1 { color: #58a6ff; text-transform: uppercase; letter-spacing: 2px; }
    
    /* הסטטיסטיקות למעלה */
    .stats-bar { 
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; 
        background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d;
    }
    .stat-box { font-size: 14px; font-weight: bold; }
    .stat-val { display: block; font-size: 20px; margin-top: 5px; color: #fff; }
    .stat-crew { color: #ff7b72; } /* אדום */
    .stat-nrg { color: #d2a8ff; } /* סגול */
    .stat-food { color: #79c0ff; } /* כחול */
    .stat-hull { color: #7ee787; } /* ירוק */
    .stat-cred { color: #f2cc60; } /* צהוב */

    /* לוג אירועים */
    .log-box { 
        background: #0d1117; border: 1px solid #30363d; padding: 15px; 
        margin: 20px 0; min-height: 60px; color: #8b949e; border-radius: 8px;
        font-family: monospace; font-size: 14px;
    }

    /* קלף האירוע המרכזי */
    .event-card {
        background: #21262d; border: 2px solid #58a6ff; border-radius: 12px;
        padding: 20px; box-shadow: 0 0 15px rgba(88, 166, 255, 0.2);
        animation: fadeIn 0.5s;
    }
    .event-title { color: #ffffff; margin-top: 0; font-size: 22px; }
    .event-desc { font-size: 16px; margin-bottom: 20px; }

    /* כפתורים */
    .choices { display: flex; flex-direction: column; gap: 10px; }
    button {
        background: #238636; color: white; border: none; padding: 12px; 
        font-size: 16px; border-radius: 6px; cursor: pointer; transition: 0.2s;
        font-weight: bold; text-align: right;
    }
    button:hover { background: #2ea043; }
    
    .week-display { margin: 20px 0; font-size: 24px; color: #8b949e; letter-spacing: 5px; }
    
    /* מסכי סיום */
    .game-over { color: #ff7b72; border-color: #ff7b72; }
    .victory { color: #7ee787; border-color: #7ee787; }
    a.btn-reset { display:inline-block; margin-top:20px; color:#58a6ff; text-decoration:none; border:1px solid #58a6ff; padding:10px 20px; border-radius:5px;}

    @keyframes fadeIn { from { opacity:0; transform: translateY(10px); } to { opacity:1; transform: translateY(0); } }
    
    /* כפתור חזור */
    .back-btn { margin-top: 30px; display: inline-block; color: #58a6ff; font-size: 12px; text-decoration: none;}
    .back-btn:hover { text-decoration: underline; }
</style>
"""

# שימו לב לשימוש ב /game3/ לפני כל נתיב יחסי
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Genesis Tycoon</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """ + STYLE + """
</head>
<body>
    <div class="container">
        <h1>🚀 GENESIS 🌌</h1>
        
        <!-- סרגל משאבים -->
        <div class="stats-bar">
            <div class="stat-box stat-crew">👥 צוות<span class="stat-val">{{ s.crew }}</span></div>
            <div class="stat-box stat-nrg">⚡ אנרגיה<span class="stat-val">{{ s.energy }}</span></div>
            <div class="stat-box stat-food">🍔 מזון<span class="stat-val">{{ s.food }}</span></div>
            <div class="stat-box stat-hull">🛡️ מעטפת<span class="stat-val">{{ s.hull }}%</span></div>
            <div class="stat-box stat-cred">💰 קרדיט<span class="stat-val">{{ s.credits }}</span></div>
        </div>

        <div class="week-display">
            שבוע {{ s.week }} / {{ s.max_weeks }}
        </div>

        <!-- תיבת טקסט לתוצאות האחרונות -->
        <div class="log-box">
            {{ s.log | safe }}
        </div>

        <!-- אזור האירוע המרכזי -->
        {% if s.game_over %}
            <div class="event-card game-over">
                <h2 class="event-title">💀 המשחק נגמר</h2>
                <p>הספינה נכשלה במשימתה. האנושות איבדה תקווה.</p>
                <a href="/game3/reset" class="btn-reset">נסה שוב מההתחלה</a>
            </div>
        {% elif s.victory %}
            <div class="event-card victory">
                <h2 class="event-title">🎉 ניצחון!</h2>
                <p>הגעתם למאדים בשלום! הקולוניה הוקמה בהצלחה.</p>
                <p>צוות ששרד: {{ s.crew }} | מצב ספינה: {{ s.hull }}%</p>
                <a href="/game3/reset" class="btn-reset">שחק שוב</a>
            </div>
        {% else %}
            <div class="event-card">
                <h2 class="event-title">⚠️ {{ s.current_event.title }}</h2>
                <div class="event-desc">{{ s.current_event.desc }}</div>
                
                <div class="choices">
                    {% for choice in s.current_event.choices %}
                        <!-- חשוב: שימוש בנתיב המותאם -->
                        <a href="/game3/act/{{ loop.index0 }}">
                            <button>{{ choice.txt }}</button>
                        </a>
                    {% endfor %}
                </div>
            </div>
        {% endif %}
        
        <a href="/" class="back-btn">חזור לתפריט המשחקים</a>

    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE, s=state)

@app.route('/act/<int:choice_idx>')
def act(choice_idx):
    if state.game_over or state.victory:
        return redirect('/game3/')  # נתיב מעודכן

    # ביצוע הבחירה
    choice = state.current_event['choices'][choice_idx]
    effects = choice['effect']
    
    # חישוב השפעת הבחירה
    log_updates = []
    
    if 'cred' in effects: 
        state.credits += effects['cred']
    
    if 'nrg' in effects:
        state.energy += effects['nrg']
        log_updates.append(f"אנרגיה ({effects['nrg']})")
    
    if 'hull' in effects:
        state.hull += effects['hull']
        log_updates.append(f"גוף ספינה ({effects['hull']})")
        
    if 'food' in effects:
        state.food += effects['food']
        log_updates.append(f"מזון ({effects['food']})")
        
    if 'crew' in effects:
        state.crew += effects['crew']
        log_updates.append(f"צוות ({effects['crew']})")

    # עדכון הלוג (מה קרה הרגע)
    state.log = f"<b>החלטה:</b> {choice['txt']}"
    
    # צריכת משאבים של סוף שבוע + מעבר שבוע
    state.consume_resources()
    state.week += 1
    
    # בדיקת ניצחון/הפסד
    state.check_status()
    
    # אם המשחק ממשיך, ג'נרט אירוע חדש
    if not state.game_over and not state.victory:
        state.generate_event()

    return redirect('/game3/')  # נתיב מעודכן

@app.route('/reset')
def reset():
    state.reset()
    return redirect('/game3/')  # נתיב מעודכן

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
