import random
import uuid
import os
from flask import Flask, render_template_string, request, jsonify, session

# הגדרת הקבוצות ונתוני הבסיס
class txt11:
    FIRST_NAMES = ["דניאל", "יוסי", "רועי", "עומר", "ברק", "עידן", "משה", "תומר", "גיא", "אור", "שון", "אביב", "יהונתן", "איתי", "נועם"]
    LAST_NAMES = ["כהן", "לוי", "מזרחי", "פרץ", "ביטון", "דוד", "אברהם", "חזן", "גולן", "אוחיון", "אשכנזי", "שפירא", "ברקוביץ'"]
    LEAGUES_DB = {
        "ENG": [
            {"name": "מנצ'סטר סיטי", "primary": "#6CABDD", "secondary": "#1C2C5B"},
            {"name": "ארסנל", "primary": "#EF0107", "secondary": "#063672"},
            {"name": "ליברפול", "primary": "#C8102E", "secondary": "#00B2A9"},
            {"name": "מנצ'סטר יונייטד", "primary": "#DA291C", "secondary": "#FBE122"},
            {"name": "צ'לסי", "primary": "#034694", "secondary": "#DBA111"}
        ],
        "ESP": [
            {"name": "ריאל מדריד", "primary": "#FFFFFF", "secondary": "#FEBE10"},
            {"name": "ברצלונה", "primary": "#004D98", "secondary": "#A50044"},
            {"name": "אתלטיקו מדריד", "primary": "#CB3524", "secondary": "#272E61"}
        ],
        "IL": [
            {"name": "מכבי תל אביב", "primary": "#ecc918", "secondary": "#051381"},
            {"name": "מכבי חיפה", "primary": "#008000", "secondary": "#ffffff"},
            {"name": "הפועל באר שבע", "primary": "#ff0000", "secondary": "#ffffff"},
            {"name": "בית״ר ירושלים", "primary": "#ffff00", "secondary": "#000000"}
        ],
        "GER": [
            {"name": "באיירן מינכן", "primary": "#DC052D", "secondary": "#FFFFFF"},
            {"name": "דורטמונד", "primary": "#FDE100", "secondary": "#000000"},
            {"name": "באייר לברקוזן", "primary": "#E32221", "secondary": "#000000"}
        ]
    }
    TEXTS = {
        "title": "FC MANAGER 24", "sub_title": "בחר את המועדון שלך ובנה קבוצת חלומות",
        "budget": "תקציב: ₪",
        "tabs": {"squad": "סגל (SQUAD)", "market": "העברות (TRANSFERS)", "table": "טבלה (STANDINGS)", "calendar": "עונה (SEASON)"},
        "squad_pitch_title": "הרכב פותח (STARTING XI)", "squad_bench_title": "מחליפים (SUBSTITUTES)",
        "market_desc": "השוק מתעדכן לאחר כל משחק ליגה.",
        "training_title": "פיתוח שחקנים", "training_desc": "שלח 3 שחקנים אקראיים לאימון אינטנסיבי בעלות של ₪15,000.",
        "btn_train": "התחל אימון (₪15K)", "btn_play_match": "שחק משחק", "btn_reboot": "מחק שמירה"
    }

app = Flask(__name__)
app.secret_key = "ea_fc_24_manager_pro_key"
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7

FORMATIONS = ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CAM", "LW", "ST", "RW"]

class Player:
    def __init__(self, pos=None):
        self.id = str(uuid.uuid4())
        self.name = f"{random.choice(txt11.FIRST_NAMES)} {random.choice(txt11.LAST_NAMES)}"
        self.natural_pos = pos if pos else random.choice(list(set(FORMATIONS)))
        self.age = random.randint(17, 34)
        
        if self.age < 21: base = random.randint(60, 76)
        elif self.age > 30: base = random.randint(72, 86)
        else: base = random.randint(65, 89)
        
        self.ovr = base
        self.pac = min(99, max(30, base + random.randint(-15, 12)))
        self.sho = min(99, max(20, base + random.randint(-20, 15)))
        self.pas = min(99, max(40, base + random.randint(-10, 12)))
        self.dri = min(99, max(40, base + random.randint(-10, 15)))
        self.dfn = min(99, max(20, base + random.randint(-20, 15)))
        self.phy = min(99, max(40, base + random.randint(-15, 15)))
        
        if self.natural_pos == "GK":
            self.pac = random.randint(30, 55); self.sho = random.randint(20, 40)
            self.dfn = min(99, self.dfn + 15)
        elif self.natural_pos in ["CB", "LB", "RB"]:
            self.dfn = min(99, self.dfn + 15); self.sho = max(20, self.sho - 15)
        elif self.natural_pos in ["ST", "LW", "RW"]:
            self.sho = min(99, self.sho + 15); self.pac = min(99, self.pac + 10); self.dfn = max(20, self.dfn - 20)
            
        self.calculate_value()
        self.injured_weeks = 0; self.red_card_weeks = 0; self.goals = 0

    def calculate_value(self):
        base_val = 1500 * (1.18 ** max(0, self.ovr - 60))
        if self.age < 22: base_val *= 1.3
        elif self.age > 30: base_val *= 0.7
        self.value = int(base_val) + random.randint(500, 2000)
        if self.value < 2000: self.value = 2000

    def tick_status(self):
        if self.injured_weeks > 0: self.injured_weeks -= 1
        if self.red_card_weeks > 0: self.red_card_weeks -= 1

    def train(self):
        if self.ovr >= 99: return False
        growth = 2 if self.age < 23 else 1
        if self.age > 30 and random.random() < 0.5: growth = 0 
        
        if growth > 0:
            self.ovr += growth
            self.pac = min(99, self.pac + growth)
            self.sho = min(99, self.sho + growth)
            self.calculate_value()
            return True
        return False

    def to_dict(self): return self.__dict__

