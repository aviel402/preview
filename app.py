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
# MENU_HTML (המרכזייה הראשית)
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
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); transition: transform 0.3s;}
        .brand-logo:hover img { transform: scale(1.05); }

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
        .about-text p { line-height: 1.6; margin-bottom: 10px; font-size: 1.05rem;}
        .about-text h3 { color: #a29bfe; margin-top: 25px; margin-bottom: 15px;}
        .about-text li { margin-bottom: 12px; }

        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition: 0.2s;}
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
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
                <a onclick="alert('מודול טבלאות הדירוגים הציבוריות יתווסף בהמשך הפיתוח! 🥇')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ ניהול השרת</button>
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

    <!-- מרכז האבטחה (התחברות והרשמה) -->
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
                <input type="email" id="f-email" class="input-box" placeholder="שחקן@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר לך כינוי לתצוגה במשחק:</label>
                <input type="text" id="f-user" class="input-box" placeholder="כינוי למשחק (למשל סופרמן55)">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>הצבע האישי שלך שיופיע במערכת:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (לפחות 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">התחבר והתחל לשחק</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי מהשרת לחלוטין</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לשחזור אימייל</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות הראשי</u></p>
        </div>
    </div>

    <!-- חלון אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד חכמה המספקת משחקי דפדפן מרתקים במגוון ז'אנרים. כל המשחקים נגישים ללא צורך בהורדות!</p>
                <h3 style="color: #a29bfe; margin-top:15px;">אודות היוצר</h3>
                <p>נוצר במומחיות ובאהבה רבה על ידי <strong>אביאל</strong>.<br>כתובת אימייל ליצירת קשר: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- חלון שליחת משוב למנהל -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת פניה למערכת</h2>
            <div class="form-group"><label>באיזה נושא הפנייה?</label><select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'"><option value="" disabled selected>-- בחר --</option><option value="bug">מצאתי תקלה / באג במשחק</option><option value="idea">יש לי רעיון לשדרוג</option><option value="other">הודעה אחרת למנהל השרת</option></select></div>
            <div class="form-group hidden-group" id="fb-text-box"><label>נא לפרט כאן בהרחבה כדי שנוכל לעזור:</label><textarea id="fb-text" rows="5"></textarea><button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שליחת ההודעה עכשיו 🚀</button></div>
        </div>
    </div>

    <!-- פאנל ניהול (מיועד רק לך כמנהל) -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">מסוף הניהול הראשי (אדמין)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול משתמשים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר ומכתבים 📥</button>
            </div>
            
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        // המיקום המדוייק לחיבור שלך למסד
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } 
        catch(e) { console.error("שגיאה! מערכת Supabase לא הצליחה להיטען כראוי.", e); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {
            // הוספת יכולת התחברות קלה דרך כפתור "Enter" (אנטר) במקלדת!['f-email', 'f-user', 'f-pass'].forEach(id => {
                const element = document.getElementById(id);
                if(element) {
                    element.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') { e.preventDefault(); executeAuthAction(); }
                    });
                }
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
                // נשיג את המידע הנוסף כמו האם הוא חסום, ואת הצבע שבחר...
                try {
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { alert("🚨 חשבונך הושעה ממערכת המשחקים. אנא פנה למנהל האתר לפרטים נוספים."); await logout(); return; }
                        if(dbProfile.message) { 
                            alert("💌 הודעה חשובה מהמערכת:\n\n" + dbProfile.message); 
                            await sp.from('profiles').update({ message: null }).eq('user_id', cUser.id);
                        }
                        cUser.customColor = dbProfile.color || '#00cec9'; 
                    } else { cUser.customColor = '#00cec9'; }
                } catch(e) { cUser.customColor = '#00cec9'; }
            }
            updateUI();
        }

        function updateUI() {
            // אם כתובת האימייל המחוברת היא המייל שלך (אביאל) נחשוף כפתור אדמין!
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            const pill = document.getElementById('user-status');
            
            if(cUser) {
                pill.style.display = 'block';
                document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
                pill.style.borderColor = cUser.customColor;
                document.getElementById('nickname-display').style.color = cUser.customColor;
            } else { pill.style.display = 'none'; }
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ עדכון פרופיל' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; 
            document.getElementById('f-pass').value = ''; document.getElementById('f-color').value = '#00cec9';
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
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל ההתחברות שלך:'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמת החשבון שלך:'; 
                btn.innerText='התחבר עכשיו והתחל לשחק'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='דוא"ל הרשמי (חשוב לגיבוי ושחזור):';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר לעצמך כינוי להצגה:'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה אישית (מעל 6 תווים חובה):'; 
                btn.innerText='צור משתמש חדש ונתחיל!'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז פרופיל ואבטחה אישית'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='כתובת האימייל המזוהה איתך (חסומה לשינוי):'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='האם תרצה לשנות את הכינוי שלך בשרת?'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='ניתן להקליד סיסמה חדשה (אם תשאיר ריק לא ישתנה):';
                btn.innerText='שמור את השינויים החדשים בחשבון'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מעבדת שחזור סיסמאות אישית'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='לאיזו כתובת אימייל שלך נשלח את האיפוס?'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='שלחו אליי למייל קישור לאיפוס סיסמה';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("מצטערים, אין תקשורת לשרת המסד. כנראה המערכת למטה מסיבות עומס.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'מבצע התחברות בשרת... אנא המתן ⏳';
            showError(); // הסתרת שגיאה קודמת ליתר ביטחון!

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
            if(!email || !p) throw new Error("אנא מלא גם אימייל וגם סיסמה בצורה תקינה בכדי להתחבר.");
            if(!email.includes('@')) throw new Error("חסרה תווית השטרודל (@) - הקפד על הזנת כתובת אימייל אמיתית בטופס.");
            
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) throw new Error("שגיאה! הסיסמה שהקשת או האימייל אינם מתאימים ו/או שגויים, אולי עדיף להיעזר בשחזור הנתונים למטה?");
            
            closeModal('auth-modal'); await checkUser();
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value; const clr = document.getElementById('f-color').value;
            if(!nickname || !email || !p) throw new Error("על מנת לפתוח חשבון אתה חייב למלא את כל השדות בצורה מלאה: כינוי, מייל וסיסמה.");
            if(!email.includes('@')) throw new Error("המשתמש מצריך שמירת אימייל תקני. נא להשתמש בכתובת הכוללת בתוכה את הסמל @ כראוי.");
            if(p.length < 6) throw new Error("לשמירת ביטחון החשבון במערכת המשתמש, הסיסמה מחויבת להכיל 6 תווים ומעלה לכל הפחות.");

            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) {
                if (error.message.includes('already')) throw new Error("אופס! מצאנו שחשבון אימייל זה בדיוק או אפילו שם זה כבר רשום במערכת שלנו, הכל קבוע... נסה התחברות קלאסית בבועה למעלה!");
                throw new Error("השרת העיד על בעיה: " + error.message);
            }
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); 
                alert("כל הכבוד, המשתמש שלך מוכן בהצלחה! משגר אותך למשחקים..."); 
                closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim(); const newC = document.getElementById('f-color').value;
            if(newN) { 
                await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); 
                await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN, color: newC }); 
            }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            closeModal('auth-modal'); await checkUser(); alert("עדכוני הגדרות המערכת שלך עברו אישור ונשמרו בהצלחה!");
        }

        async function doRecovery() {
            const emailF = document.getElementById('f-email').value.trim();
            if(!emailF.includes('@')) throw new Error("בבקשה הענק במדויק את המייל על מנת שמנועי המערכת יידעו למי למסור לינק תקני ושחזור סיסמה מהקיר.");
            const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
            if (error) throw new Error("השחזור כשל ברקע! במערכות נאמר שחסר שם מסד מתאים לכתובת כזו. יתכן ויצרת במייל דומה אצלנו.");
            alert("אם הכתובת ממוקמת אצלנו באמת - ישוגר לינק לאיפוס היישר למייל זה בתוך שניות! 📩 בדוק בבקשה גם בתיקיית ה'ספאם/קידום מכירות'."); 
            setAuthUI('LOGIN'); 
        }

        async function deleteSelf() {
            if(!confirm("עצור שניה! האם אתה באמת ובתמים בטוח בכוונתך למחוק לחלוטין את החשבון המרכזי פה? לאחר מחיקתו כל רשומה נעלמת לאלתר - האם לבצע מחיקת חשבון מוחלטת? ⚠️")) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("תם הניווט שלך בנקודה הזו, הפרופיל שלך נמחק ונקרע סופית ממסד המשחקים."); 
                closeModal('auth-modal'); cUser = null; updateUI(); 
            } catch (err) { alert(err.message); }
        }

        /* --------------------------
           כללי משוב מתוך המערכת הפתוחה!
           -------------------------- */
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; const tx = document.getElementById('fb-text').value; if(!tx || !t) return; 
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'משתמש אנונימי (לא מחובר)', topic: t, text: tx }); 
                if(error) throw error;
                alert('רעיון נהדר, ההודעה / הדיווח נשלח ממש עכשיו למנהלים בטיל! אנו מעריכים שיתופים תודה! ✉️'); 
            } catch (err) { alert("כנראה תפגוש שגיאה עקב העדר שמירת כללי הגשה ממערכת הניהול הממוחשבת של סופאביס שלך RLS: Insert פולייסי. שווה לחפש."); } 
            closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; document.getElementById('fb-text-box').style.display='none'; 
        }

        /* --------------------------
           כלי האדמין הרשמי של מערך המשחק! שליטה בהודעות אישיות + הסרה של משוב!
           -------------------------- */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">מעדכן אחי... קורא דאטה מסופאבייס 🔄</p>'; fList.innerHTML = '<p style="text-align:center;">חוצב נתוני סטאטוס ומיילים... 🔄</p>';
            
            try {
                // הבאת כל פרופילי השחקן
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); if(pErr) throw pErr;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'}; margin-bottom:10px;">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777; font-family:monospace;">User_ID (מיקוד גישה): ${u.user_id}</div>
                            ${u.banned ? '<span style="display:inline-block; margin-top:3px; background:rgba(255,0,0,0.2); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#ff4757;">🚫 המשתמש קיבל באן וחסום לגמרי</span>' : '<span style="display:inline-block; margin-top:3px; background:rgba(0,255,0,0.1); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#2ecc71;">✅ פעיל באופן קבוע ותקין</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px; justify-content:center;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 תזרוק לו הודעה לפתיחה הבאה</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 ביטול באן ופתיחה חוזרת לשחקן' : '🚫 תן לו באן אכזרי (לא יכול להתחבר!)'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחק אותו לנצח מהספירה היומיומית</button>
                        </div>
                    </div>
                    `).join('');
                } else uList.innerHTML = '<p style="text-align:center;">המדד פנוי משחקנים עתה, אין רזרבה ב- Profiles בכלל.</p>';
                
                // הזרקת המכתבים מהשולחים בתיבת FEEDBACK
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); if(fErr) throw fErr;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row" style="margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                            <span style="color:var(--primary); font-size:1rem; font-weight:bold;">נושא המשאב/פנייה שהתקבלו: ${x.topic}</span>
                            <button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="color:#ff4757; border-color:#ff4757; padding: 2px 8px;">🗑️ סיום פנייה ומחיקה</button>
                        </div>
                        <div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; font-size:0.95rem; color:#eee;">"${x.text}"</div>
                        <div style="color:#a4b0be; font-size:0.8rem; margin-top:10px; display:flex; justify-content:space-between;">
                            <span>שלחו ממשתמש (מייל מקשר): <b>${x.user_email}</b></span>
                            <span>בתאריך תקשור: ${(new Date(x.created_at)).toLocaleDateString()}</span>
                        </div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">מקסים פה מנועים על אפס תיקי הודעות ומיילים. השמירות בסביבות תיבה שקטות לגמרי!</p>';
                
            } catch(e) { uList.innerHTML = `<p style="color:#ff4757;">שיבוש רגעי בקבלת אישורים... התייצב וחשוק הוספות לפעמים על מוד פולסי אקסטרא..  השגיאה שהוחזרה: ${e.message}<br></p>`; fList.innerHTML = uList.innerHTML; }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        async function adminSendMsg(uid) { 
            let theM = prompt("הכנס הודעה אישית שתוצג לשחקן מיד כשהוא יעשה רענון או התחברות לשרת (מעין פופ-אפ אישי!):"); 
            if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("מעולה, זה תפס קבע ונארז למשלוחה לאיש הרזרבה בחוץ!"); loadAdminData();} 
        }
        
        async function adminToggleBan(uid, wasBanned) { 
            if(confirm("שיקול אחרון, אם תחתוך ותפעיל מערכת השהיה השחקן יושלך רנדומלי מהשרת האם יש לכך תוקף במאה אחוז?")) { 
                await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert(!wasBanned ? "הבנאדם לא רואה את הדלת ולא מורשה להתחבר יותר - קיבל באן! 🔨" : "שמרנו לחשבון הזדמנות לשחק ברכבות ערומות בלי באן יותר. שוחרר."); loadAdminData(); 
            } 
        }
        
        async function adminDelUser(uid) { 
            if(confirm("שים לב שלחיצה פה עלולה לאפס ולעשות דיליט על החידושים באזור האופף פה לפרופיל שלו. בטוח?")) { 
                await sp.from('profiles').delete().eq('user_id', uid); alert("כלל ההגדרות שלו עופו עם ציפור. הפרופיל אינו ברשת משמעות משחק בסיס יותר. טבלאות מתרוקנות מהנתונים הקשייים שלו פה!"); loadAdminData(); 
            } 
        }

        // אפשרות חדשה: למחוק פניות שכבר קראת/טיפלת מהמשובים בשרת בקלות
        async function adminDelFeedback(fid) {
            if(confirm("טיפלת בפניה הזו כבר והגיע הזמן לשחרר נקיון ולהעיף מההיסטוריה? (פעולה זו מוחקת סופית!)")) {
                await sp.from('feedbacks').delete().eq('id', fid); alert("כיווננו את הצינור ונקה המשוב מרישום המסד הפתוח."); loadAdminData();
            }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY_HTML (דף תוכן המשחקים – מסונכרן 100% בסרגל כלים לחלוטין מול הראשי! ✨)
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
        :root { --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709; --card-border: rgba(255, 255, 255, 0.08); --text-main: #f5f6fa; --text-sub: #a4b0be; }
        body, html { margin: 0; padding: 0; background-color: var(--bg-dark); color: #fff; font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        
        /* סינכרון מושלם ומוחלט של עיצוב חוליית הניווט (Navbar) ביחס ל-MENU_HTML לטובת נראות ללא חריגים */
        nav { height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000; }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); transition: transform 0.3s;}
        .brand-logo:hover img { transform: scale(1.05); }

        .top-links { display: flex; gap: 20px; align-items: center; margin-right: 15px; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: var(--accent); }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.98); min-width: 220px; box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid var(--card-border); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right; z-index:999;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: var(--accent); }
        
        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        
        .user-pill { background: rgba(0,0,0,0.5); border: 2px solid; color: #fff; padding: 6px 18px; border-radius: 30px; font-weight: bold; display: none; transition: 0.3s;}
        
        .btn { border: none; padding: 8px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-primary { background: #00cec9; color: #000; box-shadow: 0 0 10px rgba(0,206,201,0.2); }
        .btn-primary:not(:disabled):hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
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
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: #00cec9; }
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        .hidden-group { display: none; }
        
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }

        .about-modal-content { max-width: 650px !important; }
        .about-text p { line-height: 1.6; margin-bottom: 10px; font-size: 1.05rem;}
        .about-text h3 { color: #a29bfe; margin-top: 25px; margin-bottom: 15px;}

        /* תא הניהול אדמין שווה וסימטרי במסכי ה-PLAY שמשלים למיקום מוצק */
        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: #a4b0be; font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition: 0.2s;}
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
        .user-row { flex-direction: row; justify-content: space-between; align-items: center;}
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: #00cec9; border-radius: 10px; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station"><img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'">Arcade Station</a>
            
            <!-- הסרגל של המסך משחקים - התואם למרכזי אחד על אחד לבקשתך! -->
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
                <a onclick="alert('מודול טבלאות הדירוגים הציבוריות יתווסף בהמשך הפיתוח! 🥇')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
        </div>
        
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ ניהול השרת</button>
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
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הרשמה</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל משויכת (חובה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="שחקן@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר לך כינוי לתצוגה במשחק:</label>
                <input type="text" id="f-user" class="input-box" placeholder="כינוי למשחק (למשל סופרמן55)">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>הצבע האישי שלך שיופיע במערכת:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (לפחות 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>

            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">התחבר והתחל לשחק</button>
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי מהשרת לחלוטין</button>
            </div>
            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:#a4b0be; cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לשחזור אימייל</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות הראשי</u></p>
        </div>
    </div>

    <!-- חלון אודות - זמין כעת תמיד! -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד חכמה המספקת משחקי דפדפן מרתקים במגוון ז'אנרים. כל המשחקים נגישים ללא צורך בהורדות!</p>
                <h3 style="color: #a29bfe; margin-top:15px;">אודות היוצר</h3>
                <p>נוצר במומחיות ובאהבה רבה על ידי <strong>אביאל</strong>.<br>כתובת אימייל ליצירת קשר: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- פאנל אדמין מיוצא זהה לחלוטין במסכים אלו להחזרת משוואות ושיקוף תחת המנוע -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">מסוף הניהול הראשי (אדמין)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול משתמשים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר ומכתבים 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e){}
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-email', 'f-user', 'f-pass'].forEach(id => {
                const element = document.getElementById(id);
                if(element) {
                    element.addEventListener('keypress', function(event) {
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
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { alert("🚨 חשבונך הושעה ממערכת המשחקים. נא פנה למנהל האתר."); await logout(); return; }
                        if(dbProfile.message) { 
                            alert("💌 הודעה חשובה מהמערכת:\n\n" + dbProfile.message); 
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
            
            document.getElementById('main-action-btn').innerText = cUser ? '⚙ עדכון פרופיל' : 'התחבר / הרשם';
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
            const bU = document.getElementById('box-user'); 
            const bE = document.getElementById('box-email'); 
            const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');
            
            deleteDiv.style.display='none'; titleBox.style.display='none'; cTabContainer.style.display='flex';
            bc.style.display='none';
            
            if (mode === 'LOGIN') { 
                document.getElementById('auth-tab-login').classList.add('active'); document.getElementById('auth-tab-signup').classList.remove('active'); 
                bU.style.display='none'; 
                bE.style.display='block'; 
                bP.style.display='block';
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="אימייל ההתחברות שלך:";
                document.getElementById('lbl-pass').innerText="סיסמת החשבון שלך:";
                btn.innerText='התחבר עכשיו והתחל לשחק';
            }
            else if (mode === 'SIGNUP') { 
                document.getElementById('auth-tab-login').classList.remove('active'); document.getElementById('auth-tab-signup').classList.add('active'); 
                bU.style.display='block'; 
                bc.style.display='block';
                bE.style.display='block'; 
                bP.style.display='block';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="דוא\"ל הרשמי (חשוב לגיבוי ושחזור):";
                document.getElementById('lbl-pass').innerText="סיסמה אישית (מעל 6 תווים חובה):";
                btn.innerText='צור משתמש חדש ונתחיל!';
            }
            else if (mode === 'EDIT') {
                cTabContainer.style.display='none'; titleBox.style.display='block';
                bU.style.display='block'; bc.style.display='block'; bP.style.display='block';
                document.getElementById('f-email').disabled = true; document.getElementById('f-email').value = cUser?.email || '';
                document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                deleteDiv.style.display='block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="כתובת האימייל המזוהה איתך (חסומה לשינוי):";
                btn.innerText='שמור את השינויים החדשים בחשבון';
            }
            else if (mode === 'RECOVERY') {
                cTabContainer.style.display='none'; titleBox.style.display='block'; titleBox.innerText='מעבדת שחזור סיסמאות אישית';
                bU.style.display='none'; bP.style.display='none';
                btn.innerText='שלחו אליי למייל קישור לאיפוס סיסמה';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("מצטערים, אין כעת חיבור רשת פעיל אל בסיס הנתונים.");
            const btn = document.getElementById('auth-exec-btn'); btn.disabled = true; const original = btn.innerText; btn.innerText="מתחבר... ⏳"; showError();
            try {
                if (globalAuthMode === 'LOGIN') {
                    const em = document.getElementById('f-email').value.trim();
                    if(!em || !em.includes('@')) throw new Error("חסר @ או מידע שגוי. עליך לרשום כתובת אימייל אמיתית.");
                    const { error } = await sp.auth.signInWithPassword({ email: em.toLowerCase(), password: document.getElementById('f-pass').value });
                    if(error) showError("הנתונים שהכנסת שגויים, יתכן ויצרת את החשבון בעזרת מייל אחר?"); else { closeModal('auth-modal'); await checkUser(); }
                } else if (globalAuthMode === 'SIGNUP') {
                    const nick = document.getElementById('f-user').value.trim(); const mail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const cCol = document.getElementById('f-color').value;
                    if(p.length < 6 || !mail.includes('@') || !nick) throw new Error("עליך לוודא שהאימייל תקין, הסיסמה באורך של לפחות 6 תווים והשם הוזן כראוי.");
                    
                    const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick, color: cCol } } });
                    if(error) showError(error.message.includes('already') ? "כתובת מייל או משתמש כבר נתפסו פה בעבר במערכת!" : error.message);
                    else { 
                        if(data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nick, color: cCol, banned: false, message: null }); }
                        closeModal('auth-modal'); await checkUser(); alert("רישום הושלם בהצלחה מדהימה! צא לדרך!");
                    }
                } else if (globalAuthMode === 'EDIT') {
                    const nK = document.getElementById('f-user').value.trim(); const pP = document.getElementById('f-pass').value.trim(); const cc = document.getElementById('f-color').value;
                    if(nK) { await sp.auth.updateUser({ data: { nickname: nK, color: cc } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: nK, color: cc }); }
                    if(pP && pP.length >= 6) { await sp.auth.updateUser({ password: pP }); }
                    closeModal('auth-modal'); await checkUser(); alert("שמור על מוד הניצחון! ערוך ועודכן!");
                } else if (globalAuthMode === 'RECOVERY') {
                    const emailF = document.getElementById('f-email').value.trim();
                    if(!emailF.includes('@')) throw new Error("אנא ספק לנו כתובת מלאה ומהימנה עבור לינק החזרה שלך.");
                    const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
                    if (error) throw new Error("שגיאה! האימייל המצויין לא קושר לכאן מעולם למערכת הזו.");
                    else { alert("משקולת הצלה שוחררה בהצלחה במערכת אל הדואר שלך!"); setAuthUI('LOGIN'); }
                }
            } catch(e) { showError(e.message); } finally { btn.disabled = false; btn.innerText = original; }
        }

        async function deleteSelf() {
            if(!confirm("האם אתה בטוח בכוונה למחוק לחלוטין את רשומת השחקן שלצמיתות תיעלם מתיקיות שרת הדרופ של הענן?! (הדבר איננו ניתן לאחזור סופי!)")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("גזמנו עקבות לחלוטין ברכות מהשולחן, פרופיל כוסה לעולמי עד!"); closeModal('auth-modal'); cUser = null; updateUI(); } catch (err) { alert(err.message); }
        }

        // אפשרות חדשה ללחיצה על קוד התאמות נראות הנתונים אחיד למשוב המנהלים ב"PLAY":
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">טוען את המדדים מארכיון... 🔄</p>'; fList.innerHTML = '<p style="text-align:center;">מעמיס משאבי פניות... 🔄</p>';
            
            try {
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); if(pErr) throw pErr;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `<div class="user-row" style="border-right: 5px solid ${u.color || '#fff'}; margin-bottom:10px;"><div style="flex-grow:1; margin-right:15px;"><strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong><div style="font-size:0.8rem; color:#777;">ID: ${u.user_id}</div>${u.banned ? '<span style="color:#ff4757; font-size:0.75rem;">🚫 מושעה חסימה במלוא מובן התוצר</span>' : '<span style="color:#2ecc71; font-size:0.75rem;">✅ אקטיבי בהתרצות נראות קיר מופשט</span>'}</div><div style="display:flex; flex-direction:column; gap:5px;"><button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 תכתוב לו הודעה אישית פתיחה</button><button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 לשחרר מאילוצי המנעול (בטל חסימה)' : '🚫 תכניס חרמש ומנע מגישות פעם וגמור!'}</button><button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ רחם מנקה שרת חתול מובהק</button></div></div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">מוזר... לא מזהים נדבקי דאטה של שחקנים. צומח בעיות אכלוס שרירים.</p>';
                
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); if(fErr) throw fErr;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `<div class="feedback-row" style="margin-bottom:10px;"><div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span style="color:var(--primary); font-weight:bold;">שם סוג הבהרות: ${x.topic}</span><button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחיקת שוברי שרשראות</button></div><div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; margin:5px 0;">"${x.text}"</div><div style="color:#a4b0be; font-size:0.8rem; display:flex; justify-content:space-between;"><span>פגע במשתמש (מייל מקשר דרוזסו): <b>${x.user_email}</b></span></div></div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">כל משאבי המצפון במצב נפש תכול ריק.. אנשים שקטים מאוד בלי תקלות לפחות.</p>';
                
            } catch(e) { uList.innerHTML = `<p style="color:#ff4757;">שחיקה ביד סופא. רדיוס משאבת גמיל דוחף שיבוש כנגד... ${e.message}<br></p>`; fList.innerHTML = uList.innerHTML; }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        async function adminSendMsg(uid) { let theM = prompt("אנא הבע את כתיבת טקסט המילים המותאם פוסט בפופאפ אליו למשתמש תפסיק:"); if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("סינדיקט הוקם ומכתבים תכוסים משב ערוכים לארטיפאקט הלוחש קבע!"); loadAdminData();} }
        async function adminToggleBan(uid, wasBanned) { if(confirm("משאיל על ערוצנו באשר מוחק קווי יכולות התחברו אל התכנון באישורים ברשות אליו מגיבים מילון?")) { await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert("אמנות השיקום נפערו ברוך נמרצות מסכי הקדושות אל טווח המסנן!"); loadAdminData(); } }
        async function adminDelUser(uid) { if(confirm("לקריסות לפרצות איש נזעף תנזלו לכל דיליט מהיקומי מחזור צעיר סגר מסככם?! עקירת תמיהה בטוחה!")) { await sp.from('profiles').delete().eq('user_id', uid); alert("חילוצים מתהלכים והגיס של הגבור ניחם אל מרחקים אלפא זרוק!"); loadAdminData(); } }
        async function adminDelFeedback(fid) { if(confirm("סיים את תהפוכת החלפת המילים אל הבחן בור תגובה לחץ ניטרול כפול ככל הפחות מסכים מליצה מרוקנית נמוגה סוגר מעגליו?")) { await sp.from('feedbacks').delete().eq('id', fid); alert("נוסף טיוח שואף פשט משמדת ניתורים!"); loadAdminData(); } }

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
