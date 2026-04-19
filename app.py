from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string, send_from_directory
import os

def x():
    y = Flask(__name__)
    @y.route('/')
    def index():return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return y

# דף "בפיתוח" ללא סרגל פנימי - המעטפת (Portal) תספק את הסרגל
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
          <p style="color: #b2bec3; margin-top: 15px;">המשחק הזה נמצא עדיין בפיתוח... אנא המתן עד שיפותח.</p>
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

# הזרקת משחק לדף מלא הכולל את הסרגל תמיד (The Iframe Portal)
@main_app.route('/play/<path:target>')
def play_view(target):
    return render_template_string(PLAY_HTML, target=target)

# =======================================================
# 1. MENU_HTML - עמוד הלובי הראשי
# =======================================================
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
# THE HUB (דף ראשי מעוצב ומלא כל טוב!)
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
        /* מנקה שכפולי iFrame במקרה שנפתח בטעות משחק בתוך משחק */
        if (window.top !== window.self) {
            window.top.location = window.self.location;
        }
    </script>
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
            <a href="/" class="brand-logo" title="Arcade Station">
                <img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'"> 
                Arcade Station
            </a>
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

    <footer>&copy; 2026 Arcade Station - Aviel Aluf</footer>
    <button class="feedback-fab" onclick="openModal('feedback-modal')" title="יש לכם משוב?">💬</button>

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
                <input type="text" id="f-user" class="input-box" placeholder="שם במשחק או במערכת...">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">אימייל גיבוי למשתמש:</label>
                <input type="email" id="f-email" class="input-box" placeholder="your-email@mail.com">
            </div>

            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">אשר המשך</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לתמיד</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לחלון השחזור הבטוח.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור להתחברות רגילה</u></p>
        </div>
    </div>

    <!-- מודל אודות (בדיוק מה שביקשת) -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station | Hub</h2>
            <div class="about-text" style="text-align: right; color: var(--text-main); font-size: 1.05rem; padding: 10px;">
                <p><strong>Arcade Station | Hub</strong> הוא אתר משחקים בדפדפן.</p>
                <p>בדף הבית מופיעה ההודעה: <br><em>"בחר את ההרפתקה שלך" <br> "מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮"</em></p>
                <p>האתר מציג 11 משחקים שונים, כולם זמינים ישירות בדפדפן. כל משחק הוא הרפתקה בפני עצמה עם סגנון, קטגוריה ותיאור משלו.</p>
                
                <h3 style="color: #a29bfe; margin-top: 25px;">המשחקים הזמינים שלנו:</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><strong>הישרדות 🏝️</strong> | <small style="color:#00cec9;">ניהול משאבים</small><br>שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</li>
                    <li><strong>Gold Forest 🌲</strong> | <small style="color:#00cec9;">אקשן טקסטואלי</small><br>יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</li>
                    <li><strong>Genesis 🚀</strong> | <small style="color:#00cec9;">מסע בחלל</small><br>הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</li>
                    <li><strong>קוד אדום 💻</strong> | <small style="color:#00cec9;">סייבר</small><br>הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</li>
                    <li><strong>IRON LEGION 🔫</strong> | <small style="color:#00cec9;">יריות ושרידה</small><br>גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</li>
                    <li><strong>מבוך הצללים 🌑</strong> | <small style="color:#00cec9;">אימה</small><br>מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</li>
                    <li><strong>PROXIMA 🪐</strong> | <small style="color:#00cec9;">מחקר עולמות</small><br>חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</li>
                    <li><strong>הטפיל 🧬</strong> | <small style="color:#00cec9;">ביולוגיה</small><br>מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</li>
                    <li><strong>CLOVER 🍀</strong> | <small style="color:#00cec9;">מזל טהור</small><br>הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</li>
                    <li><strong>NEON RIDER 🏍️</strong> | <small style="color:#00cec9;">מרוץ</small><br>רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</li>
                    <li><strong>Manager PRO 📊</strong> | <small style="color:#00cec9;">ניהול קבוצות</small><br>הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</li>
                </ul>

                <hr style="border-top:1px solid rgba(255,255,255,0.1); margin:20px 0;">
                <p>האתר כולו בנוי בצורה מינימליסטית וממוקדת במשחקים. אין צורך בהורדות או הרשמה – פשוט בוחרים משחק ולוחצים. כל ההרפתקאות זמינות בעברית ומתחילות מיד.</p>
                <h3 style="color: #a29bfe;">אודות היוצר</h3>
                <p><strong>Arcade Station | Hub</strong> נוצר על ידי <strong>אביאל</strong>.</p>
                <p>כתובת אימייל: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת משוב</h2>
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-topic" class="input-box" onchange="updateFeedbackUI()">
                    <option value="" disabled selected>-- בחר --</option>
                    <option value="tech">תקלה טכנית בשרתים</option>
                    <option value="idea">הצעות למשחקים/לשיפור</option>
                    <option value="other">משהו אחר וכללי</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-game-box">
                <label>לאיזה משחק לפנות?</label>
                <select id="fb-game" class="input-box">
                    <option value="main">התחנה הראשית</option>
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
                <label>נא פרט כאן בהרחבה (המכתב מגיע אלינו!)</label>
                <textarea id="fb-text"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שגר אל השמיים 🚀</button>
            </div>
        </div>
    </div>

    <!-- חלון הניהול -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">לוח בקרה סודי - מערכת ניהול</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים מאובטח</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר ומערכות משוב 📥</button>
            </div>
            <div id="section-users" class="admin-section active">
                <input type="text" id="admin-search" class="input-box" style="margin-bottom:15px;" placeholder="חפש אותי בסירבר...">
                <div class="user-list" id="admin-user-list"></div>
            </div>
            <div id="section-feedbacks" class="admin-section">
                <div class="feedback-list" id="admin-feedback-list"><p style="color:#a4b0be; text-align:center;">טוען קבצים מאוחרים...</p></div>
            </div>
        </div>
    </div>

    <!-- THE JS -->
    <script>
        const sp = supabase.createClient('https://ryoykooazoaordzmxdat.supabase.co', 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B');
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
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || 'גיבור ללא שם');
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ עריכת משתמש / אבטחה' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn');
            const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי בחשבונך:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='קוד גישה (סיסמה):'; btn.innerText='התחבר'; btn.onclick=doLogin;
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } 
            else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי לחשבונך:'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='אימייל לשחזור במידה ואבד (מומלץ):';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה חדשה מעל 6 תווים:'; btn.innerText='הירשם'; btn.onclick=doSignUp;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } 
            else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='ניהול פרופיל'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='הכינוי שלי:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='עדכון סיסמה חזקה (השאר ריק באם לא רוצה לשנות):';
                btn.innerText='שמור שינויים לחשבון'; btn.onclick=doEditProfile; deleteDiv.style.display = 'block';
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } 
            else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מרכז שחזור סיסמאות - מאובטח'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי במשחק:'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='אימייל ההרשמה:'; bP.style.display='none';
                btn.innerText='שלח לינק לכתובת שלי'; btn.onclick=doRecovery;
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        function getSafeEmail(userInput) {
            let cln = userInput.trim().toLowerCase();
            if(cln.includes('@')) return cln;
            return cln.replace(/\s+/g, '') + "@arcadestation.local";
        }

        async function doLogin() {
            const uInput = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!uInput || !p) return alert("השדה חובה לא יכול להישאר ריק.");
            const realFormatted = getSafeEmail(uInput);
            const { error } = await sp.auth.signInWithPassword({ email: realFormatted, password: p });
            if(error) alert("שגיאה! הסיסמה או הכינוי שגויים. נסה שנית.");
            else { closeModal('auth-modal'); checkUser(); }
        }

        /* 🥇 הפתרון הענק לתקלת ההרשמה שהבאת מדוח התקלות שלך! 🥇 */
        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); 
            const theM = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value;

            if(!nickname || !p) return alert("חובה למלא כינוי וסיסמה!");
            if(p.length < 6) return alert("הסיסמה חייבת להכיל לפחות 6 תווים.");

            // שלב 1: מניעת שגיאה "שקטה" – קודם כל נבדוק האם הכינוי תפוס במסד!
            try {
                const { data: existing } = await sp.from('profiles').select('nickname').eq('nickname', nickname).maybeSingle();
                if (existing) {
                    alert("הכינוי '" + nickname + "' כבר תפוס במערכת! 🕵️‍♂️\\nאם זה החשבון שלך, אנחנו מעבירים אותך למסך התחברות עכשיו.");
                    setAuthUI('LOGIN');
                    document.getElementById('f-user').value = nickname; // משאיר לו את השם
                    return;
                }
            } catch(e) {}

            const cleanFinal = theM.includes('@') ? theM.toLowerCase() : getSafeEmail(nickname);
            
            // שלב 2: יצירת המשתמש וטיפול ברור אם Supabase כועס (איימייל קיים)
            const { data, error } = await sp.auth.signUp({ email: cleanFinal, password: p, options:{ data:{ nickname: nickname } } });
            
            if (error) {
                if (error.message.includes("already registered") || error.message.includes("already exists")) {
                    alert("הכינוי או האימייל כבר רשומים במערכת! 🚨\\nמעביר אותך למסך התחברות.");
                    setAuthUI('LOGIN');
                    document.getElementById('f-user').value = nickname;
                    return;
                }
                return alert("שגיאת הרשמה: " + error.message);
            }
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); checkUser(); alert("חשבון שחקן מוכן לאקשן! הירשמת בהצלחה."); }
            closeModal('auth-modal'); 
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); alert("סיסמת החשבון המעודכנת הוחלפה!"); }
            closeModal('auth-modal'); checkUser();
        }

        async function deleteSelf() {
            const isSure = confirm("אזהרה מהשרת 🚨\\nהאם אתה בטוח שאתה רוצה למחוק את החשבון שלך לתמיד?\\nפעולה זו תמחק אותך לגמרי ותנתק אותך מידית מהמערכת.");
            if (!isSure) return;
            try {
                await sp.from('profiles').delete().eq('user_id', cUser.id);
                await sp.auth.signOut();
                alert("פרופיל המשתמש שלך הוסר בהצלחה. 💔 תמיד תוכל לפתוח מחדש!");
                closeModal('auth-modal');
                cUser = null;
                updateUI();
            } catch (err) { alert("אירעה שגיאה בשרת למחיקת משתמש: " + err.message); }
        }

        async function doRecovery() {
            const givenName = document.getElementById('f-user').value.trim(); const givenEmail = document.getElementById('f-email').value.trim();
            if(!givenName || !givenEmail) return alert("השדות צריכים להכיל נתונים אמיתיים.");
            if(!givenEmail.includes('@') || givenEmail.includes('.local')) return alert("שחזור סיסמה במכניקת שרת חייבת אימייל תקין!");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail.toLowerCase());
            if (error) alert("תקלת כתובת. וודא מול הרישום בספריות הדואר שאיות מדוייק עובד.");
            else { alert("נשלחה בקשה. ייתכן שיקח זמן עד שתראה במייל/ספאם את השליחות הזאת. בהצלחה!"); setAuthUI('LOGIN'); }
        }

        function updateFeedbackUI() { const v = document.getElementById('fb-topic').value; document.getElementById('fb-game-box').style.display = (v === 'tech' || v === 'idea') ? 'block' : 'none'; document.getElementById('fb-text-box').style.display = v ? 'block' : 'none'; }
        async function submitFeedback() { const t = document.getElementById('fb-topic').value; const g = document.getElementById('fb-game-box').style.display === 'block' ? document.getElementById('fb-game').value : 'כללי'; const tx = document.getElementById('fb-text').value; if(!tx) return; try { await sp.from('feedbacks').insert({ user_email: cUser ? (cUser.email.includes('.local') ? cUser.user_metadata.nickname : cUser.email) : 'אורח', topic: t, game: g, text: tx }); alert('המשוב מצא את דרכו אל ההנהלה בבטחה. ✉️'); } catch (err) {} closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; updateFeedbackUI(); }
        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# PLAY SCREEN (תפריט עליון שומר את הפוקוס למשחקים + חסימת IFRAME כפול)
