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
          <p style="color: #b2bec3; margin-top: 15px;">המשחק הזה נמצא עדיין בפיתוח... אנא המתן עד שאביאל יסיים.</p>
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
        /* פורץ מסגרות: מונע מהדף הראשי להיטען בתוך משחק שחזר לאחור */
        if (window !== window.top) { window.top.location.href = "/"; }
    </script>
    <style>
        :root { --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709; --card-bg: rgba(25, 25, 32, 0.6); --card-border: rgba(255, 255, 255, 0.08); --text-main: #f5f6fa; --text-sub: #a4b0be; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; min-height: 100vh; overflow-x: hidden; }
        
        .bg-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background-image: radial-gradient(circle at 15% 20%, rgba(108, 124, 231, 0.12) 0%, transparent 40%), radial-gradient(circle at 85% 70%, rgba(0, 206, 201, 0.12) 0%, transparent 40%), linear-gradient(to bottom, #070709 0%, #111116 100%); animation: pulseBg 10s infinite alternate; }
        @keyframes pulseBg { 0% { opacity: 0.8; } 100% { opacity: 1; } }

        /* Navigation Bar */
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
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; font-weight: 500; display: none; }

        /* Main Hub */
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

        /* Modals & Forms */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .hidden-group { display: none; }
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

        /* Admin & Lists */
        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; }
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid transparent; }
        .user-row { cursor: pointer; flex-direction: row; justify-content: space-between; align-items: center;}
        
        .about-game-item { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.08); }
        .about-game-item b { color: #fff; font-size: 1.1rem; }
        .about-game-item i { color: var(--accent); font-size: 0.85rem; font-style: normal; display: block; margin-bottom: 5px; margin-top:2px; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="חזרה למסך הראשי">
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
                <a onclick="alert('מודול טבלאות מתקדם יושלם בהמשך...🥇')">טבלאות</a>
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

    <!-- ====== SECTION: MODALS (ALL popups here) ====== -->
    
    <!-- 1. ABOUT MODAL -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content" style="max-width: 600px; text-align: right; overflow-x:hidden;">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: var(--accent); margin-bottom: 20px;">אודות Arcade Station | Hub</h2>
            <p style="font-size: 1.05rem; line-height: 1.6;">
                Arcade Station | Hub הוא אתר משחקים מתקדם בדפדפן.<br>
                בדף הבית מופיעה ההודעה: <strong style="color:#fff;">"בחר את ההרפתקה שלך" - "מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮"</strong>
            </p>
            <p style="color: var(--text-sub); font-size: 0.95rem; line-height: 1.6; margin: 15px 0;">האתר מציג 11 משחקים שונים, כולם זמינים ישירות בדפדפן. כל משחק הוא הרפתקה בפני עצמה עם סגנון, קטגוריה ותיאור משלו.</p>

            <div style="max-height: 250px; overflow-y: auto; margin-bottom: 20px; padding-left:10px;">
                <div class="about-game-item"><b>הישרדות 🏝️</b> <i>ניהול משאבים</i> שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</div>
                <div class="about-game-item"><b>Gold Forest 🌲</b> <i>אקשן טקסטואלי</i> יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</div>
                <div class="about-game-item"><b>Genesis 🚀</b> <i>מסע בחלל</i> הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</div>
                <div class="about-game-item"><b>קוד אדום 💻</b> <i>סייבר</i> הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</div>
                <div class="about-game-item"><b>IRON LEGION 🔫</b> <i>יריות ושרידה</i> גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</div>
                <div class="about-game-item"><b>מבוך הצללים 🌑</b> <i>אימה</i> מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</div>
                <div class="about-game-item"><b>PROXIMA 🪐</b> <i>מחקר עולמות</i> חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</div>
                <div class="about-game-item"><b>הטפיל 🧬</b> <i>ביולוגיה</i> מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</div>
                <div class="about-game-item"><b>CLOVER 🍀</b> <i>מזל טהור</i> הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</div>
                <div class="about-game-item"><b>NEON RIDER 🏍️</b> <i>מרוץ</i> רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</div>
                <div class="about-game-item"><b>Manager PRO 📊</b> <i>ניהול קבוצות</i> הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</div>
            </div>
            <p style="font-size: 0.95rem; line-height: 1.6;">האתר כולו בנוי בצורה מינימליסטית וממוקדת במשחקים. אין צורך בהורדות או הרשמה – פשוט בוחרים משחק ולוחצים. כל ההרפתקאות זמינות בעברית ומתחילות מיד.</p>
            <hr style="border:0; border-top: 1px solid var(--card-border); margin:15px 0;">
            <p style="color: var(--text-sub); font-size: 0.95rem;"><b>אודות היוצר:</b><br>Arcade Station | Hub נוצר על ידי <b>אביאל</b>.<br>כתובת אימייל: x0583289789@gmail.com</p>
        </div>
    </div>

    <!-- 2. AUTH MODAL (Login/Signup/Edit) -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות פרופיל מתקדמות</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הקמת פרופיל</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי בחשבונך:</label>
                <input type="text" id="f-user" class="input-box" placeholder="סופרמן123...">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">אימייל גיבוי (מאפשר שחזור במקרה שתשכח סיסמה):</label>
                <input type="email" id="f-email" class="input-box" placeholder="youremail@mail.com">
            </div>

            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית:</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">שלח ובצע</button>
            
            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לשחזור גישה.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור להתחברות רגילה</u></p>
            <button id="btn-delete-self" style="display:none; width:100%; margin-top:25px; border:1px solid #ff4757; background:rgba(255, 71, 87, 0.1); color:#ff4757; border-radius:12px; padding:12px; font-weight:bold; cursor:pointer;" onclick="deleteMyAccount()">השמדת החשבון שלי לחלוטין ⚠️</button>
        </div>
    </div>

    <!-- 3. FEEDBACK MODAL -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="margin-bottom:20px;">שליחת משוב</h2>
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-topic" class="input-box" onchange="updateFeedbackUI()">
                    <option value="" disabled selected>-- בחר בבקשה --</option>
                    <option value="tech">תקלה או בעיה שגילית</option>
                    <option value="idea">בקשה לשיפור או פיתוח חדש</option>
                    <option value="other">אחר</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-game-box">
                <label>על איזה משחק מדובר?</label>
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
                <label>ספר לנו יותר כאן:</label>
                <textarea id="fb-text" style="height:120px;"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="submitFeedback()">שגר אל השרתים 🚀</button>
            </div>
        </div>
    </div>

    <!-- 4. ADMIN MODAL -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">לוח בקרה סודי - מערכת ניהול</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים מאובטח</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר ומערכות משוב 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><input type="text" id="admin-search" class="input-box" style="margin-bottom:15px;" placeholder="חפש בסירבר..."><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"><p style="color:#a4b0be; text-align:center;">טוען קבצים...</p></div></div>
        </div>
    </div>

    <!-- ====== SECTION: JAVASCRIPT (Auth + Logic) ====== -->
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
            const isAdm = cUser && (cUser.email?.toLowerCase() === 'x0583289789@gmail.com');
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || 'גיבור ללא שם');
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ ניהול פרופיל' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            const aBtn = document.getElementById('admin-btn');
            if (aBtn) aBtn.style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function getSafeEmail(userInput) { 
            let cln = userInput.trim().toLowerCase(); 
            if(cln.includes('@')) return cln; 
            return cln.replace(/[^a-z0-9א-ת_]/gi, '') + "@arcadestation.local"; 
        }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn'); const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link'); const btnDelSelf = document.getElementById('btn-delete-self');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; btnDelSelf.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי קבוע בחשבונך:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמת כניסה:'; 
                btn.innerText='כניסה לעולם המשחקים'; btn.onclick=doLogin;
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי לחשבון:'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='אימייל גיבוי לשחזורים (לא חובה):';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמה אישית (מעל 6 אותיות):'; 
                btn.innerText='קדימה, הרשם אותי עכשיו!'; btn.onclick=doSignUp;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='בקרת הפרופיל הנוכחי שלך'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שינוי שם שחקן:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='מעוניין לעדכן סיסמה לחזקה יותר? (השאר ריק אם לא):';
                btn.innerText='עדכן וחתום על הפרטים מידית'; btn.onclick=doEditProfile;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none'; btnDelSelf.style.display = 'block';
            } else if (mode === 'RECOVERY') { 
                titleEdit.style.display='block'; titleEdit.innerText='שחזור גישה מאובטח'; tabsCon.style.display='none';
                bU.style.display='none'; bE.style.display='block'; document.getElementById('lbl-email').innerHTML='הקלד את כתובת האימייל איתה פתחת את החשבון:'; bP.style.display='none';
                btn.innerText='שלח לינק לכתובת ליצירת סיסמה חדשה'; btn.onclick=doRecovery;
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function doLogin() {
            const uInput = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!uInput || !p) return alert("אנא הזן כינוי וסיסמה מלאים!");
            const safeMail = getSafeEmail(uInput);
            const { error } = await sp.auth.signInWithPassword({ email: safeMail, password: p });
            if(error) alert("זהירות! התגלו פרטים שגויים במערכת - בדוק שהסיסמה והכינוי תואמים בדיוק!");
            else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const theM = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!nickname || !p) return alert("טופס הרישום חייב לכלול לפחות את שם השחקן המבוקש ואת הסיסמה הרצויה.");
            if(p.length < 6) return alert("מערכות האבטחה שלנו קשוחות! אנא בחר סיסמה של שישה תווים ומעלה למען ביטחונך.");
            const safeMail = theM.includes('@') ? theM.toLowerCase() : getSafeEmail(nickname);
            const { data, error } = await sp.auth.signUp({ email: safeMail, password: p, options:{ data:{ nickname: nickname } } });
            if (error) return alert("מצטערים. מסד הנתונים מודיע ששחקן עם כינוי או אימייל דומה כנראה כבר תפס זאת.");
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); checkUser(); closeModal('auth-modal'); alert("יוצא לדרך! הפרופיל שלך אושר והתחברת למערכת בהצלחה. 🎮"); }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); alert("הסיסמה התעדכנה אצלנו בסרברים במצלחה!"); }
            closeModal('auth-modal'); checkUser();
        }

        async function doRecovery() {
            const givenEmail = document.getElementById('f-email').value.trim().toLowerCase();
            if(!givenEmail) return alert("השארת ריק... הקלד את כתובת הדואר שלך בבקשה.");
            if(!givenEmail.includes('@') || givenEmail.includes('.local')) return alert("רק משתמשים ששייכו דואר אותנטי בזמן ההרשמה זכאים לשחזור סיסמה כעת. אם לא סיפקת מייל, לא נוכל לשחזר.");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail);
            if (error) alert("תקלה בעת השליחה - יכול להיות שהאימייל הוקלד עם שגיאת כתיב.");
            else { alert("נשלח קישור איפוס בטוח לחשבונך במייל (בדוק ספאם)! השתמש בו כדי ליצור סיסמה מחדש למערכת."); setAuthUI('LOGIN'); }
        }

        async function deleteMyAccount() {
            if(!confirm("אזהרה מהבהבת וחמורה!\nהאם באמת ברצונך לחסל ופשוט למחוק מהמאגר שלנו לחלוטין כל נתון על משתמשך? אין דרך חזרה!")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.rpc('delete_my_account'); alert("זה רשמי: רשומי הבסיס התנקו. הפרופיל נמחק להתראות! 👋"); await logout(); closeModal('auth-modal'); window.location.href = '/'; } 
            catch (err) { alert("יש להוסיף את פקודת מחיקת ה-SQL אל שרתי ה-Supabase באדמין תחילה לפי ההדרכה."); }
        }

        function updateFeedbackUI() { const v = document.getElementById('fb-topic').value; document.getElementById('fb-game-box').style.display = (v === 'tech' || v === 'idea') ? 'block' : 'none'; document.getElementById('fb-text-box').style.display = v ? 'block' : 'none'; }
        async function submitFeedback() { const t = document.getElementById('fb-topic').value; const g = document.getElementById('fb-game-box').style.display === 'block' ? document.getElementById('fb-game').value : 'כללי'; const tx = document.getElementById('fb-text').value; if(!tx) return; try { await sp.from('feedbacks').insert({ user_email: cUser ? (cUser.email.includes('.local') ? cUser.user_metadata.nickname : cUser.email) : 'אורח', topic: t, game: g, text: tx }); alert('התקבל, תודה רבה על השתתפותך בבניית הארקייד שלנו ✉️'); } catch (err) {} closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; updateFeedbackUI(); }
        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); const { data: uData } = await sp.from('profiles').select('*'); let uH = ''; (uData||[]).forEach(u => uH += `<div class="user-row"><div style="color:var(--accent);"><b>${u.nickname}</b><br><span style="font-size:0.8rem;color:#888;">ID: ${u.user_id}</span></div></div>`); document.getElementById('admin-user-list').innerHTML = uH || 'אין נתונים'; const { data: fData, error: fE } = await sp.from('feedbacks').select('*').order('created_at', { ascending: false }); let fH = ''; if(fE || !fData || fData.length===0) fH = '<p style="text-align:center;">אין משובים.</p>'; else fData.forEach(f => fH += `<div class="feedback-row"><b style="color:var(--accent);">${f.topic} - ${f.game||'כללי'}</b><p>${f.text}</p><small style="color:#777;">מאת: ${f.user_email}</small></div>`); document.getElementById('admin-feedback-list').innerHTML = fH; }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        
        window.onload = checkUser;
    </script>
