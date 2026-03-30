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
              margin: 0;
              font-family: 'Heebo', sans-serif;
              background-color: #0a0a0c;
              background-image: 
                radial-gradient(circle at 50% 0%, rgba(108, 124, 231, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 50% 100%, rgba(0, 206, 201, 0.15) 0%, transparent 50%);
              color: #fff;
              height: 100vh;
              display: flex;
              align-items: center;
              justify-content: center;
              overflow: hidden;
            }}
            .container {{
              text-align: center;
              padding: 50px 40px;
              background: rgba(30, 30, 36, 0.6);
              backdrop-filter: blur(16px);
              -webkit-backdrop-filter: blur(16px);
              border-radius: 24px;
              border: 1px solid rgba(255, 255, 255, 0.1);
              box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 20px rgba(0, 206, 201, 0.1);
              max-width: 500px;
              width: 90%;
              transform: translateY(0);
              animation: float 6s ease-in-out infinite;
            }}
            .icon-wrapper {{
              font-size: 80px;
              margin-bottom: 20px;
              filter: drop-shadow(0 0 20px rgba(0, 206, 201, 0.4));
            }}
            h1 {{ 
              font-size: clamp(2rem, 5vw, 3rem); 
              margin: 0; 
              font-weight: 900;
              background: linear-gradient(90deg, #a29bfe, #00cec9);
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
            }}
            .subtitle {{ 
              margin-top: 16px; 
              font-size: 1.2rem; 
              color: #b2bec3;
              font-weight: 300;
            }}
            .progress-bar {{
              width: 100%;
              height: 4px;
              background: rgba(255,255,255,0.1);
              border-radius: 4px;
              margin-top: 30px;
              overflow: hidden;
              position: relative;
            }}
            .progress-bar::after {{
              content: '';
              position: absolute;
              top: 0; left: 0; height: 100%; width: 40%;
              background: linear-gradient(90deg, #6c7ce7, #00cec9);
              border-radius: 4px;
              animation: loading 2s infinite ease-in-out alternate;
            }}
            .back-btn {{
              display: inline-block;
              margin-top: 40px;
              padding: 12px 30px;
              background: rgba(255, 255, 255, 0.05);
              border: 1px solid rgba(255, 255, 255, 0.2);
              color: #fff;
              text-decoration: none;
              border-radius: 30px;
              font-weight: 700;
              transition: all 0.3s ease;
            }}
            .back-btn:hover {{
              background: rgba(255, 255, 255, 0.1);
              border-color: #00cec9;
              box-shadow: 0 0 15px rgba(0, 206, 201, 0.3);
              transform: scale(1.05);
            }}
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
# נסה לייבא - אם לא קיים, השתמש בדמה
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

# --- 3. הלאוצ'ר הראשי ---
main_app = Flask(__name__)

@main_app.route('/logo.png')
def favicon():
    return "LOGO_DATA" # placeholder - פשטתי למניעת קריסה אם אין קובץ

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
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(108, 124, 231, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(0, 206, 201, 0.08) 0%, transparent 50%),
                linear-gradient(to bottom, #070709 0%, #111116 100%);
            color: var(--text-main);
            font-family: 'Heebo', sans-serif;
            text-align: center;
            padding: 60px 20px;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .header-container {
            margin-bottom: 70px;
            position: relative;
        }

        h1 {
            font-size: clamp(2.5rem, 8vw, 4.5rem);
            margin: 0;
            background: linear-gradient(135deg, #fff, #a29bfe, #00cec9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            filter: drop-shadow(0 0 20px rgba(108, 124, 231, 0.3));
        }

        .subtitle { 
            color: var(--text-sub); 
            font-size: 1.3rem; 
            font-weight: 300; 
            margin-top: 10px;
            letter-spacing: 1px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            max-width: 1300px;
            margin: 0 auto;
            padding: 0 10px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 35px 25px;
            text-decoration: none;
            color: white;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex; 
            flex-direction: column; 
            align-items: center;
            border: 1px solid var(--card-border);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            position: relative; 
            overflow: hidden;
        }

        .card:hover {
            transform: translateY(-12px);
            border-color: rgba(0, 206, 201, 0.3);
            box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(0, 206, 201, 0.15);
            background: rgba(35, 35, 45, 0.8);
        }

        .emoji-icon { 
            font-size: 65px; 
            margin-bottom: 20px; 
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.4));
            transition: transform 0.4s ease;
        }

        .card:hover .emoji-icon {
            transform: scale(1.15) rotate(5deg);
        }
        
        .card h2 { 
            margin: 5px 0 15px 0; 
            font-size: 1.6rem; 
            font-weight: 700; 
        }
        
        .tag {
            font-size: 0.85rem; 
            color: #81ecec; 
            background: rgba(129, 236, 236, 0.1);
            padding: 6px 16px; 
            border-radius: 30px; 
            font-weight: 500;
            border: 1px solid rgba(129, 236, 236, 0.2);
        }

        footer { 
            margin-top: 100px; 
            color: #4b4b5c; 
            font-size: 0.9rem; 
            font-weight: 500;
            padding-bottom: 30px;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <h1>Arcade Station</h1>
        <p class="subtitle">בחר את ההרפתקה הבאה שלך 🎮</p>
    </div>

    <!-- LOGIN BAR - למעלה משמאל -->
    <div style="position: absolute; top: 20px; left: 20px; display: flex; align-items: center; gap: 12px; z-index: 100; flex-wrap: wrap;">
        <div id="user-status" style="background: rgba(0,0,0,0.4); padding: 8px 16px; border-radius: 30px; font-size: 0.95rem; display: none;">
            <span id="nickname-display"></span>
        </div>
        
        <button id="main-action-btn"
                onclick="showLoginModal()"
                style="background: var(--accent); color: #000; border: none; padding: 10px 20px; border-radius: 30px; font-weight: 700; cursor: pointer;">
            התחבר / הרשם
        </button>
        
        <button onclick="logout()" id="logout-btn" style="display: none; background: #ff4757; color: white; border: none; padding: 10px 20px; border-radius: 30px; font-weight: 700; cursor: pointer;">
            התנתק
        </button>
        
        <!-- כפתור אדמין -->
        <button onclick="showAdminPanel()" id="admin-btn" 
                style="display: none; background: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 30px; font-weight: 700; cursor: pointer;">
            ⚙️ פאנל אדמין
        </button>
    </div>

    <div class="grid">
        <a href="/game1/" class="card"><span class="emoji-icon">🏝️</span><h2>הישרדות</h2><div class="tag">ניהול משאבים</div></a>
        <a href="/game2/" class="card"><span class="emoji-icon">⚔️</span><h2>RPG Legend</h2><div class="tag">אקשן טקסטואלי</div></a>
        <a href="/game3/" class="card"><span class="emoji-icon">🚀</span><h2>Genesis</h2><div class="tag">מסע בחלל</div></a>
        <a href="/game4/" class="card"><span class="emoji-icon">💻</span><h2>קוד אדום</h2><div class="tag">פרוץ, גנוב, היעלם</div></a>
        <a href="/game5/" class="card"><span class="emoji-icon">🔫</span><h2>IRON LEGION</h2><div class="tag">יריות + שרידה</div></a>
        <a href="/game6/" class="card"><span class="emoji-icon">🌑</span><h2>מבוך הצללים</h2><div class="tag">אימה + חיפוש</div></a>
        <a href="/game7/" class="card"><span class="emoji-icon">🪐</span><h2>PROXIMA</h2><div class="tag">כוכב לכת חדש</div></a>
        <a href="/game8/" class="card"><span class="emoji-icon">🧬</span><h2>הטפיל</h2><div class="tag">הישרדות בגוף</div></a>
        <a href="/game9/" class="card"><span class="emoji-icon">🍀</span><h2>CLOVER</h2><div class="tag">מזל + קלובר</div></a>
        <a href="/game10/" class="card"><span class="emoji-icon">🏍️</span><h2>NEON RIDER</h2><div class="tag">מרוץ ניאון</div></a>
        <a href="/game11/" class="card"><span class="emoji-icon">📊</span><h2>Manager PRO</h2><div class="tag">ניהול קבוצה</div></a>
    </div>

    <footer>&copy; Aviel Aluf | <span>x0583289789@gmail.com</span></footer>

    <!-- ====================== SUPABASE SCRIPT ====================== -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
        const SUPABASE_URL = 'https://ryoykooazoaordzmxdat.supabase.co';
        const SUPABASE_ANON_KEY = 'sb_publishable_bQDZZLDP-n51ur0jD5XNIg_iGDdsq5B';

        const { createClient } = supabase;
        const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        let currentUser = null;

        // ====================== פונקציות בסיסיות ======================
        async function checkUser() {
            try {
                const { data: { user } } = await supabaseClient.auth.getUser();
                currentUser = user;
                updateUI();
                console.log('✅ Supabase User:', currentUser ? 'מחובר' : 'לא מחובר');
            } catch (e) {
                console.error('שגיאה בבדיקת משתמש:', e);
            }
        }

        function updateUI() {
            const status = document.getElementById('user-status');
            const mainBtn = document.getElementById('main-action-btn');
            const logoutBtn = document.getElementById('logout-btn');
            const adminBtn = document.getElementById('admin-btn');

            if (currentUser) {
                const isAdmin = currentUser.email === 'x0583289789@gmail.com';

                status.style.display = 'flex';
                document.getElementById('nickname-display').innerHTML = 
                    `👤 <strong>${currentUser.user_metadata?.nickname || currentUser.email?.split('@')[0] || 'משתמש'}</strong>`;
                
                mainBtn.textContent = 'ערוך את פרטיך';
                mainBtn.style.background = '#6c7ce7';
                mainBtn.onclick = showEditProfileModal;

                logoutBtn.style.display = 'block';
                
                if (isAdmin) {
                    adminBtn.style.display = 'block';
                } else {
                    adminBtn.style.display = 'none';
                }
            } else {
                status.style.display = 'none';
                mainBtn.textContent = 'התחבר / הרשם';
                mainBtn.style.background = 'var(--accent)';
                mainBtn.onclick = showLoginModal;
                logoutBtn.style.display = 'none';
                adminBtn.style.display = 'none';
            }
        }

        async function logout() {
            try {
                await supabaseClient.auth.signOut();
                currentUser = null;
                updateUI();
                alert('התנתקת בהצלחה ✅');
            } catch (e) {
                console.error(e);
                alert('שגיאה בהתנתקות');
            }
        }

        // ====================== מודל התחברות ======================
        function showLoginModal() {
            const modalHTML = `
            <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.92);display:flex;align-items:center;justify-content:center;z-index:99999;">
                <div style="background:#111; padding:40px; border-radius:24px; width:90%; max-width:420px; text-align:center; color:white; box-shadow:0 0 40px rgba(0,206,201,0.3);">
                    <h2 style="margin-bottom:25px;">התחברות / הרשמה</h2>
                    <input id="email" type="email" placeholder="אימייל" style="width:100%; padding:14px; margin:12px 0; border-radius:12px; font-size:1rem; border:1px solid #444;"><br>
                    <input id="password" type="password" placeholder="סיסמה (מינימום 6 תווים)" style="width:100%; padding:14px; margin:12px 0; border-radius:12px; font-size:1rem; border:1px solid #444;"><br>
                    <button onclick="login()" style="width:100%; padding:16px; background:#00cec9; color:#000; border:none; border-radius:12px; margin:12px 0; font-weight:700; font-size:1.05rem;">התחבר</button>
                    <button onclick="signup()" style="width:100%; padding:16px; background:#6c7ce7; color:white; border:none; border-radius:12px; font-weight:700; font-size:1.05rem;">הרשם חשבון חדש</button>
                    <button onclick="this.parentElement.parentElement.remove()" style="margin-top:20px; color:#888; background:none; border:none; font-size:0.95rem;">סגור</button>
                </div>
            </div>`;
            const div = document.createElement('div');
            div.innerHTML = modalHTML;
            document.body.appendChild(div);
        }

        // ====================== מודל עריכת פרטים ======================
        function showEditProfileModal() {
            const currentNickname = currentUser?.user_metadata?.nickname || currentUser?.email?.split('@')[0] || '';
            const modalHTML = `
            <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.92);display:flex;align-items:center;justify-content:center;z-index:99999;">
                <div style="background:#111; padding:40px; border-radius:24px; width:90%; max-width:420px; text-align:center; color:white; box-shadow:0 0 40px rgba(0,206,201,0.3);">
                    <h2 style="margin-bottom:25px;">ערוך את הפרטים שלך</h2>
                    <p style="margin-bottom:15px; color:#aaa;">שם תצוגה (יופיע בלידרבורד)</p>
                    <input id="new-nickname" type="text" value="${currentNickname}" placeholder="שם תצוגה" 
                           style="width:100%; padding:14px; margin:12px 0; border-radius:12px; font-size:1rem; border:1px solid #444;"><br>
                    <button onclick="updateNickname()" style="width:100%; padding:16px; background:#00cec9; color:#000; border:none; border-radius:12px; margin:15px 0; font-weight:700;">שמור שינויים</button>
                    <button onclick="this.parentElement.parentElement.remove()" style="margin-top:10px; color:#888; background:none; border:none; font-size:0.95rem;">סגור</button>
                </div>
            </div>`;
            const div = document.createElement('div');
            div.innerHTML = modalHTML;
            document.body.appendChild(div);
        }

        async function updateNickname() {
            const newNickname = document.getElementById('new-nickname').value.trim();
            if (!newNickname) return alert('נא להזין שם תצוגה');
            
            try {
                await supabaseClient.auth.updateUser({ data: { nickname: newNickname } });
                await supabaseClient.from('profiles').upsert({
                    user_id: currentUser.id,
                    nickname: newNickname
                });
                alert('✅ שם התצוגה עודכן!');
                document.querySelector('div[style*="position:fixed"]').remove();
                await checkUser();
            } catch (e) {
                alert('שגיאה: ' + e.message);
            }
        }

        // ====================== פונקציות Login / Signup ======================
        async function login() {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            if (!email || !password) return alert('נא למלא אימייל וסיסמה');
            
            try {
                const { error } = await supabaseClient.auth.signInWithPassword({ email, password });
                if (error) alert('שגיאה: ' + error.message);
                else {
                    await checkUser();
                    document.querySelector('div[style*="position:fixed"]').remove();
                }
            } catch (e) {
                alert('שגיאה טכנית');
            }
        }

        async function signup() {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            if (!email || !password || password.length < 6) return alert('סיסמה חייבת להיות לפחות 6 תווים');
            
            try {
                const { data, error } = await supabaseClient.auth.signUp({ email, password });
                if (error) alert('שגיאה: ' + error.message);
                else {
                    const nickname = prompt('בחר שם תצוגה:', email.split('@')[0]);
                    if (nickname && data.user) {
                        await supabaseClient.from('profiles').insert({ user_id: data.user.id, nickname });
                    }
                    alert('✅ הרשמה הושלמה! בדוק את האימייל');
                    document.querySelector('div[style*="position:fixed"]').remove();
                }
            } catch (e) {
                alert('שגיאה בהרשמה');
            }
        }

        // ====================== פאנל אדמין ======================
        async function showAdminPanel() {
            if (currentUser?.email !== 'x0583289789@gmail.com') {
                return alert('אין לך הרשאות אדמין!');
            }

            let html = `<h2 style="color:#e74c3c; margin-bottom:20px;">⚙️ פאנל אדמין</h2>`;

            const games = ['survival','rpg_legend','genesis','red_code','iron_legion','shadow_maze','proxima','parasite','clover','neon_rider','manager_pro'];

            for (let game of games) {
                const { data } = await supabaseClient
                    .from('high_scores')
                    .select(`*, profiles(nickname)`)
                    .eq('game_slug', game)
                    .order('metric_value', { ascending: false })
                    .limit(50);

                html += `<h3 style="margin:20px 0 10px;">${game.toUpperCase()} - ${data ? data.length : 0} רשומות</h3>`;
                html += `<table style="width:100%; border-collapse:collapse; margin-bottom:40px; font-size:0.95rem;">`;
                html += `<tr style="background:#333;"><th>#</th><th>שם</th><th>ציון</th><th>תאריך</th><th>פעולה</th></tr>`;

                (data || []).forEach((row, i) => {
                    html += `<tr style="border-bottom:1px solid #444;">
                        <td>${i+1}</td>
                        <td>${row.profiles?.nickname || '---'}</td>
                        <td><strong>${row.metric_value}</strong></td>
                        <td>${new Date(row.submitted_at).toLocaleDateString('he-IL')}</td>
                        <td><button onclick="deleteScore('${row.id}')" style="background:#e74c3c;color:white;border:none;padding:5px 12px;border-radius:6px;cursor:pointer;">מחק</button></td>
                    </tr>`;
                });
                html += `</table>`;
            }

            const modal = document.createElement('div');
            modal.style = "position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.96);display:flex;align-items:center;justify-content:center;z-index:999999;color:white;overflow:auto;";
            modal.innerHTML = `<div style="background:#1a1a2e;padding:30px;border-radius:20px;max-width:1200px;width:95%;max-height:95vh;overflow:auto;">${html}<br><button onclick="this.parentElement.parentElement.remove()" style="margin-top:30px;padding:14px 40px;background:#ff4757;color:white;border:none;border-radius:30px;">סגור פאנל</button></div>`;
            document.body.appendChild(modal);
        }

        async function deleteScore(scoreId) {
            if (!confirm('למחוק את הציון הזה לצמיתות?')) return;
            const { error } = await supabaseClient.from('high_scores').delete().eq('id', scoreId);
            if (error) alert(error.message);
            else {
                alert('✅ נמחק בהצלחה');
                showAdminPanel();
            }
        }

        // ====================== שאר הפונקציות (שמירות + לידרבורד) ======================
        async function saveGame(gameSlug, saveData) {
            if (!currentUser) {
                sessionStorage.setItem(`anon_save_${gameSlug}`, JSON.stringify(saveData));
                return;
            }
            await supabaseClient.from('game_saves').upsert({
                user_id: currentUser.id,
                game_slug: gameSlug,
                save_data: saveData
            });
        }

        async function loadGame(gameSlug) {
            if (!currentUser) {
                const data = sessionStorage.getItem(`anon_save_${gameSlug}`);
                return data ? JSON.parse(data) : null;
            }
            const { data } = await supabaseClient
                .from('game_saves')
                .select('save_data')
                .eq('user_id', currentUser.id)
                .eq('game_slug', gameSlug)
                .single();
            return data ? data.save_data : null;
        }

        async function submitScore(gameSlug, metricValue, details) {
            if (!currentUser) return alert('רק משתמשים מחוברים יכולים להיכנס ללידרבורד!');
            await supabaseClient.from('high_scores').insert({
                user_id: currentUser.id,
                game_slug: gameSlug,
                metric_value: metricValue,
                details: details
            });
            alert('✅ הציון נשלח ללידרבורד!');
        }

        async function getLeaderboard(gameSlug, limit = 10) {
            const { data } = await supabaseClient
                .from('high_scores')
                .select(`*, profiles(nickname)`)
                .eq('game_slug', gameSlug)
                .order('metric_value', { ascending: false })
                .limit(limit);
            return data || [];
        }

        async function showLeaderboard(gameSlug) {
            const leaderboard = await getLeaderboard(gameSlug, 10);
            // כאן תוכל להוסיף בהמשך מודל לידרבורד רגיל למשתמשים רגילים
            console.log('Leaderboard for', gameSlug, leaderboard);
            alert('לידרבורד זמין בפאנל אדמין (לעת עתה)');
        }

        // טעינה ראשונית
        window.addEventListener('load', () => {
            console.log('✅ Arcade Station Hub Loaded');
            checkUser();
        });
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
            return [{"name":"minigame.aeriagames.jp","id":4217},{"name":"localhost:8080","id":4217},{"name":"minigame-stg.aeriagames.jp","id":4217}];
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
