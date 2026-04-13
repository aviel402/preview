from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string, send_from_directory
import os

def x():
    y = Flask(__name__)
    @y.route('/')
    def index():return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return y

# --- דף "בפיתוח" אלגנטי למשחקים החסרים ---
def a(text):
    return f'''
      <!DOCTYPE html>
      <html lang="he" dir="rtl">
      <head>
          <meta charset="UTF-8">
          <title>{text}</title>
          <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;700;900&display=swap" rel="stylesheet">
          <style>
            body {{ margin: 0; font-family: 'Heebo', sans-serif; background-color: #0a0a0c; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }}
            .container {{ text-align: center; padding: 40px; background: rgba(30, 30, 36, 0.6); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); }}
            h1 {{ font-size: 2.5rem; background: linear-gradient(90deg, #a29bfe, #00cec9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;}}
          </style>
      </head>
      <body>
        <div class="container">
          <div style="font-size: 60px; margin-bottom: 20px;">🚧</div>
          <h1>{text}</h1>
          <p style="color: #b2bec3; margin-top: 15px;">המשחק עדיין בפיתוח... סבלנות!</p>
        </div>
      </body>
      </html>
    '''

def create_dummy_app(text):
    dummy = Flask(__name__)
    @dummy.route('/')
    def index():return a(text)
    return dummy

# --- ייבוא בטוח למשחקים שלך ---
try: from app1 import app as game1
except ImportError: game1 = create_dummy_app("הישרדות")
try: from app2 import app as game2
except ImportError: game2 = create_dummy_app("Gold Forest")
try: from app3 import app as game3
except ImportError: game3 = create_dummy_app("Genesis")
try: from app4 import app as game4
except ImportError: game4 = create_dummy_app("קוד אדום")
try: from app5 import app as game5
except ImportError: game5 = create_dummy_app("IRON LEGION")
try: from app6 import app as game6
except ImportError: game6 = create_dummy_app("מבוך הצללים")
try: from app7 import app as game7
except ImportError: game7 = create_dummy_app("PROXIMA")
try: from app8 import app as game8
except ImportError: game8 = create_dummy_app("הטפיל")
try: from app9 import app as game9
except ImportError: game9 = create_dummy_app("CLOVER")
try: from app11 import app as game11
except ImportError: game11 = create_dummy_app("Manager PRO")
try: from app10 import app as game10
except ImportError: game10 = create_dummy_app("NEON RIDER")
try: from php import app as php_app
except ImportError: php_app = create_dummy_app("PHP App")
try: from HTML import app as html_app
except ImportError: html_app = create_dummy_app("html App")

main_app = Flask(__name__)

@main_app.route('/logo.png')
def favicon(): return "LOGO_DATA" 

@main_app.route('/')
def index(): return render_template_string(MENU_HTML)

@main_app.route('/play/<path:target>')
def play_view(target):
    return render_template_string(PLAY_HTML, target=target)

