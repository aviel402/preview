from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string, send_from_directory
import os

def x():
    y = Flask(__name__)
    @y.route('/')
    def index():return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return y

# --- 1. דף "בפיתוח" מעוצב משופר ---
def a(text):
    return f'''
      <!DOCTYPE html>
      <html lang="he" dir="rtl">
      <head>
          <meta charset="UTF-8">
          <title>{text} - בפיתוח</title>
          <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;700;900&display=swap" rel="stylesheet">
          <style>
            body {{
              margin: 0; font-family: 'Heebo', sans-serif; background-color: #0a0a0c;
              background-image: radial-gradient(circle at 50% 0%, rgba(108, 124, 231, 0.15) 0%, transparent 50%),
                                radial-gradient(circle at 50% 100%, rgba(0, 206, 201, 0.15) 0%, transparent 50%);
              color: #fff; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden;
            }}
            .container {{
              text-align: center; padding: 50px 40px; background: rgba(30, 30, 36, 0.6); backdrop-filter: blur(16px);
              border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); max-width: 500px; width: 90%;
              animation: float 6s ease-in-out infinite; box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 20px rgba(0, 206, 201, 0.1);
            }}
            .icon-wrapper {{ font-size: 80px; margin-bottom: 20px; filter: drop-shadow(0 0 20px rgba(0, 206, 201, 0.4)); }}
            h1 {{ font-size: clamp(2rem, 5vw, 3rem); margin: 0; font-weight: 900; background: linear-gradient(90deg, #a29bfe, #00cec9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .subtitle {{ margin-top: 16px; font-size: 1.2rem; color: #b2bec3; font-weight: 300; }}
            .progress-bar {{ width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 30px; position: relative; overflow: hidden; }}
            .progress-bar::after {{ content: ''; position: absolute; top: 0; left: 0; height: 100%; width: 40%; background: linear-gradient(90deg, #6c7ce7, #00cec9); border-radius: 4px; animation: loading 2s infinite ease-in-out alternate; }}
            .back-btn {{ display: inline-block; margin-top: 40px; padding: 12px 30px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); color: #fff; text-decoration: none; border-radius: 30px; font-weight: 700; transition: all 0.3s ease; }}
            .back-btn:hover {{ background: rgba(255, 255, 255, 0.1); border-color: #00cec9; transform: scale(1.05); box-shadow: 0 0 15px rgba(0, 206, 201, 0.3); }}
            @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
            @keyframes loading {{ 0% {{ left: -40%; }} 100% {{ left: 100%; }} }}
          </style>
      </head>
      <body>
        <div class="container">
          <div class="icon-wrapper">🚧</div>
          <h1>{text}</h1>
          <div class="subtitle">המשחק עדיין בשלבי פיתוח במעבדה...</div>
          <div class="progress-bar"></div>
          <a href="/" class="back-btn">חזור לתחנה הראשית 🏠</a>
        </div>
      </body>
      </html>
    '''

# פונקציית דמה ליצירת אפליקציות חסרות
def create_dummy_app(text):
    dummy = Flask(__name__)
    @dummy.route('/')
    def index():return a(text)
    return dummy

# --- 2. ייבוא בטוח של האפליקציות ---
try: from app1 import app as game1
except ImportError: game1 = create_dummy_app("הישרדות")
try: from app2 import app as game2
except ImportError: game2 = create_dummy_app("RPG Legend")
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


# --- 3. הלאוצ'ר הראשי והתפריט ---
main_app = Flask(__name__)

@main_app.route('/logo.png')
def favicon():
    return "LOGO_DATA" 

