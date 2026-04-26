from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string, send_from_directory
import os

def x():
    y = Flask(__name__)
    @y.route('/')
    def index():return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return y

def a(text):
    return f'''
      <!DOCTYPE html>
      <html lang="he" dir="rtl">
      <head>
          <meta charset="UTF-8">
          <title>{text}</title>
          <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
          <style>
            body {{ margin: 0; font-family: 'Heebo', sans-serif; background-color: #0a0a0c; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }}
            .container {{ text-align: center; padding: 40px; background: rgba(30, 30, 36, 0.6); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 10px 40px rgba(0,0,0,0.7);}}
            h1 {{ font-size: 2.5rem; background: linear-gradient(90deg, #a29bfe, #00cec9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;}}
          </style>
      </head>
      <body>
        <div class="container">
          <div style="font-size: 60px; margin-bottom: 20px;">🚧</div>
          <h1>{text}</h1>
          <p style="color: #b2bec3; margin-top: 15px;">המשחק עדיין בפיתוח תחת תחנת הארקייד... סבלנות!</p>
        </div>
      </body>
      </html>
    '''

def create_dummy_app(text):
    dummy = Flask(__name__)
    @dummy.route('/')
    def index():return a(text)
    return dummy

# --- ייבוא המשחקים ---
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

# =======================================================
# MENU_HTML (המרכזייה)
# =======================================================
MENU_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade Station | Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>if (window.top !== window.self) { window.top.location = window.self.location; }</script>
    <style>
        :root { --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709; --card-bg: rgba(25, 25, 32, 0.6); --card-border: rgba(255, 255, 255, 0.08); --text-main: #f5f6fa; --text-sub: #a4b0be; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; min-height: 100vh; overflow-x: hidden; }
        
        .bg-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background-image: radial-gradient(circle at 15% 20%, rgba(108, 124, 231, 0.12) 0%, transparent 40%), radial-gradient(circle at 85% 70%, rgba(0, 206, 201, 0.12) 0%, transparent 40%), linear-gradient(to bottom, #070709 0%, #111116 100%); animation: pulseBg 10s infinite alternate; }
        @keyframes pulseBg { 0% { opacity: 0.8; } 100% { opacity: 1; } }

        nav { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(15px); border-bottom: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3); }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .top-links { display: flex; gap: 20px; align-items: center; margin-right: 15px; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: var(--accent); }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.98); min-width: 220px; box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid var(--card-border); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right; z-index:999;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: var(--accent); }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .btn { border: none; padding: 9px 24px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size:0.95rem; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-primary { background: var(--accent); color: #000; box-shadow: 0 0 10px rgba(0,206,201,0.2); }
        .btn-primary:not(:disabled):hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .btn-danger:hover { background: #dcdde1; color:#000;}
        .btn-action-small { background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.1); color: #fff; border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 0.85rem; transition: 0.2s;}
        .btn-action-small:hover { background: rgba(255,255,255,0.2); }
        
        .user-pill { background: rgba(0,0,0,0.5); border: 2px solid; color: #fff; padding: 6px 18px; border-radius: 30px; font-weight: bold; display: none; transition: 0.3s;}

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
        .feedback-fab { position: fixed; bottom: 30px; left: 30px; width: 65px; height: 65px; background: linear-gradient(135deg, #6c7ce7, #00cec9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; cursor: pointer; z-index: 990; border: none; transition: 0.3s; box-shadow: 0 8px 25px rgba(0,206,201,0.4); }
        .feedback-fab:hover { transform: scale(1.1); box-shadow: 0 15px 35px rgba(0,0,0,0.6); }

        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .input-box:disabled { opacity: 0.5; background: #111; cursor: not-allowed; }
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        .hidden-group { display: none; }

        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .about-modal-content { max-width: 650px !important; }

        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition: 0.2s;}
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); position: relative; }
        .user-row { flex-direction: row; justify-content: space-between; align-items: center;}
        
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
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
                <a onclick="alert('טבלאות דירוג יתווספו למערכת בקרוב!')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ פאנל ניהול</button>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>

    <main>
        <h1 class="main-title">בחר את ההרפתקה שלך</h1>
        <p class="subtitle">מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮</p>
        <div class="grid">
            <a href="/play/game1" class="card"><div class="card-cover">🏝️</div><div class="card-body"><h2>הישרדות</h2><span class="tag-badge">ניהול משאבים</span><p class="card-desc">שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</p></div></a>
            <a href="/play/game2" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 20px rgba(0, 206, 201, 0.5));">🌲</div><div class="card-body"><h2>Gold Forest</h2><span class="tag-badge">אקשן טקסטואלי</span><p class="card-desc">יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</p></div></a>
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

    <footer>&copy; 2026 Arcade Station</footer>
    <button class="feedback-fab" onclick="openModal('feedback-modal')">💬</button>

    <!-- מרכז האבטחה והחשבון -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות חשבון ופרופיל</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הרשמה</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל משויכת (חובה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="example@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר לך כינוי לתצוגה במשחק:</label>
                <input type="text" id="f-user" class="input-box" placeholder="שם במשחק או כינוי מזהה">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע הזיהוי שלך בפרופיל ובטבלאות:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (מעל 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">המשך</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי מהמערכת לצמיתות</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן למעבר לשחזור סיסמה דרך אימייל</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות הרגיל</u></p>
        </div>
    </div>

    <!-- מודל אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד מתקדמת המספקת משחקי דפדפן מהנים ומגוונים. כל המשחקים זמינים ללא צורך בהורדה!</p>
                <h3 style="color: #a29bfe; margin-top:10px;">אודות היוצר</h3>
                <p>נוצר ופותח על ידי <strong>אביאל</strong>.<br>כתובת אימייל לפניות: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- מודל שליחת משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת פניה או משוב</h2>
            <div class="form-group"><label>נושא הפנייה:</label><select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'"><option value="" disabled selected>-- בחר --</option><option value="bug">תקלה או בעיה טכנית</option><option value="idea">הצעה לשיפור</option><option value="other">אחר (פניה ישירה להנהלה)</option></select></div>
            <div class="form-group hidden-group" id="fb-text-box"><label>נא פרט כאן את פנייתך:</label><textarea id="fb-text" rows="5"></textarea><button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שלח פנייה 🚀</button></div>
        </div>
    </div>

    <!-- פאנל אדמין מתוקן וברור -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">פאנל ניהול למנהל המערכת</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול משתמשים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">תיבת משובים ופניות 📥</button>
            </div>
            
            <!-- מערכת רשימת שחקנים -->
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            
            <!-- מערכת פניות והודעות עם כפתור מחיקה -->
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("שגיאה! התחברות ל-Supabase נכשלה.", e); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-email', 'f-user', 'f-pass'].forEach(id => {
                document.getElementById(id).addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') { e.preventDefault(); executeAuthAction(); }
                });
            });
        });

        function openModal(id) { document.getElementById(id).classList.add('active'); showError(); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); showError(); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }
        function showError(msg = '') {
            const errBox = document.getElementById('auth-error');
            if(msg) { errBox.style.display = 'block'; errBox.innerText = '⚠️ ' + msg; } 
            else { errBox.style.display = 'none'; errBox.innerText = ''; }
        }

        async function checkUser() {
            if(!sp) return;
            const { data } = await sp.auth.getSession();
            cUser = data.session ? data.session.user : null;
            
            if(cUser) {
                try {
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { alert("חשבונך נחסם מהמערכת על ידי ההנהלה."); await logout(); return; }
                        if(dbProfile.message) { 
                            alert("💌 הודעה חדשה מההנהלה:\n" + dbProfile.message); 
                            await sp.from('profiles').update({ message: null }).eq('user_id', cUser.id);
                        }
                        cUser.customColor = dbProfile.color || '#00cec9'; 
                    } else { cUser.customColor = '#00cec9'; }
                } catch(e) { cUser.customColor = '#00cec9'; }
            }
            updateUI();
        }

        function updateUI() {
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            const pill = document.getElementById('user-status');
            
            if(cUser) {
                pill.style.display = 'block';
                document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
                pill.style.borderColor = cUser.customColor;
                document.getElementById('nickname-display').style.color = cUser.customColor;
            } else { pill.style.display = 'none'; }
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ פרופיל והגדרות' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = ''; document.getElementById('f-color').value = '#00cec9';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            globalAuthMode = mode; showError();
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); 
            const bP = document.getElementById('box-pass'); const bC = document.getElementById('box-color');
            const btn = document.getElementById('auth-exec-btn');
            const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            document.getElementById('f-email').disabled = false;
            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none'; bC.style.display='none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='כתובת אימייל:'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; 
                btn.innerText='התחברות למערכת'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='כתובת אימייל חוקית:';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי למשחק (יוצג לאחרים):'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='בחר סיסמה (לפחות 6 תווים):'; 
                btn.innerText='השלם הרשמה'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='עריכת הפרופיל האישי שלך'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל החשבון (לא ניתן לשינוי):'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי שם במשחק:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='שנה סיסמה (השאר ריק כדי לשמור את הסיסמה הנוכחית):';
                btn.innerText='שמור שינויים בחשבון'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='שחזור סיסמה למשתמש קיים'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='הכנס את כתובת האימייל של החשבון שלך:'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='שלח אלי לינק לאיפוס הסיסמה במייל';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("קיימת תקלה בהתחברות למסד הנתונים של השרת. אנא נסה שנית מאוחר יותר.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'מבצע פעולה, אנא המתן... ⏳';
            showError();

            try {
                if (globalAuthMode === 'LOGIN') await doLogin();
                else if (globalAuthMode === 'SIGNUP') await doSignUp();
                else if (globalAuthMode === 'EDIT') await doEditProfile();
                else if (globalAuthMode === 'RECOVERY') await doRecovery();
            } catch(e) { showError(e.message); } 
            finally { btn.disabled = false; btn.innerText = textOrig; }
        }

        async function doLogin() {
            const email = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!email || !p) return showError("נא למלא כתובת אימייל וסיסמה להתחברות.");
            if(!email.includes('@')) return showError("נא להזין כתובת אימייל חוקית המכילה את התו @.");
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) return showError("פרטי ההתחברות שגויים. כתובת האימייל אינה קיימת או שהסיסמה אינה נכונה.");
            else { closeModal('auth-modal'); await checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const email = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const clr = document.getElementById('f-color').value;
            if(!nickname || !email || !p) return showError("נא למלא את כל שדות החובה להרשמה (אימייל, כינוי, סיסמה).");
            if(!email.includes('@')) return showError("האימייל שהוזן אינו תקין. יש לכתוב כתובת מליאה המכילה את התו @.");
            if(p.length < 6) return showError("מטעמי אבטחה, אורך הסיסמה חייב להיות לפחות 6 תווים.");

            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) return showError(error.message.includes('already') ? "כתובת אימייל זו כבר רשומה במערכת שלנו!" : error.message);
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); alert("ההרשמה בוצעה בהצלחה! ברוך הבא לתחנת הארקייד."); closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim(); const newC = document.getElementById('f-color').value;
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN, color: newC }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            closeModal('auth-modal'); await checkUser(); alert("הגדרות הפרופיל שלך נשמרו בהצלחה.");
        }

        async function doRecovery() {
            const givenEmail = document.getElementById('f-email').value.trim();
            if(!givenEmail || !givenEmail.includes('@')) return showError("יש להזין כתובת אימייל תקנית המקושרת לחשבון כדי לשחזר את הסיסמה.");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail.toLowerCase());
            if (error) showError("אירעה שגיאה. ייתכן והאימייל הזה לא קיים במערכת.");
            else { alert("מכתב עם לינק לאיפוס סיסמה נשלח אל תיבת האימייל שלך. שים לב לבדוק גם בתיקיית הספאם (דואר זבל)."); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            if(!confirm("אזהרה! האם אתה בטוח שברצונך למחוק את החשבון שלך לצמיתות? הפעולה לא ניתנת לביטול וימחקו איתה כל הנתונים השמורים בשרת.")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("החשבון נמחק לצמיתות מהמערכת. תודה ששיחקת והתראות."); closeModal('auth-modal'); cUser = null; updateUI(); } catch (err) { alert("אירעה תקלה בעת מחיקת החשבון: " + err.message); }
        }

        /* --------------------------
           כללי משוב
           -------------------------- */
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; const tx = document.getElementById('fb-text').value; if(!tx || !t) return; 
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'משתמש אנונימי (לא מחובר)', topic: t, text: tx }); 
                if(error) throw error;
                alert('פנייתך נשלחה בהצלחה למנהל המערכת, תודה על העדכון!'); 
            } catch (err) { alert("חלה שגיאה בשליחת הפנייה. יתכן וחסרה הרשאה להוספה למסד בשרת ה-Supabase."); } 
            closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; document.getElementById('fb-text-box').style.display='none'; 
        }

        /* --------------------------
           פאנל האדמין העדכני: משוב מחיקה, וחזרה לעברית נורמלית
           -------------------------- */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">טוען את רשימת השחקנים... ⏳</p>'; fList.innerHTML = '<p style="text-align:center;">טוען את הפניות ומשובים... ⏳</p>';
            
            try {
                const { data: pList, error: pError } = await sp.from('profiles').select('*');
                if(pError) throw pError;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777; font-family:monospace;">ID: ${u.user_id}</div>
                            ${u.banned ? '<span style="display:inline-block; margin-top:3px; background:rgba(255,0,0,0.2); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#ff4757;">🚫 משתמש זה נחסם מהשרת</span>' : '<span style="display:inline-block; margin-top:3px; background:rgba(0,255,0,0.1); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#2ecc71;">✅ משתמש פעיל בחוקיות תקינה</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px; justify-content:center;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 שלח לו הודעה אישית</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 שחרר משתמש מחסימה' : '🚫 חסום את המשתמש כעת'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחק שחקן זה לצמיתות</button>
                        </div>
                    </div>
                    `).join('');
                } else uList.innerHTML = '<p style="color:#a4b0be; text-align:center;">לא קיימים שחקנים במסד הנתונים כרגע.</p>';
                
                // הזרקת המכתבי קריאות של העמך, בתוספת מחיקת משוב 🗑️
                const { data: fListDb, error: fError } = await sp.from('feedbacks').select('*');
                if(fError) throw fError;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row" style="position:relative;">
                        <button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="position:absolute; top:15px; left:15px; color:#ff4757; border-color:#ff4757; background:rgba(0,0,0,0.5);">🗑️ מחק</button>
                        <div style="margin-bottom:8px; width: 85%;">
                            <span style="color:var(--primary); font-size:1rem; font-weight:bold;">נושא הפנייה: ${x.topic}</span>
                        </div>
                        <div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; font-size:0.95rem; color:#eee; width: 95%;">"${x.text}"</div>
                        <div style="color:#a4b0be; font-size:0.8rem; margin-top:10px; display:flex; justify-content:space-between;">
                            <span>נשלח על ידי אימייל: <b dir="ltr">${x.user_email}</b></span>
                            <span>בתאריך: ${(new Date(x.created_at)).toLocaleDateString()}</span>
                        </div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="color:#a4b0be; text-align:center;">תיבת הפניות נקייה לגמרי! אין כרגע משובים מן המשתמשים.</p>';
                
            } catch(e) { 
                console.error("שגיאת אדמין בעת טעינת נתונים ממסד השרת: ", e.message);
                uList.innerHTML = `<p style="color:#ff4757; text-align:center;">שגיאת שליפה ממסד Supabase:<br>${e.message}</p>`; 
                fList.innerHTML = uList.innerHTML; 
            }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        async function adminSendMsg(uid) {
            let theM = prompt("נא להזין את תוכן ההודעה האישית שתופיע למשתמש המסומן עם כניסתו הבאה למערכת:");
            if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("הודעת מנהל הוזנה עבור המשתמש וישוגר בפעם הבאה שהוא טוען את האתר."); loadAdminData();}
        }

        async function adminToggleBan(uid, wasBanned) {
            if(confirm("האם ברצונך לבצע שינוי בסטטוס הרשאת המשחק של השחקן המבוקש?")) {
                await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert(!wasBanned ? "המשתמש הוכנס בהצלחה לרשימת החסומים ויסורב עם כניסתו." : "חסימת השחקן הוסרה. המשתמש מורשה לחזור לשחק בתחנה!"); loadAdminData();
            }
        }

        async function adminDelUser(uid) {
            if(confirm("החלטה גורלית: האם למחוק שחקן זה לצמיתות מבסיס הנתונים של השרתים לחלוטין? מחיקה איננה הפיכה!")) {
                await sp.from('profiles').delete().eq('user_id', uid); alert("משתמש זה נמחק לצמיתות מסדרת הפרופילים במערכת בצלחה."); loadAdminData();
            }
        }

        async function adminDelFeedback(fid) {
            if(confirm("האם אתה בטוח שברצונך למחוק תגובה או פנייה זו מהמערכת לתמיד?")) {
                const { error } = await sp.from('feedbacks').delete().eq('id', fid);
                if(error) alert("שגיאה בניסיון למחוק את הפנייה: " + error.message);
                else { alert("פניית המשתמש הוסרה ומחקנו אותה מתא הבקרה שלך."); loadAdminData(); }
            }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY_HTML (דף תוכן המשחק מותאם לשירותים החדשים בול כמו הMENU)
# =======================================================
PLAY_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arcade Play - {{target}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>if (window.top !== window.self) { window.top.location = window.self.location; }</script>
    <style>
        body, html { margin: 0; padding: 0; background-color: #070709; color: #fff; font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        
        /* Navbar Synchronization */
        nav { height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000; }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .top-links { display: flex; gap: 20px; align-items: center; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: #00cec9; }
        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        
        .user-pill { background: rgba(0,0,0,0.5); border: 2px solid; color: #fff; padding: 6px 18px; border-radius: 30px; font-weight: bold; display: none; transition: 0.3s;}
        
        .btn { border: none; padding: 8px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-primary { background: #00cec9; color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .btn-action-small { background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.1); color: #fff; border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 0.85rem; transition: 0.2s;}
        .btn-action-small:hover { background: rgba(255,255,255,0.2); }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height:90vh; overflow-y:auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: #a4b0be; }
        .input-box { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: #00cec9; }
        .input-box:disabled { opacity: 0.5; background: #111; cursor: not-allowed; }
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }

        /* אדמין חופף ומושלם למקרה הצורך מעמוד המשחק */
        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: #a4b0be; font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition: 0.2s;}
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); position: relative; }
        .user-row { flex-direction: row; justify-content: space-between; align-items: center;}
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: #00cec9; border-radius: 10px; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station">Arcade Station</a>
            <div class="top-links"><a href="/">חזרה לראשי</a></div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ פאנל ניהול</button>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>
    
    <iframe src="/{{target}}" title="Game"></iframe>

    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: #00cec9; margin-bottom:20px;">הגדרות חשבון ופרופיל</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות למשתמש</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הרשמה חדשה</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל להתחברות (חובה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="example@mail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">הזן את הכינוי המועדף שיציג את שמך בתחנת המשחקים:</label>
                <input type="text" id="f-user" class="input-box" placeholder="שם במשחק או כינוי מזהה">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע תיוג שיאפיין את השחקן בטבלאות והמערכות:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית משויכת:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>

            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">המשך</button>
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לחלוטין מן המערכות 💥</button>
            </div>
            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:#a4b0be; cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>זקוק לעזרה? לחץ פה לצורך שחזור הסיסמה אצלך</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור והתחבר בצורה הסטנדרטית</u></p>
        </div>
    </div>

    <!-- פאנל ניהול מהונדס נקי וסינכרוני -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">פאנל ניהול מתקדם להנהלה</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול כלל השחקנים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">ארכיון משוב ופניות חיות 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e){ console.error("כשל בהפעלת Supabase client.", e); }
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-email', 'f-user', 'f-pass'].forEach(id => {
                const f = document.getElementById(id);
                if(f) {
                    f.addEventListener('keypress', function(event) {
                        if (event.key === 'Enter') { event.preventDefault(); executeAuthAction(); }
                    });
                }
            });
        });

        function openModal(id) { document.getElementById(id).classList.add('active'); showError(); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); showError(); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }
        function showError(msg = '') { const el = document.getElementById('auth-error'); el.style.display = msg ? 'block' : 'none'; el.innerText = '⚠️ ' + msg; }

        async function checkUser() { 
            if(!sp) return; 
            const { data } = await sp.auth.getSession(); 
            cUser = data.session?.user || null; 
            
            if(cUser) {
                try {
                    const { data: profileBase } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(profileBase) {
                        if(profileBase.banned) { alert("הגישה של חשבון זה לאתר הארקייד נשללה באופן מיידי מידי האדמינים במערכת."); await logout(); return; }
                        if(profileBase.message) { 
                            alert("💌 התראה כללית/הודעה חדשה מההנהלה:\n" + profileBase.message); 
                            await sp.from('profiles').update({ message: null }).eq('user_id', cUser.id);
                        }
                        cUser.customColor = profileBase.color || '#00cec9'; 
                    } else { cUser.customColor = '#00cec9'; }
                } catch(e) { cUser.customColor = '#00cec9'; }
            }
            updateUI(); 
        }

        function updateUI() {
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            const pill = document.getElementById('user-status');
            
            if(cUser) {
                pill.style.display = 'block';
                document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
                pill.style.borderColor = cUser.customColor;
                document.getElementById('nickname-display').style.color = cUser.customColor;
            } else { pill.style.display = 'none'; }
            
            document.getElementById('main-action-btn').innerText = cUser ? '⚙ שינוי פרופיל עריכה' : 'התחבר עכשיו';
            document.getElementById('main-action-btn').onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function setAuthUI(mode) { 
            globalAuthMode = mode; showError();
            document.getElementById('f-email').disabled = false;
            
            const deleteDiv = document.getElementById('delete-acc-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); 
            const bLoginLnk = document.getElementById('back-login-link');
            const cTabContainer = document.getElementById('auth-tabs-container');
            const titleBox = document.getElementById('auth-edit-title');
            const bc = document.getElementById('box-color');
            
            deleteDiv.style.display='none'; titleBox.style.display='none'; cTabContainer.style.display='flex';
            bc.style.display='none';
            
            if (mode === 'LOGIN') { 
                document.getElementById('auth-tab-login').classList.add('active'); document.getElementById('auth-tab-signup').classList.remove('active'); 
                document.getElementById('box-user').style.display='none'; 
                document.getElementById('box-pass').style.display='block';
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="כתובת אימייל משויכת בחשבון השרת שלנו (הכרח להתחברות):";
                document.getElementById('lbl-pass').innerText="הסיסמה להרשאה ואישור גישת שחקן:";
            }
            else if (mode === 'SIGNUP') { 
                document.getElementById('auth-tab-login').classList.remove('active'); document.getElementById('auth-tab-signup').classList.add('active'); 
                document.getElementById('box-user').style.display='block'; 
                bc.style.display='block';
                document.getElementById('box-pass').style.display='block';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="אנא הבטח צירוף של אימייל מתוקף ונכון בלבד לסינכרון מלא:";
                document.getElementById('lbl-pass').innerText="סיסמת יסוד להורדת מסכים והזדהות על פי רמתך (אורך מעל 6!):";
            }
            else if (mode === 'EDIT') {
                cTabContainer.style.display='none'; titleBox.style.display='block'; titleBox.innerText='ניהול אישי מורחב וארנק מידע חשבון';
                document.getElementById('box-user').style.display='block'; bc.style.display='block'; document.getElementById('box-pass').style.display='block';
                document.getElementById('f-email').disabled = true; document.getElementById('f-email').value = cUser?.email || '';
                document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                deleteDiv.style.display='block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="כתובת קודמת נשארה לכלל - זוכה נעולה מעריכת גורם נסיעית אלא לקרקע:";
                document.getElementById('lbl-pass').innerText="לעדכון נוסף לסיסמה הכנס טקסט - במצב אחר סגר ללא השאר את השורה ריקה";
            }
            else if (mode === 'RECOVERY') {
                cTabContainer.style.display='none'; titleBox.style.display='block'; titleBox.innerText='מרפאת פתיחת דלתות לאבוד ולשכחת סיסמה פה!';
                document.getElementById('box-user').style.display='none'; document.getElementById('box-pass').style.display='none';
                document.getElementById('lbl-email').innerText="הכתובת המובטחת אצלנו נרשם עמה בפעולתו. נתז רענן לשליפת מייל נסיקה שחזור:";
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("מתנהלת הפרעה מהתחברות לאתר הליבה - שרת מנותק זמנית לעדכונים מראש בקריסות מערכת.");
            const btn = document.getElementById('auth-exec-btn'); btn.disabled = true; const original = btn.innerText; btn.innerText="המתן פעולות הרצת בדיקת מענה לוגי רציפה...⏳"; showError();
            try {
                if (globalAuthMode === 'LOGIN') {
                    const em = document.getElementById('f-email').value.trim();
                    if(!em || !em.includes('@')) throw new Error("לביטחון מרבי אנא השלם צירוף שגרתי נקי כצפוי במיל עם התיוגים התקניים ביותר! (@)");
                    const { error } = await sp.auth.signInWithPassword({ email: em.toLowerCase(), password: document.getElementById('f-pass').value });
                    if(error) showError("פרטים דלויים מהלשון: היתכן מחיקתן במאגרות או הזנח סיסמאי נשק סוגנן בכדורים של שקר?"); else { closeModal('auth-modal'); await checkUser(); }
                } else if (globalAuthMode === 'SIGNUP') {
                    const nick = document.getElementById('f-user').value.trim(); const mail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const cCol = document.getElementById('f-color').value;
                    if(p.length < 6 || !mail.includes('@') || !nick) throw new Error("סליחה ורסיות תקנוס שמועות חוסר הדיקות! המפתח לסיכומים להזנת 6 כוחת תו ולא שמות ומילים מקוטעות בהמשכויות לא זרמו. עמוד במוצגים המוחלטים נגזר פה!");
                    
                    const { data: dbHasNick } = await sp.from('profiles').select('nickname').eq('nickname', nick).maybeSingle();
                    if(dbHasNick) throw new Error("אנא פעל ברצון שם שחקני חדש לגמרי, סוכן אחר התחיל במבט הזה לפני זמן ואצף לו יבולה כבר כאן ברשת שזירת התחנה...");
                    
                    const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick, color: cCol } } });
                    if(error) showError(error.message.includes('already') ? 'פרצה מוטבעת הוכח קופסא זו! תיבת השירות שמשה בהרמת כוח במקרקע למשתמש אקזיט!' : "סיבת עניין הפלתו בשרת קיימת אלינו: " + error.message);
                    else { 
                        if(data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nick, color: cCol, banned: false, message: null }); }
                        closeModal('auth-modal'); await checkUser(); alert('נערך התקע בצירי העובדות של הפילטוק סטאנשיונר המלואן רגע ההורד פול לחזקת צמיגי משחק!');
                    }
                } else if (globalAuthMode === 'EDIT') {
                    const nK = document.getElementById('f-user').value.trim(); const pP = document.getElementById('f-pass').value.trim(); const cc = document.getElementById('f-color').value;
                    if(nK) { await sp.auth.updateUser({ data: { nickname: nK, color: cc } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: nK, color: cc }); }
                    if(pP && pP.length >= 6) { await sp.auth.updateUser({ password: pP }); }
                    closeModal('auth-modal'); await checkUser(); alert("כל הבשורה של הניהולים תובנת והוגנתי לחרוצים משחק בבסיסים! הגדרתך יחילו בערך קובץ שמיר... מבריק.");
                } else if (globalAuthMode === 'RECOVERY') {
                    const emailF = document.getElementById('f-email').value.trim();
                    if(!emailF.includes('@')) throw new Error("בשיקום אלף איפוס צלוח מתכוונים המכתב כמות תגיו חרוטה שיוך לזה (@) למלץ אימות למנגנונו של נערכות פסק... מלא עתה טופס טוב!");
                    const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
                    if (error) throw new Error("אבד במשאית המרחק השדון הנראה לשרת את דסק טבעות העבר במנגנון הדיינים סלח... לא הגיב לאמצעית כתובתי!");
                    else { alert("שדה הבקר אסף חתירה לדלגי מעלה צינור העברה פולי אקראיות של פלוט שחזור לעיני מסר זה אל כתובת קבועת החביב לדוחי דואר (ראה ספרות דואר זבל!)"); setAuthUI('LOGIN'); }
                }
            } catch(e) { showError(e.message); } finally { btn.disabled = false; btn.innerText = original; }
        }

        async function deleteSelf() {
            if(!confirm("אל לך לענות שכן מהיר באובססיות דראג המכה... לחציה מוסדית תמוקע הפרופילים מהחשבונות שלך מראש המסך שבו החברים והכבוד עתרו, ללא שוב להגיח... להמשיך להחסיל לחלוטין ולסיים גמר משחק?")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("נמחקו משעולים עברו המשתמש עוף לא קפצים יסובב אל עץ החצייה הבטוח של תדר חול ומימים. זכרוני למימים לא חוסר!"); closeModal('auth-modal'); cUser = null; updateUI(); } catch (err) { alert(err.message); }
        }

        // אותו אדמין מוטמן זהה אחד לאחד עם שכלול העברית ורשות המחיקת המשובים
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">מתבצע טעינת אוסף רשימת נתונים פנויה מן הרזולוציות... 🔄</p>'; 
            fList.innerHTML = '<p style="text-align:center;">מספר המשב הרוח ממנגנן כלי הערוץ פניות אלימות וחמימות דורכיו פנימה בסינתיזה... 🔄</p>';
            
            try {
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); if(pErr) throw pErr;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777;">מזהה מערכת גלובל: ${u.user_id}</div>
                            ${u.banned ? '<span style="color:#ff4757; font-size:0.75rem;">🚫 זהות השחקנים חסרת המערכה בהישגי חרב איומי ניגוד אבטח קסוטים דוקס. (חסום מגש מסיבי בעצירה)</span>' : '<span style="color:#2ecc71; font-size:0.75rem;">✅ אוטונמיית משחק שורשת איפוס תקינות (פנוי לנורמי חפיפות מתבצר מסע קשב מקושט!)</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 תשאיל ותשגר במכתבים מסירות מילים בהסכות לאזרחים בזה!</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 זרוק חלקי משענת הפסק כבל והחרשת שוך לאתר חביבי עז... זקוק לשרוח!' : '🚫 סור עתה לחסימה ומנע מעלי השהיית פגע קיווי בעמלו טרפ כחלי טכנאי.'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ דיסקו מעוף אדישות שחת גרומי דם עף ומחוק המגמג לעלמין בחינות יבוא!</button>
                        </div>
                    </div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">אל תשקשק השרשרת, לא היו מישהו באחוזות השאר טוען תעודתו לאכלל בזה טבלא חיה...</p>';
                
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); if(fErr) throw fErr;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row" style="position:relative;">
                        <button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="position:absolute; top:15px; left:15px; color:#ff4757; border-color:#ff4757; background:rgba(0,0,0,0.5);">🗑️ העלם ושליח השמדה על המסרון הזו.</button>
                        <div style="margin-bottom:8px; width:85%;"><span style="color:var(--primary); font-size:1rem; font-weight:bold;">תדמית נגיף ידע תא סלקציה הנגשת פניה: ${x.topic}</span></div>
                        <div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; font-size:0.95rem; color:#eee; margin:5px 0; width:95%;">"${x.text}"</div>
                        <div style="color:#a4b0be; font-size:0.8rem; margin-top:10px; display:flex; justify-content:space-between;">
                            <span>שורשר ביטחו כובש באטמוס הדואל הקל מזה המופף המאחדה סכינוה על מיקוד: <b>${x.user_email}</b></span>
                            <span>בתעלה שפלה צליחת השביליס הברקה השעה: ${(new Date(x.created_at)).toLocaleDateString()}</span>
                        </div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">משתתפי המים הזעקה יכפלו לא סנפה קשמיר משוברים תא חסך העיוור רענן שריקים משוטרים בשרשר אין תיעודי חדשה מבוך המשא...</p>';
                
            } catch(e) { 
                console.error(e.message); 
                uList.innerHTML = `<p style="color:#ff4757; text-align:center;">ארחי דחי משוב משנה את צלקות הפלייס בספארם אובל: ${e.message}<br>משטח מסננים RLS אישרה או סלע פתיחת השורות בקפיצ טבל שיתהווה...</p>`; 
                fList.innerHTML = uList.innerHTML; 
            }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        async function adminSendMsg(uid) { let theM = prompt("התקין והזרם שלום הועבר במסרת הטקסט חסכנות האלו נמעני הודע אלקטיים צמצם בהזנה ענווה תמריצים של ברז הבוטים שנוצרים לחפיצ של המסך הקול אליו בהיקוף מרוקאי!"); if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("הודעות המרצות במערכם קייצות השלח טעינן מניקוס התממשו סעק נכנס טרוסק בבנק חכמות המרחבי האתר נכון משנה יתרה הופיעה תנאי!"); loadAdminData();} }
        async function adminToggleBan(uid, wasBanned) { if(confirm("מוכן שישממו הדמוי במזק חקין התמומשויות העתיר קמבו הכללת ביאורים למנעולים במצב גילו חסימ לאירוח ההסתופק החסני הזה בעולמית משולחן דם מסע וחסירות מופעת אינפי חקי ורדו?")) { await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert("נפקד עבר הצמידו גל נשא הסטט האגוס מסכים של חילוט ודיונים מתיר החסין אל סל הארגונים הדעת המקוייר."); loadAdminData(); } }
        async function adminDelUser(uid) { if(confirm("יעד אחור שקולי החקירות התחת של הדת סכום הבת הנה תשת נחתת מחיל תוכו לארציות שחקם התיאטום מהות פסיכות עולמה יחד כוסר חתכי המלח הזרז שורץ מובלעת לכל העסוק בדירו דיליטים החצילים להשלים החליפה!?!")) { await sp.from('profiles').delete().eq('user_id', uid); alert("נמרחו החוקקים הדיירים לזילות לא מוצה אינסלס מיגס המזמן משלים למולת היעלן מסרק."); loadAdminData(); } }

        async function adminDelFeedback(fid) {
            if(confirm("אנשים רצים יסורים משבר השואב קריטי להעברת הפעילים נסיך כח המשב אל מעי הים הזורם טבול ההכחול פניה ומחשוף דיל למערכ עתיקו גושי הסעיקן למחוק לחצי סוגרת דריכות המסרון האם פועלות מחיק לולות יעד?")) {
                const { error } = await sp.from('feedbacks').delete().eq('id', fid);
                if(error) alert("קבע דגש בעיות במנצקי תולשת הזרמים אל השחיס החיוניות בקש הפונק סוק אפי: " + error.message);
                else { alert("דפי הקלד השכור מולח הנדסה המשח הפניה רעיפות חילוק הסג דחוקת כסף נמזרים עננו דש המסד תבליטו ונירצח האריכות הטיוב שואנתי."); loadAdminData(); }
            }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# שידוך כל המשחקים לרץ של הפלאסק
app = DispatcherMiddleware(main_app, {
    '/game1': game1, '/game2': game2, '/game3': game3, '/game4': game4, '/game5': game5,
    '/game6': game6, '/game7': game7, '/game8': game8, '/game9': game9, '/game9/x=v':game9,
    '/game10': game10, '/game11': game11, '/googlebf5e9f4bd69d6b9a.html':x(),
    '/php': php_app, '/html': html_app, '/app1': html_app, '/app2': php_app
})

if __name__ == "__main__":
    print("🎮 Arcade Station Running at http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