# ==========================================
# קוד 1 - התחנה הראשית (מסך המשתמש)
# ==========================================
MENU_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade Station | Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        :root {
            --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709;
            --card-bg: rgba(25, 25, 32, 0.6); --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f5f6fa; --text-sub: #a4b0be;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; min-height: 100vh; overflow-x: hidden; }
        
        .bg-layer {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background-image: radial-gradient(circle at 15% 20%, rgba(108, 124, 231, 0.12) 0%, transparent 40%),
                              radial-gradient(circle at 85% 70%, rgba(0, 206, 201, 0.12) 0%, transparent 40%),
                              linear-gradient(to bottom, #070709 0%, #111116 100%);
            animation: pulseBg 10s infinite alternate;
        }
        @keyframes pulseBg { 0% { opacity: 0.8; } 100% { opacity: 1; } }

        nav {
            position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
            background: rgba(10, 10, 15, 0.8); backdrop-filter: blur(15px); border-bottom: 1px solid var(--card-border);
            display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); }

        .top-links { display: flex; gap: 20px; align-items: center; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: var(--accent); }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.95); min-width: 200px; box-shadow: 0 10px 25px rgba(0,0,0,0.8); border: 1px solid var(--card-border); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 400px; overflow-y: auto; text-align:right; z-index:999;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: var(--accent); }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .btn { border: none; padding: 10px 22px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; }
        .btn-primary { background: var(--accent); color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; display: none; }

        main { padding: 120px 20px 60px; text-align: center; }
        h1.main-title { font-size: clamp(2.5rem, 8vw, 4.5rem); margin-bottom: 10px; background: linear-gradient(135deg, #fff, #a29bfe, #00cec9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
        .subtitle { color: var(--text-sub); font-size: 1.3rem; margin-bottom: 60px; }

        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; max-width: 1300px; margin: 0 auto; }
        .card { background: var(--card-bg); border-radius: 20px; text-decoration: none; color: white; transition: all 0.4s; border: 1px solid var(--card-border); overflow: hidden; display: flex; flex-direction: column; text-align: right; cursor:pointer; }
        .card:hover { transform: translateY(-12px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(108, 124, 231, 0.2); border-color: rgba(108, 124, 231, 0.4); }
        .card-cover { height: 130px; display: flex; align-items: center; justify-content: center; font-size: 55px; border-bottom: 1px solid var(--card-border); background: linear-gradient(135deg, rgba(108,124,231,0.2), rgba(0,206,201,0.1)); text-shadow: 0 0 20px rgba(255,255,255,0.2); }
        .card-body { padding: 25px; display: flex; flex-direction: column; }
        .card-body h2 { font-size: 1.6rem; font-weight: 700; margin-bottom: 5px; color: #fff; }
        .card-desc { font-size: 0.95rem; color: #a4b0be; margin-top: 10px; line-height: 1.4; flex-grow: 1; }
        .tag-badge { display: inline-block; align-self: flex-start; padding: 5px 12px; background: rgba(0, 206, 201, 0.15); border: 1px solid rgba(0, 206, 201, 0.3); border-radius: 20px; font-size: 0.8rem; font-weight: 500; color: #00cec9; }

        footer { margin-top: 100px; padding: 20px; text-align: center; color: #4b4b5c; font-size: 0.95rem; border-top: 1px solid var(--card-border); }
        .feedback-fab { position: fixed; bottom: 30px; left: 30px; width: 65px; height: 65px; background: linear-gradient(135deg, #6c7ce7, #00cec9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; cursor: pointer; z-index: 990; border: none; transition: 0.3s; }
        .feedback-fab:hover { transform: scale(1.1); box-shadow: 0 15px 35px rgba(0,0,0,0.6); }

        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .hidden-group { display: none; }

        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; }
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid transparent; }
        .user-row { cursor: pointer; flex-direction: row; justify-content: space-between; align-items: center;}
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="חזור למסך הראשי">
                <img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'"> 
                Arcade Station
            </a>
            
            <div class="top-links">
                <!-- משחקים / תפריט גלילה מהיר -->
                <div class="dropdown">
                    <a class="nav-item">משחקים ▾</a>
                    <div class="dropdown-content">
                        <a href="/play/game1">הישרדות 🏝️</a>
                        <a href="/play/game2">Gold Forest 🌲</a>
                        <a href="/play/game3">Genesis 🚀</a>
                        <a href="/play/game4">קוד אדום 💻</a>
                        <a href="/play/game5">IRON LEGION 🔫</a>
                        <a href="/play/game6">מבוך הצללים 🌑</a>
                        <a href="/play/game7">PROXIMA 🪐</a>
                        <a href="/play/game8">הטפיל 🧬</a>
                        <a href="/play/game9">CLOVER 🍀</a>
                        <a href="/play/game10">NEON RIDER 🏍️</a>
                        <a href="/play/game11">Manager PRO 📊</a>
                    </div>
                </div>
                <a onclick="alert('מודול טבלאות דירוגים יתווסף בהמשך הפיתוח! 🥇')">טבלאות</a>
                <a onclick="alert('Arcade Station מפותחת על ידי אביאל. מאגר משחקים מדהים עבור קהילת השחקנים!')">אודות</a>
            </div>
        </div>

        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ ניהול</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>

    <main>
        <h1 class="main-title">בחר את ההרפתקה שלך</h1>
        <p class="subtitle">מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮</p>

        <div class="grid">
            <a href="/play/game1" class="card"><div class="card-cover">🏝️</div><div class="card-body"><h2>הישרדות</h2><span class="tag-badge">ניהול משאבים</span><p class="card-desc">שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</p></div></a>
            
            <!-- המשחק השני עם סמל יער! 🌲 -->
            <a href="/play/game2" class="card"><div class="card-cover">🌲</div><div class="card-body"><h2>Gold Forest</h2><span class="tag-badge">אקשן טקסטואלי</span><p class="card-desc">יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</p></div></a>
            
            <a href="/play/game3" class="card"><div class="card-cover" style="filter: hue-rotate(80deg);">🚀</div><div class="card-body"><h2>Genesis</h2><span class="tag-badge">מסע בחלל</span><p class="card-desc">הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</p></div></a>
            <a href="/play/game4" class="card"><div class="card-cover" style="filter: hue-rotate(120deg);">💻</div><div class="card-body"><h2>קוד אדום</h2><span class="tag-badge">סייבר</span><p class="card-desc">הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</p></div></a>
            <a href="/play/game5" class="card"><div class="card-cover" style="filter: hue-rotate(160deg);">🔫</div><div class="card-body"><h2>IRON LEGION</h2><span class="tag-badge">יריות ושרידה</span><p class="card-desc">גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</p></div></a>
            <a href="/play/game6" class="card"><div class="card-cover" style="filter: hue-rotate(200deg);">🌑</div><div class="card-body"><h2>מבוך הצללים</h2><span class="tag-badge">אימה</span><p class="card-desc">מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</p></div></a>
            <a href="/play/game7" class="card"><div class="card-cover" style="filter: hue-rotate(240deg);">🪐</div><div class="card-body"><h2>PROXIMA</h2><span class="tag-badge">מחקר עולמות</span><p class="card-desc">חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</p></div></a>
            <a href="/play/game8" class="card"><div class="card-cover" style="filter: hue-rotate(280deg);">🧬</div><div class="card-body"><h2>הטפיל</h2><span class="tag-badge">ביולוגיה</span><p class="card-desc">מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</p></div></a>
            <a href="/play/game9" class="card"><div class="card-cover" style="filter: hue-rotate(320deg);">🍀</div><div class="card-body"><h2>CLOVER</h2><span class="tag-badge">מזל טהור</span><p class="card-desc">הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</p></div></a>
            <a href="/play/game10" class="card"><div class="card-cover" style="filter: hue-rotate(360deg);">🏍️</div><div class="card-body"><h2>NEON RIDER</h2><span class="tag-badge">מרוץ</span><p class="card-desc">רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</p></div></a>
            <a href="/play/game11" class="card"><div class="card-cover" style="filter: hue-rotate(25deg);">📊</div><div class="card-body"><h2>Manager PRO</h2><span class="tag-badge">ניהול קבוצות</span><p class="card-desc">הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</p></div></a>
        </div>
    </main>

    <footer>&copy; 2026 Arcade Station - Aviel Aluf</footer>
    <button class="feedback-fab" onclick="openModal('feedback-modal')">💬</button>

    <!-- מודל מערכת המשתמשים הגאוני והנסתר (מבוסס יוזר/סיסמה) -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent);">ניהול פרופיל שחקן</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">משתמש חדש</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי שחקן (Login):</label>
                <input type="text" id="f-user" class="input-box" placeholder="דוגמה: אביאל123">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label>אימייל אמיתי <span style="color:#777; font-size:0.8rem;">(אופציונלי - מאפשר לך איפוס סיסמה לעצמך אם שכחת!)</span></label>
                <input type="email" id="f-email" class="input-box" placeholder="myemail@gmail.com">
            </div>

            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">אשר</button>
            
            <p id="forgot-pw-link" style="text-align:center; margin-top:15px; font-size:0.9rem; color:var(--text-sub); cursor:pointer;" onclick="recoverPassword()">
                <u>שכחת סיסמה? לחץ כאן לאיפוס ושינוי סיסמה למשתמש</u>
            </p>
        </div>
    </div>

    <!-- מודל משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2>שליחת משוב</h2>
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-topic" class="input-box" onchange="updateFeedbackUI()">
                    <option value="" disabled selected>-- בחר --</option>
                    <option value="tech">תקלה טכנית</option>
                    <option value="idea">הצעה לשיפור</option>
                    <option value="other">משהו אחר (כללי)</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-game-box">
                <label>על איזה משחק מדובר?</label>
                <select id="fb-game" class="input-box">
                    <option value="main">התחנה הראשית (האתר)</option>
                    <option value="הישרדות">הישרדות</option>
                    <option value="Gold Forest">Gold Forest</option>
                    <option value="Genesis">Genesis</option>
                    <option value="קוד אדום">קוד אדום</option>
                    <option value="IRON LEGION">IRON LEGION</option>
                    <option value="מבוך הצללים">מבוך הצללים</option>
                    <option value="PROXIMA">PROXIMA</option>
                    <option value="הטפיל">הטפיל</option>
                    <option value="CLOVER">CLOVER</option>
                    <option value="NEON RIDER">NEON RIDER</option>
                    <option value="Manager PRO">Manager PRO</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-text-box">
                <label>פרט קצת יותר:</label>
                <textarea id="fb-text"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שלח למערכת 🚀</button>
            </div>
        </div>
    </div>

    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757;">פאנל מנהל מערכת</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">משובים והערות 📥</button>
            </div>
            <div id="section-users" class="admin-section active">
                <input type="text" id="admin-search" class="input-box" style="margin-bottom:15px;" placeholder="חפש לפי כינוי...">
                <div class="user-list" id="admin-user-list"></div>
            </div>
            <div id="section-feedbacks" class="admin-section">
                <div class="feedback-list" id="admin-feedback-list"><p style="color:#a4b0be; text-align:center;">טוען נתונים...</p></div>
            </div>
        </div>
    </div>

    <!-- הלוגיקה החשובה - זהה לדפים השניים גם כן  -->
    <script>
        const supUrl = 'https://ryoykooazoaordzmxdat.supabase.co';
        const supKey = 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B';
        const sp = supabase.createClient(supUrl, supKey);
        let cUser = null; 

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }

        async function checkUser() {
            const { data } = await sp.auth.getSession();
            cUser = data.session ? data.session.user : null;
            updateUI();
        }

        function updateUI() {
            const isAdm = cUser && (cUser.email === 'x0583289789@gmail.com');
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ פרופיל ואבטחה' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            const eTitle = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            if (mode === 'EDIT') { eTitle.style.display = 'block'; tabsCon.style.display = 'none'; setAuthUI('EDIT'); }
            else { eTitle.style.display = 'none'; tabsCon.style.display = 'flex'; setAuthUI(mode); }
            openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');
            const fPassLnk = document.getElementById('forgot-pw-link');

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי (או אימייל אמיתי אם רשמת):'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; fPassLnk.style.display='block'; btn.innerText='היכנס למערכת'; btn.onclick=doLogin;
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי (איך נציג אותך באתר):'; bE.style.display='block'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='בחר סיסמה:'; fPassLnk.style.display='none'; btn.innerText='הרשמה (לא חייב אימייל!)'; btn.onclick=doSignUp;
            } else if (mode === 'EDIT') {
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שם תצוגה חדש למשתמש:';
                document.getElementById('f-user').value = cUser.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='שנה סיסמה: (השאר ריק כדי לשמור על הישנה)';
                fPassLnk.style.display='none'; btn.innerText='שמור עדכונים למשתמש וסיסמה'; btn.onclick=doEditProfile;
            }
        }

        function getSafeEmail(userInput) {
            if(userInput.includes('@')) return userInput.trim();
            return userInput.trim().replace(/\s+/g, '') + "@arcadestation.local";
        }

        async function doLogin() {
            const userStr = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!userStr || !p) return alert("הזן כינוי וסיסמה!");
            const sysEmail = getSafeEmail(userStr);
            const { error } = await sp.auth.signInWithPassword({ email: sysEmail, password: p });
            if(error) alert("שגיאה! הפרטים לא תואמים. אולי טעית בהקלאדה בסיסמה?");
            else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const realMail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!nickname || !p) return alert("כינוי וסיסמה הם חובה להרשמה!");
            if(p.length < 6) return alert("הסיסמה צריכה להכיל לפחות 6 תווים.");
            const targetEmail = realMail.includes('@') ? realMail : getSafeEmail(nickname);
            const { data, error } = await sp.auth.signUp({ email: targetEmail, password: p, options:{ data:{ nickname: nickname } } });
            
            if (error) {
                if(error.message.includes("User already registered")) return alert("שגיאה: הכינוי הזה או המייל הזה כבר תפוס על ידי מישהו אחר. תוסיף ספרה או אות לשם!");
                return alert("שגיאת הרשמה: " + error.message);
            }
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); alert("נרשמת בהצלחה בתור: " + nickname); checkUser(); }
            closeModal('auth-modal'); 
        }

        async function doEditProfile() {
            const newNick = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newNick) { await sp.auth.updateUser({ data: { nickname: newNick } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newNick }); }
            if(newPass && newPass.length >= 6) {
                const { error } = await sp.auth.updateUser({ password: newPass });
                if(error) alert("שגיאה בעדכון הסיסמה: " + error.message);
                else alert("סיסמתך העצמית החדשה שונתה ושמורה למשתמש!");
            }
            alert("פרופיל עודכן."); closeModal('auth-modal'); checkUser();
        }

        async function recoverPassword() {
            const val = prompt('אנא הקלד את כתובת האימייל האמיתית שאיתה נרשמת (חייב אמיתית) על מנת שנשלח קישור לאיפוס סיסמתך:');
            if(!val) return;
            if(!val.includes('@') || val.includes('@arcadestation.local')) {
                return alert('לצערי לא נרשמת למערכת באמצעות כתובת אימייל פרטית בעת פתיחת המשתמש, אלא נרשמת רק דרך הכינוי שלך. מסיבה זו המערכת אינה יודעת למי לשלוח איפוס.\nצור משתמש חדש ונוסף (פעם הבאה הוסף בו מייל)!');
            }
            const { error } = await sp.auth.resetPasswordForEmail(val);
            if(error) alert("תקלה בשליחת בקשת השחזור... וודא שכתבת את הכתובת מדויק.");
            else alert("נשלח לינק לכתובת למעבר מהיר ויצירת סיסמה מחדש!");
        }

        // משוב ואדמין... (לשמור רשימות ריקות בינתיים)
        function updateFeedbackUI() {
            const v = document.getElementById('fb-topic').value; document.getElementById('fb-game-box').style.display = (v === 'tech' || v === 'idea') ? 'block' : 'none'; document.getElementById('fb-text-box').style.display = v ? 'block' : 'none';
        }
        async function submitFeedback() {
            const t = document.getElementById('fb-topic').value; const g = document.getElementById('fb-game-box').style.display === 'block' ? document.getElementById('fb-game').value : 'כללי'; const tx = document.getElementById('fb-text').value; if(!tx) return;
            try { await sp.from('feedbacks').insert({ user_email: cUser ? (cUser.email.includes('.local') ? cUser.user_metadata.nickname : cUser.email) : 'אורח', topic: t, game: g, text: tx }); alert('תודה על המשוב! ✨');
            } catch (err) { } closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; updateFeedbackUI();
        }
        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); }
        function switchAdminTab(t) {
            document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks');
            document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks');
        }
        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =========================================================================