class Team:
    def __init__(self, t_info, league_id):
        self.id = str(uuid.uuid4())
        self.name = t_info["name"]
        self.primary = t_info["primary"]
        self.secondary = t_info["secondary"]
        self.league_id = league_id
        self.is_ai = True
        
        self.points = 0; self.games_played = 0; self.wins = 0; self.draws = 0; self.losses = 0
        self.goals_for = 0; self.goals_against = 0
        self.budget = 150000 
        self.starting_11 = [Player(pos) for pos in FORMATIONS]
        self.bench = [Player() for _ in range(7)]

    def get_power(self, is_human=False):
        power = 0
        for i, p in enumerate(self.starting_11):
            multiplier = 1.0
            if p.injured_weeks > 0 or p.red_card_weeks > 0: multiplier = 0.2  
            elif is_human:
                expected_pos = FORMATIONS[i]
                if p.natural_pos != expected_pos:
                    if p.natural_pos in ["ST", "LW", "RW"] and expected_pos in ["ST", "LW", "RW"]: multiplier = 0.9 
                    elif p.natural_pos in ["CB", "LB", "RB"] and expected_pos in ["CB", "LB", "RB"]: multiplier = 0.9
                    else: multiplier = 0.7 
            power += (p.ovr * multiplier)
        return int(power / 11)

class League:
    def __init__(self):
        self.teams = []
        for l_id, teams in txt11.LEAGUES_DB.items():
            for t in teams: self.teams.append(Team(t, l_id))
                
        self.my_team_id = None; self.my_league_id = None; self.week = 1
        self.market = sorted([Player() for _ in range(12)], key=lambda x: x.ovr, reverse=True)

    def set_player_team(self, tid):
        self.my_team_id = tid
        my_team = next((t for t in self.teams if t.id == tid), None)
        self.my_league_id = my_team.league_id
        for t in self.teams: t.is_ai = (t.id != tid)

    def play_week(self):
        league_teams = [t for t in self.teams if t.league_id == self.my_league_id]
        random.shuffle(league_teams)
        matches = []
        
        for i in range(0, len(league_teams), 2):
            if i+1 < len(league_teams):
                matches.append(self.simulate_match(league_teams[i], league_teams[i+1]))
        
        self.week += 1
        self.market = self.market[:4] + [Player() for _ in range(8)]
        self.market.sort(key=lambda x: x.ovr, reverse=True)
        
        my_team = next(t for t in self.teams if t.id == self.my_team_id)
        for p in my_team.starting_11 + my_team.bench: p.tick_status()
            
        return matches

    def generate_scorers(self, team, goals):
        scorers = []
        attackers = [p for p in team.starting_11 if p.natural_pos in ["ST", "LW", "RW", "CAM"]]
        others = [p for p in team.starting_11 if p not in attackers and p.natural_pos != "GK"]
        for _ in range(goals):
            pool = attackers * 3 + others 
            if not pool: pool = team.starting_11
            scorer = random.choice(pool)
            scorer.goals += 1
            scorers.append(scorer.name)
        return scorers

    def simulate_match(self, t1, t2):
        p1_pow = t1.get_power(t1.id == self.my_team_id)
        p2_pow = t2.get_power(t2.id == self.my_team_id)
        
        raw_1 = max(0, ((p1_pow * random.uniform(0.9, 1.3)) - (p2_pow * 0.9)) / 14)
        raw_2 = max(0, ((p2_pow * random.uniform(0.8, 1.2)) - (p1_pow * 0.95)) / 14)
        
        s1 = int(round(raw_1) + (1 if random.random() > 0.8 else 0))
        s2 = int(round(raw_2) + (1 if random.random() > 0.85 else 0))
        
        t1.games_played += 1; t2.games_played += 1
        t1.goals_for += s1; t1.goals_against += s2
        t2.goals_for += s2; t2.goals_against += s1
        
        if s1 > s2: t1.points += 3; t1.wins += 1; t2.losses += 1
        elif s2 > s1: t2.points += 3; t2.wins += 1; t1.losses += 1
        else: t1.points += 1; t2.points += 1; t1.draws += 1; t2.draws += 1
        
        scorers_t1 = self.generate_scorers(t1, s1)
        scorers_t2 = self.generate_scorers(t2, s2)

        events = []
        is_mine = (t1.id == self.my_team_id or t2.id == self.my_team_id)
        
        if is_mine:
            my_team = t1 if t1.id == self.my_team_id else t2
            
            # --- מערכת מענקים כלכליים למשחקים ---
            earned = 0
            if my_team.id == t1.id and s1 > s2: earned = random.randint(20000,30000)       # ניצחון
            elif my_team.id == t2.id and s2 > s1: earned = random.randint(20000,30000)     # ניצחון
            elif s1 == s2: earned = random.randint(9000,11000)                            # תיקו
            else: earned = random.randint(4000,6000)                                      # הפסד (זכויות שידור)
            
            my_team.budget += earned
            events.append(f"💰 הכנסות מהמשחק: ₪{earned:,}")
            # -----------------------------------

            if random.random() < 0.10:
                available = [p for p in my_team.starting_11 if p.injured_weeks == 0]
                if available:
                    victim = random.choice(available)
                    victim.injured_weeks = random.randint(1, 3)
                    events.append(f"🚑 {victim.name} נפצע וייעדר {victim.injured_weeks} שבועות!")
            if random.random() < 0.05:
                available = [p for p in my_team.starting_11 if p.red_card_weeks == 0]
                if available:
                    victim = random.choice(available)
                    victim.red_card_weeks = 1
                    events.append(f"🟥 {victim.name} ספג כרטיס אדום ומושעה מהמשחק הבא!")

        return {
            "t1": t1.name, "s1": s1, "sc1": scorers_t1,
            "t2": t2.name, "s2": s2, "sc2": scorers_t2,
            "is_mine": is_mine, "events": events
        }

