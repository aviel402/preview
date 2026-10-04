import os
from flask import Flask, render_template_string
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# =======================================================
# אפליקציות דמה למשחקים השונים
# =======================================================
def create_dummy_app(text):
    dummy = Flask(__name__)
    @dummy.route('/')
    def index():
        return f'''
          <!DOCTYPE html>
          <html lang="he" dir="rtl">
          <head>
              <meta charset="UTF-8">
              <title>{text}</title>
              <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
              <style>
                body {{ margin: 0; font-family: 'Heebo', sans-serif; background-color: #0b0c10; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow:hidden;}}
                .container {{ text-align: center; padding: 40px; background: rgba(31, 40, 51, 0.6); border-radius: 20px; border: 1px solid #66fcf1; box-shadow: 0 0 25px rgba(102, 252, 241, 0.2); backdrop-filter: blur(10px);}}
                h1 {{ font-size: 3rem; color: #66fcf1; text-shadow: 0 0 10px rgba(102, 252, 241, 0.5); margin:0;}}
              </style>
          </head>
          <body>
            <div class="container">
              <div style="font-size: 60px; margin-bottom: 20px;">🚧</div>
              <h1>{text}</h1>
              <p style="color: #c5c6c7; margin-top: 15px; font-size:1.1rem;">המשחק עדיין בפיתוח... הישארו מעודכנים!</p>
            </div>
          </body>
          </html>
        '''
    return dummy

try: from app1 import app as game1
except ImportError: game1 = create_dummy_app("הישרדות 🏝️")
try: from app2 import app as game2
except ImportError: game2 = create_dummy_app("Gold Forest 🌲")
try: from app3 import app as game3
except ImportError: game3 = create_dummy_app("Genesis 🚀")
try: from app4 import app as game4
except ImportError: game4 = create_dummy_app("קוד אדום 💻")
try: from app5 import app as game5
except ImportError: game5 = create_dummy_app("IRON LEGION 🔫")
try: from app6 import app as game6
except ImportError: game6 = create_dummy_app("מבוך הצללים 🌑")
try: from app7 import app as game7
except ImportError: game7 = create_dummy_app("PROXIMA 🪐")
try: from app8 import app as game8
except ImportError: game8 = create_dummy_app("הטפיל 🧬")
try: from app9 import app as game9
except ImportError: game9 = create_dummy_app("CLOVER 🍀")
try: from app10 import app as game10
except ImportError: game10 = create_dummy_app("NEON RIDER 🏍️")
try: from app11 import app as game11
except ImportError: game11 = create_dummy_app("Manager PRO 📊")
try: from php import app as php_app
except ImportError: php_app = create_dummy_app("PHP App")
try: from HTML import app as html_app
except ImportError: html_app = create_dummy_app("HTML App")

def verification_app():
    v = Flask(__name__)
    @v.route('/')
    def index(): return 'google-site-verification: googlebf5e9f4bd69d6b9a.html'
    return v

main_app = Flask(__name__, static_folder='static') # הוגדר כדי לשרת אוטומטית מתיקיית static

def render_page(content, **kwargs):
    html = BASE_HTML.replace('<!-- CONTENT_BLOCK -->', content)
    return render_template_string(html, **kwargs)

@main_app.route('/')
def index(): 
    return render_page(MENU_CONTENT)

@main_app.route('/play/<path:target>')
def play_view(target):
    return render_page(PLAY_CONTENT, target=target)