</body>
</html>
"""


# =======================================================
# 2. PLAY_HTML - עמוד המשחק ה"עוטף" את המשחקים למסך מלא
#    מועתק בדיוק כירורגי מ-MENU כדי לוודא ששום דבר לא קורס שוב!
# =======================================================
PLAY_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Arcade Play - {{target}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        :root { --primary: #6c7ce7; --accent: #00cec9; --card-border: rgba(255, 255, 255, 0.08); --text-sub: #a4b0be; }
        body, html { margin: 0; padding: 0; background-color: #070709; color: #fff; font-family: 'Heebo', sans-serif; overflow: hidden; height: 100%; width: 100%; display: flex; flex-direction: column; }
        
        /* Navbar copied identically */
        nav { height: 70px; min-height: 70px; background: rgba(10, 10, 15, 1); border-bottom: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); z-index: 1000; }
        .nav-right-area { display: flex; align-items: center; gap: 30px; }
        .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); transition: transform 0.3s;}
        .brand-logo:hover img { transform: scale(1.05); }

        .top-links { display: flex; gap: 20px; align-items: center; margin-right: 15px;}
        .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
        .top-links a:hover { color: var(--accent); }
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.98); min-width: 220px; box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid var(--card-border); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right;}
        .dropdown:hover .dropdown-content { display: block; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
        .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: var(--accent); }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; font-weight: 500; display: none; }
        .btn { border: none; padding: 9px 24px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 0.95rem; }
        .btn-primary { background: var(--accent); color: #000; box-shadow: 0 0 10px rgba(0,206,201,0.2); }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }

        /* Game Iframe */
        iframe { flex-grow: 1; width: 100%; border: none; display: block; }
        
        /* Modal Style Sync */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto;}
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
        .modal-close:hover { color: #ff4757; }
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .hidden-group { display: none; }
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; }
        .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }
        
        .about-game-item { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.08); }
        .about-game-item b { color: #fff; font-size: 1.1rem; }
        .about-game-item i { color: var(--accent); font-size: 0.85rem; font-style: normal; display: block; margin-bottom: 5px; margin-top:2px; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="חזור לתחנת החלל ארקייד"><img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'">Arcade Station</a>
            
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
                <a onclick="alert('פיצ\'ר דירוגים בטבלאות בהכנה לקראת עלית מולטיפלייר! 🥇')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
        </div>

        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">התחבר / הרשם</button>
        </div>
    </nav>
    
    <iframe src="/{{target}}" title="Game Portal Display Window"></iframe>

    <!-- 1. ABOUT MODAL IN GAME PAGE -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content" style="max-width: 600px; text-align: right; overflow-x:hidden;">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: var(--accent); margin-bottom: 20px;">אודות Arcade Station | Hub</h2>
            <p style="font-size: 1.05rem; line-height: 1.6;">
                Arcade Station | Hub הוא אתר משחקים מתקדם בדפדפן.<br>
                בדף הבית מופיעה ההודעה: <strong style="color:#fff;">"בחר את ההרפתקה שלך" - "מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮"</strong>
            </p>
            <p style="color: var(--text-sub); font-size: 0.95rem; line-height: 1.6; margin: 15px 0;">האתר מציג 11 משחקים שונים, כולם זמינים ישירות בדפדפן. כל משחק הוא הרפתקה בפני עצמה עם סגנון, קטגוריה ותיאור משלו.</p>

            <div style="max-height: 250px; overflow-y: auto; margin-bottom: 20px; padding-left:10px;">
                <div class="about-game-item"><b>הישרדות 🏝️</b> <i>ניהול משאבים</i> שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</div>
                <div class="about-game-item"><b>Gold Forest 🌲</b> <i>אקשן טקסטואלי</i> יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</div>
                <div class="about-game-item"><b>Genesis 🚀</b> <i>מסע בחלל</i> הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</div>
                <div class="about-game-item"><b>קוד אדום 💻</b> <i>סייבר</i> הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</div>
                <div class="about-game-item"><b>IRON LEGION 🔫</b> <i>יריות ושרידה</i> גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</div>
                <div class="about-game-item"><b>מבוך הצללים 🌑</b> <i>אימה</i> מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</div>
                <div class="about-game-item"><b>PROXIMA 🪐</b> <i>מחקר עולמות</i> חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</div>
                <div class="about-game-item"><b>הטפיל 🧬</b> <i>ביולוגיה</i> מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</div>
                <div class="about-game-item"><b>CLOVER 🍀</b> <i>מזל טהור</i> הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</div>
                <div class="about-game-item"><b>NEON RIDER 🏍️</b> <i>מרוץ</i> רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</div>
                <div class="about-game-item"><b>Manager PRO 📊</b> <i>ניהול קבוצות</i> הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</div>
            </div>
            <p style="font-size: 0.95rem; line-height: 1.6;">האתר כולו בנוי בצורה מינימליסטית וממוקדת במשחקים. אין צורך בהורדות או הרשמה חובה – פשוט בוחרים משחק ולוחצים. כל ההרפתקאות זמינות בעברית ומתחילות מיד.</p>
            <hr style="border:0; border-top: 1px solid var(--card-border); margin:15px 0;">
            <p style="color: var(--text-sub); font-size: 0.95rem;"><b>אודות היוצר:</b><br>Arcade Station | Hub נוצר על ידי <b>אביאל</b>.<br>כתובת אימייל: x0583289789@gmail.com</p>
        </div>
    </div>

    <!-- 2. AUTH MODAL IN GAME PAGE -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">הגדרות פרופיל מתקדמות</h2>
            
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">התחברות</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הקמת פרופיל חדש</button>
            </div>
            
            <div class="form-group" id="box-user">
                <label id="lbl-user">כינוי קבוע בחשבונך:</label>
                <input type="text" id="f-user" class="input-box" placeholder="למשל: סופרמן123">
            </div>
            
            <div class="form-group" id="box-email" style="display:none;">
                <label id="lbl-email">אימייל (מומלץ כדי לשחזר גישה בעתיד!):</label>
                <input type="email" id="f-email" class="input-box" placeholder="youremail@mail.com">
            </div>

            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמה אישית (לפחות 6 תווים):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">תן לי לשחק כבר!</button>
            
            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>שכחת את הסיסמה? לחץ כאן לשחזור גישה.</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 חזור להתחברות רגילה</u></p>
            <button id="btn-delete-self" style="display:none; width:100%; margin-top:25px; border:1px solid #ff4757; background:rgba(255, 71, 87, 0.1); color:#ff4757; border-radius:12px; padding:12px; font-weight:bold; cursor:pointer;" onclick="deleteMyAccount()">השמדת החשבון שלי לחלוטין ⚠️</button>
        </div>
    </div>

    <script>
        // EXACT copy of the logic so it works flawlessly within the game frame
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
            btnMain.innerText = cUser ? '⚙ עריכת פרופיל' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
        }

        function getSafeEmail(userInput) { 
            let cln = userInput.trim().toLowerCase(); 
            if(cln.includes('@')) return cln; 
            return cln.replace(/[^a-z0-9א-ת_]/gi, '') + "@arcadestation.local"; 
        }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            const tL = document.getElementById('auth-tab-login'); const tS = document.getElementById('auth-tab-signup');
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass');
            const btn = document.getElementById('auth-exec-btn'); const titleEdit = document.getElementById('auth-edit-title'); const tabsCon = document.getElementById('auth-tabs-container');
            const fPassLnk = document.getElementById('forgot-pw-link'); const bLoginLnk = document.getElementById('back-login-link');
            const btnDelSelf = document.getElementById('btn-delete-self');

            titleEdit.style.display = 'none'; tabsCon.style.display = 'flex'; btnDelSelf.style.display = 'none';

            if (mode === 'LOGIN') {
                tL.classList.add('active'); tS.classList.remove('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי קבוע בחשבונך:'; bE.style.display='none'; 
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='סיסמת כניסה:'; 
                btn.innerText='חזרה למשחק (התחבר)'; btn.onclick=doLogin;
                fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } 
            else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bU.style.display='block'; document.getElementById('lbl-user').innerText='בחר כינוי לחשבונך:'; 
                bE.style.display='block'; document.getElementById('lbl-email').innerHTML='הוסף אימייל (מומלץ כדי לשחזר סיסמה):';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='בחר סיסמה מאובטחת:'; 
                btn.innerText='קדימה, הרשם אותי עכשיו!'; btn.onclick=doSignUp;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } 
            else if (mode === 'EDIT') {
                titleEdit.style.display='block'; titleEdit.innerText='בקרת אבטחת משתמש'; tabsCon.style.display='none';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='שנה את שמך התצוגה כרצונך:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bE.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='רוצה לשנות סיסמה לחזקה יותר? (השאר ריק אם לא):';
                btn.innerText='עדכן וחתום על הפרטים מידית'; btn.onclick=doEditProfile;
                fPassLnk.style.display='none'; bLoginLnk.style.display='none'; btnDelSelf.style.display = 'block';
            } 
            else if (mode === 'RECOVERY') { 
                titleEdit.style.display='block'; titleEdit.innerText='שחזור גישה מאובטח'; tabsCon.style.display='none';
                bU.style.display='none'; bE.style.display='block'; document.getElementById('lbl-email').innerHTML='הקלד כתובת אימייל אמיתית איתה פתחת חשבון:'; bP.style.display='none';
                btn.innerText='שלח לינק ליצירת סיסמה חדשה'; btn.onclick=doRecovery;
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function doLogin() {
            const uInput = document.getElementById('f-user').value.trim(); const p = document.getElementById('f-pass').value;
            if(!uInput || !p) return alert("השדות הם כרטיס הכניסה שלכם - אנא אל תשאירו ריקים.");
            const safeMail = getSafeEmail(uInput);
            const { error } = await sp.auth.signInWithPassword({ email: safeMail, password: p });
            if(error) alert("זהירות! התגלו פרטים שגויים במערכת - בדוק שהסיסמה והכינוי תואמים בדיוק!");
            else { closeModal('auth-modal'); checkUser(); }
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); const theM = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value;
            if(!nickname || !p) return alert("טופס הרישום חייב לכלול לפחות את השם הרצוי והסיסמה.");
            if(p.length < 6) return alert("מערכות האבטחה שלנו קשוחות! אנא בחר סיסמה של 6 תווים ומעלה למען ביטחונך.");
            const safeMail = theM.includes('@') ? theM.toLowerCase() : getSafeEmail(nickname);
            const { data, error } = await sp.auth.signUp({ email: safeMail, password: p, options:{ data:{ nickname: nickname } } });
            if (error) return alert("מצטערים. נראה שהכינוי או המייל כבר תפוסים על ידי משתמש אחר.");
            if (data.user) { await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nickname }); alert("הפרופיל שלך אושר והתחברת בהצלחה! 🎮"); checkUser(); closeModal('auth-modal'); }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim();
            if(newN) { await sp.auth.updateUser({ data: { nickname: newN } }); await sp.from('profiles').upsert({ user_id: cUser.id, nickname: newN }); }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); alert("הסיסמה התעדכנה בהצלחה!"); }
            closeModal('auth-modal'); checkUser();
        }

        async function doRecovery() {
            const givenEmail = document.getElementById('f-email').value.trim().toLowerCase();
            if(!givenEmail) return alert("מוקד התמיכה דורש אימייל אליו קשרת את החשבון...");
            if(!givenEmail.includes('@') || givenEmail.includes('.local')) return alert("רק מי שנרשם עם דואר אותנטי רשאי לקבל קישור שחזור כעת. אם לא סופק מייל לא נוכל לשחזר.");
            const { error } = await sp.auth.resetPasswordForEmail(givenEmail);
            if (error) alert("תקלה בעת השליחה - יכול להיות שהאימייל הוקלד עם שגיאת כתיב.");
            else { alert("נשלח קישור איפוס בטוח במייל (בדוק ספאם)! השתמש בו כדי ליצור סיסמה מחדש."); setAuthUI('LOGIN'); }
        }

        async function deleteMyAccount() {
            if(!confirm("זה לא משחק! לחץ אישור רק אם תרצה לטרוק לצוות אצלנו את הדלת - פעולה זו מוחקת לחלוטין כל נתון ולא ניתן לשחזרה!")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.rpc('delete_my_account'); alert("הפרופיל נמחק. להתראות! 👋"); await sp.auth.signOut(); window.location.href = '/'; } 
            catch (err) { alert("פנה למנהל הרשת לתקן מחיקת חשבון SQL."); }
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
