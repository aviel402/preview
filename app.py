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
        
        /* User Pill Modified to take color */
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
                <a onclick="alert('טבלאות דירוג ציבוריות תוכנות בעדכון הבא!')">טבלאות</a>
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

    <!-- מרכז האבטחה (משודרג לממשק צבע מותאם אישית ומבוסס דוא"ל נקי בלבד!) -->
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
                <input type="email" id="f-email" class="input-box" placeholder="שם-השחקן@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר לך כינוי לתצוגה במשחק:</label>
                <input type="text" id="f-user" class="input-box" placeholder="שם במשחק או כינוי מזהה">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע הזיהוי שלך למראה אישי בטבלאות:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (מעל 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">היכנס לארקייד עכשיו</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לחלוטין משרת</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן למעבר לשחזור</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות</u></p>
        </div>
    </div>

    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד חכמה המספקת משחקי דפדפן משעשעים ומרובי ז'אנרים. כל המשחקים ללא הורדות!</p>
                <h3 style="color: #a29bfe; margin-top:10px;">אודות היוצר</h3>
                <p>נוצר על ידי <strong>אביאל</strong>.<br>כתובת אימייל: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- מודל שליחת הודעות אימייל ומשוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת פניה/משוב</h2>
            <div class="form-group"><label>נושא הפנייה:</label><select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'"><option value="" disabled selected>-- בחר --</option><option value="bug">תקלה או בעיה (Bug)</option><option value="idea">רעיון שדרוג</option><option value="other">כללי/פניה ישירה לאדמין</option></select></div>
            <div class="form-group hidden-group" id="fb-text-box"><label>נא פרט כאן בהרחבה:</label><textarea id="fb-text" rows="5"></textarea><button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שגר אל השמיים 🚀</button></div>
        </div>
    </div>

    <!-- פאנל ניהול אדמין מתקדם ועצמתי -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">מסוף ניהול כח עליון (אדמין)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול והגדרת שחקנים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">תיבת משוב ובאגים 📥</button>
            </div>
            
            <!-- מערכת רשימת שחקנים -->
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            
            <!-- מערכת פניות והודעות -->
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("שגיאה! הלקוח כשל לטעון. המסד למטה."); }
        
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
                // משיכת מאגר הפרופילים כדי לעדכן צבע לבר החליפי ולבדוק אם חסמו אותו! או שלחו לו מכתב!
                try {
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { alert("🚨 מנהל התחנה נעל משתמש זה לצמיתות ממשחקים פה בשרתים. שלום ולא להתראות!"); await logout(); return; }
                        if(dbProfile.message) { 
                            alert("💌 הודעה ממשואה המערכת המרכזית:\\n" + dbProfile.message); 
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
                // הלבשת הצבע שהגיבור החמוד בחר לעצמו
                pill.style.borderColor = cUser.customColor;
                document.getElementById('nickname-display').style.color = cUser.customColor;
            } else { pill.style.display = 'none'; }
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ עריכה' : 'התחבר / הרשם';
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
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל מזהה חשבון:'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמת חשבון:'; 
                btn.innerText='בצע התחברות לשרת'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='דוא"ל ממשי לצורך אישורים וחזרה:';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי חופשי לתצוגה לחברים:'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='קבע לך סיסמת מסד אישית:'; 
                btn.innerText='רישום דנדש והמראה!'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז שליטה אישית ועריכה'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='תיבה נעולה קיימת אצלך:'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='באפשרותך להחליף כינוי עכשווי:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='אם רצוי לעדכן סיסמה ציין פה (אחרת אל תיגע):';
                btn.innerText='קבע שינויים ושמור הגדרותיי'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='זקוק לקו מילוט וסיסמה שאבדה?'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='איזה דואר עלינו לאתר פה לאיפוס מחדש?'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='שידור חי לשליחת כתובת השחזור בדוא"ל!';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("הממסד מאופס ולא נטען החיבור לגוגל אלא מקווקוו. ממתין.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'מצפין ומיירט נתונים ל-Database... 🔄';
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
            if(!email || !p) return showError("נורא קשה לנחש כשאין לא סיסמה ולא חשבון.");
            if(!email.includes('@')) return showError("סליחה גבר... חסרה פה תגידת כתובת שטחון נורמלית לאימיילים בטקסט הזה.");
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) return showError("מיסמכים הלוו חיכוך או סיסמת הענן שגויה לזרים!");
            else { closeModal('auth-modal'); await checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const email = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const clr = document.getElementById('f-color').value;
            if(!nickname || !email || !p) return showError("אל תחצה קו טופס בלי שלושת מפתחות אלו!");
            if(!email.includes('@')) return showError("רמות תקן אינן עוברות - זרוק אימייל רגיל!");
            if(p.length < 6) return showError("לא מרשה מערכת הניראות להרים עוגן ללא כספת 6 סיפרות לפחות.");

            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) return showError(error.message.includes('already') ? "צצ! מיליות זה כבר שייך לאחר שבארקייד!" : error.message);
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); alert("קפיצת הצלחה בוצעה, פרופיל אושש בעת הרמה פנימה!"); closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim(); const newC = document.getElementById('f-color').value;
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN, color: newC }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            closeModal('auth-modal'); await checkUser(); alert("שמור על המעבד ירח... נרשם חדש למסלולי העריכה!");
        }

        async function doRecovery() {
            const givenEmail = document.getElementById('f-email').value.trim();
            if(!givenEmail || !givenEmail.includes('@')) return showError("תן לה בכתובת המיל כדי שהאיפוס יראה אותך בכללל");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail.toLowerCase());
            if (error) showError("יש תקלה פוסט כזה במחסן השרתים האמיתי");
            else { alert("ישר לפח העליון או תיקיית עיקרי (אולי זבל? מי יודע) תקבל את קשירת הקסם השוטפת למיצג השיחזורי!"); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            if (!confirm("כדאי לך מאוווד לחשוב פעמיים חברי. הרשומות גובו בעקשנות ואין צ'אנס לשחזר גריסות מערכת! אישור אחרון לחדילת חשבון אישי?")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("נרצח הפרופיל והדף הלוויה הוכפל בענן."); closeModal('auth-modal'); cUser = null; updateUI(); } catch (err) { alert(err.message); }
        }

        /* --------------------------
           כללי משוב
           -------------------------- */
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; const tx = document.getElementById('fb-text').value; if(!tx || !t) return; 
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'משתמש בלתי מוכר (Anon)', topic: t, text: tx }); 
                if(error) throw error;
                alert('רעיון מצויין... הטקסט שוגר היטב פנימה אלינו להסתכלות!'); 
            } catch (err) { alert("אם קרתה תקלה יכול להיות שלא אפשרת פונקציות להקמה אל Database Feedbacks - בדוק Policies שם! (RLS: Add Insert Rule)"); } 
            closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; document.getElementById('fb-text-box').style.display='none'; 
        }

        /* --------------------------
           כלי קסם אדמין אבסולוטי: הודעות + חסימות + מחיקות מלאכות
           -------------------------- */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">טוען קבצי מנהל מ-Supabase... 🔄</p>'; fList.innerHTML = '<p style="text-align:center;">סורק מכתבי אוויר מופעל... 🔄</p>';
            
            try {
                // הבאת נתוני שחקנים מאושפזים בפרופיל הרכז 
                const { data: pList, error: pError } = await sp.from('profiles').select('*');
                if(pError) throw pError;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777; font-family:monospace;">ID: ${u.user_id}</div>
                            ${u.banned ? '<span style="display:inline-block; margin-top:3px; background:rgba(255,0,0,0.2); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#ff4757;">🚫 סילוק מהשרת מתמשך מיושם</span>' : '<span style="display:inline-block; margin-top:3px; background:rgba(0,255,0,0.1); padding:1px 6px; border-radius:5px; font-size:0.75rem; color:#2ecc71;">✅ משחק פעיל חוקי</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px; justify-content:center;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 תזרוק לו הודעה</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 תחזיר ממש להילחם' : '🚫 תעיף למנעולים עכשיו'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ תחריב דמו לצמיתות (דיליט)</button>
                        </div>
                    </div>
                    `).join('');
                } else uList.innerHTML = '<p style="color:#a4b0be; text-align:center;">לא מצאתי שחקנים לאישורך... כנראה אין Profiles לחלוץ!</p>';
                
                // הזרקת המכתבי קריאות של העמך 
                const { data: fListDb, error: fError } = await sp.from('feedbacks').select('*');
                if(fError) throw fError;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `<div class="feedback-row"><div style="margin-bottom:8px;"><span style="color:var(--primary); font-size:1rem; font-weight:bold;">נושא המשאב פניות פלדינ: ${x.topic}</span></div><div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; font-size:0.95rem; color:#eee;">"${x.text}"</div><div style="color:#a4b0be; font-size:0.8rem; margin-top:10px; display:flex; justify-content:space-between;"><span>שליח במייל סביבות העוצר: <b>${x.user_email}</b></span><span>בתאריך עקומ: ${(new Date(x.created_at)).toLocaleDateString()}</span></div></div>`).join('');
                } else fList.innerHTML = '<p style="color:#a4b0be; text-align:center;">קפסולת הפניות צהובה ומבריקה ללא טיפות משב משלחו עז! עזור להם לפרסם דאגות.</p>';
                
            } catch(e) { 
                console.error("בעיית מנהל במסד הארגוני: ", e.message);
                uList.innerHTML = `<p style="color:#ff4757; text-align:center;">תקלת פוסינג Supabase: ${e.message}<br>לפחות ראה שפתחת Policy כ-SELECT במסד כנגד תא כוח מזה!</p>`; 
                fList.innerHTML = uList.innerHTML; 
            }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        async function adminSendMsg(uid) {
            let theM = prompt("הכתב פה דבר בשליחת כרוז לשחקן החצוף או למצטיין (קופץ יחידה):");
            if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("פקס טראנסלייט שורת ההודעה בוצעת בהצלחה ויצוץ לברנש בבאפרת קהלים סנסה!"); loadAdminData();}
        }

        async function adminToggleBan(uid, wasBanned) {
            if(confirm("שיקול מהיר על מעבר ציוות גיל למשתמש רדנק זה בסוויפת האזהרות?")) {
                await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert(!wasBanned ? "הצירים הוערכו והחסם יורש עמוקה בשרטון המסחר סחורת הדרופ (נחסם!)" : "משוחרר לגישה נקייה אל האתר. פחד מאנרגיית הקבר חלף לו בהבטחה!"); loadAdminData();
            }
        }

        async function adminDelUser(uid) {
            if(confirm("אם תשחיז בסרבר ללחוץ דיליט הוא יהרוס פלטפורמת רינדורים אישיות ומעולם האפס המוחלט מתוך הטבלאות. אתה עורך השחקן אכף בפיזית?")) {
                await sp.from('profiles').delete().eq('user_id', uid); alert("נקצרו צריפי נתונים מהשורות, גוויות המשתמש התחסנו מחשבים!"); loadAdminData();
            }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY_HTML (דף תוכן המשחק מותאם לשירותים החדשים זהה לראש בול 100%)
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
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }

        /* חופפים אדמין זהה */
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
            <a href="/" class="brand-logo" title="Arcade Station">Arcade Station</a>
            <div class="top-links"><a href="/">חזרה לראשי</a></div>
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
            <h2 id="auth-edit-title" style="display:none; color: #00cec9; margin-bottom:20px;">עריכת אזור משחק וסיסמאות</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות רגילה</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">אופציה של משתמש כדש</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">רשום אימייל קבוע כאן בערוץ:</label>
                <input type="email" id="f-email" class="input-box" placeholder="example@mail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">הזדהות שלך כשם גיבור לכל שאר חברים בסטיישן:</label>
                <input type="text" id="f-user" class="input-box" placeholder="כנוי מאלף">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע חזק שישמור רקמות (קאסטם):</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה חוסה על הדגל:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>

            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">המשך זרמי מתח אטומים!</button>
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ עזוב כל הווית טבלטים (Delete) 💥</button>
            </div>
            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:#a4b0be; cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>לוצצים מחדש ספק שחזור כדחופ?!</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 תחזיר מעצמיי על חזרה פשוטה של LOGIN קבוע במחשב!</u></p>
        </div>
    </div>

    <!-- פאנל אדמין מיוצא לדף ההרצה להקל מורכבויות רבות מימדים -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">מסוף ניהול כח עליון (אדמין) - שיקוף תחת מעמקי המנוע</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקני ברזל ואבן בסיסים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דליים ושרוקי משוב וכל דבר גבאי צדיקות 📥</button>
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

        document.addEventListener('DOMContentLoaded', () => {
            ['f-email', 'f-user', 'f-pass'].forEach(id => {
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
                        if(profileBase.banned) { alert("אאוט! עמדה זאת הושחלה בענן ומצאת נחלט חלופי הרשעת דסק (חסום מאדמין)... ירד מהמרכז שלט!"); await logout(); return; }
                        if(profileBase.message) { 
                            alert("💌 הועדה הרחבית הפוסט רעדה:\n" + profileBase.message); 
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
            
            document.getElementById('main-action-btn').innerText = cUser ? '⚙ תפקוד העריכה אמתחתי שלי' : 'חבר פלטפורמות מחשוב';
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
                document.getElementById('lbl-email').innerText="שקיפית הדואר שמסגרת בה על הרכב שלנו?";
                document.getElementById('lbl-pass').innerText="אשף חזר והבאת שקעי הזיכרון פה:";
            }
            else if (mode === 'SIGNUP') { 
                document.getElementById('auth-tab-login').classList.remove('active'); document.getElementById('auth-tab-signup').classList.add('active'); 
                document.getElementById('box-user').style.display='block'; 
                bc.style.display='block';
                document.getElementById('box-pass').style.display='block';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="בחר דואל חרמש מהדק באמת לשמירות:";
                document.getElementById('lbl-pass').innerText="נבקש צירוף רעול של גראנדיוזה של 6 מספרים לחקירה:";
            }
            else if (mode === 'EDIT') {
                cTabContainer.style.display='none'; titleBox.style.display='block';
                document.getElementById('box-user').style.display='block'; bc.style.display='block'; document.getElementById('box-pass').style.display='block';
                document.getElementById('f-email').disabled = true; document.getElementById('f-email').value = cUser?.email || '';
                document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                deleteDiv.style.display='block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
                document.getElementById('lbl-email').innerText="אתרוגיות של התיבה שלך לא חריפה בערך החלפני - כסוס:";
            }
            else if (mode === 'RECOVERY') {
                cTabContainer.style.display='none'; titleBox.style.display='block'; titleBox.innerText='גלים חדשים באספקה פוסמית כהסכת מס';
                document.getElementById('box-user').style.display='none'; document.getElementById('box-pass').style.display='none';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("חוט המסננות מתופף ונקש בפס צדדי מטה למגע הרים מסורבל עם התשתית.");
            const btn = document.getElementById('auth-exec-btn'); btn.disabled = true; const original = btn.innerText; btn.innerText="מבצע תקדים, העמוד טוען בקצה...⏳"; showError();
            try {
                if (globalAuthMode === 'LOGIN') {
                    const em = document.getElementById('f-email').value.trim();
                    if(!em || !em.includes('@')) throw new Error("קוד דסק קבע פשט שאין עלון צינורי מושלם תכנן נבזה לאתר כתובות @!");
                    const { error } = await sp.auth.signInWithPassword({ email: em.toLowerCase(), password: document.getElementById('f-pass').value });
                    if(error) showError("פסק סייפי השגיב שזה חתך בעין רכבים וטריים אבן הסיסמא שלך קרסה אל נבחרתו של זיופ יתר איתוריות כרוני..."); else { closeModal('auth-modal'); await checkUser(); }
                } else if (globalAuthMode === 'SIGNUP') {
                    const nick = document.getElementById('f-user').value.trim(); const mail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const cCol = document.getElementById('f-color').value;
                    if(p.length < 6 || !mail.includes('@') || !nick) throw new Error("לא מקובץ באגר הזירו קשר אלים שמסיח מאלו חיות ההרשאות החסין. מסגר מינימום 6 ומעל ורסיות!");
                    
                    const { data: dbHasNick } = await sp.from('profiles').select('nickname').eq('nickname', nick).maybeSingle();
                    if(dbHasNick) throw new Error("הצירין שלך שקע אל השיירי כינויים שכבר נמצאת בידי גיבור אחור שנטבל...");
                    
                    const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick, color: cCol } } });
                    if(error) showError(error.message.includes('already') ? 'אל חותכי הענקים פקעת! היות ובמרומי מסך עכשו נראה שגשר רשמות נתן חניה משלך בשקיבלת לראותו בערוץ רגיל...' : error.message);
                    else { 
                        if(data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nick, color: cCol, banned: false, message: null }); }
                        closeModal('auth-modal'); await checkUser(); 
                    }
                } else if (globalAuthMode === 'EDIT') {
                    const nK = document.getElementById('f-user').value.trim(); const pP = document.getElementById('f-pass').value.trim(); const cc = document.getElementById('f-color').value;
                    if(nK) { await sp.auth.updateUser({ data: { nickname: nK, color: cc } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: nK, color: cc }); }
                    if(pP && pP.length >= 6) { await sp.auth.updateUser({ password: pP }); }
                    closeModal('auth-modal'); await checkUser(); alert("שמור על המקלדת מעתה מעשה הקטפולים גובו טנא...");
                } else if (globalAuthMode === 'RECOVERY') {
                    const emailF = document.getElementById('f-email').value.trim();
                    if(!emailF.includes('@')) throw new Error("אל תקפיל בי רסיסי רעל אם נעלמו רסיסי המסגר אישור אל הדבק @ הנתונים");
                    const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
                    if (error) throw new Error("צלקת ניסיות הפס יורה ללא צרופות!");
                    else { alert("לינק איפוס פוציא אל תסכיפי הפריקים ברורת הדואל!"); setAuthUI('LOGIN'); }
                }
            } catch(e) { showError(e.message); } finally { btn.disabled = false; btn.innerText = original; }
        }

        async function deleteSelf() {
            if(!confirm("אל תשמור ברפליקוס רגישות, האם היבסק מחיקות העיבוד יצויט במקפי החרובים והדשא העלומ לא נצפה נתניה אי אי אי... עדיף דיליט לגמרי?")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("גזמנו עקבותך של השטופים בראווה! הפרופילים משוחררים גמור!"); closeModal('auth-modal'); cUser = null; updateUI(); } catch (err) { alert(err.message); }
        }

        // אותו אדמין מוטמן
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">מעדכן אחי... 🔄</p>'; fList.innerHTML = '<p style="text-align:center;">חוצב סטאטיקות... 🔄</p>';
            
            try {
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); if(pErr) throw pErr;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `<div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};"><div style="flex-grow:1; margin-right:15px;"><strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong><div style="font-size:0.8rem; color:#777;">ID: ${u.user_id}</div>${u.banned ? '<span style="color:#ff4757; font-size:0.75rem;">🚫 משתמש סגור אבן משדל מקרב מסגרת</span>' : '<span style="color:#2ecc71; font-size:0.75rem;">✅ הועבר בסכך הדרכתית לשרתים</span>'}</div><div style="display:flex; flex-direction:column; gap:5px;"><button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 תכתוב לו מברק אמיצים</button><button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 פצץ השבתה שחקנוס' : '🚫 תעיף לממנגנון עכב שחצי'}</button><button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחק לגוון כלים אטומי רציף!</button></div></div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">המזלגות אינן ריקים... אבל אין חפיץ שחקנים לאתר קדחת...</p>';
                
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); if(fErr) throw fErr;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `<div class="feedback-row"><span style="color:var(--primary); font-weight:bold;">רצועת תקדים נושאו אוב: ${x.topic}</span><div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; margin:5px 0;">"${x.text}"</div><div style="color:#a4b0be; font-size:0.8rem; display:flex; justify-content:space-between;"><span>מיזם אל שדה כתובת הדיו: <b>${x.user_email}</b></span></div></div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">דחפו רימונים כחלחלים! לא שלחו סוגי מסרות בכלות תא משוב כוח...</p>';
                
            } catch(e) { uList.innerHTML = `<p style="color:#ff4757;">שיבוש מחלצים בקוד Supabase הפיל שגיאות... ${e.message}<br>פשוט חברו לה Policies מסמך "Select" עבור הרזרבות כדי לאפשר מבטח מסדים!</p>`; fList.innerHTML = uList.innerHTML; }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        async function adminSendMsg(uid) { let theM = prompt("הדלדל עטיפות טמפרית לברנשים בבועת המסר האישית לאחיו החוזר אחיות רשת משוב תחת מסכה:"); if(theM) { await sp.from('profiles').update({ message: theM }).eq('user_id', uid); alert("סינדיקט הוקסן במספר ההמשכים סלופ נארז ונשלח למנחתיו האמיתיות בהרגע סנסורס!"); loadAdminData();} }
        async function adminToggleBan(uid, wasBanned) { if(confirm("דרוש עיצומים ספורת חסמת כבל גולגי רדיו! כובע מורשים סמיר רשת אגנוז לאישורים רשות?")) { await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); alert("נשדך טבעתו אבסולוטיקה משתחררים מסגירות נאספים בטיוב הטרמפ אדוק!"); loadAdminData(); } }
        async function adminDelUser(uid) { if(confirm("עשה כיוון גג עציצי אגדי - דיליט לגמרי סכמת המזרחית! למחוק עליו איחולי קש פחיתיים ולשבור חקרי מימד השלושת אורך משחק סגר פצלי קבר!?")) { await sp.from('profiles').delete().eq('user_id', uid); alert("נתחסד השאריס גנרליסטי מהרזרבות... דילוג נענה"); loadAdminData(); } }

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
