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
# MENU_HTML (ברור, ממוקד אימיילים עם פאנל אדמין עובד)
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
    <script>
        if (window.top !== window.self) { window.top.location = window.self.location; }
    </script>
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
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; font-weight: 500; display: none; }

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
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}

        .about-modal-content { max-width: 650px !important; }
        .about-text p { line-height: 1.6; margin-bottom: 10px; font-size: 1.05rem;}
        .about-text h3 { color: #a29bfe; margin-top: 25px; margin-bottom: 15px;}
        .about-text li { margin-bottom: 12px; }

        /* ניהול פאנל מנהלים */
        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition:0.3s;}
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; border-bottom:2px solid var(--accent); }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; padding-left: 5px; }
        .user-row, .feedback-row { background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align:right;}
        .user-row { display: flex; justify-content: space-between; align-items: center; border-right: 4px solid var(--primary);}
        .feedback-row { border-right: 4px solid var(--accent); }
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
                <a onclick="alert('מודול טבלאות דירוגים יתווסף בהמשך הפיתוח! 🥇')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
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

    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות מתקדמות</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">חשבון חדש</button>
            </div>
            
            <div class="form-group" id="box-nickname" style="display:none;">
                <label>איך תרצה שיקראו לך במשחקים?</label>
                <input type="text" id="f-nickname" class="input-box" placeholder="לדוגמה: מלך הארקייד">
            </div>
            <div class="form-group" id="box-email">
                <label>כתובת דואר אלקטרוני (Email):</label>
                <input type="email" id="f-email" class="input-box" placeholder="כתובת אימייל אמיתית...">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">התחבר לאתר</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לתמיד</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לחלון שחזור.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור להתחברות רגילה</u></p>
        </div>
    </div>

    <!-- אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station | Hub</h2>
            <div class="about-text" style="text-align: right; color: var(--text-main); font-size: 1.05rem; padding: 10px;">
                <p><strong>Arcade Station | Hub</strong> הוא אתר משחקים בדפדפן המאפשר שמירת התקדמות למשתמשים רשומים.</p>
                <p>האתר מציג משחקים ייחודיים שכולם זמינים ישירות ללא הורדה.</p>
                <h3 style="color: #a29bfe;">יוצר האתר</h3>
                <p>נוצר על ידי <strong>אביאל</strong>.</p>
                <p>מייל תמיכה: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת משוב להנהלה</h2>
            <div class="form-group"><label>באיזה נושא תרצה לפנות?</label><select id="fb-topic" class="input-box" onchange="updateFeedbackUI()"><option value="" disabled selected>-- בחר --</option><option value="דיווח על באג/תקלה">תקלה טכנית / משחק לא טוען</option><option value="הצעת ייעול">רעיונות ושיפורים</option><option value="אחר">משהו אחר כללי</option></select></div>
            <div class="form-group" style="display:none;" id="fb-game-box"><label>זה נוגע למשחק ספציפי?</label><select id="fb-game" class="input-box"><option value="ראשי - האתר הכללי">לא, לאתר הכללי</option><option value="הישרדות">הישרדות</option><option value="Gold Forest">Gold Forest</option><option value="Genesis">Genesis</option></select></div>
            <div class="form-group" style="display:none;" id="fb-text-box"><label>נא פרט כאן בהרחבה:</label><textarea id="fb-text" class="input-box" rows="4"></textarea><button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שלח משוב אל השרת 🚀</button></div>
        </div>
    </div>

    <!-- אדמין פאנל שעובד ומושך נתונים אמיתיים! -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">פאנל הנהלה - Secret Base</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול משתמשים (טבלת Profiles)</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר אדמין ותקלות 📥</button>
            </div>
            <div id="section-users" class="admin-section active">
                <div class="user-list" id="admin-user-list">
                    <p style="color:#a4b0be; text-align:center;">טוען משתמשים ממסד הנתונים...</p>
                </div>
            </div>
            <div id="section-feedbacks" class="admin-section">
                <div class="feedback-list" id="admin-feedback-list">
                    <p style="color:#a4b0be; text-align:center;">טוען הודעות ומכתבים...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // חשוב! להזין בחזרה את כתובת ה-URL של הפרויקט
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } 
        catch(e) { console.error("שגיאת התחברות ל-Supabase", e); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-nickname', 'f-pass', 'f-email'].forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    el.addEventListener('keypress', function(event) {
                        if (event.key === 'Enter') {
                            event.preventDefault();
                            executeAuthAction();
                        }
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
            updateUI();
        }

        function updateUI() {
            // זיהוי אדמין תקין וללא שגיאות באותיות קטנות או גדולות
            const isAdm = cUser && cUser.email && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ שינוי נתונים' : 'התחברות | יצירת משתמש';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            
            // הצגת כפתור אדמין אם המייל מזהה את אביאל
            const adminBtn = document.getElementById('admin-btn');
            if(adminBtn) adminBtn.style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-nickname').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            globalAuthMode = mode; showError();
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bNick = document.getElementById('box-nickname'); const bEmail = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');
            const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none';

            // שיניתי לממשק ברור רק על בסיס אימייל!
            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bNick.style.display='none'; 
                bEmail.style.display='block'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה אישית:'; btn.innerText='כניסה לאתר 🎮';
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bNick.style.display='block'; 
                bEmail.style.display='block'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='צור סיסמה (6+ תווים):'; btn.innerText='צור לי חשבון חדש בארקייד';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז אישי למשתמש'; tabsCon.style.display='none';
                bNick.style.display='block'; document.getElementById('f-nickname').value = cUser?.user_metadata?.nickname || ''; 
                bEmail.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='שינוי סיסמה (השאר ריק אם לא תרצה):';
                btn.innerText='עדכן שמירה'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מערכת שחזור סיסמה מאובטחת'; tabsCon.style.display='none';
                bNick.style.display='none'; 
                bEmail.style.display='block';  
                bP.style.display='none'; btn.innerText='שחזר באמצעות האימייל שלי 📧';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("נראה שהשרת אופליין. ודא כי כתובת ה-URL למסד מוזנת כראוי בקוד.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'מחשב ומאמת מסמכים... ⚙️';
            showError();

            try {
                if (globalAuthMode === 'LOGIN') await doLogin();
                else if (globalAuthMode === 'SIGNUP') await doSignUp();
                else if (globalAuthMode === 'EDIT') await doEditProfile();
                else if (globalAuthMode === 'RECOVERY') await doRecovery();
            } catch(e) { showError(e.message || "שיבוש פתאומי במסד."); } 
            finally { btn.disabled = false; btn.innerText = textOrig; }
        }

        async function doLogin() {
            const theMail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!theMail || !p) return showError("חובה להזין את כל השדות בשביל להיכנס אלוף!");
            
            const { error } = await sp.auth.signInWithPassword({ email: theMail.toLowerCase(), password: p });
            if(error) return showError("האימייל או הסיסמה שגויים. נסה שנית!");
            else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nick = document.getElementById('f-nickname').value.trim(); 
            const mail = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value;
            
            if(!nick || !mail || !p) return showError("אנא השלם כינוי, אימייל אמיתי וסיסמה.");
            if(!mail.includes('@')) return showError("יש להזין אימייל בתצורה תקנית (לדוגמה me@gmail.com).");
            if(p.length < 6) return showError("אבטחת המערכת דורשת לפחות 6 תווים בסיסמה!");

            // בדיקת קיום שם במשחק בטבלה
            const { data: exist } = await sp.from('profiles').select('nickname').eq('nickname', nick).maybeSingle();
            if (exist) return showError(`הכינוי '${nick}' תפוס בשרת. אולי אתה גיבור מקורי אז בחר שם אחר.`);

            const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick } } });
            
            if (error) {
                if (error.message.includes("already registered")) return showError("כתובת האימייל הזו כבר תפוסה ורשומה אצלנו במסד! חזור למסך 'התחברות'.");
                return showError("משהו חרק שם בשרת: " + error.message);
            }
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nick }); 
                checkUser(); alert("הרשמה עברה בהצלחה פנומנלית! ברוך הבא 🔥"); closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-nickname').value.trim(); 
            const newPass = document.getElementById('f-pass').value.trim();
            if(newN) { 
                await sp.auth.updateUser({ data: { nickname: newN } }); 
                await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN }); 
            }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            closeModal('auth-modal'); checkUser(); alert("השינויים נשמרו בחשבונך!");
        }

        async function doRecovery() {
            const mail = document.getElementById('f-email').value.trim();
            if(!mail || !mail.includes('@')) return showError("יש להזין אימייל מדויק כדי למשוך את השמירה אל התיבה.");
            const { error } = await sp.auth.resetPasswordForEmail(mail.toLowerCase());
            if (error) showError("שגיאה, האם האימייל הזה אכן רשום בתחנת המשחקים שלנו?");
            else { alert("שחזור התבצע! 📩 צוות הטילים שלנו שלח כרגע מייל ישירות אליך לחילוץ סיסמה."); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            const isSure = confirm("למחוק ולפוצץ לצמיתות? אין חזרה על תהליך קשוח כזה... \nזה מאפס הכל. למחוק בטוח?");
            if (!isSure) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("המחיקה שלמה עקב דרישתך."); 
                closeModal('auth-modal'); cUser = null; updateUI(); 
            } catch (err) { alert(err.message); }
        }

        /* --- מודול פידבק חכם --- */
        function updateFeedbackUI() { 
            const v = document.getElementById('fb-topic').value; 
            document.getElementById('fb-game-box').style.display = v ? 'block' : 'none'; 
            document.getElementById('fb-text-box').style.display = v ? 'block' : 'none'; 
        }
        
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; 
            const g = document.getElementById('fb-game-box').style.display === 'block' ? document.getElementById('fb-game').value : 'כללי'; 
            const tx = document.getElementById('fb-text').value; 
            if(!tx) return; 
            try { 
                await sp.from('feedbacks').insert({ 
                    user_email: cUser ? cUser.email : 'משתמש אנונימי מהרחוב', 
                    topic: t, game: g, text: tx 
                }); 
                alert('דואר המשוב שוגר בהצלחה למחנה ההנהלה, תודה שאתה תורם לתחנה שלנו ✉️'); 
            } catch (err) { alert("ישנה בעיה בשילוח, מצטערים."); } 
            closeModal('feedback-modal'); document.getElementById('fb-text').value=''; 
        }

        /* === פונקציות פאנל אדמין מתפקד === */
        function switchAdminTab(tab) {
            document.getElementById('tab-users-btn').classList.toggle('active', tab === 'users');
            document.getElementById('tab-feedbacks-btn').classList.toggle('active', tab === 'feedbacks');
            document.getElementById('section-users').classList.toggle('active', tab === 'users');
            document.getElementById('section-feedbacks').classList.toggle('active', tab === 'feedbacks');
        }

        async function loadAdminData() {
            if (!sp || !cUser || cUser.email.toLowerCase() !== 'x0583289789@gmail.com') return;

            // 1. קבלת כל הפרופילים שנרשמו (שמנים במסד profiles)
            const listUsers = document.getElementById('admin-user-list');
            try {
                const { data: users, error: err1 } = await sp.from('profiles').select('*');
                if (err1) throw err1;
                if (users && users.length > 0) {
                    listUsers.innerHTML = users.map(u => 
                        `<div class="user-row">
                            <span style="font-weight:bold; color:var(--text-main);">🎮 כינוי במשחק: ${u.nickname}</span>
                            <span style="color:var(--text-sub); font-size: 0.85em;">User ID: ${u.user_id.substring(0,8)}...</span>
                        </div>`
                    ).join('');
                } else {
                    listUsers.innerHTML = `<p style="color:#a4b0be; text-align:center;">המסד נקי כרגע ממשתמשים 🤷‍♂️</p>`;
                }
            } catch (error) { listUsers.innerHTML = `<p style="color:#ff4757; text-align:center;">נכשל במשיכת רשימת שחקנים (ודא שטבלת Profiles קיימת עם נתונים) אחי.</p>`; }

            // 2. קבלת פידבקים שנשלחו לאתר (טבלת feedbacks)
            const listFeeds = document.getElementById('admin-feedback-list');
            try {
                const { data: feeds, error: err2 } = await sp.from('feedbacks').select('*');
                if (err2) throw err2;
                if (feeds && feeds.length > 0) {
                    listFeeds.innerHTML = feeds.map(f => 
                        `<div class="feedback-row">
                            <div style="color:var(--accent); font-weight:bold; margin-bottom:5px;">📝 [${f.game}] - ${f.topic}</div>
                            <div style="color:#a4b0be; font-size:0.85em; margin-bottom:10px;">👤 שוגר ממייל: ${f.user_email}</div>
                            <div style="background:rgba(0,0,0,0.5); padding:10px; border-radius:6px; font-size:0.95em;">"${f.text}"</div>
                        </div>`
                    ).reverse().join(''); // Reverse ככה שהחדשים יופיעו תמיד למעלה
                } else {
                    listFeeds.innerHTML = `<p style="color:#a4b0be; text-align:center;">הכל דבש ושלם אחי, אף אחד לא פתח כרטיסי תלונה כרגע 🥳</p>`;
                }
            } catch (error) { listFeeds.innerHTML = `<p style="color:#ff4757; text-align:center;">טבלת פידבקים ריקה או נעדרת...</p>`; }
        }

        async function openAdminModal() { 
            openModal('admin-modal'); 
            switchAdminTab('users');
            loadAdminData(); // טוען בזמן אמת בחי לחיצה !
        }
        
        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY_HTML (מעודכן להיות מקביל ולפעול עם מייל נקי)
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
        nav { height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000; }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .top-links { display: flex; gap: 20px; align-items: center; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: #00cec9; }
        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; display: none; font-weight: 500;}
        .btn { border: none; padding: 8px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-primary { background: #00cec9; color: #000; }
        .btn-danger { background: #ff4757; color: #fff; }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: #a4b0be; }
        .input-box { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station">Arcade Station</a>
            <div class="top-links"><a href="/">חזרה לתחנה הראשית</a></div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>
    
    <iframe src="/{{target}}" title="Game"></iframe>

    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: #00cec9; margin-bottom:20px;">הגדרות מתקדמות</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">צור משתמש</button>
            </div>
            
            <div class="form-group" id="box-nickname" style="display:none;">
                <label>איך תרצה שיקראו לך במשחק?</label>
                <input type="text" id="f-nickname" class="input-box" placeholder="שם לשחקן במערכת...">
            </div>
            <div class="form-group" id="box-email">
                <label>דואר אלקטרוני קבוע:</label>
                <input type="email" id="f-email" class="input-box" placeholder="my_mail@com..">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית וקשוחה:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>

            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">המשך למשחקים בבטחה</button>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור לעמוד האמת הרגיל</u></p>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e){}
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-nickname', 'f-pass', 'f-email'].forEach(id => {
                let el = document.getElementById(id);
                if(el) { el.addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') { event.preventDefault(); executeAuthAction(); }
                });}
            });
        });

        function openModal(id) { document.getElementById(id).classList.add('active'); showError(); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); showError(); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }
        function showError(msg = '') { const el = document.getElementById('auth-error'); el.style.display = msg ? 'block' : 'none'; el.innerText = '⚠️ ' + msg; }

        async function checkUser() { if(!sp) return; const { data } = await sp.auth.getSession(); cUser = data.session?.user || null; updateUI(); }
        
        function updateUI() {
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            document.getElementById('main-action-btn').innerText = cUser ? '⚙ עריכה מתקדמת' : 'התחבר / הרשם';
            document.getElementById('main-action-btn').onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            document.getElementById('logout-btn').style.display = cUser ? 'block' : 'none';
        }
        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function setAuthUI(mode) { 
            globalAuthMode = mode; showError();
            const btn = document.getElementById('auth-exec-btn');
            
            if (mode === 'LOGIN') { 
                document.getElementById('auth-tab-login').classList.add('active'); document.getElementById('auth-tab-signup').classList.remove('active'); 
                document.getElementById('box-nickname').style.display='none'; document.getElementById('box-email').style.display='block'; btn.innerText='התחבר לארקייד כעת';
            }
            else if (mode === 'SIGNUP') { 
                document.getElementById('auth-tab-login').classList.remove('active'); document.getElementById('auth-tab-signup').classList.add('active'); 
                document.getElementById('box-nickname').style.display='block'; document.getElementById('box-email').style.display='block'; btn.innerText='סגור חשבון כמשתמש רשום';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("המערכת מנותקת כרגע ממסד הנתונים!");
            const btn = document.getElementById('auth-exec-btn'); btn.disabled = true; const original = btn.innerText; btn.innerText="שולף ניירת במרכז החלל.. 🌌"; showError();
            try {
                if (globalAuthMode === 'LOGIN') {
                    const theM = document.getElementById('f-email').value; const p = document.getElementById('f-pass').value;
                    const { error } = await sp.auth.signInWithPassword({ email: theM.toLowerCase(), password: p });
                    if(error) showError("נפילת מטח? האימייל שרשמת פשוט אינו בסנכרון עם סיסמה במאגר."); else { closeModal('auth-modal'); checkUser(); }
                } else if (globalAuthMode === 'SIGNUP') {
                    const nick = document.getElementById('f-nickname').value.trim(); const mail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
                    if(!nick || !mail) return showError("בחר את כל התיבות במלואן אדוני הדליפ!");
                    if(p.length < 6) return showError("לפחות אבטח את עצמך במסגרות העולות מ-6 חוליות מחרוזת!");
                    if(!mail.includes('@')) return showError("יש פגום בעסקים שכן כתובת המייל צריכה צורת מפתח אותנטי !");
                    
                    const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick } } });
                    if(error) showError(error.message.includes('already') ? 'שמור לך משתמש כזה בחיווי. השב אל טווח ההתחברות מעתה.' : error.message);
                    else { closeModal('auth-modal'); checkUser(); }
                }
            } catch(e) { showError(e.message); } finally { btn.disabled = false; btn.innerText = original; }
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
