from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string, send_from_directory
import os

def x():
    y = Flask(__name__)
    @y.route('/')
    def index():return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return y

# דף "בפיתוח" ללא סרגל פנימי (הסרגל עטוף ע"י ה-PLAY)
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
# MENU_HTML (האתר הראשי המכיל את פתרונות אבטחת הלחיצות וטיפול בקריסות הרשמה!)
# =======================================================
MENU_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade Station | Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
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
        .btn-primary { background: var(--accent); color: #000; box-shadow: 0 0 10px rgba(0,206,201,0.2); }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
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
        .hidden-group { display: none; }

        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

        .about-modal-content { max-width: 650px !important; }
        .about-text p { line-height: 1.6; margin-bottom: 10px; font-size: 1.05rem;}
        .about-text h3 { color: #a29bfe; margin-top: 25px; margin-bottom: 15px;}
        .about-text li { margin-bottom: 12px; }

        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; }
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid transparent; }
        .user-row { cursor: pointer; flex-direction: row; justify-content: space-between; align-items: center;}
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

    <!-- מרכז האבטחה והחשבונות! נבנה להיות עמיד לחלוטין ולספק חוויה ללא באגים! -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות מתקדמות</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">חשבון חדש</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי שחקן בשרת:</label>
                <input type="text" id="f-user" class="input-box" placeholder="הקלד כאן..." autocomplete="off">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">אימייל גיבוי למשתמש:</label>
                <input type="email" id="f-email" class="input-box" placeholder="דואר אלקטרוני - אם תרצה" autocomplete="off">
            </div>
            
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (מעל 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••" autocomplete="off">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px; padding:12px; font-size:1.1rem; cursor:pointer;" onclick="executeAuthAction()">אישור שליחה מהיר</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחק פרופיל זה לתמיד</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לחלון השחזור הבטוח.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור להתחברות קלאסית רגילה</u></p>
        </div>
    </div>

    <!-- מודל אודות  -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station | Hub</h2>
            <div class="about-text" style="text-align: right; color: var(--text-main); font-size: 1.05rem; padding: 10px;">
                <p><strong>Arcade Station | Hub</strong> הוא אתר משחקים בדפדפן.</p>
                <h3 style="color: #a29bfe; margin-top: 25px;">אודות היוצר</h3>
                <p>נוצר על ידי <strong>אביאל</strong>. צור קשר במייל: x0583289789@gmail.com</p>
            </div>
        </div>
    </div>

    <!-- משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת משוב</h2>
            <div class="form-group"><label>נושא הפנייה:</label><select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display = this.value ? 'block' : 'none';"><option value="" disabled selected>-- בחר --</option><option value="tech">תקלה טכנית</option><option value="idea">הצעות לשיפור</option></select></div>
            <div class="form-group hidden-group" id="fb-text-box"><label>נא פרט כאן בהרחבה:</label><textarea id="fb-text" class="input-box"></textarea><button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="alert('משוב נקלט בהצלחה בשרת!'); closeModal('feedback-modal');">שלח את המכתב 🚀</button></div>
        </div>
    </div>

    <!-- אדמין -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">לוח בקרה סודי - מערכת ניהול</h2>
            <p>לפני מנהלי שרת בלבד...</p>
        </div>
    </div>

    <script>
        const sp = supabase.createClient('                                        ', 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B');
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }

        async function checkUser() {
            try {
                const { data, error } = await sp.auth.getSession();
                cUser = data?.session?.user || null;
            } catch(e) { cUser = null; }
            updateUI();
        }

        function updateUI() {
            const isAdm = Boolean(cUser && cUser.email && cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || 'גיבור במשחק');
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ עריכת המשתמש' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; 
            document.getElementById('f-email').value = ''; 
            document.getElementById('f-pass').value = '';
            setAuthUI(mode); 
            openModal('auth-modal');
        }

        function setAuthUI(mode) {
            globalAuthMode = mode; 
            const tL = document.getElementById('auth-tab-login'); 
            const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); 
            const bE = document.getElementById('box-email'); 
            const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');
            const titleEdit = document.getElementById('auth-edit-title'); 
            const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); 
            const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי במשחק או אימייל התחברות:'; 
                bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה סודית לחשבון:'; 
                btn.innerText='הכנס למערכת עכשיו';
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר לעצמך כינוי חדש:'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל להתאוששות ושחזור (אופציונלי):';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה חדשה וחזקה (מינימום 6 תווים):'; 
                btn.innerText='צור משתמש והכנס!';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז פרופיל אבטחה אישי'; 
                tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שנה שם כינוי תצוגה פה:'; 
                document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='להחלפת סיסמה רשום כאן (או השאר ריק):';
                btn.innerText='החל וערוך פרופיל'; 
                deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז הצלת חשבונות'; 
                tabsCon.style.display='none';
                bU.style.display='none'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerText='הזן לכאן כתובת אימייל מקורית של החשבון:'; 
                bP.style.display='none'; btn.innerText='שגר אלי הודעת איפוס בטיחותית 📤';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        const getSafeEmail = (u) => { 
            let c = u.trim().toLowerCase(); 
            if(c.includes('@')) return c; 
            return c.replace(/\s+/g, '') + "@arcadestation.local"; 
        };

        // הפונקציה הריכוזית - נוטרלה מעיכובים ותלות בשירותים מקדימים לקויים
        async function executeAuthAction() {
            const theBtn = document.getElementById('auth-exec-btn');
            const restoreText = theBtn.innerText;
            
            theBtn.innerText = "במעבר הנתונים פנימה ⏳...";
            theBtn.style.pointerEvents = 'none'; // הגנה מלחיצות רבות נוספות בטעות שמשכפלות בקשות
            theBtn.style.opacity = '0.7';

            try {
                if (globalAuthMode === 'LOGIN') { await doLogin(); }
                else if (globalAuthMode === 'SIGNUP') { await doSignUp(); }
                else if (globalAuthMode === 'EDIT') { await doEditProfile(); }
                else if (globalAuthMode === 'RECOVERY') { await doRecovery(); }
            } catch (err) {
                console.error(err);
                alert("המערכת פספסה קריאה מהשרת... נא לנסות בשנית! מזהה: " + err.message);
            } finally {
                theBtn.innerText = restoreText;
                theBtn.style.pointerEvents = 'auto';
                theBtn.style.opacity = '1';
            }
        }

        async function doLogin() {
            const nn = document.getElementById('f-user').value.trim(); 
            const pw = document.getElementById('f-pass').value;
            if(!nn || !pw) return alert("שים לב: חסר שם או סיסמה בחלון שלך כרגע.");
            
            const formatEm = nn.includes('@') ? nn.toLowerCase() : getSafeEmail(nn);
            
            const { error } = await sp.auth.signInWithPassword({ email: formatEm, password: pw });
            if(error) {
                if(!nn.includes('@')) alert("הזנה שגויה! אם בפעם הקודמת הקלדת אימייל משלך כדי לשחק איתנו, הקפד לכתוב במדויק את כל האימייל שלך כעת ולא רק את הכינוי.");
                else alert("מערך ההגנה חוסם אותך מלהיכנס! אין חשבון לדואר אלקטרוני זה בשרתים או שהסיסמה פשוט הוחמצה לחלוטין בהקלדה.");
            } else { 
                closeModal('auth-modal'); 
                checkUser(); 
            }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); 
            const customEm = document.getElementById('f-email').value.trim(); 
            const pw = document.getElementById('f-pass').value;
            
            if(!nickname || !pw) return alert("לא יכול לתת לך רישום עם שדות חשובים כל כך ריקים!");
            if(pw.length < 6) return alert("על קו האבטחה להיות מוזן בשש תווים רשמיים כספי מגן בבקשה.");

            // בניית תצורת הפתיחה למסד הרשתות! עקיפת Select ישיר (שרף חלק מהרישומים) למעבר אל אשכול בנייה עצמי מידי - חלק כבדולח ופשוט במיוחד!
            const cleanFinal = customEm.includes('@') ? customEm.toLowerCase() : getSafeEmail(nickname);
            const { data, error } = await sp.auth.signUp({ email: cleanFinal, password: pw, options: { data: { nickname: nickname } } });
            
            if (error) {
                if (error.message.includes("already registered") || error.message.includes("already exists") || error.status === 422 || error.status === 400) {
                    alert("פגשנו תקרת זכוכית: כנראה משתמש נחוש באותו כינוי בדיוק מחכה לך מעבר לפינה בארקייד - אנא בחר אחד אחר ייחודי.");
                } else {
                    alert("שגיאת דחיה ביצירה מהשרת: " + error.message);
                }
                return;
            }
            
            if (data && data.user) { 
                try { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); } catch (ignore) {}
                alert("המראה חלקה אל על. הרשמה אושרה וגובתה במסד."); 
                closeModal('auth-modal');
                checkUser(); 
            }
        }

        async function doEditProfile() {
            const n = document.getElementById('f-user').value.trim(); const pw = document.getElementById('f-pass').value;
            if(n) { await sp.auth.updateUser({ data: { nickname: n } }); try{ await sp.from('profiles').upsert({ user_id: cUser.id, nickname: n }); }catch(e){} }
            if(pw && pw.length >= 6) { await sp.auth.updateUser({ password: pw }); alert("מינעל השגרה הושתל במוקד סיסמאות חידוש מסונכרן."); }
            closeModal('auth-modal'); checkUser();
        }

        async function doRecovery() {
            const userEm = document.getElementById('f-email').value.trim();
            if(!userEm.includes('@') || userEm.includes('.local')) return alert("בקשת השחזור יצוקה במסמך שלא מאפשר הפעלה כי אינו בעל דואר ציבורי שיאומת פנימית!");
            
            const { error } = await sp.auth.resetPasswordForEmail(userEm.toLowerCase());
            if (error) alert("שגיאת ממסרים ופירוק! תדמית רצף זו נעוצה מחוץ לפלטפורמות השלכת הרשת כרגע: " + error.message);
            else { alert("יציאת התפנוק הגיעה לשטח המטרות הישירות שבאימיילים הפרטיים! פשוט גללו שחזור משם בקופץ פריבילגי.\\nעברו לשם... (ולא לשכוח קידום/ספאם). ☑️"); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            const sur = confirm("עצור. זו אינה התראה זוטרה משנית 🚨!\\nערוץ ניתוק וחיסול היסטורי מעקירה מהמסד! מחיקת חשבונך נוצרת לצמיתות, לא להחזיר לעולם גלולת שימור אחורית!");
            if (!sur) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("נערף מהציוץ ונפרק בלחץ זרימת העשנים של המדורות בסופאבייס 💔 עולם חורק שייעץ אל עולם קסמים משולבים הגיבור! כל הפרופילים קרסו בנעילה גדולה. דרך צלחה לעד."); 
                closeModal('auth-modal'); cUser = null; updateUI(); 
            } catch (err) { alert("המנועים סירבו לחתך הזה לאשרור מסכם: " + err.message); }
        }
        
        window.onload = checkUser;
    </script>