LEAGUES_DB_STORAGE = {}

def get_game():
    uid = session.get('manager_fifa_11_key')
    if not uid or uid not in LEAGUES_DB_STORAGE:
        uid = str(uuid.uuid4())
        session.permanent = True
        session['manager_fifa_11_key'] = uid
        LEAGUES_DB_STORAGE[uid] = League()
    return LEAGUES_DB_STORAGE[uid]

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE, texts=txt11.TEXTS)

@app.route('/api/data', methods=['GET'])
def get_data():
    g = get_game()
    if not g.my_team_id:
        teams_lite = [{"id": t.id, "name": t.name, "c1": t.primary, "c2": t.secondary, "lg": t.league_id} for t in g.teams]
        return jsonify({"needs_setup": True, "teams_available": teams_lite})

    my_team = next(t for t in g.teams if t.id == g.my_team_id)
    league_teams = [t for t in g.teams if t.league_id == g.my_league_id]
    table = sorted(league_teams, key=lambda t: (t.points, t.goals_for - t.goals_against, t.goals_for), reverse=True)

    return jsonify({
        "needs_setup": False,
        "my_team": { 
            "name": my_team.name, "budget": my_team.budget, 
            "starting_11": [p.to_dict() for p in my_team.starting_11],
            "bench": [p.to_dict() for p in my_team.bench],
            "col": my_team.primary, "power": my_team.get_power(True)
        },
        "table": [{"pos": i+1, "name": t.name, "pts": t.points, "p": t.games_played, "w":t.wins, "d":t.draws, "l":t.losses, "gd": t.goals_for - t.goals_against} for i, t in enumerate(table)],
        "market": [p.to_dict() for p in g.market], "week": g.week
    })

@app.route('/api/pick_team', methods=['POST'])
def pick_team():
    get_game().set_player_team(request.json.get('team_id'))
    return jsonify({"status": "success"})

@app.route('/api/play', methods=['POST'])
def play_week(): return jsonify(get_game().play_week())

@app.route('/api/swap', methods=['POST'])
def swap_players():
    g = get_game()
    idx1, idx2 = request.json.get('idx1'), request.json.get('idx2')
    loc1, loc2 = request.json.get('loc1'), request.json.get('loc2')
    my_team = next(t for t in g.teams if t.id == g.my_team_id)
    list1 = my_team.starting_11 if loc1 == 'pitch' else my_team.bench
    list2 = my_team.starting_11 if loc2 == 'pitch' else my_team.bench
    try:
        list1[int(idx1)], list2[int(idx2)] = list2[int(idx2)], list1[int(idx1)]
        return jsonify({"status": "ok"})
    except: return jsonify({"err": "שגיאה בביצוע החילוף."})

@app.route('/api/auto_lineup', methods=['POST'])
def auto_lineup():
    g = get_game()
    my_team = next((t for t in g.teams if t.id == g.my_team_id), None)
    if not my_team: return jsonify({"err": "קבוצה לא נמצאה"})
    pool = my_team.starting_11 + my_team.bench
    pool.sort(key=lambda x: x.ovr, reverse=True)
    new_11 = []
    target_formation = ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CAM", "LW", "ST", "RW"]
    for pos in target_formation:
        match = next((p for p in pool if p.natural_pos == pos), None)
        if match:
            new_11.append(match); pool.remove(match)
        else: new_11.append(pool.pop(0))
    my_team.starting_11 = new_11; my_team.bench = pool
    return jsonify({"msg": "ההרכב סודר אוטומטית בצורה הטובה ביותר! 🪄", "type": "success"})

@app.route('/api/train', methods=['POST'])
def train_team():
    my_team = next(t for t in get_game().teams if t.id == get_game().my_team_id)
    cost = 15000
    if my_team.budget >= cost:
        my_team.budget -= cost
        pool = [p for p in my_team.starting_11 + my_team.bench if p.ovr < 99]
        if not pool: return jsonify({"err": "כל השחקנים הגיעו למקסימום פוטנציאל!"})
        trainees = random.sample(pool, min(3, len(pool)))
        success_names = [p.name for p in trainees if p.train()]
        if success_names: return jsonify({"msg": f"אימון עבר בהצלחה! השתפרו: {', '.join(success_names)}", "type": "success"})
        else: return jsonify({"msg": "האימון הסתיים, אך לא נרשם שיפור משמעותי.", "type": "warning"})
    return jsonify({"err": "אין מספיק תקציב לאימון."})

@app.route('/api/transfer', methods=['POST'])
def transfer():
    g = get_game()
    action, pid = request.json.get('action'), request.json.get('player_id')
    my_team = next(t for t in g.teams if t.id == g.my_team_id)
    
    if action == 'buy':
        target = next((p for p in g.market if p.id == pid), None)
        if target:
            if my_team.budget >= target.value:
                if len(my_team.bench) >= 15: return jsonify({"err": "הספסל מלא! מכור שחקנים קודם."})
                my_team.budget -= target.value
                my_team.bench.append(target)
                g.market.remove(target)
                return jsonify({"msg": f"החתמת את {target.name}!", "type": "success"})
            return jsonify({"err": "אין מספיק תקציב."})
        return jsonify({"err": "השחקן כבר לא זמין בשוק."})

    if action == 'sell':
        target = next((p for p in my_team.bench if p.id == pid), None)
        if target:
            sell_price = int(target.value * 0.8)
            my_team.budget += sell_price
            my_team.bench.remove(target)
            return jsonify({"msg": f"מכרת את {target.name} תמורת ₪{sell_price:,}.", "type": "info"})
        return jsonify({"err": "ניתן למכור רק שחקנים הנמצאים בספסל."})
    return jsonify({"err": "פעולה לא חוקית."})

