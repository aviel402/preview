import requests
import re
import io
import zipfile
import os
import mimetypes
from flask import Flask, render_template_string, request, Response, send_file, url_for
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup  

app = Flask(__name__)

# --- קונפיגורציה ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'en-US,en;q=0.5'
}

def clean_filename(url):
    path = urlparse(url).path
    filename = os.path.basename(unquote(path))
    if not filename: return "file"
    return re.sub(r'[^a-zA-Z0-9._-]', '', filename)

def fix_url(url):
    url = unquote(url)
    if url and not url.startswith('http'):
        url = 'https://' + url
    return url

def generate_fixed_zip(url):
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        response = session.get(url, timeout=15)
        response.encoding = response.apparent_encoding
        
        if response.status_code != 200: return None

        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = url
        zip_buffer = io.BytesIO()
        downloaded_files = {} 
        file_counter = 0

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            tags_to_process = [
                ('img', ['src', 'data-src'], 'assets_img'),
                ('script', ['src'], 'assets_js'),
                ('link', ['href'], 'assets_css')
            ]

            for tag_name, attrs, folder in tags_to_process:
                for tag in soup.find_all(tag_name):
                    
                    if tag.has_attr('srcset'): del tag['srcset'] 
                    if tag.has_attr('crossorigin'): del tag['crossorigin']
                    if tag.has_attr('integrity'): del tag['integrity']

                    target_attr = None
                    original_val = None
                    for attr in attrs:
                        if tag.has_attr(attr) and tag[attr]:
                            target_attr = attr
                            original_val = tag[attr]
                            break
                    
                    if not target_attr: continue
                    if original_val.startswith('data:') or original_val.startswith('#'): continue

                    abs_url = urljoin(base_url, original_val)
                    
                    if abs_url in downloaded_files:
                        tag[target_attr] = downloaded_files[abs_url] 
                        continue

                    try:
                        file_res = session.get(abs_url, timeout=5)
                        if file_res.status_code == 200:
                            file_counter += 1
                            ext = os.path.splitext(clean_filename(abs_url))[1]
                            if not ext:
                                content_type = file_res.headers.get('Content-Type', '')
                                ext = mimetypes.guess_extension(content_type.split(';')[0]) or '.bin'

                            local_filename = f"{folder}/res_{file_counter}{ext}"
                            zf.writestr(local_filename, file_res.content)
                            tag[target_attr] = local_filename
                            
                            if target_attr == 'data-src':
                                tag['src'] = local_filename
                                del tag['data-src']

                            downloaded_files[abs_url] = local_filename
                    except Exception as e:
                        pass

            extra_css = soup.new_tag("style")
            extra_css.string = "body { margin: 0; padding: 0; overflow-x: hidden; } img { max-width: 100%; }"
            if soup.head: soup.head.append(extra_css)

            zf.writestr('index.html', soup.prettify())
        
        zip_buffer.seek(0)
        return zip_buffer

    except Exception as e:
        print(f"Error generating ZIP: {e}")
        return None