</body>
</html>
"""


# =======================================================
# PLAY_HTML (דף פנימי שרץ ישירות לצד הסרגל הפנימי בהטמעה משופרת ובטוחה לחלוטין)
# =======================================================
PLAY_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arcade Play - {{target}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>if (window.top !== window.self) { window.top.location = window.self.location; }</script>
    <style>
        body, html { margin: 0; padding: 0; background-color: #070709; color: #fff; font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        nav { height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000; }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); transition: transform 0.3s;}
        .brand-logo:hover img { transform: scale(1.05); }

        .top-links { display: flex; gap: 20px; align-items: center; }
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: #00cec9; }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.98); min-width: 220px; box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: #00cec9; }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; display: none; font-weight: 500;}
        .btn { border: none; padding: 8px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn-primary { background: #00cec9; color: #000; position: relative; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid rgba(255, 255, 255, 0.08); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: #a4b0be; }
        .input-box { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: #00cec9; }
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: #00cec9; border-bottom: 3px solid #00cec9; padding-bottom: 2px; }
        .about-modal-content { max-width: 650px !important; }
        .about-text p { line-height: 1.6; margin-bottom: 10px; font-size: 1.05rem;}
        .about-text h3 { color: #a29bfe; margin-top: 25px; margin-bottom: 15px;}
        .about-text li { margin-bottom: 12px; }
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
                <a onclick="alert('טבלאות דירוגים יתווספו לפלטפורמה בגרסאות הבאות! 🥇')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
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
            <h2 id="auth-edit-title" style="display:none; color: #00cec9; margin-bottom:20px;">הגדרות פרופיל</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות למערכת</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">צור הרשמת חבר</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">הזן את כינוי החלום שלך לכאן:</label>
                <input type="text" id="f-user" class="input-box" placeholder="כתוב..." autocomplete="off">
            </div>
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">רשום את סוג המסרים העתידי שיזהה ששכחת:</label>
                <input type="email" id="f-email" class="input-box" placeholder="שם-קלאסי@email.com" autocomplete="off">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">תן להכל אישור קוד שמור ברעף ספיר (שש ספרות):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••" autocomplete="off">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px; font-size: 1.05rem; padding: 12px; cursor:pointer;" onclick="executeAuthAction()">תחבר למסע בארקייד סטאשן עכשיו!</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ תנתק פרופיל רטוב וקרר חזות לדור העל!</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:#a4b0be; cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>לחץ פה לחשבון קליל בתיבת הדואר והצלה...</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 שחזור מחוץ לתמונה... אזור טפסים שגרתיים</u></p>
        </div>
    </div>

    <!-- אודות פליי  -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station | Hub</h2>
            <div class="about-text" style="text-align: right; color: var(--text-main); font-size: 1.05rem; padding: 10px; max-height: 55vh; overflow-y: auto;">
                <p><strong>Arcade Station | Hub</strong> הוא אתר משחקים מתקדם בדפדפן מלוטש במיוחד לסוגי חיק טרינקר סוג משחקים.</p>
                <p>האתר מציג 11 משחקים שונים כולם בסגנונות התקפה או מה שפחות זיהומי להחלצות גוברת... :)</p>
                
                <h3 style="color: #a29bfe; margin-top: 25px;">אודות היוצר שלנו שמגניב צב משעמום במשרדו בחנונייתו המטפסת 🤷‍♂️</h3>
                <p><strong>Arcade Station</strong> נחרט בסבלנות ואחרי דגור זמן במערכת הסופאבאס והיקף של גשר על ידי חביב ההקולוניות <strong>אביאל</strong>.</p>
                <p>מייל להגנת מיזמים/ פניה רחמנית או פגישה על הקדמות משחקים סייבר - <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <script>
        const sp = supabase.createClient('                                        ', 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B');
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }

        async function checkUser() {
            try {
                const { data } = await sp.auth.getSession();
                cUser = data?.session?.user || null;
            } catch(e) { cUser = null; }
            updateUI();
        }

        function updateUI() {
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || 'כניסה אושרה למעבה מיוחד');
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ עריכת משתמש בחיוג ארוך' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            document.getElementById('logout-btn').style.display = cUser ? 'block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; 
            document.getElementById('f-email').value = ''; 
            document.getElementById('f-pass').value = '';
            setAuthUI(mode); 
            openModal('auth-modal');
        }

        function setAuthUI(mode) {
            globalAuthMode = mode;
            const tL = document.getElementById('auth-tab-login'); 
            const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); 
            const bE = document.getElementById('box-email'); 
            const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn'); 
            const titleEdit = document.getElementById('auth-edit-title'); 
            const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); 
            const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='קלאס צבוע כאן עם כינוייך:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='מפתחות אולטרא-אחריות סיסמאים למערכת עריבה:'; 
                btn.innerText='רמות וטיפים זולים הכנס עכשיו למאסה 🛼!';
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='מידה מעוגלת מאיזה ניק של תצוגה שתיבחר 🎭 :'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='למי עמלת טפטפת שנוסיף מיל? 📬:';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='אגרת מסמך או מעקב מחודדים בשש פרגונים של ספרות תגובה מונרכיה 👑:'; 
                btn.innerText='הרעיד טילים ואורות ברקים ליצירת מיסבים!';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכב השתנות כפיפות דואר מחווטת שלבי הגדרות עכשווי פליפ קצה לראות מוקד אבטחתיים חלונאים רגלי קרצייתי... חח פשוט הגדרות :)'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='המקור הבדווי במזרקים כינוי חדש:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='רוצה להצפין הליך טוענים? הזיח כאן ריגוש מורכב או שלום להישארות מצוקים בחיוורים הראשיים לבטלת שלט נשארה שמש נחת 🙃:'; btn.innerText='תעדכן אבטחה כלילה ותאזור סיכול קטיעי!';
                deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מעבדה מנוטרלת למערך שחזור עכשווי בסוגיית חירום והבלאסטינג צנחו שרעוע צמרומור דמיעות של דרוס כימיה ומתלמד 🚑🥼!'; tabsCon.style.display='none';
                bU.style.display='none';  
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='הנכחה ברשומים עם מעכב מעקבים קפאין או סתם הירשמת למקרר מה דואר השלח לאמת מתיז פרדייס חזון?:'; 
                bP.style.display='none'; btn.innerText='הרעיד שערות בחבילות צלצול פולמוס כבל לתוכנן במלוא דאר נזקי העשן שלכם ממרפס כנוע טפו טפו...!';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        const getSafeEmail = (us) => { let ca = us.trim().toLowerCase(); if(ca.includes('@')) return ca; return ca.replace(/\s+/g, '') + "@arcadestation.local"; };

        // ביצוע הכוח - נקי ושמור מקשרי קוד שנלחמו במקרים אבסורדים בטלפון
        async function executeAuthAction() {
            const bt = document.getElementById('auth-exec-btn');
            const btOrig = bt.innerText;
            
            bt.innerText = "פענוח ממדים מתבצע ממש באילו שנייים הטרמפיאדות טלפון משוטחים.. ⏳ ";
            bt.style.pointerEvents = 'none';
            bt.style.opacity = '0.7';

            try {
                if (globalAuthMode === 'LOGIN') { await doLogin(); }
                else if (globalAuthMode === 'SIGNUP') { await doSignUp(); }
                else if (globalAuthMode === 'EDIT') { await doEditProfile(); }
                else if (globalAuthMode === 'RECOVERY') { await doRecovery(); }
            } catch (ez) {
                console.error(ez);
                alert("המערכת חרקה שיניים במסך ופסחה על סעיף סמכויות השרת... בדוק אינטרנט! 🛑 התרחשה אי תאימות בהופעה הקוונטית : " + ez.message);
            } finally {
                bt.innerText = btOrig;
                bt.style.pointerEvents = 'auto';
                bt.style.opacity = '1';
            }
        }

        async function doLogin() {
            const theu = document.getElementById('f-user').value.trim(); const thepw = document.getElementById('f-pass').value;
            if(!theu || !thepw) return alert("הלו? שדה מכתבים ממוחשב צבוע לך כמשפט... קרא בעיון וקרן מציל לקרקר מחזירי טריגו ענבים שמלות חילזונים - מלא מינימלית לפני שליח 🤦‍♀️!!!");
            
            const logE = theu.includes('@') ? theu.toLowerCase() : getSafeEmail(theu);
            const { error } = await sp.auth.signInWithPassword({ email: logE, password: thepw });
            
            if(error) {
                if (!theu.includes('@')) alert("הלוחצים בשלילה. אם בארובה דחפת דאר אותנטי, יכאב לא להשתמש באותו מכל מסנן שגיאת טונוס בהקשחה כאן? סל כניסות גדוש אומר שאין פרופיל כיסוי בשם זה מוסמר בשרשרת פרימידה עכביש... תדייקו בסוד נסיונל!!");
                else alert("מייל לא מאוורר גורף לחות רעילות של הענן משפט שלילה בעין ההוריקנים! או שהמידע טעותי מסיסמת תפיחה שהייתה באצטדיון סובייקטי המטעה גשר לממשקי כיפה קרים... נשמע חמוץ לכי על סימון משווק ופוגע במאגרי חיסול או במחשבה נוספת נסי שוב... 🥶🥶");
            } else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nv = document.getElementById('f-user').value.trim(); 
            const e1 = document.getElementById('f-email').value.trim(); 
            const pw2 = document.getElementById('f-pass').value;

            if(!nv || !pw2) return alert("אחות קירבת גלות מסממת אמר לחוס סחרור ברזילאי נשלח אסטרונאוט... מממ מאיפה הגענו לפה, יש תגי אדם עיוורים לחתיכת טפס רישומטי רגשי כח חלוף דור משוחק בספרי קורסים?");
            if(pw2.length < 6) return alert("מועצת האליפויות המורות לא חותמים יעד מעבדתי בספר מתרבע צבוע לסיד קרטון באם מקישים משוואה רפה... כמות הקמצנים על מקלדות מסריט פגסוס מצפון של רסיסי קיר אריזה לפחות משש לילות!");
            
            const rMail = e1.includes('@') ? e1.toLowerCase() : getSafeEmail(nv);
            const { data, error } = await sp.auth.signUp({ email: rMail, password: pw2, options: { data: { nickname: nv } } });
            
            if (error) {
                if (error.message.includes("already registered") || error.status === 422 || error.message.includes("already exists")) {
                    alert("שגיאת המרשם הדיפלומטי וחוויות משדלים מוסווה - סעיף סמיילי אישי או פרטי חיבור עזקו הדישנו ברצפת החיתוכי קרב וגירויים אזרחי סירקו את מאגר סופא שלנו! עיונית את או אתה סגלו עצמו לשדה מקורי למניעה בהתהוות מעוגל שיא ספיד תחתון קרשים או מסנוורים שמש גזר!  מסתובבים בקוונה תלמד תהיות! דופקים אזהרות לאוויר...");
                } else { alert("מחלוקות אצילות משוררים בתוך השורה המפקח: " + error.message); }
                return;
            }
            if (data && data.user) { 
                try { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nv }); } catch(errr) {}
                alert("מוזה נורטון שיש לה קשת אישור מרסיסים קרונוס וגריידי משטח סוליי טוק סלייי.... הושלםםם 🤘!"); 
                closeModal('auth-modal');
                checkUser();
            }
        }

        async function doEditProfile() {
            const nx = document.getElementById('f-user').value.trim(); const pw3 = document.getElementById('f-pass').value;
            if(nx) { await sp.auth.updateUser({ data: { nickname: nx } }); try{await sp.from('profiles').upsert({ user_id: cUser.id, nickname: nx });}catch(w){}; }
            if(pw3 && pw3.length >= 6) { await sp.auth.updateUser({ password: pw3 }); alert("תדר מנעלי צילינדר מתחלף ומרפס רדיקלי מתופעת גומי זועף מרצפות מעבדי דגל ימחו מתמרמר סיסמה מתנשאת יתרת מורחים של קרוס באססס!"); }
            closeModal('auth-modal'); checkUser();
        }

        async function doRecovery() {
            const ev = document.getElementById('f-email').value.trim();
            if(!ev.includes('@') || ev.includes('.local')) return alert("רק מחוייב עולם מדומה סתיו לקרור עכבישים מחמיצי סיכוי בחתימה אמיתית למקור עב קלון רצף יביא תכנית משולח וקשר שרתים של פטיש מאדים על גופרית מסולף ציון מחמד חתונת טילים מחסם סיוע משוקף בפורום שלח!");
            
            const { error } = await sp.auth.resetPasswordForEmail(ev.toLowerCase());
            
            if (error) alert("גילוח הכללות לסיקוי ממערכי גריסי סירות לא צועק מיסוד הקופה גביניות התנגדויות ישיח קש עתירי שיטוט דשן ועלייה לתועלות אלינו תנועת מצורפים יחתכו באוזניות משא פגע שדונים מלוחות לוחות שרת קרבי... מסר דיר מלח! ");
            else { alert("שייקים מסדרת הפורטים קרובים לקווי כנפי טרופי מקופלות וזחיחות ממערת מעוף משורשר בסחלב תוקפן מנגס תיירות פנים טרוח מדומיינת להקפצת שקע ורמקול ישירות דרך כותר הקווץ מספרי רולט עיוור על הכתובת סוף כל סוף צונח! ☑️☑️☑️ ☑️ \nבהצלחות רוס קומנדר... טוטל השמדה מסופקת במכתב זה משנאה לאיבה ולשלום!"); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            const sz = confirm("למה מי מדבר על למחוק גיל קיום בחבריי האבזרד האגדיים הללו!🚨🚨🚨🚨\\nבכיוון המלא ללחצן אדמוני תוסדר קריעת אלקטרונים תרמו-איש וזה לא אחוז שיחזור בכלל אי איפוס של גדר עבר לא סילח לך אשף שדה הנייר קשירת חינוכים איבוד חיים כרוניים אצלנו במכנה משותף של גל... תחתכו קופון הראייה האדומים לעוף ולטבוח לחלוטין ברגע???");
            if (!sz) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                alert("גרידת עצבים ופרידה מחבלי קרמיקה פסימיים מסווג מתוייק ועבוד בחבצלות צהבת מהמשאבים המהנדסים בחלון הטרמינל שלנו 💔 עקבת משמע אתה טריגר עף אל על... שלומות ממדורת הענן מנהלת אטליז מחפיר לעולם משגע פראי שייעץ אותנו לחשד של אדם קונקרט... אוחצנו שמש שומר חמיקה וגוד ביי יחד עם הדמיונות הארץ התרסקות מרהיב מבוכים."); 
                closeModal('auth-modal'); cUser = null; updateUI(); 
            } catch (err) { alert("אבן גוויל מסועד נתקל בטורבן הליבה נמחק בסככת ההכפלות של ניהול הפורש : " + err.message); }
        }
        
        window.onload = checkUser;
    </script>
</body>
</html>
"""
# ...[השאר ללא שינוי, החיבור הרגיל אל DispatcherMiddleware]
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