@main_app.route('/')
def index():
    return render_template_string(MENU_HTML)

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
            --primary: #6c7ce7;
            --accent: #00cec9;
            --bg-dark: #070709;
            --card-bg: rgba(25, 25, 32, 0.6);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f5f6fa;
            --text-sub: #a4b0be;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Heebo', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* רקע דינמי עם חלקיקים/אורות ניאון */
        .bg-layer {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(108, 124, 231, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 70%, rgba(0, 206, 201, 0.12) 0%, transparent 40%),
                linear-gradient(to bottom, #070709 0%, #111116 100%);
            animation: pulseBg 10s infinite alternate;
        }
        @keyframes pulseBg {
            0% { opacity: 0.8; }
            100% { opacity: 1; }
        }

        /* שורת ניווט עליונה (Navbar) חכמה ויפה */
        nav {
            position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
            background: rgba(10, 10, 15, 0.8); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            border-bottom: 1px solid var(--card-border);
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }

        .brand-logo { font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav-controls { display: flex; gap: 15px; align-items: center; }
        
        /* כפתורים מודרניים */
        .btn {
            border: none; padding: 10px 22px; border-radius: 30px; font-weight: 700; cursor: pointer;
            font-family: 'Heebo', sans-serif; transition: all 0.3s ease; display: inline-flex; align-items: center; justify-content: center;
        }
        .btn-primary { background: var(--accent); color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .btn-danger:hover { box-shadow: 0 0 15px rgba(255, 71, 87, 0.4); }
        
        /* מראה פרופיל בנביגיישן */
        .user-pill {
            background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3);
            color: #fff; padding: 8px 18px; border-radius: 30px; font-weight: 500; font-size: 0.95rem; display: none;
        }

        /* כותרת מרכזית בדף */
        main { padding: 120px 20px 60px; text-align: center; }
        h1.main-title {
            font-size: clamp(2.5rem, 8vw, 4.5rem); margin-bottom: 10px;
            background: linear-gradient(135deg, #fff, #a29bfe, #00cec9);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;
        }
        .subtitle { color: var(--text-sub); font-size: 1.3rem; margin-bottom: 60px; }

        /* כרטיסי משחקים מחודשים */
        .grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px; max-width: 1300px; margin: 0 auto;
        }

        .card {
            background: var(--card-bg); border-radius: 20px; text-decoration: none; color: white;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid var(--card-border); overflow: hidden; position: relative;
            display: flex; flex-direction: column; text-align: right;
        }

        .card:hover { 
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(108, 124, 231, 0.2); 
            border-color: rgba(108, 124, 231, 0.4);
        }

        /* "תמונת נושא" מדורגת למשחק (הגרדיאנט משתנה טיפה לכל קלף ע"י JS אופציונלי או CSS) */
        .card-cover {
            height: 140px; width: 100%; display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, rgba(108,124,231,0.2) 0%, rgba(0,206,201,0.1) 100%);
            border-bottom: 1px solid var(--card-border);
            font-size: 65px; text-shadow: 0 0 20px rgba(255,255,255,0.2);
        }

        .card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .card-body h2 { font-size: 1.8rem; font-weight: 700; margin-bottom: 10px; color: #fff; }
        .tag-badge {
            align-self: flex-start; padding: 6px 12px; background: rgba(0, 206, 201, 0.15); 
            border: 1px solid rgba(0, 206, 201, 0.3); border-radius: 20px; font-size: 0.85rem; font-weight: 500; color: #00cec9;
        }

        footer { margin-top: 100px; padding: 20px; text-align: center; color: #4b4b5c; font-size: 0.95rem; border-top: 1px solid var(--card-border); }
        
        /* כפתור משוב מרחף (Floating Action Button) */
        .feedback-fab {
            position: fixed; bottom: 30px; left: 30px; width: 65px; height: 65px;
            background: linear-gradient(135deg, #6c7ce7, #00cec9);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 28px; color: white; cursor: pointer; z-index: 990;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5), 0 0 15px rgba(0, 206, 201, 0.4);
            border: none; transition: transform 0.3s, box-shadow 0.3s;
        }
        .feedback-fab:hover { transform: scale(1.1); box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 25px rgba(0, 206, 201, 0.6); }

        /* מודלים - עיצוב חלונות פופ-אפ כללי */
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
            display: none; align-items: center; justify-content: center; z-index: 10000;
            opacity: 0; transition: opacity 0.3s ease;
        }
        .modal-overlay.active { display: flex; opacity: 1; }
        
        .modal-content {
            background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border);
            padding: 40px; border-radius: 24px; width: 90%; max-width: 500px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right;
            transform: scale(0.9); transition: transform 0.3s ease; max-height: 90vh; overflow-y: auto;
        }
        .modal-overlay.active .modal-content { transform: scale(1); }

        .modal-close {
            position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be;
            font-size: 24px; cursor: pointer; transition: color 0.3s;
        }
        .modal-close:hover { color: #ff4757; }

        .modal-content h2 { margin-bottom: 25px; color: #fff; text-align: center; font-size: 2rem; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); font-size: 0.95rem; }
        .input-box, select, textarea {
            width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4);
            border: 1px solid var(--card-border); color: white; font-size: 1rem;
            font-family: 'Heebo', sans-serif; transition: border-color 0.3s;
        }
        .input-box:focus, select:focus, textarea:focus { outline: none; border-color: var(--accent); }
        textarea { resize: vertical; min-height: 100px; }

        /* ייחודי לפאנל ניהול */
        .admin-modal { max-width: 900px; }
        .search-box { display: flex; margin-bottom: 20px; }
        .user-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; padding-left: 5px; }
        
        /* סקרולברים (Scrollbars) כהים לאתר ולתיבות הגלילה */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }

        /* שורת משתמש בודד בתוך טבלת מנהלים */
        .user-row {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid transparent;
            transition: border-color 0.3s; cursor: pointer;
        }
        .user-row:hover { border-color: var(--primary); background: rgba(0,0,0,0.5); }
        .user-row-info div { margin-bottom: 4px; }
        
        /* כרטיס תצוגת פרטי משתמש בתוך האדמין */
        #admin-user-details-pane {
            display: none; background: rgba(10,10,15,0.8); border: 1px solid var(--card-border);
            border-radius: 16px; padding: 25px; margin-top: 20px; animation: fadeIn 0.3s forwards;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .admin-actions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 25px; }

        /* חלקות היררכיה בטופס הפידבק */
        .hidden-group { display: none; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <!-- Navigation Bar -->
    <nav>
        <div class="brand-logo">Arcade Station 🕹️</div>
        <div class="nav-controls">
            <div id="user-status" class="user-pill">
                <span id="nickname-display"></span>
            </div>
            <button id="main-action-btn" class="btn btn-primary" onclick="openModal('auth-modal')">התחבר / הרשם</button>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ ניהול</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">התנתק</button>
        </div>
    </nav>

    <main>
        <h1 class="main-title">בחר את ההרפתקה שלך</h1>
        <p class="subtitle">מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮</p>

        <!-- רשת המשחקים -->
        <div class="grid">
            <a href="/game1/" class="card">
                <div class="card-cover">🏝️</div>
                <div class="card-body">
                    <h2>הישרדות</h2>
                    <span class="tag-badge">ניהול משאבים</span>
                </div>
            </a>
            <a href="/game2/" class="card"><div class="card-cover" style="filter: hue-rotate(40deg);">⚔️</div><div class="card-body"><h2>RPG Legend</h2><span class="tag-badge">אקשן טקסטואלי</span></div></a>
            <a href="/game3/" class="card"><div class="card-cover" style="filter: hue-rotate(80deg);">🚀</div><div class="card-body"><h2>Genesis</h2><span class="tag-badge">מסע בחלל</span></div></a>
            <a href="/game4/" class="card"><div class="card-cover" style="filter: hue-rotate(120deg);">💻</div><div class="card-body"><h2>קוד אדום</h2><span class="tag-badge">סייבר ומחשבים</span></div></a>
            <a href="/game5/" class="card"><div class="card-cover" style="filter: hue-rotate(160deg);">🔫</div><div class="card-body"><h2>IRON LEGION</h2><span class="tag-badge">יריות ושרידה</span></div></a>
            <a href="/game6/" class="card"><div class="card-cover" style="filter: hue-rotate(200deg);">🌑</div><div class="card-body"><h2>מבוך הצללים</h2><span class="tag-badge">אימה חיפוש</span></div></a>
            <a href="/game7/" class="card"><div class="card-cover" style="filter: hue-rotate(240deg);">🪐</div><div class="card-body"><h2>PROXIMA</h2><span class="tag-badge">כוכב לכת חדש</span></div></a>
            <a href="/game8/" class="card"><div class="card-cover" style="filter: hue-rotate(280deg);">🧬</div><div class="card-body"><h2>הטפיל</h2><span class="tag-badge">ביולוגי והישרדות</span></div></a>
            <a href="/game9/" class="card"><div class="card-cover" style="filter: hue-rotate(320deg);">🍀</div><div class="card-body"><h2>CLOVER</h2><span class="tag-badge">מזל טהור</span></div></a>
            <a href="/game10/" class="card"><div class="card-cover" style="filter: hue-rotate(360deg);">🏍️</div><div class="card-body"><h2>NEON RIDER</h2><span class="tag-badge">מרוץ סייברפאנק</span></div></a>
            <a href="/game11/" class="card"><div class="card-cover" style="filter: hue-rotate(25deg);">📊</div><div class="card-body"><h2>Manager PRO</h2><span class="tag-badge">ניהול קבוצות</span></div></a>
        </div>
    </main>

    <footer>&copy; 2024 Arcade Station - Aviel Aluf | x0583289789@gmail.com</footer>

    <!-- כפתור המשוב המרחף -->
    <button class="feedback-fab" onclick="openModal('feedback-modal')" title="יש לך הערה או הצעת ייעול?">💬</button>

    <!-- ============================== מודלים (חלונות קופצים) ============================== -->
    
    <!-- 1. מודל התחברות / עדכון פרופיל (כשהמשתמש אורח זה התחברות, כשהוא מחובר זה שינוי פרטים) -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-modal-title">התחבר למערכת</h2>
            <div class="form-group" id="group-email">
                <label>אימייל:</label>
                <input type="email" id="auth-email" class="input-box" placeholder="example@gmail.com">
            </div>
            <div class="form-group" id="group-password">
                <label>סיסמה:</label>
                <input type="password" id="auth-pass" class="input-box" placeholder="••••••••">
            </div>
            <div class="form-group hidden-group" id="group-nickname">
                <label>שם תצוגה במשחק:</label>
                <input type="text" id="auth-nick" class="input-box" placeholder="הכנס כינוי מדליק">
            </div>
            <button id="auth-submit-btn" class="btn btn-primary" style="width: 100%; margin-top: 10px;" onclick="handleAuthAction()">המשך</button>
            <p id="auth-toggle-text" style="text-align: center; margin-top: 20px; font-size: 0.9rem; cursor: pointer; color: var(--accent);" onclick="toggleAuthMode()">אין לך חשבון? לחץ כאן להרשמה.</p>
        </div>
    </div>

    <!-- 2. מודל שליחת משוב מותאם אישית (הבקשה המיוחדת שלך) -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2>שליחת משוב</h2>
            
            <div class="form-group">
                <label>נושא הפנייה:</label>
                <select id="fb-main-topic" class="input-box" onchange="handleFeedbackCategories()">
                    <option value="" disabled selected>-- בחר נושא --</option>
                    <option value="tech">תקלה טכנית</option>
                    <option value="general">הערה כללית</option>
                    <option value="idea">הצעות לשיפור</option>
                </select>
            </div>

            <!-- אפשרויות תלויות - נפתחות רק אם נבחר משהו מסוים -->
            <div class="form-group hidden-group" id="fb-tech-opts">
                <label>סוג התקלה:</label>
                <select id="fb-tech-select" class="input-box">
                    <option value="list">רשימת המשחקים</option>
                    <option value="main">דף ראשי</option>
                    <option value="other">אחר</option>
                </select>
            </div>

            <div class="form-group hidden-group" id="fb-idea-opts">
                <label>סוג הצעה:</label>
                <select id="fb-idea-select" class="input-box">
                    <option value="existing">שיפור של משהו קיים</option>
                    <option value="new">הצעה למשהו חדש לגמרי</option>
                </select>
            </div>

            <div class="form-group hidden-group" id="fb-text-container">
                <label>פרט קצת יותר:</label>
                <textarea id="fb-text" placeholder="ספר לנו מה עובר לך בראש..."></textarea>
            </div>

            <button class="btn btn-primary hidden-group" id="fb-submit" style="width:100%; margin-top:10px;" onclick="sendFeedback()">שלח משוב 🚀</button>
        </div>
    </div>

    <!-- 3. מודל פאנל מנהלים עשיר ומפורט -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; text-shadow: 0 0 10px rgba(255, 71, 87, 0.4);">פאנל בקרה - אדמין</h2>
            
            <div class="form-group search-box">
                <input type="text" id="admin-search" class="input-box" placeholder="🔍 חפש לפי שם או אימייל..." oninput="filterAdminUsers()">
            </div>

            <div class="user-list" id="admin-user-list-container">
                <!-- כאן ייכנסו השורות של המשתמשים ב-JS -->
                <p style="text-align:center; color:#777;">טוען משתמשים...</p>
            </div>

            <!-- אזור שמופיע כשתלחץ על שורה בטבלה כדי לראות ולבצע פעולות (כרטיס ביקור משתמש) -->
            <div id="admin-user-details-pane">
                <h3 id="det-name" style="margin-bottom:5px; color:#fff;"></h3>
                <p style="color:var(--text-sub); margin-bottom:15px; font-size:0.95rem;">ID: <span id="det-id"></span> | Email: <span id="det-email"></span></p>
                
                <div class="admin-actions-grid">
                    <button class="btn btn-secondary" onclick="adminActionChangeName()">✏️ שינוי שם / כינוי</button>
                    <button class="btn btn-primary" onclick="adminActionSendMessage()">📩 שלח הודעה אישית</button>
                    <button class="btn btn-secondary" style="color: #ffa502; border-color: #ffa502;" onclick="adminActionMock('חסום את המייל / החשבון', 'שים לב, כדי לחסום חשבונות לצמיתות יש צורך בהרשאות צד-שרת מיוחדות. הממשק כרגע מדמה פעולה.')">🚫 חסימת מייל</button>
                    <button class="btn btn-danger" onclick="adminActionMock('מחק את המשתמש לצמיתות', 'מחיקת Auth user מצריכה Service Role מסיבות אבטחה ב-Supabase. בעתיד אפשר להוסיף Edge Function או שרת Node.')">🗑️ מחיקת משתמש</button>
                </div>
            </div>
        </div>
    </div>


    <!-- ============================== SUPABASE SCRIPT & LOGIC ============================== -->
    <script>
        // Supabase Init
        const SUPABASE_URL = 'https://ryoykooazoaordzmxdat.supabase.co';
        const SUPABASE_ANON_KEY = 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B'; // תשאיר ככה כבקשתך
        const { createClient } = supabase;
        const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        let currentUser = null;
        let isSignUpMode = false;
        
        // --- כלים בסיסיים של ה-UI (פתיחת מודלים וכו) ---
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { 
            document.getElementById(id).classList.remove('active'); 
            if(id === 'admin-modal') { document.getElementById('admin-user-details-pane').style.display = 'none'; }
        }
        function closeOnBgClick(event, id) { if(event.target.id === id) closeModal(id); }

        // --- ניהול משתמש נוכחי (Session) ---
        async function checkUser() {
            try {
                const { data: { user } } = await supabaseClient.auth.getUser();
                currentUser = user;
                updateUI();
            } catch (e) { console.error(e); }
        }

        function updateUI() {
            const statusBox = document.getElementById('user-status');
            const nickDisplay = document.getElementById('nickname-display');
            const mainBtn = document.getElementById('main-action-btn');
            const logoutBtn = document.getElementById('logout-btn');
            const adminBtn = document.getElementById('admin-btn');

            if (currentUser) {
                const isAdmin = currentUser.email === 'x0583289789@gmail.com';
                const displayName = currentUser.user_metadata?.nickname || currentUser.email?.split('@')[0];

                statusBox.style.display = 'block';
                nickDisplay.innerText = `👤 ${displayName}`;

                // המשתמש מחובר - הכפתור הראשי הופך ל"ערוך פרופיל"
                mainBtn.textContent = '⚙ ערוך פרופיל';
                mainBtn.onclick = () => setupProfileEditMode(displayName);

                logoutBtn.style.display = 'inline-flex';
                adminBtn.style.display = isAdmin ? 'inline-flex' : 'none';
            } else {
                statusBox.style.display = 'none';
                mainBtn.textContent = 'התחבר / הרשם';
                mainBtn.onclick = () => { isSignUpMode = false; setupLoginMode(); openModal('auth-modal'); };
                logoutBtn.style.display = 'none';
                adminBtn.style.display = 'none';
            }
        }

        async function logout() {
            await supabaseClient.auth.signOut();
            currentUser = null;
            updateUI();
            alert('התנתקת בהצלחה! להתראות במשחקים הבאים. 👾');
        }

        // --- התחברות / הרשמה / שינוי פרופיל ---
        function toggleAuthMode() {
            isSignUpMode = !isSignUpMode;
            if(isSignUpMode) setupSignUpMode();
            else setupLoginMode();
        }

        function setupLoginMode() {
            document.getElementById('auth-modal-title').innerText = 'התחבר למערכת';
            document.getElementById('group-email').style.display = 'block';
            document.getElementById('group-password').style.display = 'block';
            document.getElementById('group-nickname').classList.add('hidden-group');
            document.getElementById('auth-submit-btn').innerText = 'כניסה';
            document.getElementById('auth-toggle-text').style.display = 'block';
            document.getElementById('auth-toggle-text').innerText = 'אין לך חשבון? לחץ כאן להרשמה.';
        }

        function setupSignUpMode() {
            document.getElementById('auth-modal-title').innerText = 'הרשמה לשחקן חדש';
            document.getElementById('group-email').style.display = 'block';
            document.getElementById('group-password').style.display = 'block';
            document.getElementById('group-nickname').classList.remove('hidden-group');
            document.getElementById('auth-submit-btn').innerText = 'צור חשבון';
            document.getElementById('auth-toggle-text').style.display = 'block';
            document.getElementById('auth-toggle-text').innerText = 'יש לך כבר חשבון? חזור להתחברות.';
        }

        function setupProfileEditMode(currentNick) {
            document.getElementById('auth-modal-title').innerText = 'ערוך פרטים אישיים';
            document.getElementById('group-email').style.display = 'none';
            document.getElementById('group-password').style.display = 'none';
            document.getElementById('group-nickname').classList.remove('hidden-group');
            document.getElementById('auth-nick').value = currentNick;
            document.getElementById('auth-submit-btn').innerText = 'שמור שינויים במערכת';
            document.getElementById('auth-toggle-text').style.display = 'none';
            isSignUpMode = 'EDIT'; 
            openModal('auth-modal');
        }

        async function handleAuthAction() {
            const email = document.getElementById('auth-email').value;
            const pass = document.getElementById('auth-pass').value;
            const nick = document.getElementById('auth-nick').value;

            try {
                if (isSignUpMode === 'EDIT') {
                    // עדכון שם בלבד
                    if(!nick) return alert('הכנס כינוי!');
                    await supabaseClient.auth.updateUser({ data: { nickname: nick } });
                    await supabaseClient.from('profiles').upsert({ user_id: currentUser.id, nickname: nick });
                    alert('פרטיך עודכנו בבסיס הנתונים! ✨');
                    closeModal('auth-modal');
                    checkUser();
                } 
                else if (isSignUpMode === true) {
                    // הרשמה
                    if(!email || !pass || !nick) return alert('נא למלא את כל השדות!');
                    const { data, error } = await supabaseClient.auth.signUp({
                        email, password: pass, options: { data: { nickname: nick } }
                    });
                    if (error) throw error;
                    // הכנסה ל- profiles
                    if(data.user) {
                        await supabaseClient.from('profiles').insert({ user_id: data.user.id, nickname: nick });
                    }
                    alert('ברוך הבא לארקייד! ההרשמה עברה בהצלחה.');
                    closeModal('auth-modal');
                    checkUser();
                } 
                else {
                    // התחברות
                    if(!email || !pass) return alert('נא למלא אימייל וסיסמה!');
                    const { error } = await supabaseClient.auth.signInWithPassword({ email, password: pass });
                    if (error) throw error;
                    closeModal('auth-modal');
                    checkUser();
                }
            } catch (err) {
                alert('שגיאה: ' + err.message);
            }
        }


        // --- הגיון טופס משוב (חכם) ---
        function handleFeedbackCategories() {
            const mainSelection = document.getElementById('fb-main-topic').value;
            const techDiv = document.getElementById('fb-tech-opts');
            const ideaDiv = document.getElementById('fb-idea-opts');
            const textDiv = document.getElementById('fb-text-container');
            const btnDiv = document.getElementById('fb-submit');

            // נסתיר את הכל ורק נראה מה שרלוונטי
            techDiv.classList.add('hidden-group');
            ideaDiv.classList.add('hidden-group');
            
            if (mainSelection === 'tech') {
                techDiv.classList.remove('hidden-group');
            } else if (mainSelection === 'idea') {
                ideaDiv.classList.remove('hidden-group');
            }

            // במקרה שבוחרים נושא, בכל מקרה נרצה שהוא ירשום מלל, אז נציג תמיד את המלל:
            if(mainSelection) {
                textDiv.classList.remove('hidden-group');
                btnDiv.classList.remove('hidden-group');
            }
        }

        async function sendFeedback() {
            // כאן קולטים את כל הנתונים, אתה צודק לחלוטין שמיילים לא עובדים מפרונט-אנד רגיל (HTML).
            // הדרך הנכונה שלך לשמור משוב היא להכניס את זה לטבלת "feedbacks" בסופאבייס!
            const mainType = document.getElementById('fb-main-topic').value;
            let subType = '';
            if (mainType === 'tech') subType = document.getElementById('fb-tech-select').value;
            if (mainType === 'idea') subType = document.getElementById('fb-idea-select').value;
            const details = document.getElementById('fb-text').value;

            if(!details.trim()) return alert("נשמח אם תפרט קצת כדי שנוכל להבין 😊");

            // במקום קריאת שרת לאימייל: סימולציה מצוינת
            console.log("Feedback Payload:", { type: mainType, subtype: subType, details: details, userEmail: currentUser?.email || 'Guest' });
            
            /* אם תיצור טבלה feedbacks פשוט תשחרר את הבלוק הזה מהערה:
            await supabaseClient.from('feedbacks').insert({
                user_email: currentUser?.email || 'GUEST', type: mainType, subtype: subType, details: details
            });
            */
            
            alert('המשוב נשלח בהצלחה למערכת. המון תודה שאתה עוזר לנו להשתפר! 📨');
            closeModal('feedback-modal');
            
            // ניקוי הטופס
            document.getElementById('fb-main-topic').value = '';
            document.getElementById('fb-text').value = '';
            handleFeedbackCategories(); // מעלים בחזרה אלמנטים
        }


        // --- לוגיקה ואסטרטגיה של חלון המנהלים החדש ---
        let globalAdminUsers =[]; // רשימת המשתמשים הגלובלית לסינון מקומי
        let currentEditingUserId = null; 

        async function openAdminModal() {
            openModal('admin-modal');
            document.getElementById('admin-user-list-container').innerHTML = '<p style="text-align:center;">שואב נתונים מהשרת...</p>';
            
            // המשיכה היא מטבלת הפרופילים כדי לאתר את השמות ואיידי, בהמשך עדיף Edge function שמושכת Auth
            const { data, error } = await supabaseClient.from('profiles').select('*');
            if (error) {
                document.getElementById('admin-user-list-container').innerHTML = '<p style="color:#ff4757;">שגיאה במשיכת נתונים.</p>';
                return;
            }

            // יצירת מערך שניתן לעבוד עליו
            globalAdminUsers = data ||[];
            renderAdminUsersList(globalAdminUsers);
        }

        function renderAdminUsersList(users) {
            const listContainer = document.getElementById('admin-user-list-container');
            if(users.length === 0) {
                listContainer.innerHTML = '<p style="color:#a4b0be; text-align:center;">לא נמצאו משתמשים לפי חיפוש זה.</p>';
                return;
            }

            let html = '';
            users.forEach(u => {
                html += `
                <div class="user-row" onclick="viewUserDetails('${u.user_id}', '${u.nickname}')">
                    <div class="user-row-info">
                        <strong style="color:var(--accent); font-size:1.1rem;">${u.nickname || 'משתמש חדש'}</strong>
                        <div style="font-size:0.8rem; color:#888;">ID: ${u.user_id}</div>
                    </div>
                    <div style="color: #6c7ce7;">&gt;&gt;</div>
                </div>`;
            });
            listContainer.innerHTML = html;
        }

        function filterAdminUsers() {
            const query = document.getElementById('admin-search').value.toLowerCase();
            const filtered = globalAdminUsers.filter(u => {
                const n = (u.nickname || '').toLowerCase();
                const i = (u.user_id || '').toLowerCase();
                return n.includes(query) || i.includes(query);
            });
            renderAdminUsersList(filtered);
        }

        // כאשר המנהל לוחץ על משתמש ספציפי
        function viewUserDetails(userId, nickname) {
            currentEditingUserId = userId;
            document.getElementById('admin-user-details-pane').style.display = 'block';
            document.getElementById('det-name').innerText = `👤 כרטיס שחקן: ${nickname || 'אין כינוי'}`;
            document.getElementById('det-id').innerText = userId;
            
            // בSupabase בגלל אבטחה כבדה, כתובות המייל נמצאות ב Auth ולא בטבלה. לכן שמים סעיף מסביר בUI
            document.getElementById('det-email').innerText = 'לצורכי אבטחה ופרטיות מידע זה חסוי (ניתן לפנות לשחקן בעזרת כפתור הודעה)';
        }

        // פעולות אדמין (שעובדות בפועל ב-Database)
        async function adminActionChangeName() {
            const newName = prompt('שם תצוגה חדש שידרוס את הנוכחי:', '');
            if(newName && newName.trim().length > 0) {
                await supabaseClient.from('profiles').update({ nickname: newName }).eq('user_id', currentEditingUserId);
                alert('שם התצוגה עודכן! עליו להתחבר מחדש או לרענן מסך כדי לראות שינויים.');
                openAdminModal(); // רענון מהיר לרשימה
            }
        }

        function adminActionSendMessage() {
            // כמנהל אתה רוצה לשלוח לו הודעה שקופצת באפליקציה או אימייל
            const msg = prompt('כתוב הודעה אישית שתוצג למשתמש: (דורש מערכת התראות מובנית שנוסיף בעתיד, אבל הממשק מוכן!)');
            if(msg) alert("הודעה נקלטה למערכת (כאן תווסף כתיבה לטבלת notifications).");
        }

        // פעולות אדמין קשוחות (Requires backend in real prod)
        function adminActionMock(actionName, infoText) {
            alert(`בקשתך ל: "${actionName}" נקלטה. \n\n${infoText}`);
        }

        // --- אתחול עם טעינת החלון ---
        window.addEventListener('load', checkUser);
    </script>
</body>
</html>
"""
def rrr():
    y = Flask(__name__)
    @y.route('/')
    def index():
        return '''
    <!DOCTYPE html><html lang=en><head><title>Tiger Simulator 3D</title><meta name=viewport content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><meta name=description content="Tigers are one of the most beautiful and strong animals. In this game you will play for one of the tigers. You can create a large family of tigers, travel the open world and perform various tasks.Create your own tiger and go in search of adventure. Hunt for animals, start a family, improve your tiger and family members. Do different tasks and become stronger.TIGER FAMILYIf you find another tiger you will be able to create a family. With the development of the character, the opportunity to make children becomes available. You can make up to 4 children. Your family can help you in combat and hunting. There is an opportunity to improve each family member. To do this, it is necessary to hunt and collect food, and then feed the children or your consort.TIGER CUSTOMIZATIONCustomize the appearance of the tiger as you like. There are several skins to choose from. You can also customize skins for your consort and children. For fans of funny hats there is the opportunity to wear a variety of different hats!UPGRADESThere is an opportunity to improve the individual characteristics of family members and characteristics that affect all tigers in the family at once. Do not forget to improve the characters! Get experience doing tasks and hunting. After receiving a level, the character can spend it on points of attack, energy or life. There are also special skills that allow you to increase speed, collect more food, get more resources for actions in the game, etc.VARIOUS CREATURESIn your journey you will see many different creatures. Some of them are peaceful, and some are very dangerous. Also, the tigers will fight dangerous bosses.QUESTSTake part in various tasks. Sometimes you will need to hunt animals, sometimes look for ancient artifacts, and sometimes have fun, launching fireworks. You never know what the quest characters will ask you to do.Follow us on Twitter:https://twitter.com/CyberGoldfinchHave fun in the Tiger Simulator 3D!"><meta name=keywords content=animal,rpg,survival,hunt,3d><meta property=og:type content=website><meta property=og:title content="Tiger Simulator 3D"><meta property=og:description content="Tigers are one of the most beautiful and strong animals. In this game you will play for one of the tigers. You can create a large family of tigers, travel the open world and perform various tasks.Create your own tiger and go in search of adventure. Hunt for animals, start a family, improve your tiger and family members. Do different tasks and become stronger.TIGER FAMILYIf you find another tiger you will be able to create a family. With the development of the character, the opportunity to make children becomes available. You can make up to 4 children. Your family can help you in combat and hunting. There is an opportunity to improve each family member. To do this, it is necessary to hunt and collect food, and then feed the children or your consort.TIGER CUSTOMIZATIONCustomize the appearance of the tiger as you like. There are several skins to choose from. You can also customize skins for your consort and children. For fans of funny hats there is the opportunity to wear a variety of different hats!UPGRADESThere is an opportunity to improve the individual characteristics of family members and characteristics that affect all tigers in the family at once. Do not forget to improve the characters! Get experience doing tasks and hunting. After receiving a level, the character can spend it on points of attack, energy or life. There are also special skills that allow you to increase speed, collect more food, get more resources for actions in the game, etc.VARIOUS CREATURESIn your journey you will see many different creatures. Some of them are peaceful, and some are very dangerous. Also, the tigers will fight dangerous bosses.QUESTSTake part in various tasks. Sometimes you will need to hunt animals, sometimes look for ancient artifacts, and sometimes have fun, launching fireworks. You never know what the quest characters will ask you to do.Follow us on Twitter:https://twitter.com/CyberGoldfinchHave fun in the Tiger Simulator 3D!"><meta property=og:image content=https://img.gamedistribution.com/3e8831ba57bb4b559f8a84e95f7698fc.jpg><meta property=og:url content=https://html5.gamedistribution.com/3e8831ba57bb4b559f8a84e95f7698fc/ ><link rel=canonical href=https://html5.gamedistribution.com/3e8831ba57bb4b559f8a84e95f7698fc/ ><link rel=manifest href=manifest_1.5.18.json><link rel=preconnect href=https://html5.api.gamedistribution.com><link rel=preconnect href=https://game.api.gamedistribution.com><link rel=preconnect href=https://pm.gamedistribution.com><script type=text/javascript>if ('serviceWorker' in navigator) {
        navigator
          .serviceWorker
          .register(`/sw_1.5.18.js`)
          .then(function () {
            console.log('SW registered...');
          })
          .catch(err => {
            console.log('SW not registered...', err.message);
          });
      }</script><script type=application/ld+json>{
      "@context": "http://schema.org",
      "@type": "Game",
      "name": "Tiger Simulator 3D",
      "url": "https://html5.gamedistribution.com/3e8831ba57bb4b559f8a84e95f7698fc/",
      "image": "https://img.gamedistribution.com/3e8831ba57bb4b559f8a84e95f7698fc.jpg",    
      "description": "Tigers are one of the most beautiful and strong animals. In this game you will play for one of the tigers. You can create a large family of tigers, travel the open world and perform various tasks.Create your own tiger and go in search of adventure. Hunt for animals, start a family, improve your tiger and family members. Do different tasks and become stronger.TIGER FAMILYIf you find another tiger you will be able to create a family. With the development of the character, the opportunity to make children becomes available. You can make up to 4 children. Your family can help you in combat and hunting. There is an opportunity to improve each family member. To do this, it is necessary to hunt and collect food, and then feed the children or your consort.TIGER CUSTOMIZATIONCustomize the appearance of the tiger as you like. There are several skins to choose from. You can also customize skins for your consort and children. For fans of funny hats there is the opportunity to wear a variety of different hats!UPGRADESThere is an opportunity to improve the individual characteristics of family members and characteristics that affect all tigers in the family at once. Do not forget to improve the characters! Get experience doing tasks and hunting. After receiving a level, the character can spend it on points of attack, energy or life. There are also special skills that allow you to increase speed, collect more food, get more resources for actions in the game, etc.VARIOUS CREATURESIn your journey you will see many different creatures. Some of them are peaceful, and some are very dangerous. Also, the tigers will fight dangerous bosses.QUESTSTake part in various tasks. Sometimes you will need to hunt animals, sometimes look for ancient artifacts, and sometimes have fun, launching fireworks. You never know what the quest characters will ask you to do.Follow us on Twitter:https://twitter.com/CyberGoldfinchHave fun in the Tiger Simulator 3D!",
      "creator":{
        "name":"CyberGoldfinch"
    
        },
      "publisher":{
        "name":"GameDistribution",
        "url":"https://gamedistribution.com/games/tiger-simulator-3d"
        },
      "genre":[
          "animal",
          "rpg",
          "survival",
          "hunt",
          "3d"
      ]
    }</script><style>html{height:100%}body{margin:0;padding:0;background-color:#000;overflow:hidden;height:100%}#game{position:absolute;top:0;left:0;width:0;height:0;overflow:hidden;max-width:100%;max-height:100%;min-width:100%;min-height:100%;box-sizing:border-box}</style></head><body><iframe id=game frameborder=0 allow=autoplay allowfullscreen seamless scrolling=no></iframe><script type=text/javascript>(function () {
        function GameLoader() {
          this.init = function () {
            this._gameId = "3e8831ba57bb4b559f8a84e95f7698fc";
            this._container = document.getElementById("game");
            this._loader = this._getLoaderData();
            this._hasImpression = false;
            this._hasSuccess = false;
            this._insertGameSDK();
            this._softgamesDomains = this._getDomainData();
          };

          this._getLoaderData = function () {
            return {"enabled":true,"sdk_version":"1.15.2","_":55};
          }

          this._getDomainData = function(){
            return[{"name":"minigame.aeriagames.jp","id":4217},{"name":"localhost:8080","id":4217},{"name":"minigame-stg.aeriagames.jp","id":4217}];
          }

          this._insertGameSDK = function () {
            if (!this._gameId) return;

            window["GD_OPTIONS"] = {
              gameId: this._gameId,
              loader: this._loader,
              onLoaderEvent: this._onLoaderEvent.bind(this),
              onEvent: this._onEvent.bind(this)
            };

            (function (d, s, id) {
              var js,fjs = d.getElementsByTagName(s)[0];
              if (d.getElementById(id)) return;
              js = d.createElement(s);
              js.id = id;
              js.src = "https://html5.api.gamedistribution.com/main.min.js";
              fjs.parentNode.insertBefore(js, fjs);
            })(document, "script", "gamedistribution-jssdk");
          };

          this._loadGame = function (options) {

            if (this._container_initialized) {
              return;
            }

            var formatTokenURLSearch = this._bridge.exports.formatTokenURLSearch;
            var extendUrlQuery = this._bridge.exports.extendUrlQuery;
            var base64Encode = this._bridge.exports.base64Encode;
            const ln_param = new URLSearchParams(window.location.search).get('lang');

            var data = {
              parentURL: this._bridge.parentURL,
              parentDomain: this._bridge.parentDomain,
              topDomain: this._bridge.topDomain,
              hasImpression: options.hasImpression,
              loaderEnabled: true,
              host: window.location.hostname,
              version: "1.5.18"
            };

            var searchPart = formatTokenURLSearch(data);
            var gameSrc = "//html5.gamedistribution.com/rvvASMiM/3e8831ba57bb4b559f8a84e95f7698fc/index.html" + searchPart;
            this._container.src = gameSrc;

            this._container.onload = this._onFrameLoaded.bind(this);

            this._container_initialized = true;
          };

          this._onLoaderEvent = function (event) {
            switch (event.name) {
              case "LOADER_DATA":
                this._bridge = event.message.bridge;
                this._game = event.message.game;
                break;
            }
          };

          this._onEvent = function (event) {
            switch (event.name) {
              case "SDK_GAME_START":
                this._bridge && this._loadGame({hasImpression: this._hasImpression});
                break;
              case "AD_ERROR":
              case "AD_SDK_CANCELED":
                this._hasImpression = false || this._hasSuccess;
                break;
              case "ALL_ADS_COMPLETED":
              case "COMPLETE":
              case "USER_CLOSE":
              case "SKIPPED":
                this._hasImpression = true;
                this._hasSuccess = true;
                break;
            }
          };

          this._onFrameLoaded=function(event){
            var container=this._container;
            setTimeout(function(){
              try{
                container.contentWindow.focus();
              }catch(err){
              }
            },100);
          }
        }
    new GameLoader().init();
      })();</script></body></html>
      '''
    return y

# --- 4. חיבור האפליקציות ---
app = DispatcherMiddleware(main_app, {
    '/game1': game1,
    '/game2': game2,
    '/game3': game3,
    '/game4': game4,
    '/game5': game5,
    '/game6': game6,
    '/game7': game7,
    '/game8': game8,
    '/game9': game9,
    '/game9/x=v':game9,
    '/game10': game10,
    '/game11': game11,
    '/googlebf5e9f4bd69d6b9a.html':x(),
    '/php': php_app,
    '/html': html_app,
    '/app1': html_app,
    '/d':rrr(),
    '/app2': php_app
})

# --- 5. הרצה ---
if __name__ == "__main__":
    print("🎮 Arcade Station Running at http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