# =======================================================
# תבנית בסיס (BASE_HTML) - עיצוב סייברפאנק / ארקייד חדש!
# =======================================================
BASE_HTML = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>if (window.top !== window.self) { window.top.location = window.self.location; }</script>
    <style>
        /* Neon Cyberpunk Theme */
        :root { 
            --primary: #c501e2;       /* Neon Pink/Magenta */
            --accent: #66fcf1;        /* Cyber Cyan */
            --accent-dark: #45a29e;   /* Darker Cyan */
            --bg-dark: #0b0c10;       /* Very Dark Navy/Black */
            --card-bg: #1f2833;       /* Blueish Grey for cards */
            --text-main: #ffffff;     /* Bright White */
            --text-sub: #c5c6c7;      /* Grey/Silver */
            --danger: #ff0055;        /* Neon Red */
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; display: flex; flex-direction: column; overflow: hidden; background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; }
        
        /* Grid Animated Background */
        .bg-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
            background: linear-gradient(rgba(11, 12, 16, 0.9), rgba(11, 12, 16, 0.9)), 
                        repeating-linear-gradient(transparent, transparent 40px, rgba(102, 252, 241, 0.05) 40px, rgba(102, 252, 241, 0.05) 41px),
                        repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(102, 252, 241, 0.05) 40px, rgba(102, 252, 241, 0.05) 41px);
        }

        /* Navbar - Glass/Neon effect */
        nav { height: 75px; flex-shrink: 0; background: rgba(11, 12, 16, 0.85); border-bottom: 2px solid rgba(102, 252, 241, 0.3); backdrop-filter: blur(12px); display: flex; justify-content: space-between; align-items: center; padding: 0 40px; z-index: 1000; position:relative; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.8); }
        .nav-right-area { display: flex; align-items: center; gap: 40px; }
        
        .brand-logo { display: flex; align-items: center; gap: 15px; text-decoration: none; font-size: 1.8rem; font-weight: 900; color: #fff; letter-spacing: 1px; text-shadow: 0 0 10px var(--accent); transition: 0.3s; }
        .brand-logo img { height: 45px; transition: 0.3s; filter: drop-shadow(0 0 5px var(--accent)); }
        .brand-logo:hover { text-shadow: 0 0 20px var(--primary); }
        .brand-logo:hover img { transform: scale(1.1); filter: drop-shadow(0 0 10px var(--primary)); }

        .top-links { display: flex; gap: 25px; align-items: center; }
        .top-links a { color: var(--text-sub); text-decoration: none; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.5px; transition: 0.3s; cursor:pointer; text-transform: uppercase;}
        .top-links a:hover { color: var(--accent); text-shadow: 0 0 8px var(--accent); }
        
        /* Dropdown Setup */
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background: rgba(31, 40, 51, 0.95); min-width: 240px; border: 1px solid var(--accent); box-shadow: 0 10px 40px rgba(102, 252, 241, 0.2); border-radius: 8px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right; z-index:999;}
        .dropdown:hover .dropdown-content { display: block; animation: fadeUp 0.3s ease; }
        .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; border-left: 3px solid transparent; transition: 0.2s; font-weight: 500;}
        .dropdown-content a:hover { background: rgba(102, 252, 241, 0.1); border-left: 3px solid var(--accent); color: var(--accent); padding-right: 25px;}
        
        @keyframes fadeUp { from {opacity:0; transform: translateY(10px);} to {opacity:1; transform: translateY(0);} }

        .nav-left-area { display: flex; gap: 15px; align-items: center; }
        .user-pill { background: rgba(11, 12, 16, 0.8); border: 2px solid; color: #fff; padding: 6px 20px; border-radius: 5px; font-weight: 900; display: none; transition: 0.3s; text-shadow: 0 0 5px rgba(255,255,255,0.5);}
        
        /* Buttons */
        .btn { border: none; padding: 10px 24px; border-radius: 4px; font-weight: 900; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px;}
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .btn-primary { background: transparent; color: var(--accent); border: 2px solid var(--accent); box-shadow: inset 0 0 10px rgba(102,252,241,0.2), 0 0 10px rgba(102,252,241,0.2); }
        .btn-primary:not(:disabled):hover { background: var(--accent); color: var(--bg-dark); box-shadow: 0 0 20px var(--accent); }
        .btn-secondary { background: var(--card-bg); color: var(--text-main); border: 1px solid var(--text-sub); }
        .btn-secondary:hover { border-color: var(--text-main); box-shadow: 0 0 10px rgba(255,255,255,0.2); }
        .btn-danger { background: transparent; color: var(--danger); border: 2px solid var(--danger); }
        .btn-danger:hover { background: var(--danger); color: #fff; box-shadow: 0 0 15px var(--danger); }
        .btn-action-small { background: rgba(31,40,51,0.8); border:1px solid; border-radius: 4px; padding: 6px 12px; cursor: pointer; font-size: 0.85rem; transition: 0.2s; font-weight: bold;}
        .btn-action-small:hover { filter: brightness(1.5); }

        /* Structure */
        .content-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; z-index: 1;}
        .scroll-content { overflow-y: auto; width: 100%; height: 100%; padding-bottom: 80px;}
        .iframe-content { width: 100%; height: 100%; border: none; }

        /* Modals Cyberpunk Style */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(11, 12, 16, 0.9); backdrop-filter: blur(5px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
        .modal-overlay.active { display: flex; opacity: 1; }
        .modal-content { background: var(--card-bg); border: 1px solid var(--accent); padding: 40px; border-radius: 10px; width: 90%; max-width: 500px; box-shadow: 0 0 30px rgba(102, 252, 241, 0.15); position: relative; text-align: right; max-height:90vh; overflow-y:auto; }
        .modal-close { position: absolute; top: 15px; left: 15px; background: none; border: none; color: var(--text-sub); font-size: 28px; cursor: pointer; transition: 0.3s; font-weight: 300;}
        .modal-close:hover { color: var(--danger); transform: scale(1.1); text-shadow: 0 0 10px var(--danger);}
        
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); font-weight: bold; font-size: 0.9rem; letter-spacing: 0.5px;}
        .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 4px; background: #12181f; border: 1px solid rgba(102,252,241,0.2); color: white; font-size: 1rem; font-family:'Heebo'; transition: 0.3s;}
        .input-box:focus { outline: none; border-color: var(--accent); box-shadow: inset 0 0 5px rgba(102,252,241,0.5); }
        .input-box:disabled { opacity: 0.6; background: #0b0c10; }
        input[type="color"] { cursor: pointer; height: 50px; padding: 2px;}
        .hidden-group { display: none; }
        
        #auth-error { color: #fff; background: rgba(255, 0, 85, 0.2); border-right: 4px solid var(--danger); padding: 12px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right; font-weight: bold;}
        
        .auth-tabs { display: flex; gap: 10px; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; }
        .auth-tab-btn { background: none; border: none; color: var(--text-sub); font-size: 1.2rem; cursor: pointer; padding: 10px 15px; font-weight: bold; transition: 0.3s; text-transform: uppercase;}
        .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); text-shadow: 0 0 8px rgba(102,252,241,0.4);}

        .admin-modal { max-width: 900px; }
        .admin-tabs { display: flex; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;}
        .admin-tab { background: transparent; border: 1px solid var(--text-sub); color: var(--text-sub); font-size: 1rem; cursor: pointer; padding: 8px 20px; border-radius: 4px; transition: 0.2s; font-weight:bold;}
        .admin-tab.active { border-color: var(--primary); color: var(--primary); background: rgba(197, 1, 226, 0.1); text-shadow: 0 0 5px var(--primary);}
        .admin-section { display: none; }
        .admin-section.active { display: block; animation: fadeUp 0.4s; }
        
        .user-list, .feedback-list { max-height: 450px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; padding-left: 5px; padding-right:5px;}
        .user-row, .feedback-row { display: flex; flex-direction: column; background: #12181f; padding: 18px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); transition: 0.3s; border-right: 5px solid transparent; }
        .user-row:hover, .feedback-row:hover { border-color: rgba(255,255,255,0.2); background: rgba(31, 40, 51, 0.8);}
        .user-row { flex-direction: row; justify-content: space-between; align-items: center;}
        
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: var(--bg-dark); } ::-webkit-scrollbar-thumb { background: var(--accent-dark); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station">
                <img src="/static/logo.png" alt="👾" onerror="this.style.display='none'"> 
                ARCADE STATION
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
                <a onclick="alert('טבלאות דירוג ציבוריות בגרסת הרשת יגיעו בקרוב!')">טבלאות</a>
                <a onclick="openModal('about-modal')">אודות</a>
            </div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ SYSTEM</button>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">CONNECT</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">LOGOUT</button>
        </div>
    </nav>
    
    <div class="content-area">
        <!-- CONTENT_BLOCK -->
    </div>

    <!-- מודל התחברות / הרשמה / עריכה -->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 25px; font-weight:900;">הגדרות סייבר</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">LOGIN</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">REGISTER</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">סיסמת קשר (אימייל):</label>
                <input type="email" id="f-email" class="input-box" placeholder="player@arcade.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">זיהוי שחקן (כינוי):</label>
                <input type="text" id="f-user" class="input-box" placeholder="הכנס שם שחקן...">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label>צבע אאורה (לזיהוי אישי):</label>
                <input type="color" id="f-color" class="input-box" value="#66fcf1" style="height:45px;">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">קוד סודי (סיסמה):</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:15px; font-size:1.1rem; padding:12px;" onclick="executeAuthAction()">אתחל חיבור</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 20px;">
                <button class="btn btn-danger" style="width:100%;" onclick="deleteSelf()">מחק ישות סייבר לצמיתות 🗑️</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:20px; font-size:0.9rem; color:var(--text-sub); cursor:pointer; font-weight:bold;" onclick="setAuthUI('RECOVERY')"><u>> שחזר סיסמה <</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:20px; font-size:0.9rem; color:var(--accent); cursor:pointer; font-weight:bold;" onclick="setAuthUI('LOGIN')"><u>> ביטול ופנייה למסך חיבור <</u></p>
        </div>
    </div>

    <!-- מודל אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content" style="max-width: 650px;">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: var(--primary); margin-bottom:15px; text-shadow: 0 0 10px var(--primary); font-weight:900;">ARCADE STATION v2.0</h2>
            <div style="text-align: right; color: var(--text-main); font-size: 1.1rem; line-height:1.6;">
                <p>מערכת ארקייד סייברפאנק חכמה. אוסף משימות רשת, משחקי הישרדות ואתגרים ישירות בדפדפן - אפס הורדות.</p>
                <div style="background: rgba(0,0,0,0.5); padding: 15px; border-left: 4px solid var(--accent); margin-top: 20px; border-radius: 4px;">
                    <h3 style="color: var(--accent); font-size:1rem; margin-bottom:5px;">[ TERMINAL ROOT_AUTHOR ]</h3>
                    <p style="margin:0;">נבנה ומתוחזק ע"י <strong>אביאל</strong>.</p>
                    <p style="margin:5px 0 0 0; font-size:0.95rem;">קוד התקשרות: <span style="color:var(--primary); font-family:monospace; letter-spacing:1px;">x0583289789@gmail.com</span></p>
                </div>
            </div>
        </div>
    </div>

    <!-- מודל שליחת משוב -->
    <div id="feedback-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'feedback-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('feedback-modal')">✖</button>
            <h2 style="color:var(--accent); margin-bottom:20px; text-shadow:0 0 5px var(--accent);">שידור הודעה למערכת 📡</h2>
            <div class="form-group">
                <label>סוג חבילת נתונים:</label>
                <select id="fb-topic" class="input-box" onchange="document.getElementById('fb-text-box').style.display=this.value?'block':'none'">
                    <option value="" disabled selected>-- בחר --</option>
                    <option value="bug">זיהוי באג (תקלה טכנית)</option>
                    <option value="idea">שדרוג חומרה (רעיון לשיפור)</option>
                    <option value="other">תשדורת רגילה</option>
                </select>
            </div>
            <div class="form-group hidden-group" id="fb-text-box">
                <label>תוכן השדר:</label>
                <textarea id="fb-text" rows="5" class="input-box"></textarea>
                <button class="btn btn-primary" style="width:100%; margin-top:15px;" onclick="submitFeedback()">> SHIFT_SEND</button>
            </div>
        </div>
    </div>

    <!-- פאנל ניהול אדמין -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: var(--danger); margin-bottom: 20px; font-weight:900; text-shadow:0 0 10px rgba(255,0,85,0.4);">[ ROOT ACCESS // SYSTEM OVERRIDE ]</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">USERS_DB 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">INBOX_STREAM 📥</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>

    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("Supabase failed", e); }
        
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        // הגנת XSS
        function escapeHTML(str) {
            if (!str) return '';
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

        document.addEventListener('DOMContentLoaded', () => {
            ['f-email', 'f-user', 'f-pass'].forEach(id => {
                const el = document.getElementById(id);
                if(el) el.addEventListener('keypress', e => { if (e.key === 'Enter') { e.preventDefault(); executeAuthAction(); } });
            });
        });

        function openModal(id) { document.getElementById(id).classList.add('active'); showError(); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); showError(); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }
        function showError(msg = '') {
            const errBox = document.getElementById('auth-error');
            if(msg) { errBox.style.display = 'block'; errBox.innerText = '! ' + msg; } 
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
                            alert("❌ החשבון הוגדר כחסום. מנתק תקשורת..."); 
                            await logout(); 
                            return; 
                        }
                        if(dbProfile.message) { 
                            alert(">>> תשדורת מנהל <<<\\n\\n" + dbProfile.message); 
                            await sp.from('profiles').update({ message: null }).eq('user_id', cUser.id);
                        }
                        cUser.customColor = dbProfile.color || cUser.user_metadata?.color || '#66fcf1'; 
                    } else { 
                        cUser.customColor = cUser.user_metadata?.color || '#66fcf1'; 
                    }
                } catch(e) { cUser.customColor = '#66fcf1'; }
            }
            updateUI();
        }

        function updateUI() {
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            const pill = document.getElementById('user-status');
            
            if(cUser) {
                pill.style.display = 'block';
                let nick = cUser.user_metadata?.nickname || cUser.email.split('@')[0];
                document.getElementById('nickname-display').innerText = 'SYS.ID: ' + nick.toUpperCase();
                pill.style.borderColor = cUser.customColor;
                document.getElementById('nickname-display').style.color = cUser.customColor;
                pill.style.boxShadow = `0 0 10px ${cUser.customColor}40`;
            } else { pill.style.display = 'none'; }
            
            const btnMain = document.getElementById('main-action-btn');
            btnMain.innerText = cUser ? 'CONFIG' : 'CONNECT';
            btnMain.onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = ''; 
            document.getElementById('f-color').value = cUser?.customColor || '#66fcf1';
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
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל זיהוי:'; 
                bU.style.display='none'; bC.style.display='none'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='קוד גישה (סיסמה):'; 
                btn.innerText='אתחל חיבור למערכת'; fPassLnk.style.display='block'; bLoginLnk.style.display='none';
            } else if (mode === 'SIGNUP') {
                tL.classList.remove('active'); tS.classList.add('active');
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל להתקשרות חדשה:';
                bU.style.display='block'; document.getElementById('lbl-user').innerText='כינוי סייבר בשרת:'; 
                bC.style.display='block'; bP.style.display='block'; document.getElementById('lbl-pass').innerText='הגדר קוד (6 תווים מינימום):'; 
                btn.innerText='בצע רישום וחיבור מלא'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'EDIT') {
                titleEdit.style.display='block'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='אימייל נעול:'; document.getElementById('f-email').value = cUser?.email || ''; document.getElementById('f-email').disabled = true;
                bU.style.display='block'; document.getElementById('lbl-user').innerText='עדכן כינוי:'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = cUser?.customColor || '#66fcf1';
                bP.style.display='block'; document.getElementById('lbl-pass').innerText='עדכון סיסמה (השאר ריק אם אין שינוי):';
                btn.innerText='SAVE DATA // עריכה'; deleteDiv.style.display = 'block'; fPassLnk.style.display='none'; bLoginLnk.style.display='none';
            } else if (mode === 'RECOVERY') {
                titleEdit.style.display='block'; titleEdit.innerText='OVERRIDE: שחזור הרשאות'; tabsCon.style.display='none';
                bE.style.display='block'; document.getElementById('lbl-email').innerText='הזן את אימייל הזיהוי שלך:'; 
                bU.style.display='none'; bP.style.display='none'; btn.innerText='בקש קוד חדש';
                fPassLnk.style.display='none'; bLoginLnk.style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("שגיאת מערכת. התחברות ל-DB נכשלה.");
            const btn = document.getElementById('auth-exec-btn');
            btn.disabled = true; const textOrig = btn.innerText; btn.innerText = 'PROCESSING... ⏳';
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
            if(!email || !p) return showError("שדות חסרים להתחברות.");
            const { error } = await sp.auth.signInWithPassword({ email: email.toLowerCase(), password: p });
            if(error) return showError("גישה נדחתה. פרטים שגויים.");
            closeModal('auth-modal'); await checkUser();
        }

        async function doSignUp() {
            const nickname = document.getElementById('f-user').value.trim(); 
            const email = document.getElementById('f-email').value.trim(); 
            const p = document.getElementById('f-pass').value; 
            const clr = document.getElementById('f-color').value;
            
            if(!nickname || !email || !p) return showError("יש למלא את כל השדות כדי ליצור יישות רשת.");
            if(p.length < 6) return showError("הקוד קצר מדי.");

            const { data: dbHasNick } = await sp.from('profiles').select('nickname').eq('nickname', nickname).maybeSingle();
            if(dbHasNick) return showError("הכינוי כבר רשום במערכת ע''י סוכן אחר.");
            
            const { data, error } = await sp.auth.signUp({ email: email.toLowerCase(), password: p, options:{ data:{ nickname: nickname, color: clr } } });
            
            if (error) return showError("תקלה ברישום: " + error.message);
            if (data.user) { 
                await sp.from('profiles').insert({ user_id: data.user.id, nickname: nickname, color: clr, banned: false, message: null }); 
                await checkUser(); 
                alert("יישות הרשת נוצרה בהצלחה. ברוך הבא."); 
                closeModal('auth-modal'); 
            }
        }

        async function doEditProfile() {
            const newN = document.getElementById('f-user').value.trim(); 
            const newPass = document.getElementById('f-pass').value.trim(); 
            const newC = document.getElementById('f-color').value;
            
            if(newN) { 
                await sp.auth.updateUser({ data: { nickname: newN, color: newC } }); 
                // שינוי קריטי: מעבר מ-upsert ל-update מפורש ו-eq כדי להבטיח שהנתון יישמר 
                const {error} = await sp.from('profiles').update({ nickname: newN, color: newC }).eq('user_id', cUser.id);
                if(error) console.warn("אזהרת DB בשמירת צבע:", error);
            }
            if(newPass && newPass.length >= 6) { await sp.auth.updateUser({ password: newPass }); }
            
            closeModal('auth-modal'); 
            await checkUser(); // מרפרש את הצבע לויזואל
            alert("תצורת פרופיל עודכנה בהצלחה!");
        }

        async function doRecovery() {
            const emailF = document.getElementById('f-email').value.trim();
            const { error } = await sp.auth.resetPasswordForEmail(emailF.toLowerCase());
            if (error) showError("שגיאה, בדוק שהאימייל תקין.");
            else { alert("שדר איפוס נשלח לתיבת המייל."); setAuthUI('LOGIN'); }
        }

        async function deleteSelf() {
            if(!confirm("אזהרת מחיקה: הפעולה בלתי הפיכה! למחוק הכל?")) return;
            try { 
                await sp.from('profiles').delete().eq('user_id', cUser.id); 
                await sp.auth.signOut(); 
                closeModal('auth-modal'); cUser = null; updateUI(); 
            } catch (err) { alert("Failed: " + err.message); }
        }

        async function submitFeedback() { 
            const t = document.getElementById('fb-topic').value; 
            const tx = document.getElementById('fb-text').value; 
            if(!tx || !t) return alert("יש לבחור נושא ותוכן לשדר.");
            try { 
                const {error} = await sp.from('feedbacks').insert({ user_email: cUser ? cUser.email : 'GUEST_USER', topic: t, text: tx }); 
                if(error) throw error;
                alert('התשדורת נקלטה במאגרי המערכת המרכזית. תודה!'); 
                closeModal('feedback-modal'); document.getElementById('fb-topic').value=''; document.getElementById('fb-text').value=''; document.getElementById('fb-text-box').style.display='none';
            } catch (err) { alert("DB REJECTED: ודא שמדיניות האבטחה (RLS) של הטבלה מתירה הוספה (INSERT). " + err.message); } 
        }

        // ---------- אדמין פאנל ----------
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">SCANNING DB... ⏳</p>'; fList.innerHTML = '<p style="text-align:center;">SCANNING... ⏳</p>';
            try {
                const { data: pList, error: pErr } = await sp.from('profiles').select('*'); 
                if(pErr) throw pErr;
                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => `
                    <div class="user-row" style="border-right-color: ${escapeHTML(u.color) || '#fff'};">
                        <div style="flex-grow:1; margin-right:15px;">
                            <strong style="color:${escapeHTML(u.color) || 'var(--accent)'}; font-size:1.2rem;">${escapeHTML(u.nickname)}</strong>
                            <div style="font-size:0.8rem; color:var(--text-sub);">SYS.ID: ${escapeHTML(u.user_id)}</div>
                            ${u.banned ? '<span style="color:var(--danger); font-size:0.75rem; font-weight:bold;">[ RESTRICTED ]</span>' : '<span style="color:#00e676; font-size:0.75rem; font-weight:bold;">[ ACTIVE ]</span>'}
                        </div>
                        <div style="display:flex; flex-direction:column; gap:8px;">
                            <button class="btn-action-small" onclick="adminSendMsg('${u.user_id}')" style="color:var(--accent); border-color:var(--accent);">MESSAGE 📩</button>
                            <button class="btn-action-small" onclick="adminToggleBan('${u.user_id}', ${u.banned})" style="color:#ffb74d; border-color:#ffb74d;">${u.banned ? 'UNBLOCK 🟢' : 'BLOCK 🚫'}</button>
                            <button class="btn-action-small" onclick="adminDelUser('${u.user_id}')" style="color:var(--danger); border-color:var(--danger);">DELETE 💀</button>
                        </div>
                    </div>`).join('');
                } else uList.innerHTML = '<p style="text-align:center;">DB is empty.</p>';
                
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*'); 
                if(fErr) throw fErr;
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `
                    <div class="feedback-row">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:var(--accent); font-weight:bold; letter-spacing:1px;">TAG: [${escapeHTML(x.topic).toUpperCase()}]</span>
                            <button class="btn-action-small" onclick="adminDelFeedback('${escapeHTML(String(x.id))}')" style="color:var(--danger); border-color:var(--danger);">DESTROY</button>
                        </div>
                        <div style="padding:15px; background:#0b0c10; border-radius:4px; margin:10px 0; border:1px solid rgba(102,252,241,0.1); color:#fff; font-family:monospace;">${escapeHTML(x.text)}</div>
                        <div style="color:var(--text-sub); font-size:0.8rem;">SENDER: <span style="color:#fff;">${escapeHTML(x.user_email)}</span></div>
                    </div>`).join('');
                } else fList.innerHTML = '<p style="text-align:center;">NO INBOX MESSAGES.</p>';
            } catch(e) { uList.innerHTML = fList.innerHTML = `<p style="color:var(--danger); text-align:center;">SYS ERR: ${escapeHTML(e.message)}</p>`; }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }
        async function adminSendMsg(uid) { let msg = prompt("INJECT MESSAGE:"); if(msg) { await sp.from('profiles').update({ message: msg }).eq('user_id', uid); loadAdminData(); } }
        async function adminToggleBan(uid, wasBanned) { if(confirm(wasBanned ? "GRANT ACCESS?" : "RESTRICT USER ACCESS?")) { await sp.from('profiles').update({ banned: !wasBanned }).eq('user_id', uid); loadAdminData(); } }
        async function adminDelUser(uid) { if(confirm("PERMANENTLY DESTROY USER RECORD?")) { await sp.from('profiles').delete().eq('user_id', uid); loadAdminData(); } }
        
        async function adminDelFeedback(fid) {
            if(!confirm("האם למחוק נתונים אלו? הפעולה בלתי הפיכה.")) return;
            try {
                // הבטחה שהקריאה רצה ושומרת שגיאות כדי שנדע מה קרה באמת אם נכשל
                const { error } = await sp.from('feedbacks').delete().eq('id', fid);
                if(error) {
                    console.error("Delete Error:", error);
                    alert("פעולת המחיקה נחסמה! הודעת השרת: " + error.message + "\\n(וודא ש-RLS מאפשר מחיקה או שמזהה הטבלה 'id' תואם לחוקים).");
                    return;
                }
                loadAdminData(); // טוען מחדש מיד אחרי הצלחה
            } catch (err) { alert("ERROR FETCH: " + err.message); }
        }

        window.onload = checkUser;
    </script>