# =======================================================
PLAY_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arcade Play - {{target}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
        /* התיקון לסיוט האינסופי שנוצר בתמונות - לעולם לא מרשה לעצמו להיטען כחלק מפנימיות האתר!! */
        if (window.top !== window.self) { window.top.location = window.self.location; }
    </script>
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
        .btn-primary { background: #00cec9; color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }

        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        /* Modals  */
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
                <a onclick="alert('טבלאות יגיעו בהמשך')">טבלאות</a>
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
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">צור שחקן</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי במערכת:</label>
                <input type="text" id="f-user" class="input-box" placeholder="שם...">
            </div>
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">אימייל גיבוי מצידך:</label>
                <input type="email" id="f-email" class="input-box" placeholder="אופציונלי לשחזור מהיר">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">אשר המשך לתוכן</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ מחיקת החשבון שלי לתמיד</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:#a4b0be; cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת סוד חשבון? תגיש בקשה למכונות כאן.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:#00cec9; cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור לחיבור</u></p>
        </div>
    </div>

    <!-- מודל אודות משובט -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content about-modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: #00cec9;">אודות Arcade Station | Hub</h2>
            <div class="about-text" style="text-align: right; color: var(--text-main); font-size: 1.05rem; padding: 10px; max-height: 55vh; overflow-y: auto;">
                <p><strong>Arcade Station | Hub</strong> הוא אתר משחקים מתקדם בדפדפן.</p>
                <p>בדף הבית מופיעה ההודעה: <br><em>"בחר את ההרפתקה שלך" <br> "מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮"</em></p>
                <p>האתר מציג 11 משחקים שונים, כולם זמינים ישירות בדפדפן. כל משחק הוא הרפתקה בפני עצמה עם סגנון, קטגוריה ותיאור משלו.</p>
                
                <h3 style="color: #a29bfe; margin-top: 25px;">המשחקים הזמינים שלנו:</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;"><strong>הישרדות 🏝️</strong> | <small style="color:#00cec9;">ניהול משאבים</small><br>שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</li>
                    <li style="margin-bottom: 10px;"><strong>Gold Forest 🌲</strong> | <small style="color:#00cec9;">אקשן טקסטואלי</small><br>יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</li>
                    <li style="margin-bottom: 10px;"><strong>Genesis 🚀</strong> | <small style="color:#00cec9;">מסע בחלל</small><br>הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</li>
                    <li style="margin-bottom: 10px;"><strong>קוד אדום 💻</strong> | <small style="color:#00cec9;">סייבר</small><br>הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</li>
                    <li style="margin-bottom: 10px;"><strong>IRON LEGION 🔫</strong> | <small style="color:#00cec9;">יריות ושרידה</small><br>גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</li>
                    <li style="margin-bottom: 10px;"><strong>מבוך הצללים 🌑</strong> | <small style="color:#00cec9;">אימה</small><br>מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</li>
                    <li style="margin-bottom: 10px;"><strong>PROXIMA 🪐</strong> | <small style="color:#00cec9;">מחקר עולמות</small><br>חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</li>
                    <li style="margin-bottom: 10px;"><strong>הטפיל 🧬</strong> | <small style="color:#00cec9;">ביולוגיה</small><br>מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</li>
                    <li style="margin-bottom: 10px;"><strong>CLOVER 🍀</strong> | <small style="color:#00cec9;">מזל טהור</small><br>הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</li>
                    <li style="margin-bottom: 10px;"><strong>NEON RIDER 🏍️</strong> | <small style="color:#00cec9;">מרוץ</small><br>רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</li>
                    <li style="margin-bottom: 10px;"><strong>Manager PRO 📊</strong> | <small style="color:#00cec9;">ניהול קבוצות</small><br>הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</li>
                </ul>

                <hr style="border-top:1px solid rgba(255,255,255,0.1); margin:20px 0;">
                <p>האתר כולו בנוי בצורה מינימליסטית וממוקדת במשחקים. אין צורך בהורדות או הרשמה – פשוט בוחרים משחק ולוחצים. כל ההרפתקאות זמינות בעברית ומתחילות מיד.</p>
                <h3 style="color: #a29bfe;">אודות היוצר</h3>
                <p><strong>Arcade Station | Hub</strong> נוצר ומתוחזק באהבה גדולה על ידי <strong>אביאל</strong>.</p>
                <p>לפניות ובקשות במייל: <span style="color:#00cec9;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <script>
        const sp = supabase.createClient('https://ryoykooazoaordzmxdat.supabase.co', 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B');
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
            btnMain.innerText = cUser ? '⚙ עריכת משתמש / אבטחה' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn'); const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link');
            const deleteDiv = document.getElementById('delete-acc-container');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; deleteDiv.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה:'; btn.innerText='הכנס למערכת המשחקים'; btn.onclick=doLogin;
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי רצוי:'; bE.style.display='block'; document.getElementById('lbl-email').innerHTML='אימייל גיבוי:';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה לפרופיל החדש:'; btn.innerText='הפוך לרשמי בפלטפורמה'; btn.onclick=doSignUp;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='אבטחה והגדרות אישיות'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי שם במשחק:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='רוצה סיסמה חדשה? כתוב פה:'; btn.innerText='שמור נתוני צד שרת'; btn.onclick=doEditProfile;
                deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='מעבדה רשמית לשחזורי גישה'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי שלך פה:'; bE.style.display='block'; document.getElementById('lbl-email').innerHTML='כתובת מייל המשויכת מוקדם יותר:'; 
                bP.style.display='none'; btn.innerText='תן במייל בקשת שליחה לחידוש'; btn.onclick=doRecovery;
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        function getSafeEmail(userInput) { let cln = userInput.trim().toLowerCase(); if(cln.includes('@')) return cln; return cln.replace(/\s+/g, '') + "@arcadestation.local"; }

        async function doLogin() {
            const uInput = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!uInput || !p) return alert("הכנס פרטי משתמש רשומים וברורים מוקפדים יוסף!");
            const realFormatted = getSafeEmail(uInput);
            const { error } = await sp.auth.signInWithPassword({ email: realFormatted, password: p });
            if(error) alert("תקלת סיסמה / משתמש שלא נמצא ברישומיי הספר הלאומי.");
            else { closeModal('auth-modal'); checkUser(); }
        }

        /* 🥇 הפתרון לתקלת ההרשמה הוכנס גם פה! 🥇 */
        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const theM = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!nickname || !p) return alert("שדות כינוי וסיסמא אינם לוקחים הברזה!");
            if(p.length < 6) return alert("סיסמא אליבא צריכה להיבנות עם יותר מ6.");

            // שלב 1: מניעת הרשמה כפולה ובריחה מושלמת ל-LOGIN
            try {
                const { data: existing } = await sp.from('profiles').select('nickname').eq('nickname', nickname).maybeSingle();
                if (existing) {
                    alert("הכינוי '" + nickname + "' תפוס על ידי סירבר רשום. 🕵️‍♂️\\nאם היית פה, נווט אותך מול התחברות קלאסית.");
                    setAuthUI('LOGIN');
                    document.getElementById('f-user').value = nickname; 
                    return;
                }
            } catch(e) {}

            const cleanFinal = theM.includes('@') ? theM.toLowerCase() : getSafeEmail(nickname);
            
            // שלב 2: טיפול שגיאה על אימייל כבר בשימוש
            const { data, error } = await sp.auth.signUp({ email: cleanFinal, password: p, options:{ data:{ nickname: nickname } } });
            
            if (error) {
                if (error.message.includes("already registered") || error.message.includes("already exists")) {
                    alert("הכינוי או המייל כבר נושמים אצלנו, אין טעם להיכנס פעמיים בלוטו ההרשמה.\\nמועבר מיד ללשונית התחברות טבעית.");
                    setAuthUI('LOGIN');
                    document.getElementById('f-user').value = nickname;
                    return;
                }
                return alert("אופס נראה לי רע. זה תפוס! ("+error.message+")");
            }
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); checkUser(); alert("שם משתמש כוונן והכנס אל סעדות הבשר..."); }
            closeModal('auth-modal'); 
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); alert("סיסמתך החשאית הוחלפה!"); }
            closeModal('auth-modal'); checkUser();
        }

        async function deleteSelf() {
            const isSure = confirm("האם אתה סגור וגמור עקב למחוק פול-סרוור מעורך משחקים אצלנו?\\nזה לא ישאיר זכר והכל מתאבד באותו צעד סופי.");
            if (!isSure) return;
            try {
                await sp.from('profiles').delete().eq('user_id', cUser.id);
                await sp.auth.signOut();
                alert("המכונה העלימה שחקן זה מגלקסיית הארקייד שלנו 💔 היית אחלה! 🏁");
                closeModal('auth-modal');
                cUser = null;
                updateUI();
            } catch (err) { alert("בעיה בסירבר החיקוק - אנא דבר עם אדמין : " + err.message); }
        }

        async function doRecovery() {
            const givenName = document.getElementById('f-user').value.trim(); const givenEmail = document.getElementById('f-email').value.trim();
            if(!givenName || !givenEmail) return alert("דרוש אימייל אמיתי לטקטיקת מודול שליחת המכתבים");
            if(!givenEmail.includes('@') || givenEmail.includes('.local')) return alert("רק דואר עם שטרודל קיים בממשקות העשירים מאחור. כתובת נקייה תקבל יעד שליחה!");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail.toLowerCase());
            if (error) alert("שגיאת המרצה וריברס - כתובת לא קיימת בבלאס ארכיב... שים יד על המדוייקת במאתים.");
            else { alert("הלינק הועבר באוויר לחלל המייל האישי! בדוק באגפים השונים דקה שניים..."); setAuthUI('LOGIN'); }
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
