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
            z-index: 1;
        }

        /* פס זוהר עליון בכרטיסייה */
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }

        /* אפקט הברקה במעבר עכבר */
        .card::after {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
            opacity: 0;
            transform: scale(0.5);
            transition: all 0.6s ease;
            z-index: -1;
        }

        .card:hover {
            transform: translateY(-12px);
            border-color: rgba(0, 206, 201, 0.3);
            box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(0, 206, 201, 0.15);
            background: rgba(35, 35, 45, 0.8);
        }

        .card:hover::before { opacity: 1; }
        .card:hover::after { opacity: 1; transform: scale(1); }

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
            letter-spacing: 0.5px;
        }
        
        .tag {
            font-size: 0.85rem; 
            color: #81ecec; 
            background: rgba(129, 236, 236, 0.1);
            padding: 6px 16px; 
            border-radius: 30px; 
            font-weight: 500;
            border: 1px solid rgba(129, 236, 236, 0.2);
            backdrop-filter: blur(5px);
        }

        footer { 
            margin-top: 100px; 
            color: #4b4b5c; 
            font-size: 0.9rem; 
            font-weight: 500;
            padding-bottom: 30px;
        }

        footer span {
            color: var(--primary);
        }

        /* Responsive */
        @media (max-width: 600px) {
            .grid { grid-template-columns: 1fr; }
            body { padding: 40px 15px; }
            .header-container { margin-bottom: 40px; }
        }
    </style>
</head>
<body>
    <div class="header-container">
        <h1>Arcade Station</h1>
        <p class="subtitle">בחר את ההרפתקה הבאה שלך 🎮</p>
    </div>

    <div class="grid">
        <a href="/game1/" class="card"><span class="emoji-icon">🏝️</span><h2>הישרדות</h2><div class="tag">ניהול משאבים</div></a>
        <a href="/game2/" class="card"><span class="emoji-icon">⚔️</span><h2>RPG Legend</h2><div class="tag">אקשן טקסטואלי</div></a>
        <a href="/game3/" class="card"><span class="emoji-icon">🚀</span><h2>Genesis</h2><div class="tag">מסע בחלל</div></a>
        <a href="/game4/" class="card"><span class="emoji-icon">💻</span><h2>קוד אדום</h2><div class="tag">פרוץ, גנוב, היעלם</div></a>
        <a href="/game5/" class="card"><span class="emoji-icon">🔫</span><h2>IRON LEGION</h2><div class="tag">מלחמות</div></a>
        <a href="/game6/" class="card"><span class="emoji-icon">🗝️</span><h2>מבוך הצללים</h2><div class="tag">הרפתקה אפלה</div></a>
        <a href="/game7/" class="card"><span class="emoji-icon">🔥</span><h2>PROXIMA</h2><div class="tag">אסטרטגיית חלל</div></a>
        <a href="/game8/" class="card"><span class="emoji-icon">🦠</span><h2>הטפיל</h2><div class="tag">החלפת גופות</div></a>
        <a href="/game9/" class="card"><span class="emoji-icon">♣️</span><h2>CLOVER</h2><div class="tag">Action Platformer</div></a>
        <a href="/game10/" class="card"><span class="emoji-icon">⚡</span><h2>NEON RIDER</h2><div class="tag">מרוץ התחמקות רטרו</div></a>
        <a href="/game11/" class="card"><span class="emoji-icon">⚽</span><h2>Manager PRO</h2><div class="tag">ניהול כדורגל טקטי</div></a>
    </div>

    <footer>&copy; Aviel Aluf | <span>x0583289789@gmail.com</span></footer>
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