</body>
</html>
"""

# =======================================================
# תפריט ראשי
# =======================================================
MENU_CONTENT = """
<style>
    main { padding: 50px 20px 80px; text-align: center; }
    h1.main-title { font-size: clamp(3rem, 6vw, 5rem); margin-bottom: 5px; color: var(--accent); font-weight: 900; letter-spacing: 2px; text-shadow: 0 0 15px rgba(102, 252, 241, 0.4); text-transform: uppercase;}
    .subtitle { color: var(--text-sub); font-size: 1.2rem; margin-bottom: 50px; font-weight:bold; letter-spacing: 1px;}

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; max-width: 1400px; margin: 0 auto; }
    
    .card { background: var(--card-bg); border-radius: 8px; text-decoration: none; color: white; transition: all 0.3s; border: 1px solid rgba(102, 252, 241, 0.1); overflow: hidden; display: flex; flex-direction: column; text-align: right; position:relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5);}
    
    .card:hover { transform: translateY(-8px); border-color: var(--accent); box-shadow: 0 15px 40px rgba(0,0,0,0.7), 0 0 20px rgba(102, 252, 241, 0.3); z-index:2; }
    
    .card::before { content:''; position:absolute; top:0; left:-100%; width:50%; height:100%; background:linear-gradient(90deg, transparent, rgba(102,252,241,0.1), transparent); transform:skewX(-20deg); transition: 0.5s; }
    .card:hover::before { left: 150%; transition: 0.6s ease-in-out; }

    .card-cover { height: 160px; display: flex; align-items: center; justify-content: center; font-size: 65px; border-bottom: 1px solid rgba(102, 252, 241, 0.1); background: #0b0c10; transition:0.3s; }
    .card:hover .card-cover { background: #12181f; transform: scale(1.05); text-shadow: 0 0 20px rgba(255,255,255,0.8);}
    
    .card-body { padding: 25px; display: flex; flex-direction: column; flex-grow:1; background: var(--card-bg); z-index:1; }
    .card-body h2 { font-size: 1.6rem; font-weight: 900; margin-bottom: 10px; color: #fff; text-shadow: 0 0 5px rgba(255,255,255,0.2); text-transform:uppercase;}
    .card-desc { font-size: 1rem; color: var(--text-sub); margin-top: 15px; line-height: 1.5; flex-grow: 1; }
    .tag-badge { display: inline-block; align-self: flex-start; padding: 4px 10px; border: 1px solid var(--primary); background: rgba(197,1,226,0.1); border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: var(--primary); letter-spacing:0.5px;}

    .feedback-fab { position: fixed; bottom: 30px; left: 30px; width: 60px; height: 60px; background: transparent; border: 2px solid var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--accent); cursor: pointer; z-index: 990; transition: 0.3s; box-shadow: inset 0 0 10px rgba(102,252,241,0.2), 0 0 15px rgba(102,252,241,0.2); }
    .feedback-fab:hover { transform: scale(1.1) rotate(15deg); background: var(--accent); color:#000; box-shadow: 0 0 25px var(--accent); }
    
    .status-bar { text-align:center; padding:15px; margin-top:60px; color:rgba(255,255,255,0.3); font-family:monospace; border-top:1px dashed rgba(102, 252, 241, 0.2); }
</style>

<div class="scroll-content">
    <main>
        <h1 class="main-title">SYS.LINK ESTABLISHED</h1>
        <p class="subtitle">בחר שרת חווית מציאות רבודה להלן.</p>
        <div class="grid">
            <a href="/play/game1" class="card"><div class="card-cover">🏝️</div><div class="card-body"><h2>הישרדות</h2><span class="tag-badge">RESOURCE_MGMT</span><p class="card-desc">שרדו בסביבה עוינת, אספו חומרים ובנו את בסיס האם מאפס מוחלט.</p></div></a>
            <a href="/play/game2" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 15px #ffd700);">🌲</div><div class="card-body"><h2>Gold Forest</h2><span class="tag-badge">TEXT_ACTION</span><p class="card-desc">גלו סימולטור פנטזיה אדיר במעמקי יער מיתולוגי מלא באקשן בלתי צפוי.</p></div></a>
            <a href="/play/game3" class="card"><div class="card-cover" style="filter: hue-rotate(80deg);">🚀</div><div class="card-body"><h2>Genesis</h2><span class="tag-badge">SPACE_SIM</span><p class="card-desc">הטיסו חללית במרחבי הגלקסיה, סרקו כוכבים והרחיבו את אופקי החלל.</p></div></a>
            <a href="/play/game4" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 15px var(--danger));">💻</div><div class="card-body"><h2>קוד אדום</h2><span class="tag-badge">CYBER_HACK</span><p class="card-desc">הפכו להאקרים בשירות הצללים. פרצו מערכות, השמידו עדויות והשלימו את המשימה.</p></div></a>
            <a href="/play/game5" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 15px #aaa);">🔫</div><div class="card-body"><h2>IRON LEGION</h2><span class="tag-badge">SHOOTER_SURVIVAL</span><p class="card-desc">רובוטים, חצי-קיבורגים ונשקים עתידניים - תעמדו מולם ותישארו אחרונים.</p></div></a>
            <a href="/play/game6" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 10px #fff);">🌑</div><div class="card-body"><h2>מבוך הצללים</h2><span class="tag-badge">HORROR_ESCAPE</span><p class="card-desc">חווית אימה על חושית. ברחו מההיכלים החשוכים לפני ש"הדבר" יתפוס אתכם.</p></div></a>
            <a href="/play/game7" class="card"><div class="card-cover" style="filter: hue-rotate(240deg);">🪐</div><div class="card-body"><h2>PROXIMA</h2><span class="tag-badge">PLANETARY_EXPLORE</span><p class="card-desc">נחתתם על כוכב הלכת פרוקסימה. מהם סודותיו העתיקים?</p></div></a>
            <a href="/play/game8" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 15px #00e676);">🧬</div><div class="card-body"><h2>הטפיל</h2><span class="tag-badge">BIOLOGY_WARFARE</span><p class="card-desc">משחק ננו-טכנולוגיה בתוך גוף פונדקאי להשמדת ווירוס-טפיל מפלצתי.</p></div></a>
            <a href="/play/game9" class="card"><div class="card-cover" style="filter: hue-rotate(320deg);">🍀</div><div class="card-body"><h2>CLOVER</h2><span class="tag-badge">PURE_LUCK</span><p class="card-desc">סימולטור הגורלות. בחרו בהחלטות אמיצות - כל הקופה בידיים שלכם.</p></div></a>
            <a href="/play/game10" class="card"><div class="card-cover" style="filter: drop-shadow(0 0 15px var(--primary));">🏍️</div><div class="card-body"><h2>NEON RIDER</h2><span class="tag-badge">CYBER_RACING</span><p class="card-desc">רכבו על מנועי פלזמה בלב ליבה של עיר סייברפאנק תזזיתית.</p></div></a>
            <a href="/play/game11" class="card"><div class="card-cover" style="filter: hue-rotate(25deg);">📊</div><div class="card-body"><h2>Manager PRO</h2><span class="tag-badge">ESPORTS_MANAGER</span><p class="card-desc">ניהול פיננסי ואסטרטגי מלא להובלת צוות הספורט האלקטרוני הטוב בעולם.</p></div></a>
        </div>
        <div class="status-bar">> STATUS: ONLINE | SERVERS: ACTIVE | SYSTEM DB: CONNECTED // &copy; 2026 ARCADE STATION </div>
    </main>
    <button class="feedback-fab" onclick="openModal('feedback-modal')">!</button>
</div>
"""

PLAY_CONTENT = """
<iframe class="iframe-content" src="/{{target}}" title="Game"></iframe>
"""

# =======================================================
# חיבור מודולים מלא
# =======================================================
app = DispatcherMiddleware(main_app, {
    '/game1': game1, '/game2': game2, '/game3': game3, '/game4': game4, '/game5': game5,
    '/game6': game6, '/game7': game7, '/game8': game8, '/game9': game9, '/game9/x=v': game9,
    '/game10': game10, '/game11': game11, 
    '/googlebf5e9f4bd69d6b9a.html': verification_app(),
    '/php': php_app, '/html': html_app, '/app1': html_app, '/app2': php_app
})

if __name__ == "__main__":
    print("👾 INITIALIZING ARCADE STATION SYSTEM DIRECTORY AT: http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