# חלון עטיפת משחק PLAY_HTML (פה ביצעתי את הפתרונות המהפכניים לסרגל!)
# שורת ההרשמה הוכנסה לפה וממלאת את המסך, אין את סמל היציאה בכלל - פשוט "התחבר", או משתמש ורק בלוגו ניתן לצאת חזרה לראשי
# =========================================================================
PLAY_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arcade Play - {{target}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        body, html { margin: 0; padding: 0; background-color: #070709; color: #fff; font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        
        nav {
            height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000;
        }
        
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); }

        .top-links { display: flex; gap: 20px; align-items: center; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: #00cec9; }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.95); min-width: 200px; box-shadow: 0 10px 25px rgba(0,0,0,0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 400px; overflow-y: auto; text-align:right;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: #00cec9; }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; display: none; }
        .btn { border: none; padding: 8px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn-primary { background: #00cec9; color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        /* Modal Style copied for Game View Login support! */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; }
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: #a4b0be; }
        .input-box { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: #00cec9; }
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }
    </style>
</head>
<body>
    <nav>
        <!-- צד ימין (טבלאות / משחקים - פשוט עכשיו בגרסת השחקן) -->
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station"><img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'">Arcade Station</a>
            
            <div class="top-links">
                <div class="dropdown">
                    <a class="nav-item">משחקים ▾</a>
                    <div class="dropdown-content">
                        <a href="/play/game1">הישרדות 🏝️</a>
                        <a href="/play/game2">Gold Forest 🌲</a>
                        <a href="/play/game3">Genesis 🚀</a>
                        <a href="/play/game4">קוד אדום 💻</a>
                        <a href="/play/game5">IRON LEGION 🔫</a>
                        <a href="/play/game6">מבוך הצללים 🌑</a>
                        <a href="/play/game7">PROXIMA 🪐</a>
                        <a href="/play/game8">הטפיל 🧬</a>
                        <a href="/play/game9">CLOVER 🍀</a>
                        <a href="/play/game10">NEON RIDER 🏍️</a>
                        <a href="/play/game11">Manager PRO 📊</a>
                    </div>
                </div>
                <a onclick="alert('טבלאות יגיעו בהמשך')">טבלאות</a>
                <a onclick="alert('משחק קטלני זה לא?')">אודות</a>
            </div>
        </div>

        <!-- הצד השמאלי המהפכני והמעודכן שמצוי בתוך המשחקים שלך מעתה והלאה:
             * אין כפתור חזור, יוצאים עם הפיצ'ר של הלוגו שחיים עליו. 
             * הרשמה תמיד נוכחת בזמן משחק!!!
        -->
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>
    
    <iframe src="/{{target}}" title="Game"></iframe>

    <!-- מודל ההתחברות גם פה (מועתק ממש במדויק בשביל עקיצות שגיאות לחיצה באמצע הקרב) -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: #00cec9;">ניהול פרופיל שחקן</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">משתמש חדש</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי שחקן:</label>
                <input type="text" id="f-user" class="input-box" placeholder="אביאל123">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label>אימייל אמיתי <span style="color:#777; font-size:0.8rem;">(מומלץ לאיפוס სიסמה)</span></label>
                <input type="email" id="f-email" class="input-box">
            </div>

            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">אשר</button>
        </div>
    </div>

    <!-- הלוגיקה החשובה בשביל משחקים -> Auth Logic Sync -->
    <script>
        const supUrl = 'https://ryoykooazoaordzmxdat.supabase.co';
        const supKey = 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B';
        const sp = supabase.createClient(supUrl, supKey);
        let cUser = null; 

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }

        async function checkUser() {
            const { data } = await sp.auth.getSession();
            cUser = data.session ? data.session.user : null;
            updateUI();
        }

        function updateUI() {
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ ערוך פרופיל' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            document.getElementById('logout-btn').style.display = cUser ? 'block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            const eTitle = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            if (mode === 'EDIT') { eTitle.style.display = 'block'; tabsCon.style.display = 'none'; setAuthUI('EDIT'); }
            else { eTitle.style.display = 'none'; tabsCon.style.display = 'flex'; setAuthUI(mode); }
            openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; btn.innerText='הכנס למערכת'; btn.onclick=doLogin;
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי רצוי:'; bE.style.display='block'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='צור סיסמה:'; btn.innerText='צור פרופיל למערכת'; btn.onclick=doSignUp;
            } else if (mode === 'EDIT') {
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי שם לחשבון שלי:'; document.getElementById('f-user').value = cUser.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='הקש סיסמה חדשה במידה והינך מעוניין (חובה מ6 אותיות):'; btn.innerText='אישור ושמירת שינויים מכל הלב'; btn.onclick=doEditProfile;
            }
        }

        function getSafeEmail(u) { return u.includes('@') ? u.trim() : u.trim().replace(/\s+/g, '') + "@arcadestation.local"; }

        async function doLogin() {
            const usrStr = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!usrStr || !p) return alert("הזן פרטים מוקפדים יוסף!");
            const sysMail = getSafeEmail(usrStr);
            const { error } = await sp.auth.signInWithPassword({ email: sysMail, password: p });
            if(error) alert("שגיאה! אנא בדוק אם קראו נכון באישורך שאינך מזויף לכול עברה ושנה סיסמתך...");
            else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const rM = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!nickname || !p) return alert("נאלץ למלא כינוי לפחות");
            const finalEm = rM.includes('@') ? rM : getSafeEmail(nickname);
            const { data, error } = await sp.auth.signUp({ email: finalEm, password: p, options:{ data:{ nickname: nickname } } });
            
            if (error) return alert("שגיאה: זה רשום כבר במערכת.");
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); checkUser(); }
            closeModal('auth-modal'); 
        }

        async function doEditProfile() {
            const newNick = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newNick) { await sp.auth.updateUser({ data: { nickname: newNick } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newNick }); }
            if(newPass && newPass.length >= 6) await sp.auth.updateUser({ password: newPass });
            closeModal('auth-modal'); checkUser(); alert("עדכון הועבר באמינות מלאה, המשך קולות מלחמת הרעם.");
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# מחקתי את ררר מפה ומתוך הדפדפות שזהו, הטיגריס של הילד יחכה לפעם הבאה בספרייה! ;)
app = DispatcherMiddleware(main_app, {
    '/game1': game1, '/game2': game2, '/game3': game3, '/game4': game4, '/game5': game5,
    '/game6': game6, '/game7': game7, '/game8': game8, '/game9': game9, '/game9/x=v':game9,
    '/game10': game10, '/game11': game11, '/googlebf5e9f4bd69d6b9a.html':x(),
    '/php': php_app, '/html': html_app, '/app1': html_app, '/app2': php_app
})

if __name__ == "__main__":
    print("🎮 Arcade Station Running at http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
