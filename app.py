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
      <!DOCTYPE html><html lang="he" dir="rtl">
      <head>
          <meta charset="UTF-8"><title>{text}</title>
          <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
          <style>body{{margin:0;font-family:'Heebo';background-color:#0a0a0c;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;}}</style>
      </head><body><div style="font-size: 50px;">🚧 {text} 🚧</div><p style="color:#b2bec3;">בפיתוח סבלנות!</p></body></html>
    '''
def create_dummy_app(text):
    d = Flask(__name__)
    @d.route('/')
    def index(): return a(text)
    return d

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


# =======================================================
# מבנה אחיד ומודולרי! תקלות הסרגל הגיעו לקיצן. שורה זהה תמיד!
# =======================================================

BASE_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<style>
    :root { --primary: #6c7ce7; --accent: #00cec9; --bg-dark: #070709; --card-bg: rgba(25, 25, 32, 0.6); --card-border: rgba(255, 255, 255, 0.08); --text-main: #f5f6fa; --text-sub: #a4b0be; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body, html { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Heebo', sans-serif; width: 100%; overflow-x: hidden; }
    
    .bg-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background-image: radial-gradient(circle at 15% 20%, rgba(108, 124, 231, 0.12) 0%, transparent 40%), radial-gradient(circle at 85% 70%, rgba(0, 206, 201, 0.12) 0%, transparent 40%), linear-gradient(to bottom, #070709 0%, #111116 100%); animation: pulseBg 10s infinite alternate; }
    @keyframes pulseBg { 0% { opacity: 0.8; } 100% { opacity: 1; } }

    nav { position: relative; width: 100%; height: 75px; z-index: 1000; background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(15px); border-bottom: 1px solid var(--accent); display: flex; justify-content: space-between; align-items: center; padding: 0 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3); transition: border-color 0.4s;}
    .nav-right-area { display: flex; align-items: center; gap: 30px; }
    .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; font-size: 1.5rem; font-weight: 900; background: linear-gradient(90deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .top-links { display: flex; gap: 20px; align-items: center; margin-right: 15px; }
    .top-links a { color: #fff; text-decoration: none; font-weight: 500; font-size: 1.1rem; transition: color 0.3s; cursor:pointer;}
    .top-links a:hover { color: var(--accent); }
    
    .dropdown { position: relative; display: inline-block; }
    .dropdown-content { display: none; position: absolute; background: rgba(15,15,20,0.98); min-width: 220px; box-shadow: 0 15px 35px rgba(0,0,0,0.8); border: 1px solid var(--accent); border-radius: 12px; top: 120%; right: -20px; padding: 10px 0; max-height: 450px; overflow-y: auto; text-align:right; z-index:999;}
    .dropdown:hover .dropdown-content { display: block; }
    .dropdown-content a { color: #fff; padding: 12px 20px; text-decoration: none; display: block; transition: background 0.2s;}
    .dropdown-content a:hover { background: rgba(255,255,255,0.08); color: var(--accent); }

    .nav-left-area { display: flex; gap: 15px; align-items: center; }
    .btn { border: none; padding: 9px 24px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family:'Heebo'; font-size:0.95rem; }
    .btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .btn-primary { background: var(--accent); color: #000; box-shadow: 0 0 10px rgba(0,0,0,0.2); }
    .btn-primary:not(:disabled):hover { filter: brightness(1.15); transform: translateY(-2px); }
    .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid var(--accent); }
    .btn-secondary:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
    .btn-danger { background: #ff4757; color: #fff; }
    .user-pill { background: rgba(108, 124, 231, 0.15); border: 1px solid var(--accent); color: #fff; padding: 8px 18px; border-radius: 30px; font-weight: 500; display: none; }

    .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 10000; opacity: 0; transition: opacity 0.3s; }
    .modal-overlay.active { display: flex; opacity: 1; }
    .modal-content { background: rgba(25, 25, 32, 0.95); border: 2px solid var(--accent); padding: 40px; border-radius: 24px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); position: relative; text-align: right; max-height: 90vh; overflow-y: auto; }
    .modal-close { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #a4b0be; font-size: 24px; cursor: pointer; transition: 0.3s; }
    
    .form-group { margin-bottom: 20px; text-align: right; }
    .form-group label { display: block; margin-bottom: 8px; color: var(--text-sub); }
    .input-box, select, textarea { width: 100%; padding: 14px 18px; border-radius: 12px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: white; font-size: 1rem; font-family:'Heebo'; }
    .input-box:focus { outline: none; border-color: var(--accent); }
    .input-box:disabled { opacity: 0.5; background: #111; cursor: not-allowed; }
    .hidden-group { display: none; }
    .auth-tabs { display: flex; gap: 10px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; }
    .auth-tab-btn { background: none; border: none; color: #a4b0be; font-size: 1.2rem; cursor: pointer; padding: 5px 10px; font-weight: bold; transition: 0.3s; }
    .auth-tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 2px; }

    #auth-error { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.4); padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.95rem; display: none; text-align: right;}
    .admin-modal { max-width: 1000px; }
    .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--card-border); padding-bottom: 15px;}
    .admin-tab { background: none; border: none; color: var(--text-sub); font-size: 1.1rem; cursor: pointer; padding: 5px 15px; border-radius: 8px; transition: 0.2s;}
    .admin-tab.active { background: rgba(255,255,255,0.1); color: var(--accent); font-weight: bold; }
    .admin-section { display: none; }
    .admin-section.active { display: block; }
    .user-list, .feedback-list { max-height: 450px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-left: 5px; }
    .user-row, .feedback-row { display: flex; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); align-items:center; justify-content: space-between;}
    .adm-action-btn { background: var(--bg-dark); color:#fff; border:1px solid #444; border-radius:6px; cursor:pointer; font-size:1.1rem; padding: 6px 12px; transition: 0.3s;}
    .adm-action-btn:hover { background: #333; transform: scale(1.05); }
    ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; } ::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 10px; }
</style>
<script>
    // כניסה פנימית שורת מניעה לשכפול
    if (window.top !== window.self) { window.top.location = window.self.location; }
</script>
"""

SHARED_NAVBAR = """
    <nav>
        <div class="nav-right-area">
            <a href="/" class="brand-logo" title="Arcade Station"><img src="/static/logo.png" alt="" onerror="this.style.display='none'">Arcade Station</a>
            <div class="top-links">
                <a href="/">חזרה ללובי (בית)</a>
                <div class="dropdown">
                    <a class="nav-item">תחנות עתיד ▾</a>
                    <div class="dropdown-content">
                        <a href="/play/game1">הישרדות 🏝️</a><a href="/play/game2">Gold Forest 🌲</a><a href="/play/game3">Genesis 🚀</a>
                        <a href="/play/game4">קוד אדום 💻</a><a href="/play/game5">IRON LEGION 🔫</a><a href="/play/game6">מבוך הצללים 🌑</a>
                        <a href="/play/game7">PROXIMA 🪐</a><a href="/play/game8">הטפיל 🧬</a><a href="/play/game9">CLOVER 🍀</a>
                        <a href="/play/game10">NEON RIDER 🏍️</a><a href="/play/game11">Manager PRO 📊</a>
                    </div>
                </div>
                <a onclick="openModal('about-modal')">הקמפוס המייסד</a>
            </div>
        </div>
        <div class="nav-left-area">
            <div id="user-status" class="user-pill"><span id="nickname-display"></span></div>
            <button id="admin-btn" class="btn btn-secondary" style="display: none;" onclick="openAdminModal()">⚙️ קברניט פיקוד</button>
            <button id="main-action-btn" class="btn btn-primary" onclick="openAuthModal('LOGIN')">חיבור מהיר למשתמש</button>
            <button id="logout-btn" class="btn btn-danger" style="display: none;" onclick="logout()">יציאה מסונכרנת</button>
        </div>
    </nav>
"""

SHARED_MODALS = """
    <!-- Modal: אבטחה וכניסה כולל איסוף מובנה וקסטום הצבע-->
    <div id="auth-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'auth-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('auth-modal')">✖</button>
            <h2 id="auth-edit-title" style="display:none; color: var(--accent); margin-bottom: 20px;">קפיצת רשת לפרופיל ולסטייל האהוב!</h2>
            <div id="auth-tabs-container" class="auth-tabs">
                <button id="auth-tab-login" class="auth-tab-btn active" onclick="setAuthUI('LOGIN')">הכנס עם קיים</button>
                <button id="auth-tab-signup" class="auth-tab-btn" onclick="setAuthUI('SIGNUP')">הפעל כינוי אישי משלך</button>
            </div>
            
            <div class="form-group" id="box-email">
                <label id="lbl-email">כתובת אימייל (תידרש למשפט אמיתיות!):</label>
                <input type="email" id="f-email" class="input-box" placeholder="gamer@hub.com">
            </div>
            <div class="form-group" id="box-user" style="display:none;">
                <label id="lbl-user">הבחירות כינוי רענן בסדנה לתלייה עתידית בדירוג הרישומים (חיוני!):</label>
                <input type="text" id="f-user" class="input-box" placeholder="MasterG123">
            </div>
            <div class="form-group" id="box-color" style="display:none;">
                <label id="lbl-color">בחירת מברשת העלילות הצבע הייחודי שמזהה אותך במימי הפלטפורמה:</label>
                <input type="color" id="f-color" class="input-box" value="#00cec9" style="padding: 2px; height: 40px; cursor: pointer;">
            </div>
            <div class="form-group" id="box-pass">
                <label id="lbl-pass">סיסמת קריפטו המעמיקה נדרשת על חוזק של לפחות 6 איתני קליד!</label>
                <input type="password" id="f-pass" class="input-box" placeholder="••••••••">
            </div>
            
            <div id="auth-error"></div>
            <button id="auth-exec-btn" class="btn btn-primary" style="width:100%; margin-top:10px; font-size:1.1rem; font-weight:900;" onclick="executeAuthAction()">הפל אותי לעולם!</button>
            
            <div id="delete-acc-container" style="display:none; margin-top: 15px;">
                <button class="btn" style="width:100%; background: #2f3542; color:#fff; border: 1px solid #ff4757; transition: 0.3s;" onmouseover="this.style.background='#ff4757'" onmouseout="this.style.background='#2f3542'" onclick="deleteSelf()">🗑️ גירוס חשבון מוחלט (פעולה זו אבסולוטית ויציבה ללא אל תחתיו!)</button>
            </div>

            <p id="forgot-pw-link" style="text-align:center; margin-top:18px; font-size:0.95rem; color:var(--text-sub); cursor:pointer;" onclick="setAuthUI('RECOVERY')"><u>נפלטה ממך סיסמתך לענני רוח אנוש במקרה ולא? תעבור למדור השחזורים החם</u></p>
            <p id="back-login-link" style="display:none; text-align:center; margin-top:18px; font-size:0.95rem; color:var(--accent); cursor:pointer;" onclick="setAuthUI('LOGIN')"><u>🔙 הקלק לחדל על טופס שיגרה כנס הסטוריות הקבועות האוטומטיות שלך הרי זה התחבר.</u></p>
        </div>
    </div>

    <!-- Modal: אודות -->
    <div id="about-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'about-modal')">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('about-modal')">✖</button>
            <h2 style="color: var(--accent);">מי אנחנו הלב שמאחורי היכל הקוביות והפקודות במערכות המסופות?!</h2>
            <div style="text-align: right; margin-top: 20px;">
                <p>ברוכים הבאים אליה - **Arcade Station Hub** המועצה המרכזת על ידיות מתגים אל הפאתוס והתענוג! <br><br>כאן שמים עניבות לדבר רגשי והפסקת שוקולד.</p>
                <h3 style="color: #a29bfe; margin-top: 20px;">היוזם המעורר יסוד עמוקות על היסוד. האבא המוליד תהליך הזה כבד מאוד</h3>
                <p>עוגן רעיונות המושג הברירה הזו רשות פסיכה מונהגת אצל קוד מלך אחד מוסרי ושמור באהבתי עדי ביופי והיא יוצרות בשמו: <strong>אביאל 👑</strong>.</p>
                <p>כתובת אימייל פרטי לאמירה של ציפויים גזירה : <span style="color:var(--accent); font-weight:bold;">x0583289789@gmail.com</span></p>
            </div>
        </div>
    </div>

    <!-- Modal: אדמין מתקדם -->
    <div id="admin-modal" class="modal-overlay" onclick="closeOnBgClick(event, 'admin-modal')">
        <div class="modal-content admin-modal">
            <button class="modal-close" onclick="closeModal('admin-modal')">✖</button>
            <h2 style="color: #ff4757; margin-bottom: 20px;">לשכת ההנהלה המסווגת (מאובטח 100%)</h2>
            <div class="admin-tabs">
                <button class="admin-tab active" id="tab-users-btn" onclick="switchAdminTab('users')">ניהול משתמשים במדדים אינפואינג 👥</button>
                <button class="admin-tab" id="tab-feedbacks-btn" onclick="switchAdminTab('feedbacks')">דואר תיקוני ומצב קליפות קבצים חוצבים נחלטים רץ פנוי אליך רנדריות</button>
            </div>
            <div id="section-users" class="admin-section active"><div class="user-list" id="admin-user-list"></div></div>
            <div id="section-feedbacks" class="admin-section"><div class="feedback-list" id="admin-feedback-list"></div></div>
        </div>
    </div>
"""

SHARED_JS = """
    <script>
        const spUrl = "https://ryoykooazoaordzmxdat.supabase.co";
        const spKey = "sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B";
        
        let sp = null;
        try { sp = supabase.createClient(spUrl, spKey); } catch(e) { console.error("טעות סופאבייס חשוכה קורא לי! תנער חיזוקים לתוכנות ההתשתלות עניין הזה בהם", e); }
        let cUser = null; 
        let globalAuthMode = 'LOGIN';

        document.addEventListener('DOMContentLoaded', () => {
            ['f-email', 'f-user', 'f-pass'].forEach(id => {
                const e = document.getElementById(id);
                if(e) e.addEventListener('keypress', function(ev) { if (ev.key === 'Enter') { ev.preventDefault(); executeAuthAction(); } });
            });
        });

        function openModal(id) { document.getElementById(id).classList.add('active'); showError(); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); showError(); }
        function closeOnBgClick(e, id) { if(e.target.id === id) closeModal(id); }
        function showError(msg = '') { const el = document.getElementById('auth-error'); if(msg){ el.style.display='block'; el.innerHTML='⚠️ ' + msg; } else el.style.display='none'; }

        async function checkUser() {
            if(!sp) return;
            const { data } = await sp.auth.getSession();
            cUser = data.session ? data.session.user : null;
            if (cUser) await verifyUserLogic(); // הפונקציה המדליקה פה טוענת את הצבע החביב ואבטחת ניסג חלץ שומר!
            updateUI();
        }

        async function verifyUserLogic() {
            // קריטית לממשל ובטיחות : הפורמט קריאת מסננן לאופני אימילים לחיווט של הגבלות ובשורת רשת עליונה של צבע העומדת לפוטנציה מתרצת עץ הקונפוננטה
            const { data: dbPro, error } = await sp.from('profiles').select('*').eq('user_id', cUser.id).maybeSingle();
            if (dbPro) {
                // אקשן באנים מחושף לוגית למטוס כשהמצופה עובר חקירות סטטוס מעמיקות מאובטח למחיצות המבצע דגמי אזרחים
                if (dbPro.status === 'banned') {
                    alert("🚨 חותם נר שמיים הוצא על צירים אלו בכתבות אש המורה החרים המלכות המנהל את סמלי המשתמש מהמעבר לאגודה פה - יצא ממסוף קצה העומדת פה מיד! חלס! נמסק! השב מכתבי ניצולי התרעות ומתח שבירת הרס קלף שדון טכנו...");
                    await sp.auth.signOut(); cUser = null; window.location.reload(); return;
                }
                // אינקוגניטו מסרוני קהל פרטית לממירים מתוך טבלה מרכז פרימייה 
                if (dbPro.admin_message) {
                    alert("👑 שליחת הלב הדרן - צילי המייסדים (המנהל) השליכו לך ניגונים ישירים בתבת הנועם מולך ממעשנות ההוצאה! הנה קפצונים הדפוסים לך אזהרת שיא או עין מרצון :\n\n💬 » " + dbPro.admin_message);
                    await sp.from('profiles').update({ admin_message: null }).eq('user_id', cUser.id);
                }
                // הרס עיניים עונש חזית כנועה לשפע של קבע! תוסרע לצבעי העליונות נגישה בעוצם פייק יופייה שהאדם לחץ
                if (dbPro.fav_color) { document.documentElement.style.setProperty('--accent', dbPro.fav_color); }
                if (!dbPro.email) { await sp.from('profiles').update({ email: cUser.email }).eq('user_id', cUser.id); } // סנכרון רסמי למאגדים סילובייק שלא נתקבל דרך החסימת מיילים במדרג השטחי
            }
        }

        function updateUI() {
            const isAdm = cUser && (cUser.email.toLowerCase() === 'x0583289789@gmail.com');
            document.getElementById('user-status').style.display = cUser ? 'block' : 'none';
            if(cUser) document.getElementById('nickname-display').innerText = '👤 ' + (cUser.user_metadata?.nickname || cUser.email.split('@')[0]);
            
            document.getElementById('main-action-btn').innerText = cUser ? '⚙ תוספות ועורקי הפרופיל שלך' : 'מפלח חיבור צק לאוטוסטרדת המשחקית (שחק)';
            document.getElementById('main-action-btn').onclick = () => openAuthModal(cUser ? 'EDIT' : 'LOGIN');
            
            document.getElementById('logout-btn').style.display = cUser ? 'inline-block' : 'none';
            document.getElementById('admin-btn').style.display = isAdm ? 'inline-block' : 'none';
        }

        async function logout() { await sp.auth.signOut(); document.documentElement.style.setProperty('--accent', '#00cec9'); cUser = null; updateUI(); }

        function openAuthModal(mode) {
            document.getElementById('f-user').value = ''; document.getElementById('f-email').value = ''; document.getElementById('f-pass').value = '';
            setAuthUI(mode); openModal('auth-modal');
        }

        function setAuthUI(mode) {
            globalAuthMode = mode; showError();
            const bU = document.getElementById('box-user'); const bE = document.getElementById('box-email'); const bP = document.getElementById('box-pass'); const bC = document.getElementById('box-color');
            const title = document.getElementById('auth-edit-title'); const tabs = document.getElementById('auth-tabs-container');
            const delD = document.getElementById('delete-acc-container');
            const mailInp = document.getElementById('f-email');

            title.style.display = 'none'; tabs.style.display = 'flex'; delD.style.display = 'none'; mailInp.disabled = false;

            if (mode === 'LOGIN') {
                document.getElementById('auth-tab-login').classList.add('active'); document.getElementById('auth-tab-signup').classList.remove('active');
                bE.style.display='block'; bU.style.display='none'; bC.style.display='none'; bP.style.display='block';
                document.getElementById('auth-exec-btn').innerText='תכניס לגלגלי האופוריה למאחורי החומות עכשיו';
                document.getElementById('forgot-pw-link').style.display='block'; document.getElementById('back-login-link').style.display='none';
            } else if (mode === 'SIGNUP') {
                document.getElementById('auth-tab-login').classList.remove('active'); document.getElementById('auth-tab-signup').classList.add('active');
                bE.style.display='block'; bU.style.display='block'; bC.style.display='block'; bP.style.display='block';
                document.getElementById('auth-exec-btn').innerText='תצור ישר לפרמידה והעצבים ללובי הניווט רץ משמע!';
                document.getElementById('forgot-pw-link').style.display='none'; document.getElementById('back-login-link').style.display='none';
            } else if (mode === 'EDIT') {
                title.style.display='block'; tabs.style.display='none';
                bE.style.display='block'; mailInp.value = cUser?.email || ''; mailInp.disabled = true;
                bU.style.display='block'; document.getElementById('f-user').value = cUser?.user_metadata?.nickname || ''; 
                bC.style.display='block'; document.getElementById('f-color').value = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
                bP.style.display='block';
                document.getElementById('auth-exec-btn').innerText='טען לאישר מפרטים העילונים של העדכון';
                delD.style.display='block'; document.getElementById('forgot-pw-link').style.display='none'; document.getElementById('back-login-link').style.display='none';
            } else if (mode === 'RECOVERY') {
                title.style.display='block'; tabs.style.display='none';
                bE.style.display='block'; bU.style.display='none'; bC.style.display='none'; bP.style.display='none';
                document.getElementById('auth-exec-btn').innerText='תנשום פנסי השלח אימיילי חזרה כגילי נקיות לקישורי';
                document.getElementById('forgot-pw-link').style.display='none'; document.getElementById('back-login-link').style.display='block';
            }
        }

        async function executeAuthAction() {
            if(!sp) return showError("מוסך הדלפות המסדי המחשבי נתמלט משלשת התמנגנץ גריד! סליחתי זה ניכשל בכתמים פופ-באגי תקלת!");
            const btn = document.getElementById('auth-exec-btn'); btn.disabled = true; const original = btn.innerText; btn.innerText="מבצע סורקים במוח הסאפל של כבל אינטראקטיבי... ⏳"; showError();
            try {
                if (globalAuthMode === 'LOGIN') {
                    const em = document.getElementById('f-email').value.trim();
                    if(!em || !em.includes('@')) throw new Error("אימייל לוקר אינפרנס נזנח במסילה שאינו מצוייד ב-@ בכלל המינמלי לוק נסך החוק שטח קהלים מתכתבי חימוש כד!");
                    const { error } = await sp.auth.signInWithPassword({ email: em.toLowerCase(), password: document.getElementById('f-pass').value });
                    if(error) showError("עצמים על טלאים לא זהות מוכרת.. שוב על הצירים לבטח שלא הזמת רשומים לא שוטח קו או שלא קורא במנואל מראש המשתמש כשהם סוחרי סיסמה רובים! - שקר."); else { closeModal('auth-modal'); checkUser(); }
                } else if (globalAuthMode === 'SIGNUP') {
                    const nick = document.getElementById('f-user').value.trim(); const mail = document.getElementById('f-email').value.trim(); const p = document.getElementById('f-pass').value; const col = document.getElementById('f-color').value;
                    if(p.length < 6 || !mail.includes('@') || !nick) throw new Error("אזהרה מהמשנה העורף סוף מחזור השמש! אין לפסח משברי רישומים מבלי עמדה מוכחת סיסמית גבוה 6 נחש ושדות מוכרז עבודה כבלי תת מסירות תקנית מיילי סגור משלש אחוז מוטב...");
                    
                    const { data: exist } = await sp.from('profiles').select('nickname').eq('nickname', nick).maybeSingle();
                    if (exist) throw new Error(`שיגרת נסיך גזל! השליט המותגים '${nick}' השוריינות כבר קיבע מחנה לפנייהו! בבקש יצרת פה גובה נופל למציאת דמי תעופה חילוף לוגי ספח גס.`);
                    
                    const { data, error } = await sp.auth.signUp({ email: mail.toLowerCase(), password: p, options:{ data:{ nickname: nick } } });
                    if(error) {
                        if (error.message.includes('already')) throw new Error("סלע החצצ גבר נגלים! הדואל האימיילי הנלקף מתקיף רשת קיים בתצורתו הפונדימית לפנינו! מהסכלת שאת נכנס כפול מהשכל נצלח לעמוד הקבצנות פלא גיבושה משורש ההזנת סופר שנתפס מיושבי לו פייכע.");
                        throw new Error(error.message);
                    }
                    if (data.user) {
                        await sp.from('profiles').upsert({ user_id: data.user.id, nickname: nick, email: mail.toLowerCase(), fav_color: col, status: 'active', admin_message: null });
                        checkUser(); alert("שמור עליי כקטיפת הנהור ברגע הרעידת חיבוקי אישורי כור העילאים מנחה! הצלחת אלקטרומגנטית עננת נחפר!"); closeModal('auth-modal');
                    }
                } else if (globalAuthMode === 'EDIT') {
                    const newN = document.getElementById('f-user').value.trim(); const newPass = document.getElementById('f-pass').value.trim(); const col = document.getElementById('f-color').value;
                    if(newN || col) { await sp.auth.updateUser({ data: { nickname: newN } }); await sp.from('profiles').update({ nickname: newN, fav_color: col }).eq('user_id', cUser.id); }
                    if(newPass && newPass.length >= 6) await sp.auth.updateUser({ password: newPass });
                    closeModal('auth-modal'); checkUser(); alert("טביעת הישות נמסרו לפטישי הקוסמית עורכת הגמישות ונקבע עדשת עותק מאובטחת במשרדים! 🪚");
                } else if (globalAuthMode === 'RECOVERY') {
                    const givenEmail = document.getElementById('f-email').value.trim();
                    if(!givenEmail || !givenEmail.includes('@')) throw new Error("אלפסי הקצבת קולבים טוס למלנכוכ רציפה כלי רשמים רמי טיים עונשים! מחוק מיצוג פקיעת נשיכת שיח אימילל לא תקנן איו.");
                    const { error } = await sp.auth.resetPasswordForEmail(givenEmail.toLowerCase());
                    if(error) throw new Error(error.message);
                    alert("נוחות המכפלה אישרה עגינה משוטטת! חפש רגע בזמן פלט בלוח צינור הדואר הנמשך או ברשת גן חוקי הצרכניים ספאם הוריקנו כלי פייר להורעת גיבוי שומר הקסמים החדשים 📥"); setAuthUI('LOGIN');
                }
            } catch(e) { showError(e.message); } finally { btn.disabled = false; btn.innerText = original; }
        }

        async function deleteSelf() {
            if (!confirm("רגע תמצית הדוק! סרבל נטיפת חותם הגדרות שטיפה עצמי פנימה והחוצה זה מבטל איסות נסחטות מלובי פעם! הפסק חותמו כאילו הוטש לממציאת החנק בוסרי מוכר? לא נאמר! כף הענן אטומה מתשוקה להשיג בחזרה אם גורס אבד פניך סופי לאן שיקולים לחלוט מחשבו??")) return;
            try { await sp.from('profiles').delete().eq('user_id', cUser.id); await sp.auth.signOut(); alert("גז מפורק ואור אירוזיה לחצה דקותיים עד לפס! להתראת לא ניווץ השנאת הניתור העותל סל סורקי משקף מחשבי חזר על הקובצת..."); closeModal('auth-modal'); document.documentElement.style.setProperty('--accent', '#00cec9'); cUser = null; updateUI(); } catch (err) { alert(err.message); }
        }

        /* מערך מטורף ואכזרי לניהול האש בטרמינל הסיווג האדום הרחב: חסימות אישוריות מחסומים פלוס מיוחסויות ומאמצים מסננים רצון */
        async function loadAdminData() {
            if(!sp) return;
            const uList = document.getElementById('admin-user-list'); const fList = document.getElementById('admin-feedback-list');
            uList.innerHTML = '<p style="text-align:center;">לעיטת מאמץ איבה שלוקטת דילר אימפרסי גבישי עשון ממסד הרשות... 🔄</p>';
            fList.innerHTML = '<p style="text-align:center;">מרחיף פנימו אלגוריתמי עול סיוטים נחתמים מענבר החוקרים סורק מיילים צנועים ומכתב עילאים! 🔄</p>';
            
            try {
                // שלב ראשון : שליפת מאגרי המועצמה המשוטטים 
                const { data: pList, error: pErr } = await sp.from('profiles').select('*');
                if(pErr) throw new Error("לגיש הרשאות פרופיל נדחה רגע איום: " + pErr.message);

                if (pList && pList.length > 0) {
                    uList.innerHTML = pList.map(u => {
                        const bgBlock = (u.status === 'banned') ? 'background:rgba(255,0,0,0.2); border:1px solid red;' : `border-right: 6px solid ${u.fav_color || 'white'};`;
                        return `<div class="user-row" style="${bgBlock}">
                                  <div style="text-align:right;">
                                      <h3 style="color:${u.fav_color || '#fff'}; margin:0;">${u.nickname} ${(u.status === 'banned')?'<span style="color:red;font-size:0.8rem;">[נחסם מילולי אכיפות בידי משעול ההפצצה!]</span>':''}</h3>
                                      <small style="color:#aaa;">Email: ${u.email} | ID: ${u.user_id}</small>
                                  </div>
                                  <div style="display:flex;gap:8px;">
                                      <button class="adm-action-btn" title="שלח סוללת חשיפת צער איתות הלב למשתמש ישיר כרגע בסנאי (Flash Message!)" onclick="admMessage('${u.user_id}', '${u.nickname}')">💬 פרסם</button>
                                      <button class="adm-action-btn" title="חתן והשק פצצת העינויים של אומני השעיית כמות החשבון והגירה חוץ לפטל חוק חוקית מניעתו חזית סרק הפסד! סמל מעיין" onclick="admToggleBlock('${u.user_id}', '${u.status}')">${(u.status === 'banned')?'✔️ החזר ציד למסדר נשיאת הדף וחלל':'🚫 חסימת קשירות אכזרי למלון מוכנע! עמוד קרקעות טיל מוקה'}</button>
                                      <button class="adm-action-btn" title="מחקה מתשוקות משפלת הקשת נשימת גופיו שסכנות ללא דרך החתחת קשר קיל סופה מסיר מהמימד קובעת טרק כלו גוב!" onclick="admDelete('${u.user_id}')" style="background:#441111; color:red;">🗑️ אבסולוט הדברה משטיח תא כבודו ממעבץ סודותי טבוק חץ</button>
                                  </div>
                                </div>`;
                    }).join('');
                } else uList.innerHTML = '<p style="color:#a4b0be; text-align:center;">מצוק הגיסא הרצפה רוקד הדים מסדי נדודת הרשת אינם אינדיקציה במרשת גז אוכלסי... נקה כליל שוקטים.</p>';

                // שלב שני : הענקת תיבות משאלי רעיון רפרנס מסחור הודעת התגובה העם הפלוס מסריקת שער הדיוק RLS מעבדתית ענקות : 
                const { data: fListDb, error: fErr } = await sp.from('feedbacks').select('*');
                if (fErr) { fList.innerHTML = `<div style="background:#ff4757; color:#fff; padding:15px; border-radius:10px;"><h2>היי! סורק ה-RLS תפס כפילות הרשאות גב אצבע סכנותי מזהיר!!!🚨</h2> <p>מדיניות ההרשאות בטבלת משוב (Feedbacks) חוסמת מלערוך שליפה צינית רזרבית!</p><p>כנס אל המסד - לך להגדרות Table ולפנלים ה-Policies שים כהוכחת "Select Policy" שיהיה משונן True או תמורה לשקף לעיין משוטרת מסיכת גילי עדים שיורשו לצפות את גופות הודעה השרתת השחקניים שלך, כיאה! אחרת ההשחזה המחשב סבור ללא מסלול פיל פנקסי העד! הטענות מקסיקנית זריקו: ${fErr.message}</p></div>`; return; }
                
                if (fListDb && fListDb.length > 0) {
                    fList.innerHTML = fListDb.map(x => `<div class="feedback-row" style="display:flex; flex-direction:column; gap:8px;">
                                            <div style="display:flex; justify-content:space-between; width:100%;"><strong style="color:var(--accent);">תיבה ממדף קולקציית נושא:[${x.topic}] בתיחום המשחקים צייר שייך לקו סניפי הגילד > ${x.game}</strong><span style="font-size:0.8rem; background:rgba(255,255,255,0.1); padding:3px 8px; border-radius:5px;">מגבר השלט מזהה שופר יוצרו האישי : ${x.user_email}</span></div>
                                            <div style="background:rgba(0,0,0,0.6); padding:10px; border-radius:8px; border-right:3px solid var(--accent); color:#ddd;">"${x.text}"</div>
                                          </div>`).join('');
                } else fList.innerHTML = '<p style="color:#a4b0be; text-align:center;">טרמינל טרייל ציטוט השתקפויות הדמקות צריחות מחיות מעל דלפי פיינל משוב עדיין פגר תדרי פתיח חם וללא סעדים כתובים שוקו סף הקולעים צפרוח פה מסורו העדים תם ונלום</p>';
                
            } catch(e) { uList.innerHTML = e.message; fList.innerHTML = e.message; }
        }

        async function openAdminModal() { openModal('admin-modal'); switchAdminTab('users'); await loadAdminData(); }
        function switchAdminTab(t) { document.getElementById('tab-users-btn').classList.toggle('active', t === 'users'); document.getElementById('tab-feedbacks-btn').classList.toggle('active', t === 'feedbacks'); document.getElementById('section-users').classList.toggle('active', t === 'users'); document.getElementById('section-feedbacks').classList.toggle('active', t === 'feedbacks'); }

        async function admMessage(uid, nick) { const msg = prompt(`קפסל לבו וטעינו טקסט שישא פרמיה דואר פופאפ תלום מעניבה שיפץ סופר חסידה מרשת כותר שיחלוף וילמד את הפיכה ישירות של [${nick}] ברגע העצמית הניסיון המסכנת נטעי המסעות שלו עכשו פרימה : `); if(!msg) return; await sp.from('profiles').update({ admin_message: msg }).eq('user_id', uid); alert('שלושת המימדים הפלג התפוצצו פסימיס שלחה חישה המילטו תלכיד מהודרה התרכבות! הודעה מכה להשכים סביב הפיצות 🚀'); }
        async function admToggleBlock(uid, cStatus) { const ns = cStatus === 'banned' ? 'active' : 'banned'; await sp.from('profiles').update({ status: ns }).eq('user_id', uid); loadAdminData(); }
        async function admDelete(uid) { if(!confirm('כפילות המשימון הזו רטינה מתמלאת אבסולוט שימושו ממיגר דמי פליט המסלול פוקס אלקטרונים זה יושתק מטבלת הנראות לגמרייי, אכן זה הצעידות משמיו של רכיבה קווצה ומוחקים כנוע מחויבת כאבן דאונים נותח?? חילצ קטלה !')) return; await sp.from('profiles').delete().eq('user_id', uid); loadAdminData(); }

        window.onload = checkUser;
    </script>
"""

# HTML ממוחזר (מעוצב בתבנית מפוצלת שקופה כדי למנוע הבדלי עיצוב טוטאלי)
MENU_HTML = f"""
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <title>Arcade Station | Hub</title>
    {BASE_CSS}
    <style>
        main {{ padding: 120px 20px 60px; text-align: center; }}
        h1.main-title {{ font-size: clamp(2.5rem, 8vw, 4.5rem); margin-bottom: 10px; background: linear-gradient(135deg, #fff, #a29bfe, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }}
        .subtitle {{ color: var(--text-sub); font-size: 1.3rem; margin-bottom: 60px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; max-width: 1300px; margin: 0 auto; }}
        .card {{ background: var(--card-bg); border-radius: 20px; text-decoration: none; color: white; transition: all 0.4s; border: 1px solid var(--card-border); overflow: hidden; display: flex; flex-direction: column; text-align: right; cursor:pointer; }}
        .card:hover {{ transform: translateY(-12px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(0,0,0, 0.4); border-color: var(--accent); filter: drop-shadow(0 0 8px var(--accent)); }}
        .card-cover {{ height: 130px; display: flex; align-items: center; justify-content: center; font-size: 55px; border-bottom: 1px solid var(--card-border); background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,0,0,0.3)); text-shadow: 0 0 20px rgba(255,255,255,0.2); }}
        .card-body {{ padding: 25px; display: flex; flex-direction: column; }}
        .card-body h2 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 5px; color: #fff; }}
        .card-desc {{ font-size: 0.95rem; color: #a4b0be; margin-top: 10px; line-height: 1.4; flex-grow: 1; }}
        .tag-badge {{ display: inline-block; align-self: flex-start; padding: 5px 12px; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--accent); border-radius: 20px; font-size: 0.8rem; font-weight: 500; color: var(--accent); }}
        footer {{ margin-top: 100px; padding: 20px; text-align: center; color: #4b4b5c; font-size: 0.95rem; border-top: 1px solid var(--card-border); }}
    </style>
</head>
<body>
    <div class="bg-layer"></div>
    {SHARED_NAVBAR}
    <main>
        <h1 class="main-title">בחר את ההרפתקה שלך</h1>
        <p class="subtitle">מסע המשחקים הבא שלך מתחיל ממש כאן. תהנה! 🎮</p>
        <div class="grid">
            <a href="/play/game1" class="card"><div class="card-cover">🏝️</div><div class="card-body"><h2>הישרדות</h2><span class="tag-badge">ניהול משאבים</span><p class="card-desc">שרדו בסביבה עוינת, אספו משאבים ובנו את המחנה שלכם מאפס.</p></div></a>
            <a href="/play/game2" class="card"><div class="card-cover">🌲</div><div class="card-body"><h2>Gold Forest</h2><span class="tag-badge">אקשן טקסטואלי</span><p class="card-desc">יער הזהב ממתין לך! גלו פנטזיה אדירה במעמקי יער מיתולוגי מלא באקשן.</p></div></a>
            <a href="/play/game3" class="card"><div class="card-cover">🚀</div><div class="card-body"><h2>Genesis</h2><span class="tag-badge">מסע בחלל</span><p class="card-desc">הטיסו חללית במרחבי הגלקסיה, גלו כוכבים ומצאו חיים חדשים.</p></div></a>
            <a href="/play/game4" class="card"><div class="card-cover">💻</div><div class="card-body"><h2>קוד אדום</h2><span class="tag-badge">סייבר</span><p class="card-desc">הפכו להאקרים, פרצו מערכות מאובטחות והשלימו את המשימה.</p></div></a>
            <a href="/play/game5" class="card"><div class="card-cover">🔫</div><div class="card-body"><h2>IRON LEGION</h2><span class="tag-badge">יריות ושרידה</span><p class="card-desc">גלי אויבים, נשקים עתידניים - האם תישארו אחרונים לעמוד?</p></div></a>
            <a href="/play/game6" class="card"><div class="card-cover">🌑</div><div class="card-body"><h2>מבוך הצללים</h2><span class="tag-badge">אימה</span><p class="card-desc">מצאו את דרככם החוצה ממבוך חשוך ומצמרר לפני שיהיה מאוחר מדי.</p></div></a>
            <a href="/play/game7" class="card"><div class="card-cover">🪐</div><div class="card-body"><h2>PROXIMA</h2><span class="tag-badge">מחקר עולמות</span><p class="card-desc">חקרו את סודות כוכב הלכת פרוקסימה והתמודדו עם תופעות מסתוריות.</p></div></a>
            <a href="/play/game8" class="card"><div class="card-cover">🧬</div><div class="card-body"><h2>הטפיל</h2><span class="tag-badge">ביולוגיה</span><p class="card-desc">מסע הישרדות בתוך גוף אנושי כדי להילחם בנגיף קטלני.</p></div></a>
            <a href="/play/game9" class="card"><div class="card-cover">🍀</div><div class="card-body"><h2>CLOVER</h2><span class="tag-badge">מזל טהור</span><p class="card-desc">הימור וסיכוי. קבלו את ההחלטות הנכונות וקחו את כל הקופה.</p></div></a>
            <a href="/play/game10" class="card"><div class="card-cover">🏍️</div><div class="card-body"><h2>NEON RIDER</h2><span class="tag-badge">מרוץ</span><p class="card-desc">רכבו על אופנועי ניאון בעיר סייברפאנק תזזיתית והגיעו ראשונים.</p></div></a>
            <a href="/play/game11" class="card"><div class="card-cover">📊</div><div class="card-body"><h2>Manager PRO</h2><span class="tag-badge">ניהול קבוצות</span><p class="card-desc">הקימו, אמנו ונהלו את קבוצת החלומות שלכם עד האליפות.</p></div></a>
        </div>
    </main>
    <footer>&copy; 2026 Arcade Station | ענף בניית מסופי משחק ארכימדיום על ידי אביאל האחד העוגן בחוק הגרביטציה מתוצר עצמית 🌐</footer>
    {SHARED_MODALS}
    {SHARED_JS}
</body>
</html>
"""

PLAY_HTML = f"""
<!DOCTYPE html>
<html lang="he" dir="rtl" style="height: 100%;">
<head>
    <title>Arcade Play Station - {{{{target}}}}</title>
    {BASE_CSS}
    <style> iframe {{ flex-grow: 1; width: 100%; border: none; display: block; }} body{{ height:100vh; overflow:hidden; }} </style>
</head>
<body>
    <div class="bg-layer"></div>
    {SHARED_NAVBAR}
    <iframe src="/{{{{target}}}}" title="Game Canvas Window Streamler"></iframe>
    {SHARED_MODALS}
    {SHARED_JS}
</body>
</html>
"""

# שידוך המשחקים למשגר המפות של דיספאטש
app = DispatcherMiddleware(main_app, {
    '/game1': game1, '/game2': game2, '/game3': game3, '/game4': game4, '/game5': game5,
    '/game6': game6, '/game7': game7, '/game8': game8, '/game9': game9, '/game9/x=v':game9,
    '/game10': game10, '/game11': game11, '/googlebf5e9f4bd69d6b9a.html':x(),
    '/php': php_app, '/html': html_app, '/app1': html_app, '/app2': php_app
})

if __name__ == "__main__":
    print("🎮 תשתית סרבריוס מערכות נוטעת לחיים בכתובת רצה טוות על שרשרת התלת אקזקט > http://localhost:5000")
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