@app.route('/api/restart')
def force_restart():
    session.clear()
    return jsonify({"ok":True})


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ texts.title }}</title>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;800&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
<style>
/* EA FC 24 Color Palette */
:root { 
    --bg-main: #090e14; 
    --bg-panel: rgba(18, 24, 33, 0.8); 
    --fc-volt: #d2ff00; 
    --fc-cyan: #00ffcc; 
    --white: #ffffff;
    --text-muted: #8b9bb4;
    --red: #ff3366;
    --pitch-bg: radial-gradient(circle at center, #14202c 0%, #090e14 100%);
    --card-gold: linear-gradient(135deg, #fceca1 0%, #d4af37 50%, #8a6a1c 100%);
}
body { 
    margin: 0; background-color: var(--bg-main); 
    background-image: radial-gradient(circle at 15% 50%, rgba(210, 255, 0, 0.03) 0%, transparent 50%),
                      radial-gradient(circle at 85% 30%, rgba(0, 255, 204, 0.03) 0%, transparent 50%);
    color: var(--white); font-family: 'Assistant', sans-serif; padding-bottom: 90px; overflow-x: hidden;
}
* { box-sizing: border-box; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-main); }
::-webkit-scrollbar-thumb { background: var(--fc-volt); border-radius: 10px; }

/* Global Loader */
#global-loader {
    position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); z-index: 99999;
    display: none; justify-content: center; align-items: center; cursor: wait;
}
.spinner { width: 60px; height: 60px; border: 4px solid rgba(210, 255, 0, 0.2); border-top-color: var(--fc-volt); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Header */
.header-bar { 
    position: sticky; top:0; z-index:100; background: rgba(9, 14, 20, 0.85); padding: 15px 25px; 
    display: flex; justify-content: space-between; align-items:center; backdrop-filter:blur(15px); -webkit-backdrop-filter: blur(15px);
    border-bottom: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 30px rgba(0,0,0,0.8);
}
.team-branding { display: flex; align-items: center; gap: 15px; }
.team-power { background: rgba(255,255,255,0.05); color: var(--fc-volt); padding: 5px 12px; border-radius: 6px; font-weight: bold; font-family: 'Oswald', sans-serif; font-size: 16px; border: 1px solid rgba(210,255,0,0.2); letter-spacing: 1px;}
.budget-pod { font-family: 'Oswald', sans-serif; font-size: 22px; color: var(--white); display: flex; align-items: center; gap: 8px;}
.budget-pod span { color: var(--fc-volt); }

/* Setup Screen */
#setup-screen { position: fixed; inset:0; background: var(--bg-main); background-image: radial-gradient(circle at top right, rgba(210,255,0,0.1), transparent 40%); padding: 60px 20px; z-index:500; text-align:center; overflow-y:auto;}
.grid-teams { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); max-width: 1100px; gap:25px; margin:40px auto; }
.team-option { 
    border-radius:0; padding:30px 20px; text-align:center; cursor:pointer; 
    border: 1px solid rgba(255,255,255,0.05); background: var(--bg-panel);
    backdrop-filter: blur(10px); transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative; overflow: hidden;
}
.team-option::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--c2, var(--fc-volt)); transition: width 0.3s ease;}
.team-option:hover::before { width: 100%; opacity: 0.1; }
.team-option:hover { transform: translateY(-8px); border-color: var(--fc-volt); box-shadow: 0 15px 40px rgba(0,0,0,0.6), 0 0 20px rgba(210, 255, 0, 0.15);}

/* Tabs Menu */
.tabs-tray { display: flex; max-width:1150px; margin: 30px auto 0; gap:2px; padding:0 20px; overflow-x: auto; scrollbar-width: none; border-bottom: 2px solid rgba(255,255,255,0.05);}
.tab-b { 
    flex:1; min-width: max-content; background: transparent; color: var(--text-muted); 
    border: none; padding:16px 20px; font-weight:800; font-size:14px; letter-spacing: 1px;
    cursor: pointer; transition:0.3s; position: relative; font-family: 'Oswald', sans-serif;
}
.tab-b:hover { color: var(--white); }
.tab-b.active { color:var(--fc-volt); }
.tab-b.active::after { content:''; position:absolute; bottom:-2px; left:0; width:100%; height:2px; background:var(--fc-volt); box-shadow: 0 -2px 10px var(--fc-volt);}

.content-box { display: none; background: transparent; max-width:1150px; margin: 0 auto; padding:30px 20px; min-height: 500px;}
.content-box.active { display:block; animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);}
@keyframes fadeUp { from{opacity:0; transform:translateY(20px);} to{opacity:1; transform:translateY(0);} }

/* EA FC 24 FUT CARD STYLE */
.fut-card {
    width: 120px; min-height: 185px; height: auto;
    position: relative; padding: 10px 8px; 
    font-family: 'Oswald', sans-serif; cursor: pointer; transition: all 0.2s;
    display: flex; flex-direction: column; justify-content: flex-start;
    user-select: none;
    background-size: cover; background-position: center;
    clip-path: polygon(15% 0, 100% 0, 100% 100%, 0 100%, 0 10%);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2);
}

