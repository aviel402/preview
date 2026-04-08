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

def create_dummy_app(text):
    dummy = Flask(__name__)
    @dummy.route('/')
    def index():return a(text)
    return dummy

# --- ייבוא בטוח ---
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

main_app = Flask(__name__)

# שמירת מנגנון הלוגו (אם פונים לנתיב הזה ספציפית בטעות, אבל העדפנו /static/logo.png בהמשך)
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

        /* ניווט */
        nav {
            position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
            background: rgba(10, 10, 15, 0.8); backdrop-filter: blur(15px); border-bottom: 1px solid var(--card-border);
            display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }
        .brand-logo { 
            display: flex; align-items: center; gap: 12px; text-decoration: none;
            font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, #a29bfe); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        }
        .brand-logo img { height: 40px; border-radius: 8px; filter: drop-shadow(0 0 8px rgba(108,124,231,0.5)); }
        
        .nav-controls { display: flex; gap: 15px; align-items: center; }
        .btn { border: none; padding: 10px 22px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; }
        .btn-primary { background: var(--accent); color: #000; }
        .btn-primary:hover { box-shadow: 0 0 15px rgba(0, 206, 201, 0.4); transform: translateY(-2px); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
        .btn-danger { background: #ff4757; color: #fff; }
        .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid rgba(108, 124, 231, 0.3); color: #fff; padding: 8px 18px; border-radius: 30px; display: none; }

        /* תוכן ראשי וכרטיסים */
        main { padding: 120px 20px 60px; text-align: center; }
        h1.main-title { font-size: clamp(2.5rem, 8vw, 4.5rem); margin-bottom: 10px; background: linear-gradient(135deg, #fff, #a29bfe, #00cec9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
        .subtitle { color: var(--text-sub); font-size: 1.3rem; margin-bottom: 60px; }

        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; max-width: 1300px; margin: 0 auto; }
        .card { background: var(--card-bg); border-radius: 20px; text-decoration: none; color: white; transition: all 0.4s; border: 1px solid var(--card-border); overflow: hidden; display: flex; flex-direction: column; text-align: right; }
        .card:hover { transform: translateY(-12px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(108, 124, 231, 0.2); border-color: rgba(108, 124, 231, 0.4); }
        .card-cover { height: 130px; display: flex; align-items: center; justify-content: center; font-size: 55px; border-bottom: 1px solid var(--card-border); background: linear-gradient(135deg, rgba(108,124,231,0.2), rgba(0,206,201,0.1)); text-shadow: 0 0 20px rgba(255,255,255,0.2); }
        .card-body { padding: 25px; display: flex; flex-direction: column; }
        .card-body h2 { font-size: 1.6rem; font-weight: 700; margin-bottom: 5px; color: #fff; }
        .card-desc { font-size: 0.95rem; color: #a4b0be; margin-top: 10px; line-height: 1.4; flex-grow: 1; }
        .tag-badge { display: inline-block; align-self: flex-start; padding: 5px 12px; background: rgba(0, 206, 201, 0.15); border: 1px solid rgba(0, 206, 201, 0.3); border-radius: 20px; font-size: 0.8rem; font-weight: 500; color: #00cec9; }

        footer { margin-top: 100px; padding: 20px; text-align: center; color: #4b4b5c; font-size: 0.95rem; border-top: 1px solid var(--card-border); }
        
        .feedback-fab { position: fixed; bottom: 30px; left: 30px; width: 65px; height: 65px; background: linear-gradient(135deg, #6c7ce7, #00cec9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; cursor: pointer; z-index: 990; border: none; transition: 0.3s; }
        .feedback-fab:hover { transform: scale(1.1); box-shadow: 0 15px 35px rgba(0,0,0,0.6); }

        /* חלונות מודל */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: rgba(25, 25, 32, 0.95); border: 1px solid var(--card-border); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto; }
        .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; }
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); color: white; font-size: 1rem; font-family:'Heebo'; }
        .input-box:focus { outline: none; border-color: var(--accent); }
        .hidden-group { display: none; }

        /* ניהול אדמין עשיר */
        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
        .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; }
        .admin-tab.active { background: rgba(255,255,255,0.1); color: #fff; }
        .admin-section { display: none; }
        .admin-section.active { display: block; }
        .user-list, .feedback-list { max-height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
        .user-row, .feedback-row { display: flex; flex-direction: column; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid transparent; }
        .user-row { cursor: pointer; flex-direction: row; justify-content: space-between; align-items: center;}
        .user-row:hover { border-color: var(--primary); }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
        <a href="/" class="brand-logo">
            <img src="/static/logo.png" alt="לוגו" onerror="this.style.display='none'"> 
            Arcade Station
        </a>
        <div class="nav-controls">
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
            <a href="/game1/" class="card"><div class="card-cover">🏝️</div><div class="card-body"><h2>הישרדות</h2><span class="tag-badge">ניהול משאבים</span><p class="card-desc">שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</p></div></a>
            <a href="/game2/" class="card"><div class="card-cover" style="filter: hue-rotate(40deg);">⚔️</div><div class="card-body"><h2>RPG Legend</h2><span class="tag-badge">אקשן טקסטואלי</span><p class="card-desc">הכנסו לעולם פנטזיה אפי בו כל החלטה קובעת את גורלכם בקרב.</p></div></a>
            <a href="/game3/" class="card"><div class="card-cover" style="filter: hue-rotate(80deg);">🚀</div><div class="card-body"><h2>Genesis</h2><span class="tag-badge">מסע בחלל</span><p class="card-desc">הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</p></div></a>
            <a href="/game4/" class="card"><div class="card-cover" style="filter: hue-rotate(120deg);">💻</div><div class="card-body"><h2>קוד אדום</h2><span class="tag-badge">סייבר</span><p class="card-desc">הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</p></div></a>
            <a href="/game5/" class="card"><div class="card-cover" style="filter: hue-rotate(160deg);">🔫</div><div class="card-body"><h2>IRON LEGION</h2><span class="tag-badge">יריות ושרידה</span><p class="card-desc">גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</p></div></a>
            <a href="/game6/" class="card"><div class="card-cover" style="filter: hue-rotate(200deg);">🌑</div><div class="card-body"><h2>מבוך הצללים</h2><span class="tag-badge">אימה</span><p class="card-desc">מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</p></div></a>
            <a href="/game7/" class="card"><div class="card-cover" style="filter: hue-rotate(240deg);">🪐</div><div class="card-body"><h2>PROXIMA</h2><span class="tag-badge">מחקר עולמות</span><p class="card-desc">חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</p></div></a>
            <a href="/game8/" class="card"><div class="card-cover" style="filter: hue-rotate(280deg);">🧬</div><div class="card-body"><h2>הטפיל</h2><span class="tag-badge">ביולוגיה</span><p class="card-desc">מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</p></div></a>
            <a href="/game9/" class="card"><div class="card-cover" style="filter: hue-rotate(320deg);">🍀</div><div class="card-body"><h2>CLOVER</h2><span class="tag-badge">מזל טהור</span><p class="card-desc">הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</p></div></a>
            <a href="/game10/" class="card"><div class="card-cover" style="filter: hue-rotate(360deg);">🏍️</div><div class="card-body"><h2>NEON RIDER</h2><span class="tag-badge">מרוץ</span><p class="card-desc">רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</p></div></a>
            <a href="/game11/" class="card"><div class="card-cover" style="filter: hue-rotate(25deg);">📊</div><div class="card-body"><h2>Manager PRO</h2><span class="tag-badge">ניהול קבוצות</span><p class="card-desc">הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</p></div></a>
        </div>
    </main>

    <footer>&copy; 2026 Arcade Station - Aviel Aluf | x0583289789@gmail.com</footer>

    <!-- משוב -->
    <button class="feedback-fab" onclick="openModal('feedback-modal')">💬</button>

    <!-- מודל התחברות מדויק יותר -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-title"></h2>
            
            <div class="form-group" id="box-email"><label>אימייל:</label><input type="email" id="f-email" class="input-box"></div>
            <div class="form-group" id="box-pass"><label>סיסמה:</label><input type="password" id="f-pass" class="input-box"></div>
            <div class="form-group" id="box-nick"><label>כינוי:</label><input type="text" id="f-nick" class="input-box"></div>
            
            <!-- נשמור ב-JS מה מצב החלון כדי שלא יהיו שגיאות -->
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px;">אשר</button>
            
            <div id="auth-switch-link" style="text-align:center; margin-top:15px; color:var(--accent); cursor:pointer;"></div>
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
            <!-- רשימת המשחקים שמופיעה רק כצריך! -->
            <div class="form-group hidden-group" id="fb-game-box">
                <label>על איזה משחק מדובר?</label>
                <select id="fb-game" class="input-box">
                    <option value="main">התחנה הראשית (האתר)</option>
                    <option value="הישרדות">הישרדות</option>
                    <option value="RPG Legend">RPG Legend</option>
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

    <!-- מודל מנהל משודרג (משתמשים + משובים) -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757;">פאנל מנהל מערכת</h2>
            
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול שחקנים</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">משובים והערות 📥</button>
            </div>

            <!-- אזור ניהול שחקנים -->
            <div id="section-users" class="admin-section active">
                <input type="text" id="admin-search" class="input-box" style="margin-bottom:15px;" placeholder="חפש לפי כינוי...">
                <div class="user-list" id="admin-user-list"></div>
            </div>

            <!-- אזור משובים -->
            <div id="section-feedbacks" class="admin-section">
                <div class="feedback-list" id="admin-feedback-list">
                    <p style="color:#a4b0be; text-align:center;">טוען נתונים מהשרת...</p>
                </div>
            </div>
        </div>
    </div>

    <!-- JS -->
    <script>
        const supUrl = 'https://ryoykooazoaordzmxdat.supabase.co';
        const supKey = 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B';
        const sp = supabase.createClient(supUrl, supKey);
        let cUser = null;
        let currentAuthMode = 'LOGIN'; // LOGIN | SIGNUP | EDIT

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }

        async function checkUser() {
            const { data } = await sp.auth.getUser();
            cUser = data.user;
            updateUI();
        }

        function updateUI() {
            const isAdm = cUser && cUser.email === 'x0583289789@gmail.com';
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? '⚙ פרופיל' : 'התחבר / הרשם';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        /* ======== טיפול משופר ללא באגים בהתחברות ובהרשמה ======== */
        function openAuthModal(mode) {
            currentAuthMode = mode;
            document.getElementById('f-email').value = '';
            document.getElementById('f-pass').value = '';
            
            const eBox = document.getElementById('box-email');
            const pBox = document.getElementById('box-pass');
            const nBox = document.getElementById('box-nick');
            const tTxt = document.getElementById('auth-title');
            const bBtn = document.getElementById('auth-exec-btn');
            const lnk = document.getElementById('auth-switch-link');

            if (mode === 'LOGIN') {
                tTxt.innerText = 'התחברות'; eBox.style.display = 'block'; pBox.style.display = 'block'; nBox.style.display = 'none';
                bBtn.innerText = 'כניסה למערכת';
                lnk.style.display = 'block'; lnk.innerText = 'משתמש חדש? לחץ כאן להרשמה.';
                lnk.onclick = () => openAuthModal('SIGNUP');
                bBtn.onclick = doLogin;
            } else if (mode === 'SIGNUP') {
                tTxt.innerText = 'הרשמה'; eBox.style.display = 'block'; pBox.style.display = 'block'; nBox.style.display = 'block';
                bBtn.innerText = 'צור חשבון';
                lnk.style.display = 'block'; lnk.innerText = 'יש לך חשבון? התחבר כאן.';
                lnk.onclick = () => openAuthModal('LOGIN');
                bBtn.onclick = doSignUp;
            } else if (mode === 'EDIT') {
                tTxt.innerText = 'עדכון שם תצוגה'; eBox.style.display = 'none'; pBox.style.display = 'none'; nBox.style.display = 'block';
                document.getElementById('f-nick').value = cUser.user_metadata?.nickname || '';
                bBtn.innerText = 'שמור פרופיל'; lnk.style.display = 'none';
                bBtn.onclick = doEditProfile;
            }
            openModal('auth-modal');
        }

        async function doLogin() {
            const e = document.getElementById('f-email').value; const p = document.getElementById('f-pass').value;
            if(!e || !p) return alert("חסרים פרטים");
            const { error } = await sp.auth.signInWithPassword({ email:e, password:p });
            if (error) return alert("שגיאת התחברות: " + error.message);
            closeModal('auth-modal'); checkUser();
        }

        async function doSignUp() {
            const e = document.getElementById('f-email').value; const p = document.getElementById('f-pass').value; const n = document.getElementById('f-nick').value;
            if(!e || !p || !n) return alert("נא למלא את כל השדות!");
            const { data, error } = await sp.auth.signUp({ email:e, password:p, options:{ data:{ nickname:n } } });
            if (error) return alert("שגיאת הרשמה: " + error.message);
            if (data.user) await sp.from('profiles').upsert({ user_id: data.user.id, nickname: n });
            alert("נרשמת בהצלחה!"); closeModal('auth-modal'); checkUser();
        }

        async function doEditProfile() {
            const n = document.getElementById('f-nick').value;
            if(!n) return alert("הכנס כינוי");
            await sp.auth.updateUser({ data: { nickname: n } });
            await sp.from('profiles').upsert({ user_id: cUser.id, nickname: n });
            alert("פרופיל עודכן"); closeModal('auth-modal'); checkUser();
        }


        /* ======== משובים ======== */
        function updateFeedbackUI() {
            const v = document.getElementById('fb-topic').value;
            document.getElementById('fb-game-box').style.display = (v === 'tech' || v === 'idea') ? 'block' : 'none';
            document.getElementById('fb-text-box').style.display = v ? 'block' : 'none';
        }

        async function submitFeedback() {
            const top = document.getElementById('fb-topic').value;
            const gam = document.getElementById('fb-game-box').style.display === 'block' ? document.getElementById('fb-game').value : 'כללי';
            const txt = document.getElementById('fb-text').value;
            if(!txt) return alert("בבקשה פרט קצת.");

            try {
                // המערכת מנסה להכניס נתונים לטבלת feedbacks בשרת! 
                // אם היא לא קיימת ב-Supabase תקפוץ שגיאה, לכן תקרא את ההנחיות למטה.
                const { error } = await sp.from('feedbacks').insert({
                    user_email: cUser ? cUser.email : 'אורח',
                    topic: top, game: gam, text: txt
                });
                if(error) {
                    console.log(error);
                    alert("שימו לב אדמין: אם מופיעה שגיאה 404, זה בגלל שעוד לא פתחתם את טבלת 'feedbacks' ב-Supabase! הנתונים למטה יראו איך זה יראה כשיעבוד.");
                } else {
                    alert('תודה רבה! המשוב נשלח בהצלחה 📨');
                }
            } catch (err) { console.error(err); }
            closeModal('feedback-modal');
            document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; updateFeedbackUI();
        }

        /* ======== פאנל אדמין מורחב ======== */
        async function openAdminModal() {
            openModal('admin-modal'); switchAdminTab('users');
            
            // שאיבת משתמשים
            const { data: uData } = await sp.from('profiles').select('*');
            let uHtml = '';
            (uData||[]).forEach(u => uHtml += `<div class="user-row"><div style="color:var(--accent);"><b>${u.nickname}</b><br><span style="font-size:0.8rem;color:#888;">ID: ${u.user_id}</span></div></div>`);
            document.getElementById('admin-user-list').innerHTML = uHtml || 'אין נתונים';

            // שאיבת משובים - יעבוד רק אחרי שתיצור את הטבלה בסופאבייס
            const { data: fData, error: fErr } = await sp.from('feedbacks').select('*').order('created_at', { ascending: false });
            let fHtml = '';
            if(fErr || !fData || fData.length===0) {
                fHtml = '<div style="text-align:center; padding:20px;">אין משובים במערכת עדיין.<br><span style="font-size:0.8rem; color:#888;">(וודא שיצרת טבלת feedbacks ב-Supabase)</span></div>';
            } else {
                fData.forEach(f => {
                    const dType = f.topic === 'tech' ? '🛠️ תקלה' : f.topic === 'idea' ? '💡 הצעה' : '💬 הערה';
                    fHtml += `
                    <div class="feedback-row">
                        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                            <strong style="color:var(--accent);">${dType} | משחק: ${f.game || 'כללי'}</strong>
                            <small style="color:#777;">מאת: ${f.user_email}</small>
                        </div>
                        <p style="background:rgba(0,0,0,0.5); padding:10px; border-radius:8px; margin:0; font-size:0.95rem;">${f.text}</p>
                    </div>`;
                });
            }
            document.getElementById('admin-feedback-list').innerHTML = fHtml;
        }

        function switchAdminTab(tabName) {
            document.getElementById('tab-users-btn').classList.toggle('active', tabName === 'users');
            document.getElementById('tab-feedbacks-btn').classList.toggle('active', tabName === 'feedbacks');
            document.getElementById('section-users').classList.toggle('active', tabName === 'users');
            document.getElementById('section-feedbacks').classList.toggle('active', tabName === 'feedbacks');
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

def rrr():
    y = Flask(__name__)
    @y.route('/')
    def index():
        return '''
    <!DOCTYPE html><html lang=en><head><title>Tiger Simulator 3D</title><meta name=viewport content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><meta name=description content="Tigers are one of the most beautiful and strong animals..."><style>html{height:100%}body{margin:0;padding:0;background-color:#000;overflow:hidden;height:100%}#game{position:absolute;top:0;left:0;width:0;height:0;overflow:hidden;max-width:100%;max-height:100%;min-width:100%;min-height:100%;box-sizing:border-box}</style></head><body><iframe id=game frameborder=0 allow=autoplay allowfullscreen seamless scrolling=no></iframe><script type=text/javascript>(function(){function GameLoader(){this.init=function(){this._gameId="3e8831ba57bb4b559f8a84e95f7698fc";this._container=document.getElementById("game");this._loader={"enabled":true,"sdk_version":"1.15.2","_":55};this._hasImpression=false;this._hasSuccess=false;this._insertGameSDK();};this._insertGameSDK=function(){window["GD_OPTIONS"]={gameId:this._gameId,loader:this._loader,onLoaderEvent:this._onLoaderEvent.bind(this),onEvent:this._onEvent.bind(this)};(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(d.getElementById(id))return;js=d.createElement(s);js.id=id;js.src="https://html5.api.gamedistribution.com/main.min.js";fjs.parentNode.insertBefore(js,fjs);})(document,"script","gamedistribution-jssdk");};this._loadGame=function(options){if(this._container_initialized)return;var searchPart="?hasImpression="+options.hasImpression+"&loaderEnabled=true&host="+window.location.hostname;var gameSrc="//html5.gamedistribution.com/rvvASMiM/"+this._gameId+"/index.html"+searchPart;this._container.src=gameSrc;this._container.onload=this._onFrameLoaded.bind(this);this._container_initialized=true;};this._onLoaderEvent=function(e){if(e.name==="LOADER_DATA"){this._bridge=e.message.bridge;this._game=e.message.game;}};this._onEvent=function(e){switch(e.name){case"SDK_GAME_START":this._bridge&&this._loadGame({hasImpression:this._hasImpression});break;case"AD_ERROR":case"AD_SDK_CANCELED":this._hasImpression=false||this._hasSuccess;break;case"ALL_ADS_COMPLETED":case"COMPLETE":case"USER_CLOSE":case"SKIPPED":this._hasImpression=true;this._hasSuccess=true;break;}};this._onFrameLoaded=function(){var container=this._container;setTimeout(function(){try{container.contentWindow.focus();}catch(err){}},100);};}new GameLoader().init();})();</script></body></html>
    '''
    return y

app = DispatcherMiddleware(main_app, {
    '/game1': game1, '/game2': game2, '/game3': game3, '/game4': game4, '/game5': game5,
    '/game6': game6, '/game7': game7, '/game8': game8, '/game9': game9, '/game9/x=v':game9,
    '/game10': game10, '/game11': game11, '/googlebf5e9f4bd69d6b9a.html':x(),
    '/php': php_app, '/html': html_app, '/app1': html_app, '/d':rrr(), '/app2': php_app
})

if __name__ == "__main__":
    print("🎮 Arcade Station Running at http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
