from flask import Flask, render_template_string

app = Flask(__name__)

GAME_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SURVIVAL OS:3.0v</title>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0d0d0d;
            --card-bg: #15191f;
            --main-c: #00ffd5; 
            --bad-c: #ff3333;
            --warn-c: #ffaa00;
            --font-ui: 'Rubik', sans-serif;
            --font-code: 'Share Tech Mono', monospace;
        }

        body {
            background-color: var(--bg-color);
            color: white;
            font-family: var(--font-ui);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .os-container {
            width: 100%; max-width: 450px;
            background: var(--card-bg);
            border: 2px solid #333;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
            display: flex; flex-direction: column; gap: 10px;
            position: relative;
        }

        /* Top HUD */
        .header {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid #333; padding-bottom: 10px;
        }
        .day-info { font-family: var(--font-code); color: var(--main-c); font-size: 20px;}
        .weather { font-size: 14px; color: #aaa; }

        /* Stats Grid */
        .grid-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .bar-wrap { background: #000; height: 18px; border-radius: 4px; border: 1px solid #444; position: relative;}
        .bar { height: 100%; width: 50%; transition: 0.3s;}
        .val-text { position: absolute; right: 5px; top: 0; font-size: 12px; text-shadow: 1px 1px 1px black;}

        .bg-r { background: var(--bad-c); } /* HP */
        .bg-b { background: #00aaff; } /* WATER */
        .bg-o { background: var(--warn-c); } /* FOOD */
        .bg-g { background: #33ff33; } /* ENERGY */

        /* LOG Screen */
        .terminal {
            background: black;
            border: 1px solid #555;
            height: 140px;
            overflow-y: auto;
            padding: 10px;
            font-family: var(--font-code);
            font-size: 13px;
            color: #ccc;
        }
        .ln { margin-bottom: 4px; padding-bottom: 2px; border-bottom: 1px solid #222; }
        .bad { color: var(--bad-c); } .good { color: var(--main-c); } .sys { color: #aaa; }

        /* Gear & Inv */
        .gear-panel {
            background: #111; padding: 10px; border-radius: 6px; 
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;
            text-align: center;
        }
        .item-slot {
            background: #222; border: 1px solid #444; padding: 5px; border-radius: 4px; font-size: 11px;
            position: relative; cursor: pointer; transition: 0.2s;
        }
        .item-slot:hover { border-color: var(--main-c); }
        .item-count { font-weight: bold; font-size: 14px; display: block; color: var(--main-c);}

        /* Actions */
        .deck { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 5px;}
        .btn {
            background: #222; color: #eee; border: 1px solid #444;
            padding: 12px; border-radius: 6px; cursor: pointer; font-size: 14px;
            transition: 0.2s; font-weight: bold;
        }
        .btn:hover { background: #333; border-color: var(--main-c); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; border-color: #333; }

        .btn-big { grid-column: 1 / -1; background: #261600; border-color: #630;}
        .btn-big:hover { background: #3a2200; border-color: orange;}

        /* Goal Progress */
        .goal { font-size: 12px; text-align: center; color: #777; margin-top: 5px;}
        .goal span { color: white; }

        /* Modal */
        .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 10; display: none; align-items: center; justify-content: center; flex-direction: column; text-align: center;}
        .over-t { font-size: 50px; color: var(--bad-c); margin-bottom: 20px;}
        .over-btn { padding: 15px 40px; font-size: 20px; background: white; color: black; border: none; cursor: pointer;}
    </style>
</head>
<body>

    <!-- Game Over Screen -->
    <div id="scr-lose" class="overlay">
        <div class="over-t">GAME OVER</div>
        <p>לא שרדת את השממה.</p>
        <button class="over-btn" onclick="location.reload()">התחל מחדש</button>
    </div>

    <!-- Win Screen -->
    <div id="scr-win" class="overlay">
        <div class="over-t" style="color:var(--main-c)">נ י צ ח ו ן</div>
        <p>צוות החילוץ הגיע ביום ה-20.</p>
        <button class="over-btn" onclick="location.reload()">שחק שוב</button>
    </div>

    <div class="os-container">
        
        <div class="header">
            <div>
                <div class="day-info">יום <span id="val-day">1</span> <span style="font-size:14px; color:#555;">(20)</span></div>
            </div>
            <div class="weather" id="txt-weather">☀️ בהיר ונעים</div>
        </div>

        <div class="grid-stats">
            <div>
                <small>בריאות</small>
                <div class="bar-wrap"><div id="b-hp" class="bar bg-r"></div><span id="v-hp" class="val-text">100</span></div>
            </div>
            <div>
                <small>רעב</small>
                <div class="bar-wrap"><div id="b-fd" class="bar bg-o"></div><span id="v-fd" class="val-text">100</span></div>
            </div>
            <div>
                <small>מים</small>
                <div class="bar-wrap"><div id="b-wt" class="bar bg-b"></div><span id="v-wt" class="val-text">100</span></div>
            </div>
            <div>
                <small>אנרגיה</small>
                <div class="bar-wrap"><div id="b-en" class="bar bg-g"></div><span id="v-en" class="val-text">100</span></div>
            </div>
        </div>

        <div class="terminal" id="console">
            <div class="ln sys">>המשחק מתחיל!!!</div>
        </div>

        <!-- Inventory -->
        <div style="font-size:12px; color:#aaa; margin-bottom:-5px;">תיק (נפח: <span id="v-slots">10</span>)</div>
        <div class="gear-panel">
            <div class="item-slot" onclick="game.eat()">
                🥫 אוכל<br><span id="i-food" class="item-count">0</span>
            </div>
            <div class="item-slot" onclick="game.drink()">
                🥤 מים<br><span id="i-water" class="item-count">0</span>
            </div>
            <div class="item-slot" onclick="game.med()">
                💉 תרופה<br><span id="i-med" class="item-count">0</span>
            </div>
            <div class="item-slot">
                🧱 חומרים<br><span id="i-scrap" class="item-count">0</span>
            </div>
            <!-- ציוד קבוע -->
            <div class="item-slot" style="grid-column: span 2; border-color:#555;">
                🗡️ סכין: <span id="has-knife" style="color:var(--bad-c)">אין</span>
            </div>
            <div class="item-slot" style="grid-column: span 2; border-color:#555;">
                🎒 תרמיל: <span id="has-bag" style="color:var(--bad-c)">אין</span>
            </div>
        </div>
        
        <div class="deck">
            <button class="btn btn-big" id="btn-explore" onclick="game.explore()">🌍 יציאה לסיור (משאבים)</button>
            
            <button class="btn" onclick="game.craft('knife')">🛠️ צור סכין (10🧱)</button>
            <button class="btn" onclick="game.craft('bag')">🧵 תרמיל (20🧱)</button>
            
            <button class="btn" style="background:#001133; grid-column: 1 / -1" onclick="game.sleep()">💤 שינה (סיום יום)</button>
        </div>

    </div>

    <script>
        // Game Engine
        const game = {
            s: { hp:100, fd:100, wt:100, en:100 },
            inv: { food:3, water:3, med:1, scrap:0 },
            gear: { knife:false, bag:false },
            day: 1,
            max_inv: 10,
            weather: 'clear', // clear, rain, storm
            
            // Core
            update: function() {
                // UI Bars
                document.getElementById('b-hp').style.width = this.s.hp + "%";
                document.getElementById('v-hp').innerText = Math.floor(this.s.hp);
                
                document.getElementById('b-fd').style.width = this.s.fd + "%";
                document.getElementById('v-fd').innerText = Math.floor(this.s.fd);
                
                document.getElementById('b-wt').style.width = this.s.wt + "%";
                document.getElementById("v-wt").innerText = Math.floor(this.s.wt);

                document.getElementById('b-en').style.width = this.s.en + "%";
                document.getElementById('v-en').innerText = Math.floor(this.s.en);

                // Info
                document.getElementById('val-day').innerText = this.day;
                
                // Weather Text
                let wtx = "☀️ בהיר";
                if(this.weather == 'rain') wtx = "🌧️ גשם";
                if(this.weather == 'storm') wtx = "⛈️ סופה (מסוכן!)";
                document.getElementById('txt-weather').innerText = wtx;

                // Inv
                document.getElementById('i-food').innerText = this.inv.food;
                document.getElementById('i-water').innerText = this.inv.water;
                document.getElementById('i-med').innerText = this.inv.med;
                document.getElementById('i-scrap').innerText = this.inv.scrap;
                
                this.max_inv = this.gear.bag ? 20 : 10;
                document.getElementById('v-slots').innerText = this.max_inv;
                
                document.getElementById('has-knife').innerText = this.gear.knife ? "יש" : "אין";
                document.getElementById('has-knife').style.color = this.gear.knife ? "#0f0" : "#555";
                
                document.getElementById('has-bag').innerText = this.gear.bag ? "יש" : "אין";
                document.getElementById('has-bag').style.color = this.gear.bag ? "#0f0" : "#555";

                // Game Over Check
                if(this.s.hp <= 0) document.getElementById('scr-lose').style.display='flex';
                if(this.day >= 20) document.getElementById('scr-win').style.display='flex';
            },

            log: function(txt, cls="sys") {
                let div = document.createElement("div");
                div.className = "ln " + cls;
                div.innerHTML = "> " + txt;
                let c = document.getElementById("console");
                c.prepend(div);
            },

            // --- ACTIONS ---

            explore: function() {
                // בדיקת אנרגיה ומזג אוויר
                if(this.s.en < 15) { this.log("אין לך כוח לצאת! לך לישון.", "bad"); return; }
                if(this.weather == 'storm') { 
                    this.log("סופה בחוץ! אי אפשר לצאת.", "bad");
                    return; 
                }

                this.s.en -= 15;
                this.s.fd -= 5;
                this.s.wt -= 8;

                let luck = Math.random();
                // השפעת מזג אוויר וסכין
                let risk = 0.3; // 30% סיכוי לאסון
                if(this.weather == 'rain') risk = 0.5;
                if(this.gear.knife) risk -= 0.15; // סכין מוריד סיכון

                this.log("יצאת לסיור בשממה...");

                // בדיקת אסון
                if (Math.random() < risk) {
                    let dmg = Math.floor(Math.random() * 15) + 5;
                    this.s.hp -= dmg;
                    this.log(`⚠️ הותקפת ע"י זאב! (-${dmg} חיים)`, "bad");
                } 
                else {
                    // מציאה (Loot)
                    let found = [];
                    // יותר סיכויים
                    if(Math.random() > 0.4) { this.inv.scrap += Math.floor(Math.random()*3)+1; found.push("חומרים"); }
                    if(Math.random() > 0.5) { this.inv.food += 1; found.push("אוכל"); }
                    if(Math.random() > 0.6) { this.inv.water += 1; found.push("מים"); }
                    
                    if(found.length > 0) this.log(`מצאת: ${found.join(', ')}`, "good");
                    else this.log("לא מצאת כלום.", "sys");
                }
                
                this.update();
            },

            craft: function(item) {
                if(item == 'knife') {
                    if(this.gear.knife) { this.log("כבר יש לך סכין.", "sys"); return; }
                    if(this.inv.scrap >= 10) {
                        this.inv.scrap -= 10;
                        this.gear.knife = true;
                        this.log("בנית סכין! (פחות פציעות)", "good");
                    } else this.log("צריך 10 חומרים.", "bad");
                }
                if(item == 'bag') {
                    if(this.gear.bag) { this.log("כבר יש לך תרמיל.", "sys"); return; }
                    if(this.inv.scrap >= 20) {
                        this.inv.scrap -= 20;
                        this.gear.bag = true;
                        this.log("תפרת תרמיל! (+מקום)", "good");
                    } else this.log("צריך 20 חומרים.", "bad");
                }
                this.update();
            },

            eat: function() {
                if(this.inv.food > 0) {
                    this.inv.food--;
                    this.s.fd = Math.min(100, this.s.fd + 30);
                    this.s.hp = Math.min(100, this.s.hp + 5);
                    this.log("אכלת. (+30 רעב)", "good");
                } else this.log("אין אוכל.", "bad");
                this.update();
            },

            drink: function() {
                if(this.inv.water > 0) {
                    this.inv.water--;
                    this.s.wt = Math.min(100, this.s.wt + 40);
                    this.s.en = Math.min(100, this.s.en + 5);
                    this.log("שתית. (+40 מים)", "good");
                } else this.log("אין מים.", "bad");
                this.update();
            },

            med: function() {
                if(this.inv.med > 0) {
                    this.inv.med--;
                    this.s.hp = Math.min(100, this.s.hp + 40);
                    this.log("הזרקת תרופה. (+40 חיים)", "good");
                } else this.log("אין תרופות.", "bad");
                this.update();
            },

            sleep: function() {
                // סיום יום
                this.day++;
                this.log(`=== בוקר יום ${this.day} ===`, "sys");
                
                // שינוי מזג אוויר ליום הבא
                let r = Math.random();
                if(r < 0.6) this.weather = 'clear';
                else if(r < 0.9) this.weather = 'rain';
                else this.weather = 'storm';

                if(this.weather == 'storm') this.log("⚠️ סופה בחוץ! היזהר.", "bad");

                // סטטים בשינה
                this.s.en = 100; // שינה ממלאת אנרגיה
                this.s.fd -= 15;
                this.s.wt -= 20;

                // ענישה אם הולכים לישון רעבים
                if(this.s.fd < 0) { this.s.hp -= 10; this.s.fd = 0; this.log("התעוררת מורעב (-10 חיים)", "bad"); }
                if(this.s.wt < 0) { this.s.hp -= 10; this.s.wt = 0; this.log("התעוררת מיובש (-10 חיים)", "bad"); }
                
                this.update();
            }
        };

        game.update();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(GAME_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
