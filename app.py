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
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
        .user-row { flex-direction: row; justify-content: space-between; align-items: center;}
        
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station">Arcade Station</a>
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
                <a onclick="alert('טבלאות דירוג ציבוריות מתוכננות לעדכון הבא!')">טבלאות</a>
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

    <!-- מודל התחברות / הרשמה -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות חשבון ופרופיל</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הרשמה</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל (חובה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="example@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר כינוי למשחקים:</label>
                <input type="text" id="f-user" class="input-box" placeholder="הכנס כינוי...">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע אישי לזיהוי במשחקים:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה (לפחות 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">התחבר לארקייד</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לחלוטין</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לאיפוס</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות</u></p>
        </div>
    </div>

    <!-- מודל אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד חכמה המספקת משחקי דפדפן משעשעים ומרובי ז'אנרים. כל המשחקים זמינים ללא הורדות!</p>
                <h3 style="color: #a29bfe; margin-top:10px;">אודות היוצר</h3>
                <p>נוצר על ידי <strong>אביאל</strong>.<br>כתובת אימייל לפניות: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- מודל שליחת משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת פנייה / משוב</h2>
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'">
                    <option value="" disabled selected>-- בחר נושא --</option>
                    <option value="bug">דיווח על תקלה (Bug)</option>
                    <option value="idea">רעיון או הצעה לשיפור</option>
                    <option value="other">פנייה כללית למנהל</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-text-box">
                <label>פירוט הפנייה:</label>
                <textarea id="fb-text" rows="5"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שלח פנייה 🚀</button>
            </div>
        </div>
    </div>

    <!-- פאנל ניהול אדמין -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">פאנל ניהול שרת (אדמין)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">פניות ומשובים 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("שגיאה בטעינת Supabase"); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {['f-email', 'f-user', 'f-pass'].forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    el.addEventListener('keypress', function(e) {
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
                try {
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { 
                            alert("🚨 החשבון שלך נחסם על ידי מנהל השרת. אתה מנותק כעת."); 
                            await logout(); 
                            return; 
                        }
                        if(dbProfile.message) { 
                            alert("💌 הודעה ממנהל השרת:\n\n" + dbProfile.message); 
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
            btnMain.innerText = cUser ? '⚙ עריכת פרופיל' : 'התחבר / הרשם';
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
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל מזהה (חובה):'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; 
                btn.innerText='התחבר לארקייד'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='כתובת אימייל ליצירת החשבון:';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי להצגה בשרת:'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='בחר סיסמה (לפחות 6 תווים):'; 
                btn.innerText='צור חשבון חדש והיכנס'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='עריכת פרופיל והגדרות אבטחה'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל החשבון (לא ניתן לשינוי):'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי הכינוי שלך:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='עדכון סיסמה (השאר ריק כדי לשמור את הנוכחית):';
                btn.innerText='שמור שינויים בפרופיל'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='שחזור סיסמה מאובטח'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='הזן את האימייל שאיתו נרשמת:'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='שלח לי קישור לאיפוס סיסמה';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("המערכת מנותקת כרגע ממסד הנתונים. נסה לרענן.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'טוען נתונים... 🔄';
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
            const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value;
            if(!email || !p) return showError("יש להזין אימייל וסיסמה כדי להתחבר.");
            if(!email.includes('@')) return showError("כתובת האימייל אינה חוקית.");
            
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) return showError("האימייל או הסיסמה שגויים. נסה שוב.");
            else { closeModal('auth-modal'); await checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); 
            const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value; 
            const clr = document.getElementById('f-color').value;
            
            if(!nickname || !email || !p) return showError("יש למלא את כל השדות כדי ליצור חשבון.");
            if(!email.includes('@')) return showError("כתובת האימייל אינה חוקית.");
            if(p.length < 6) return showError("הסיסמה חייבת להכיל לפחות 6 תווים.");

            const { data: dbHasNick } = await sp.from('profiles').select('nickname').eq('nickname', nickname).maybeSingle();
            if(dbHasNick) return showError("הכינוי שבחרת כבר תפוס על ידי משתמש אחר.");
            
            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) return showError(error.message.includes('already') ? "כתובת האימייל הזו כבר רשומה במערכת." : "שגיאה בהרשמה: " + error.message);
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); 
                alert("ההרשמה בוצעה בהצלחה! ברוך הבא לארקייד."); 
                closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); 
            const newPass = document.getElementById('f-pass').value.trim(); 
            const newC = document.getElementById('f-color').value;
            
            if(newN) { 
                await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); 
                await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN, color: newC }); 
            }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            
            closeModal('auth-modal'); 
            await checkUser(); 
            alert("הפרופיל שלך עודכן בהצלחה!");
        }

        async function doRecovery() {
            const emailF = document.getElementById('f-email').value.trim();
            if(!emailF.includes('@')) return showError("יש להזין כתובת אימייל חוקית לשחזור.");
            const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
            if (error) showError("אירעה שגיאה. בדוק שהאימייל תקין ורשום במערכת.");
            else { alert("קישור לאיפוס סיסמה נשלח לאימייל שלך (בדוק גם בתיקיית הספאם)."); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            if(!confirm("האם אתה בטוח שברצונך למחוק את החשבון לחלוטין? פעולה זו אינה ניתנת לביטול!")) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("החשבון נמחק לצמיתות. להתראות!"); 
                closeModal('auth-modal'); 
                cUser = null; 
                updateUI(); 
            } catch (err) { alert("שגיאה במחיקת החשבון: " + err.message); }
        }

        /* --------------------------
           מערכת פניות ומשוב
           -------------------------- */
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; 
            const tx = document.getElementById('fb-text').value; 
            if(!tx || !t) { alert("חובה לבחור נושא ולכתוב את תוכן הפנייה."); return; }
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'משתמש אורח', topic: t, text: tx }); 
                if(error) throw error;
                alert('הפנייה נשלחה בהצלחה למנהל השרת. תודה רבה!'); 
                closeModal('feedback-modal'); 
                document.getElementById('fb-topic').value=''; 
                document.getElementById('fb-text').value=''; 
                document.getElementById('fb-text-box').style.display='none';
            } catch (err) { alert("שגיאה בשליחת הפנייה. ייתכן שיש חסימה במסד הנתונים."); console.error(err); } 
        }

        /* --------------------------
           פאנל הניהול (אדמין)
           -------------------------- */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); 
            const fList = document.getElementById('admin-feedback-list');
            
            uList.innerHTML = '<p style="text-align:center;">טוען רשימת שחקנים... 🔄</p>'; 
            fList.innerHTML = '<p style="text-align:center;">טוען פניות ומשובים... 🔄</p>';
            
            try {
                // חילוץ שחקנים
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); 
                if(pErr) throw pErr;
                
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777;">ID: ${u.user_id}</div>
                            ${u.banned ? '<span style="color:#ff4757; font-size:0.75rem;">🚫 משתמש חסום</span>' : '<span style="color:#2ecc71; font-size:0.75rem;">✅ משתמש פעיל</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 שלח הודעה למשתמש</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 שחרר חסימה' : '🚫 חסום משתמש'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחיקת משתמש</button>
                        </div>
                    </div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">לא נמצאו שחקנים רשומים.</p>';
                
                // חילוץ משובים
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); 
                if(fErr) throw fErr;
                
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:var(--primary); font-weight:bold;">נושא הפנייה: ${x.topic}</span>
                            <button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחק פנייה</button>
                        </div>
                        <div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; margin:5px 0;">"${x.text}"</div>
                        <div style="color:#a4b0be; font-size:0.8rem;">
                            <span>מאת: <b>${x.user_email}</b></span>
                        </div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">אין פניות או משובים כרגע.</p>';
                
            } catch(e) { 
                uList.innerHTML = `<p style="color:#ff4757;">שגיאה בטעינת הנתונים: ${e.message}</p>`; 
                fList.innerHTML = uList.innerHTML; 
            }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        async function adminSendMsg(uid) { 
            let msg = prompt("הכנס את ההודעה שתרצה לשלוח לשחקן:"); 
            if(msg) { 
                await sp.from('profiles').update({ message: msg }).eq('user_id', uid); 
                alert("ההודעה נשלחה למשתמש בהצלחה!"); 
                loadAdminData();
            } 
        }
        
        async function adminToggleBan(uid, wasBanned) { 
            if(confirm(wasBanned ? "האם לשחרר את החסימה למשתמש זה?" : "האם לחסום משתמש זה מהשרת?")) { 
                await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); 
                alert(wasBanned ? "המשתמש שוחרר." : "המשתמש נחסם."); 
                loadAdminData(); 
            } 
        }
        
        async function adminDelUser(uid) { 
            if(confirm("האם אתה בטוח שברצונך למחוק משתמש זה לחלוטין ממאגר הנתונים?")) { 
                await sp.from('profiles').delete().eq('user_id', uid); 
                alert("המשתמש נמחק בהצלחה."); 
                loadAdminData(); 
            } 
        }

        async function adminDelFeedback(fid) {
            if(confirm("האם אתה בטוח שברצונך למחוק פנייה זו?")) {
                await sp.from('feedbacks').delete().eq('id', fid);
                alert("הפנייה נמחקה.");
                loadAdminData();
            }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY_HTML (זהה לחלוטין ל-MENU_HTML לטובת חוויה חלקה בתוך המשחקים)
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
        :root { --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709; --card-bg: rgba(25, 25, 32, 0.6); --card-border: rgba(255, 255, 255, 0.08); --text-main: #f5f6fa; --text-sub: #a4b0be; }
        body, html { margin: 0; padding: 0; background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        
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
        .btn-primary { background: var(--accent); color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .btn-action-small { background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.1); color: #fff; border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 0.85rem; transition: 0.2s;}
        .btn-action-small:hover { background: rgba(255,255,255,0.2); }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height:90vh; overflow-y:auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: var(--text-sub); font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .input-box:disabled { opacity: 0.5; background: #111; cursor: not-allowed; }
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        .hidden-group { display: none; }
        
        #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: var(--text-sub); font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

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
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 10px; }
    </style>
</head>
<body>
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
                <a onclick="alert('טבלאות דירוג ציבוריות מתוכננות לעדכון הבא!')">טבלאות</a>
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
            <h2 id="auth-edit-title" style="display:none; color: #00cec9; margin-bottom: 20px;">הגדרות חשבון ופרופיל</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הרשמה</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל (חובה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="example@gmail.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">בחר כינוי למשחקים:</label>
                <input type="text" id="f-user" class="input-box" placeholder="הכנס כינוי...">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע אישי לזיהוי במשחקים:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה (לפחות 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="executeAuthAction()">התחבר לארקייד</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לחלוטין</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לאיפוס</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור למסך ההתחברות</u></p>
        </div>
    </div>

    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station</h2>
            <div style="text-align: right; color: #fff; font-size: 1.05rem;">
                <p>מערכת ארקייד חכמה המספקת משחקי דפדפן משעשעים ומרובי ז'אנרים. כל המשחקים זמינים ללא הורדות!</p>
                <h3 style="color: #a29bfe; margin-top:10px;">אודות היוצר</h3>
                <p>נוצר על ידי <strong>אביאל</strong>.<br>כתובת אימייל לפניות: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- מודל שליחת משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת פנייה / משוב</h2>
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'">
                    <option value="" disabled selected>-- בחר נושא --</option>
                    <option value="bug">דיווח על תקלה (Bug)</option>
                    <option value="idea">רעיון או הצעה לשיפור</option>
                    <option value="other">פנייה כללית למנהל</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-text-box">
                <label>פירוט הפנייה:</label>
                <textarea id="fb-text" rows="5"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שלח פנייה 🚀</button>
            </div>
        </div>
    </div>

    <!-- פאנל ניהול אדמין -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">פאנל ניהול שרת (אדמין)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">פניות ומשובים 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("שגיאה בטעינת Supabase"); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {
            ['f-email', 'f-user', 'f-pass'].forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    el.addEventListener('keypress', function(e) {
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
                try {
                    const { data: dbProfile } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
                    if(dbProfile) {
                        if(dbProfile.banned) { 
                            alert("🚨 החשבון שלך נחסם על ידי מנהל השרת. אתה מנותק כעת."); 
                            await logout(); 
                            return; 
                        }
                        if(dbProfile.message) { 
                            alert("💌 הודעה ממנהל השרת:\n\n" + dbProfile.message); 
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
            btnMain.innerText = cUser ? '⚙ עריכת פרופיל' : 'התחבר / הרשם';
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
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל מזהה (חובה):'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; 
                btn.innerText='התחבר לארקייד'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='כתובת אימייל ליצירת החשבון:';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי להצגה בשרת:'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='בחר סיסמה (לפחות 6 תווים):'; 
                btn.innerText='צור חשבון חדש והיכנס'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='עריכת פרופיל והגדרות אבטחה'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל החשבון (לא ניתן לשינוי):'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי הכינוי שלך:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#00cec9';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='עדכון סיסמה (השאר ריק כדי לשמור את הנוכחית):';
                btn.innerText='שמור שינויים בפרופיל'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='שחזור סיסמה מאובטח'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='הזן את האימייל שאיתו נרשמת:'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='שלח לי קישור לאיפוס סיסמה';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("המערכת מנותקת כרגע ממסד הנתונים. נסה לרענן.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'טוען נתונים... 🔄';
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
            const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value;
            if(!email || !p) return showError("יש להזין אימייל וסיסמה כדי להתחבר.");
            if(!email.includes('@')) return showError("כתובת האימייל אינה חוקית.");
            
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) return showError("האימייל או הסיסמה שגויים. נסה שוב.");
            else { closeModal('auth-modal'); await checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); 
            const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value; 
            const clr = document.getElementById('f-color').value;
            
            if(!nickname || !email || !p) return showError("יש למלא את כל השדות כדי ליצור חשבון.");
            if(!email.includes('@')) return showError("כתובת האימייל אינה חוקית.");
            if(p.length < 6) return showError("הסיסמה חייבת להכיל לפחות 6 תווים.");

            const { data: dbHasNick } = await sp.from('profiles').select('nickname').eq('nickname', nickname).maybeSingle();
            if(dbHasNick) return showError("הכינוי שבחרת כבר תפוס על ידי משתמש אחר.");
            
            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) return showError(error.message.includes('already') ? "כתובת האימייל הזו כבר רשומה במערכת." : "שגיאה בהרשמה: " + error.message);
            if (data.user) { 
                await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); 
                alert("ההרשמה בוצעה בהצלחה! ברוך הבא לארקייד."); 
                closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); 
            const newPass = document.getElementById('f-pass').value.trim(); 
            const newC = document.getElementById('f-color').value;
            
            if(newN) { 
                await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); 
                await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN, color: newC }); 
            }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            
            closeModal('auth-modal'); 
            await checkUser(); 
            alert("הפרופיל שלך עודכן בהצלחה!");
        }

        async function doRecovery() {
            const emailF = document.getElementById('f-email').value.trim();
            if(!emailF.includes('@')) return showError("יש להזין כתובת אימייל חוקית לשחזור.");
            const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
            if (error) showError("אירעה שגיאה. בדוק שהאימייל תקין ורשום במערכת.");
            else { alert("קישור לאיפוס סיסמה נשלח לאימייל שלך (בדוק גם בתיקיית הספאם)."); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            if(!confirm("האם אתה בטוח שברצונך למחוק את החשבון לחלוטין? פעולה זו אינה ניתנת לביטול!")) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("החשבון נמחק לצמיתות. להתראות!"); 
                closeModal('auth-modal'); 
                cUser = null; 
                updateUI(); 
            } catch (err) { alert("שגיאה במחיקת החשבון: " + err.message); }
        }

        /* --------------------------
           מערכת פניות ומשוב
           -------------------------- */
        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; 
            const tx = document.getElementById('fb-text').value; 
            if(!tx || !t) { alert("חובה לבחור נושא ולכתוב את תוכן הפנייה."); return; }
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'משתמש אורח', topic: t, text: tx }); 
                if(error) throw error;
                alert('הפנייה נשלחה בהצלחה למנהל השרת. תודה רבה!'); 
                closeModal('feedback-modal'); 
                document.getElementById('fb-topic').value=''; 
                document.getElementById('fb-text').value=''; 
                document.getElementById('fb-text-box').style.display='none';
            } catch (err) { alert("שגיאה בשליחת הפנייה. ייתכן שיש חסימה במסד הנתונים."); console.error(err); } 
        }

        /* --------------------------
           פאנל הניהול (אדמין)
           -------------------------- */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); 
            const fList = document.getElementById('admin-feedback-list');
            
            uList.innerHTML = '<p style="text-align:center;">טוען רשימת שחקנים... 🔄</p>'; 
            fList.innerHTML = '<p style="text-align:center;">טוען פניות ומשובים... 🔄</p>';
            
            try {
                // חילוץ שחקנים
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); 
                if(pErr) throw pErr;
                
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right: 5px solid ${u.color || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${u.color || '#00cec9'}; font-size:1.2rem;">${u.nickname}</strong>
                            <div style="font-size:0.8rem; color:#777;">ID: ${u.user_id}</div>
                            ${u.banned ? '<span style="color:#ff4757; font-size:0.75rem;">🚫 משתמש חסום</span>' : '<span style="color:#2ecc71; font-size:0.75rem;">✅ משתמש פעיל</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:5px;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:#0984e3; border-color:#0984e3;">💌 שלח הודעה למשתמש</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#e1b12c; border-color:#e1b12c;">${u.banned ? '🟢 שחרר חסימה' : '🚫 חסום משתמש'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחיקת משתמש</button>
                        </div>
                    </div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">לא נמצאו שחקנים רשומים.</p>';
                
                // חילוץ משובים
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); 
                if(fErr) throw fErr;
                
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:var(--primary); font-weight:bold;">נושא הפנייה: ${x.topic}</span>
                            <button class="btn-action-small" onclick="adminDelFeedback('${x.id}')" style="color:#ff4757; border-color:#ff4757;">🗑️ מחק פנייה</button>
                        </div>
                        <div style="padding:10px; background:rgba(0,0,0,0.5); border-radius:5px; margin:5px 0;">"${x.text}"</div>
                        <div style="color:#a4b0be; font-size:0.8rem;">
                            <span>מאת: <b>${x.user_email}</b></span>
                        </div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">אין פניות או משובים כרגע.</p>';
                
            } catch(e) { 
                uList.innerHTML = `<p style="color:#ff4757;">שגיאה בטעינת הנתונים: ${e.message}</p>`; 
                fList.innerHTML = uList.innerHTML; 
            }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        async function adminSendMsg(uid) { 
            let msg = prompt("הכנס את ההודעה שתרצה לשלוח לשחקן:"); 
            if(msg) { 
                await sp.from('profiles').update({ message: msg }).eq('user_id', uid); 
                alert("ההודעה נשלחה למשתמש בהצלחה!"); 
                loadAdminData();
            } 
        }
        
        async function adminToggleBan(uid, wasBanned) { 
            if(confirm(wasBanned ? "האם לשחרר את החסימה למשתמש זה?" : "האם לחסום משתמש זה מהשרת?")) { 
                await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); 
                alert(wasBanned ? "המשתמש שוחרר." : "המשתמש נחסם."); 
                loadAdminData(); 
            } 
        }
        
        async function adminDelUser(uid) { 
            if(confirm("האם אתה בטוח שברצונך למחוק משתמש זה לחלוטין ממאגר הנתונים?")) { 
                await sp.from('profiles').delete().eq('user_id', uid); 
                alert("המשתמש נמחק בהצלחה."); 
                loadAdminData(); 
            } 
        }

        async function adminDelFeedback(fid) {
            if(confirm("האם אתה בטוח שברצונך למחוק פנייה זו?")) {
                await sp.from('feedbacks').delete().eq('id', fid);
                alert("הפנייה נמחקה.");
                loadAdminData();
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