# --- HTML תבנית (בעיצוב מחודש ועם תיקוני ניתוב עבור DispatcherMiddleware) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Web Ripper PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Heebo', sans-serif;
            background: radial-gradient(circle at 15% 50%, #151928, #0a0a0f 85%);
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow: hidden;
        }

        /* בועות רקע זוהרות */
        .glow-circle {
            position: absolute; width: 400px; height: 400px;
            background: #8b5cf6; border-radius: 50%;
            filter: blur(120px); z-index: -1; opacity: 0.25; animation: drift 15s infinite alternate;
        }
        .glow-circle.second {
            background: #0ea5e9; right: -50px; bottom: -50px;
            animation-duration: 20s;
        }

        @keyframes drift {
            from { transform: translateY(0px) translateX(0px); }
            to { transform: translateY(-50px) translateX(50px); }
        }

        .glass-panel {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 40px;
            width: 100%; max-width: 550px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            position: relative;
        }

        .title-badge {
            background: rgba(14, 165, 233, 0.1); color: #38bdf8;
            padding: 6px 14px; border-radius: 20px;
            font-size: 0.8rem; font-weight: 700;
            display: inline-block; margin-bottom: 15px; border: 1px solid rgba(56, 189, 248, 0.2);
        }

        h1 {
            font-size: 2.2rem; font-weight: 900; margin-bottom: 5px;
            background: linear-gradient(135deg, #f8fafc, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }

        .subtitle { color: #94a3b8; font-weight: 300; font-size: 0.95rem; margin-bottom: 30px; }

        .input-group {
            position: relative; margin-bottom: 30px;
        }

        .form-control {
            width: 100%;
            background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.1);
            color: white; padding: 16px 20px; font-size: 1.1rem; text-align: left; /* יישור הקישור משמאל לימין למראה מקצועי */
            border-radius: 14px; direction: ltr; outline: none; transition: 0.3s;
        }
        
        .form-control::placeholder { color: #475569; text-align: left; }
        
        .form-control:focus {
            border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
            background: rgba(15, 23, 42, 0.8);
        }

        .action-btn {
            display: flex; align-items: center; justify-content: center; gap: 10px;
            padding: 16px; font-size: 1.05rem; font-weight: 700; width: 100%;
            border: none; border-radius: 14px; margin-bottom: 12px; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden;
        }
        
        .action-btn:disabled { filter: grayscale(1); cursor: wait; transform: scale(0.98); }
        .action-btn:not(:disabled):hover { transform: translateY(-3px); }

        .btn-copy {
            background: linear-gradient(135deg, #4c1d95, #6d28d9); color: #fff;
            box-shadow: 0 10px 20px rgba(109, 40, 217, 0.3);
        }
        .btn-html {
            background: linear-gradient(135deg, #0284c7, #0369a1); color: #fff;
            box-shadow: 0 10px 20px rgba(2, 132, 199, 0.3);
        }
        .btn-zip {
            background: linear-gradient(135deg, #be185d, #e11d48); color: #fff;
            box-shadow: 0 10px 20px rgba(225, 29, 72, 0.3);
        }

        .btn-icon { font-size: 1.3rem; }

        #msg-box { font-weight: 700; margin-top: 15px; font-size: 0.95rem; min-height: 20px; color: #f43f5e; transition: 0.3s; }
        .msg-success { color: #10b981 !important; }
    </style>
</head>
<body>

    <div class="glow-circle"></div>
    <div class="glow-circle second"></div>

    <div class="glass-panel">
        <div class="title-badge">גרסה 4.0 Pro</div>
        <h1>מחלץ המערכות</h1>
        <p class="subtitle">הזן כתובת אתר לייצוא נתונים מלא בקליק אחד בלבד</p>
        
        <div class="input-group">
            <input type="url" id="urlInput" class="form-control" placeholder="https://example.com" required>
        </div>

        <button id="btnCopy" onclick="handleDirectAction('copy')" class="action-btn btn-copy">
            <span class="btn-icon">📋</span> העתק רק קוד מקור (HTML)
        </button>
        
        <button id="btnHtml" onclick="handleDirectAction('html')" class="action-btn btn-html">
            <span class="btn-icon">📄</span> הורד את הקוד כקובץ מיושר
        </button>
        
        <button id="btnZip" onclick="handleDirectAction('zip')" class="action-btn btn-zip">
            <span class="btn-icon">📦</span> צור ושמור חבילה מלאה (+נכסים)
        </button>

        <div id="msg-box"></div>
    </div>

    <script>
        // שימוש בפונקציה של פלאסק שיודעת בדיוק מאיזה ראוט פתחנו את השרת
        // זה מבטיח שאפילו אם האפליקציה בראוט /php דרך Dispatcher, הנתיבים יכתבו אוטומטית כ- /php/api/get_html
        const routes = {
            copy: "{{ url_for('api_get_html') }}",
            html: "{{ url_for('download_html') }}",
            zip:  "{{ url_for('download_zip_route') }}"
        };

        function showMessage(text, isSuccess = false) {
            const box = document.getElementById('msg-box');
            box.innerText = text;
            box.className = isSuccess ? 'msg-success' : '';
            if(!isSuccess && text !== '') {
                setTimeout(() => { if(box.innerText === text) box.innerText = ""; }, 3000);
            }
        }

        function getUrl() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) {
                showMessage("❌ שגיאה: יש להדביק קישור לפני ביצוע פעולה.");
                return null;
            }
            if(!url.startsWith("http://") && !url.startsWith("https://")) {
                showMessage("❌ הקישור צריך להתחיל ב http:// או https://");
                return null;
            }
            return url;
        }

        async function handleDirectAction(type) {
            const url = getUrl();
            if(!url) return;

            showMessage(""); 
            const routeTarget = routes[type] + '?target=' + encodeURIComponent(url);

            if(type === 'copy') {
                const btn = document.getElementById('btnCopy');
                const origHtml = btn.innerHTML;
                
                btn.innerHTML = 'מייבא נתונים מסרבר מרחוק ⏳...';
                btn.disabled = true;

                try {
                    const res = await fetch(routeTarget);
                    if(!res.ok) throw new Error();
                    const text = await res.text();
                    
                    await navigator.clipboard.writeText(text);
                    btn.innerHTML = '<span class="btn-icon">✅</span> ההעתקה הושלמה בהצלחה';
                    showMessage("✔ הקוד נשמר בלוח הגזירים!", true);
                } catch(e) {
                    btn.innerHTML = '<span class="btn-icon">❌</span> קריסה בקריאה';
                    showMessage("האתר לא זמין, לא ניתן לייבא.");
                }

                setTimeout(() => { btn.innerHTML = origHtml; btn.disabled = false; }, 2500);

            } 
            else {
                const btn = type === 'html' ? document.getElementById('btnHtml') : document.getElementById('btnZip');
                const origHtml = btn.innerHTML;
                
                btn.innerHTML = 'מעבד ומתכנן להורדה... ⏳';
                btn.disabled = true;
                
                // הניתוב משתמש בנתיב המותאם מה-DispatcherMiddleware + הקישור כפרמטר
                window.location.href = routeTarget;

                setTimeout(() => { btn.innerHTML = origHtml; btn.disabled = false; }, 3500);
            }
        }
    </script>
</body>
</html>
"""

# --- ניתובים מאחורי הקלעים ---
@app.route('/')
def index():
    return render_template_string(HTML_UI)

@app.route('/api/get_html')
def api_get_html():
    url = fix_url(request.args.get('target', ''))
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        res = session.get(url, timeout=10)
        res.encoding = res.apparent_encoding
        return res.text
    except Exception as e:
        return "Error loading page.", 400

@app.route('/download/html')
def download_html():
    url = fix_url(request.args.get('target', ''))
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        res = session.get(url, timeout=15)
        res.encoding = res.apparent_encoding
        return Response(res.text, mimetype="text/html", headers={"Content-Disposition": "attachment; filename=ripped_source.html"})
    except:
        return "Error fetching file.", 400

@app.route('/download/zip')
def download_zip_route():
    url = fix_url(request.args.get('target', ''))
    zip_buffer = generate_fixed_zip(url)
    if zip_buffer:
        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='ripped_full_website.zip')
    else:
        return "Error building zip. Check server blocks.", 400

# אפשר לבדוק גם לבד על קובץ ספציפי אבל הלאנצ'ר מריץ אותו
if __name__ == '__main__':
    app.run(debug=True, port=5000)