.card-gold { background: var(--card-gold); color: #211900; }
.card-gold::after { content:''; position:absolute; inset:0; background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, transparent 50%, rgba(0,0,0,0.2) 100%); pointer-events: none;}
.card-silver { background: linear-gradient(135deg, #cbd5e1, #64748b); color: #0f172a; }
.card-bronze { background: linear-gradient(135deg, #cd7f32, #6b4423); color: #fff; }

.fut-card:hover { transform: translateY(-5px) scale(1.04); filter: brightness(1.1); }
.fut-card.selected { transform: scale(1.08) translateY(-5px); z-index: 20; filter: drop-shadow(0 0 15px var(--fc-volt)); outline: 2px solid var(--fc-volt);}

.fut-ovr { position: absolute; top: 8px; left: 10px; font-size: 26px; font-weight: 700; line-height: 1; z-index:2;}
.fut-pos { position: absolute; top: 32px; left: 10px; font-size: 11px; font-weight: 700; z-index:2;}
.fut-nat-pos { position: absolute; top: 8px; right: 8px; font-size: 10px; font-weight: bold; background: rgba(0,0,0,0.5); color: var(--white); border-radius: 2px; padding: 2px 4px; z-index:2;}
.fut-age { position: absolute; top: 30px; right: 8px; font-size: 9px; opacity: 0.8; z-index:2;}

.fut-pic { width: 50px; height: 50px; background: rgba(0,0,0,0.1); border-radius: 50%; margin: 18px auto 4px; display:flex; justify-content:center; align-items:flex-end; font-size:30px; overflow:hidden; z-index:2; position: relative;}

.fut-name { 
    text-align: center; font-size: 14px; font-weight: 800; 
    margin: 6px 0; padding-bottom: 4px; border-bottom: 1px solid rgba(0,0,0,0.15); 
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2; z-index:2; text-transform: uppercase;
}

.fut-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 8px; font-size: 11px; margin-bottom: 6px; text-align: center; font-weight: 600; z-index:2; font-family: 'Assistant', sans-serif;}
.fut-status { position: absolute; top:2px; right:40%; font-size:16px; background: rgba(0,0,0,0.8); border-radius:50%; width:24px; height:24px; display:flex; justify-content:center; align-items:center; z-index: 5;}

/* Pitch Layout - Tactical */
.pitch-container { 
    background: var(--pitch-bg); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; 
    position: relative; margin-bottom: 30px; padding: 30px 20px;
    min-height: 900px; display: grid; 
    grid-template-rows: 1fr 1fr 1fr 1fr;
    grid-template-areas: "att" "mid" "def" "gk";
    box-shadow: inset 0 0 100px rgba(0,0,0,0.8); row-gap: 15px;
    background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.pitch-container::before { content:''; position:absolute; top:50%; left:5%; width:90%; height:1px; background:rgba(255,255,255,0.1); }
.pitch-container::after { content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:150px; height:150px; border:1px solid rgba(255,255,255,0.1); border-radius:50%;}

.pitch-row { display: flex; justify-content: center; align-items: center; gap: 20px; width: 100%; z-index: 2;}
#r-att { grid-area: att; align-items: flex-end;}
#r-mid { grid-area: mid; }
#r-def { grid-area: def; align-items: flex-start;}
#r-gk { grid-area: gk; align-items: flex-end;}

.pitch-slot { display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 2;}
.slot-label {
    font-size: 11px; font-weight: 800; background: rgba(0,0,0,0.7); padding: 4px 12px; 
    border-radius: 4px; z-index: 10; font-family: 'Assistant', sans-serif; letter-spacing: 0.5px;
    text-align: center; border-bottom: 2px solid; backdrop-filter: blur(4px);
}

.bench-container { display: flex; gap: 15px; overflow-x: auto; padding: 20px; background: var(--bg-panel); border: 1px solid rgba(255,255,255,0.05); border-radius: 0; backdrop-filter: blur(10px);}

/* Buttons & Utils */
.market-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 20px;}
.act-btn { width:100%; padding:8px 4px; margin-top:auto; border:none; border-radius:0; font-weight:800; cursor:pointer; font-family:'Assistant'; transition: 0.2s; font-size: 13px; text-transform: uppercase; z-index: 10; position:relative;}
.act-btn:active { transform: scale(0.95); }
.buy-btn { background: var(--fc-volt); color:#000; } .buy-btn:hover{background:#b8e600;}
.sell-btn { background: transparent; color:var(--red); border: 1px solid var(--red);} .sell-btn:hover{background:var(--red); color:#fff;}

.auto-sort-btn { background: rgba(255,255,255,0.05); color: var(--white); padding: 8px 20px; border: 1px solid rgba(255,255,255,0.1); border-radius: 0; font-weight: 800; cursor: pointer; font-family: 'Oswald'; display: flex; align-items: center; gap: 8px; transition: 0.3s; letter-spacing: 1px;}
.auto-sort-btn:hover { background: var(--white); color: #000; border-color: var(--white);}

.tbl { width:100%; border-collapse:collapse; background: var(--bg-panel); border-radius:0; overflow:hidden;}
.tbl th { background: rgba(0,0,0,0.5); padding: 18px; text-align: center; color: var(--text-muted); font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;}
.tbl td { padding: 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.02); font-weight: 600;}
.tbl tr:hover { background: rgba(255,255,255,0.03); }
.tr-my { background: rgba(210, 255, 0, 0.05) !important; color:var(--fc-volt);}

.flt-wrap { position:fixed; bottom:0; left:0; width:100%; background:rgba(9, 14, 20, 0.9); backdrop-filter:blur(15px); -webkit-backdrop-filter: blur(15px); padding:20px; text-align:center; z-index:400; border-top: 1px solid rgba(255,255,255,0.05);}
.pl-wk { padding:15px 50px; background: var(--fc-volt); color:#000; font-size:20px; font-weight:800; border:none; cursor:pointer; transition: 0.3s; font-family:'Oswald'; letter-spacing: 1px; text-transform: uppercase; clip-path: polygon(5% 0, 100% 0, 95% 100%, 0 100%);}
.pl-wk:hover { transform: scale(1.05); background: var(--white); }
.pl-wk:disabled { background: #334155; color: #94a3b8; cursor: not-allowed; transform: none;}

/* Match Overlay */
#over { position:fixed; inset:0; background:rgba(0, 0, 0, 0.95); backdrop-filter: blur(10px); z-index:900; display:none; flex-direction:column; align-items:center; padding-top:60px; overflow-y:auto;}
.match-card { background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent); padding:25px; width:95%; max-width:700px; margin-bottom:20px; text-align:center; border-bottom:1px solid rgba(255,255,255,0.1);}
.match-score { font-size:48px; font-family:'Oswald'; font-weight:bold; color:var(--white); margin:10px 0; background: rgba(210, 255, 0, 0.1); padding: 5px 30px; border-radius: 4px; display:inline-block; border: 1px solid var(--fc-volt);}
.scorers { font-size: 14px; color: var(--text-muted); display: flex; justify-content: space-between; margin-top: 15px; font-family: 'Assistant';}
.scorers div { flex: 1; }
.match-events { font-size:15px; color:var(--fc-cyan); margin-top:20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); font-weight: bold;}

/* Toast Notifications */
#toast-container { position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; pointer-events: none;}
.toast { background: rgba(0,0,0,0.8); backdrop-filter: blur(5px); color: var(--white); padding: 15px 25px; border-radius: 0; border-right: 4px solid var(--fc-volt); font-weight: 600; animation: slideIn 0.3s ease forwards; min-width: 250px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);}
.toast.success { border-right-color: var(--fc-volt); color: var(--fc-volt); }
.toast.error { border-right-color: var(--red); color: var(--red); }
@keyframes slideIn { from{transform:translateX(100%); opacity:0;} to{transform:translateX(0); opacity:1;} }
@keyframes fadeOut { from{opacity:1;} to{opacity:0;} }
</style>
</head>
<body>

<div id="global-loader"><div class="spinner"></div></div>
<div id="toast-container"></div>

<div id="setup-screen">
    <h1 style="color:var(--white); font-size:60px; font-family:'Oswald'; letter-spacing:4px; margin-bottom: 5px; text-transform: uppercase;">{{ texts.title }}</h1>
    <div style="width: 100px; height: 4px; background: var(--fc-volt); margin: 0 auto 20px;"></div>
    <p style="font-size: 20px; color: var(--text-muted); font-weight: 600;">{{ texts.sub_title }}</p>
    <div id="sel-render" class="grid-teams"></div>
</div>

<div id="m-body" style="display:none;">
    <div class="header-bar">
        <div class="team-branding">
            <h2 id="dynN" style="margin:0; font-family:'Oswald'; font-size:26px; text-transform: uppercase; letter-spacing: 1px;"></h2>
            <div class="team-power" id="t-power" title="כוח קבוצה">OVR 0</div>
        </div>
        <div class="budget-pod"><span>₪</span> <span id="budget" style="color:var(--white);">0</span></div>
    </div>

    <div class="tabs-tray">
        <button class="tab-b active" onclick="goTab('vSqd', this)">{{ texts.tabs.squad }}</button>
        <button class="tab-b" onclick="goTab('vMkt', this)">{{ texts.tabs.market }}</button>
        <button class="tab-b" onclick="goTab('vTbl', this)">{{ texts.tabs.table }}</button>
        <button class="tab-b" onclick="goTab('vCal', this)">{{ texts.tabs.calendar }}</button>
    </div>

    <div class="content-box active" id="vSqd">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; flex-wrap: wrap; gap: 10px;">
            <div style="color:var(--white); font-weight:800; font-size:20px; font-family:'Oswald'; letter-spacing: 1px;">{{ texts.squad_pitch_title }}</div>
            <button class="auto-sort-btn" onclick="autoSortLineup()">🪄 AUTO BUILD</button>
        </div>
        
        <div class="pitch-container" id="pitch-ui">
            <div class="pitch-row" id="r-att"></div>
            <div class="pitch-row" id="r-mid"></div>
            <div class="pitch-row" id="r-def"></div>
            <div class="pitch-row" id="r-gk"></div>
        </div>

        <div style="color:var(--white); margin:30px 0 15px; font-weight:800; font-size:20px; font-family:'Oswald'; letter-spacing: 1px;">{{ texts.squad_bench_title }}</div>
        <div class="bench-container" id="bench-ui"></div>
    </div>
    
    <div class="content-box" id="vMkt">
        <p style="color:var(--text-muted); margin-bottom:25px; font-size: 16px;">{{ texts.market_desc }}</p>
        <div class="market-grid" id="r_mkt"></div>
    </div>
    
    <div class="content-box" id="vTbl">
        <table class="tbl">
             <thead><tr><th>#</th><th>מועדון</th><th>PTS</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GD</th></tr></thead>
             <tbody id="r_tbl"></tbody>
        </table>
    </div>

    <div class="content-box" id="vCal">
        <div style="background:var(--bg-panel); padding: 40px; text-align:center; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;">
            <h2 style="color:var(--white); font-family:'Oswald'; font-size:36px; margin:0 0 10px; text-transform:uppercase;">MATCHDAY <span id="wwW" style="color:var(--fc-volt);"></span></h2>
            <p style="color:var(--text-muted); font-size: 18px;">התכונן למשחק הליגה הבא שלך.</p>
        </div>
        
        <div style="background:var(--bg-panel); padding: 40px; border: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; align-items: center; text-align: center;">
            <h3 style="color:var(--fc-cyan); margin-top:0; font-family:'Oswald'; font-size:28px; letter-spacing: 1px;">TRAINING HUB ⚡</h3>
            <p style="color:var(--text-muted); font-size: 16px; max-width: 400px; margin-bottom: 25px;">{{ texts.training_desc }}</p>
            <button class="auto-sort-btn" style="background:var(--fc-cyan); color:#000; border:none; padding:12px 30px;" onclick="trainSquad()">{{ texts.btn_train }}</button>
        </div>
    </div>

    <div class="flt-wrap">
        <button class="pl-wk" onclick="pDay(this)" id="btn-play">{{ texts.btn_play_match }}</button>
        <div style="margin-top:15px; cursor:pointer; color:var(--text-muted); font-size:12px; letter-spacing:1px; text-transform:uppercase;" onclick="reZ()">{{ texts.btn_reboot }}</div>
    </div>
</div>

<div id="over">
    <h2 style="color:var(--white); font-family:'Oswald'; font-size:50px; margin-bottom: 40px; letter-spacing: 2px;">FULL TIME</h2>
    <div id="pOverList" style="width:100%; display:flex; flex-direction:column; align-items:center;"></div>
    <button class="pl-wk" onclick="gEl('over').style.display='none'; _runBld();" style="margin-top:40px; margin-bottom:80px; background:var(--white); color:#000;">ADVANCE</button>
</div>

<script>
let basePath = window.location.pathname;
if (!basePath.endsWith('/')) { basePath += '/'; }
basePath = basePath.replace(/\/+$/, '/');

const API = {
   data: basePath + "api/data", pick: basePath + "api/pick_team",
   play: basePath + "api/play", swap: basePath + "api/swap",
   transfer: basePath + "api/transfer", train: basePath + "api/train", 
   restart: basePath + "api/restart", auto_lineup: basePath + "api/auto_lineup"
};

function gEl(id){ return document.getElementById(id); }
function showLoader() { gEl('global-loader').style.display = 'flex'; }
function hideLoader() { gEl('global-loader').style.display = 'none'; }

function showToast(msg, type='info') {
    const container = gEl('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = msg;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function goTab(vid, btn) {
    document.querySelectorAll('.content-box').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.tab-b').forEach(x => x.classList.remove('active'));
    gEl(vid).classList.add('active'); btn.classList.add('active');
    window.scrollTo({top:0, behavior:'smooth'});
}

async function fireReq(epKey, payload={}, withLoad=true) {
    showLoader(); 
    let pms = {method: payload ? 'POST' : 'GET'};
    if(payload && Object.keys(payload).length>0){ 
        pms.body = JSON.stringify(payload); 
        pms.headers = {'Content-Type':'application/json'}; 
    }
    try {
        let rx = await fetch(API[epKey], pms); 
        if(!rx.ok) throw new Error("Server error");
        let rz = await rx.json();
        if(rz.err) showToast(rz.err, 'error'); 
        else if (rz.msg) showToast(rz.msg, rz.type || 'success');
        if(withLoad) await _runBld(); 
        hideLoader();
        return rz;
    } catch(e) {
        hideLoader();
        showToast("Network Error - Please try again.", "error");
    }
}

let selPlayer = null; 
function handlePlayerClick(idx, loc) {
    if(!selPlayer) {
        selPlayer = {idx, loc};
        _runBld(); 
    } else {
        if(selPlayer.idx === idx && selPlayer.loc === loc) {
            selPlayer = null; 
            _runBld();
        } else {
            fireReq('swap', {idx1: selPlayer.idx, loc1: selPlayer.loc, idx2: idx, loc2: loc});
            selPlayer = null;
        }
    }
}

async function autoSortLineup() {
    await fireReq('auto_lineup', {action: 'auto'});
}

function getCardClass(ovr) {
    if(ovr >= 80) return 'fut-card card-gold';
    if(ovr >= 70) return 'fut-card card-silver';
    return 'fut-card card-bronze';
}

function getStatusIcon(p) {
    if(p.red_card_weeks > 0) return `<div class="fut-status">🟥</div>`;
    if(p.injured_weeks > 0) return `<div class="fut-status">🚑</div>`;
    return '';
}

function RPlCard(p, mode, index=null) {
    let isSel = (selPlayer && selPlayer.idx === index && selPlayer.loc === mode);
    let selClass = isSel ? "selected" : "";
    let btn = "";
    
    if(mode === "market") {
        btn = `<button class="act-btn buy-btn" onclick="fireReq('transfer', {action:'buy', player_id:'${p.id}'}, true)">קנה ₪${p.value.toLocaleString()}</button>`;
    } else if(mode === "bench") {
        btn = `<button class="act-btn sell-btn" onclick="event.stopPropagation(); fireReq('transfer', {action:'sell', player_id:'${p.id}'}, true)">מכור ₪${Math.floor(p.value*0.8).toLocaleString()}</button>`;
    }
    
    let onClick = (mode === "pitch" || mode === "bench") ? `onclick="handlePlayerClick(${index}, '${mode}')"` : "";

    return `
    <div style="position:relative; display:flex; flex-direction:column; height:100%;">
        <div class="${getCardClass(p.ovr)} ${selClass}" ${onClick}>
            ${getStatusIcon(p)}
            <div class="fut-ovr">${p.ovr}</div>
            <div class="fut-nat-pos">${p.natural_pos}</div>
            <div class="fut-age">${p.age} YRS</div>

            <div class="fut-pic">👤</div>
            <div class="fut-name" title="${p.name}">${p.name}</div>
            <div class="fut-stats">
                <div>PAC ${p.pac}</div> <div>DRI ${p.dri}</div>
                <div>SHO ${p.sho}</div> <div>DEF ${p.dfn}</div>
                <div>PAS ${p.pas}</div> <div>PHY ${p.phy}</div>
            </div>
            ${btn}
        </div>
    </div>`;
}

async function BldUi(data) {
   gEl('dynN').innerHTML = `⚽ ${data.my_team.name}` ;
   gEl('t-power').innerText = `OVR ${data.my_team.power}`;
   
   const elBudget = gEl('budget');
   const currentB = parseInt(elBudget.innerText.replace(/,/g, '')) || 0;
   if(currentB !== data.my_team.budget) {
       elBudget.innerText = data.my_team.budget.toLocaleString();
       elBudget.style.color = 'var(--fc-volt)';
       setTimeout(()=> elBudget.style.color = 'var(--white)', 500);
   }

   gEl('wwW').innerText = data.week;
   gEl('btn-play').innerText = "PLAY MATCH " + data.week;
   
   const s11 = data.my_team.starting_11;
   
   const FORMATION = ["GK", "LB", "CB", "CB", "RB", "CM", "CM", "CAM", "LW", "ST", "RW"];
   const LABELS = { "GK": "GK", "LB": "LB", "CB": "CB", "RB": "RB", "CM": "CM", "CAM": "CAM", "LW": "LW", "ST": "ST", "RW": "RW" };

   let htmlAtt = "", htmlMid = "", htmlDef = "", htmlGk = "";
   
   s11.forEach((p, i) => {
       let expectedPos = FORMATION[i];
       let isMatch = p.natural_pos === expectedPos;
       let labelColor = isMatch ? "var(--fc-volt)" : "var(--red)";

       let slotHtml = `
       <div class="pitch-slot">
           <div class="slot-label" style="color: ${labelColor}; border-bottom-color: ${labelColor};">${LABELS[expectedPos]}</div>
           ${RPlCard(p, "pitch", i)}
       </div>`;

       if(i >= 8) htmlAtt += slotHtml;
       else if(i >= 5) htmlMid += slotHtml;
       else if(i >= 1) htmlDef += slotHtml;
       else htmlGk += slotHtml;
   });

   gEl('r-att').innerHTML = htmlAtt;
   gEl('r-mid').innerHTML = htmlMid;
   gEl('r-def').innerHTML = htmlDef;
   gEl('r-gk').innerHTML = htmlGk;
   
   gEl('bench-ui').innerHTML = data.my_team.bench.map((p, i) => RPlCard(p, "bench", i)).join('');
   gEl('r_mkt').innerHTML= data.market.map(p => RPlCard(p, "market")).join('');

   gEl('r_tbl').innerHTML= data.table.map((t, i) =>`
      <tr class="${t.name===data.my_team.name?'tr-my':''}">
          <td>${i+1}</td> 
          <td style="font-weight:bold; text-align:right;">${t.name}</td> 
          <td style="color:var(--white); font-weight:800; font-size:16px;">${t.pts}</td>
          <td>${t.p}</td> <td>${t.w}</td> <td>${t.d}</td> <td>${t.l}</td>
          <td dir="ltr" style="color:${t.gd>0?'var(--fc-volt)':t.gd<0?'var(--red)':''}">${t.gd>0?'+'+t.gd:t.gd}</td>
      </tr>`).join('');
}

async function _runBld() {
   try {
       let rx = await fetch(API.data); 
       if(!rx.ok) return;
       let js = await rx.json();
       if(js.needs_setup) {
           gEl('setup-screen').style.display = 'block';
           gEl('sel-render').innerHTML = js.teams_available.map(tc=>`
               <div class="team-option" style="--c2: ${tc.c2};" onclick="fireReq('pick',{team_id:'${tc.id}'})">
                  <div style="width:70px; height:70px; background:${tc.c1}; border:4px solid ${tc.c2}; border-radius:50%; margin:0 auto 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);"></div>
                  <div style="font-weight:800; font-size:24px; color:var(--white); font-family:'Oswald'; letter-spacing:1px; text-transform:uppercase;">${tc.name}</div>
               </div>
           `).join('');
       } else {
           gEl('setup-screen').style.display = 'none'; gEl('m-body').style.display = 'block'; await BldUi(js);
       }
   } catch(e) { console.error(e); }
}

async function pDay(btn) {
   btn.disabled = true;
   let originalText = btn.innerText;
   btn.innerText = "SIMULATING... ⚽";
   
   let ans = await fireReq('play', {}, false);
   if(ans && !ans.err) {
       gEl('pOverList').innerHTML = ans.map(m=>`
          <div class="match-card" style="${m.is_mine ? 'border-color:var(--fc-volt); background: rgba(210, 255, 0, 0.03);' : ''}">
              <div style="display:flex; justify-content:space-between; align-items:center; color:var(--white);">
                 <div style="flex:1; text-align:right; font-size:24px; font-weight:800; font-family:'Oswald'; text-transform:uppercase;">${m.t1}</div>
                 <div class="match-score">${m.s1} - ${m.s2}</div>
                 <div style="flex:1; text-align:left; font-size:24px; font-weight:800; font-family:'Oswald'; text-transform:uppercase;">${m.t2}</div>
              </div>
              <div class="scorers">
                 <div style="text-align:right;">${m.sc1.map(s => `⚽ ${s}`).join('<br>')}</div>
                 <div style="text-align:left;">${m.sc2.map(s => `⚽ ${s}`).join('<br>')}</div>
              </div>
              ${m.events && m.events.length > 0 ? '<div class="match-events">' + m.events.map(e => `<div>${e}</div>`).join('') + '</div>' : ''}
          </div>`
       ).join('');

       gEl('over').style.display = 'flex';
   }
   btn.disabled = false;
   btn.innerText = originalText;
}

function trainSquad() { fireReq('train'); }
function reZ(){ if(confirm('Are you sure you want to delete your save?')) fireReq('restart'); }

_runBld();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
