import requests
import re
import random
from flask import Flask, render_template_string, request
from urllib.parse import urljoin

app = Flask(__name__)

# --- הגדרות עיצוב ---
THEMES = [
    {"name": "Cyberpunk", "bg": "#0f0524", "primary": "#ff00ff", "secondary": "#00ffff", "text": "#ffffff", "code_theme": "prism-tomorrow"},
    {"name": "Deep Ocean", "bg": "#011627", "primary": "#2081C3", "secondary": "#63D2FF", "text": "#d6e8ee", "code_theme": "prism-okaidia"},
    {"name": "Forest Dark", "bg": "#1a1f16", "primary": "#5e8c31", "secondary": "#a2d240", "text": "#e8f0e2", "code_theme": "prism-twilight"},
    {"name": "Midnight Gold", "bg": "#121212", "primary": "#D4AF37", "secondary": "#FFD700", "text": "#f4f4f4", "code_theme": "prism-funky"},
    {"name": "Mars Rover", "bg": "#2b0f0e", "primary": "#e27d60", "secondary": "#e8a87c", "text": "#ffffff", "code_theme": "prism-coy"},
    {"name": "Soft Purple", "bg": "#2d1b33", "primary": "#c39bd3", "secondary": "#f06292", "text": "#f5f5f5", "code_theme": "prism-dark"},
    {"name": "Matrix", "bg": "#000000", "primary": "#00ff41", "secondary": "#008f11", "text": "#00ff41", "code_theme": "prism-tomorrow"},
    {"name": "Nordic Ice", "bg": "#2e3440", "primary": "#88c0d0", "secondary": "#81a1c1", "text": "#eceff4", "code_theme": "prism-nord"},
    {"name": "Vaporwave Sunset", "bg": "#241744", "primary": "#ff71ce", "secondary": "#01cdfe", "text": "#fff2f1", "code_theme": "prism-tomorrow"},
    {"name": "Dracula Night", "bg": "#282a36", "primary": "#bd93f9", "secondary": "#ff79c6", "text": "#f8f8f2", "code_theme": "prism-tomorrow"},
    {"name": "Emerald City", "bg": "#021c1e", "primary": "#00676b", "secondary": "#2fb98a", "text": "#d8f3dc", "code_theme": "prism-okaidia"},
    {"name": "Monokai Classic", "bg": "#2d2a2e", "primary": "#ffd866", "secondary": "#ff6188", "text": "#fcfcfa", "code_theme": "prism-okaidia"},
    {"name": "Arctic Frost", "bg": "#f0f4f8", "primary": "#1b6ca8", "secondary": "#4ba3c3", "text": "#243b53", "code_theme": "prism-coy"},
    {"name": "Coffee House", "bg": "#3c2f2f", "primary": "#be9b7b", "secondary": "#854442", "text": "#fff4e6", "code_theme": "prism-twilight"},
    {"name": "Red Alert", "bg": "#0a0000", "primary": "#ff4d4d", "secondary": "#b30000", "text": "#ffe6e6", "code_theme": "prism-funky"},
    {"name": "Royal Velvet", "bg": "#1a1c2c", "primary": "#f4d03f", "secondary": "#d4af37", "text": "#e0e0e0", "code_theme": "prism-tomorrow"}
]

# --- פונקציות עזר ---

def fix_url(url):
    """מוודא שיש פרוטוקול תקין לכתובת"""
    if not url: return ""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def extract_data(html, base_url):
    """חילוץ תמונות וכותרות מה-HTML"""
    # חילוץ תמונות
    img_urls = re.findall(r'<img [^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    # המרת נתיבים יחסיים למוחלטים
    full_img_urls = list(set([urljoin(base_url, u) for u in img_urls if u]))
    
    # חילוץ כותרת
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "ללא כותרת"

    # חילוץ תיאור
    desc_match = re.search(r'<meta name=["\']description["\'] content=["\'](.*?)["\']', html, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else "ללא תיאור"

    return {
        "images": full_img_urls[:12], # רק 12 ראשונות
        "total_images": len(full_img_urls),
        "title": title,
        "description": description
    }

# --- תבנית ה-HTML ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web-Scanner Pro | {{ theme.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/{{ theme.code_theme }}.min.css" rel="stylesheet" />
    
    <style>
        :root { 
            --bg: {{ theme.bg }}; 
            --primary: {{ theme.primary }}; 
            --secondary: {{ theme.secondary }}; 
            --text: {{ theme.text }}; 
        }
        body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; transition: 0.3s; min-height: 100vh; }
        
        .glass-card { 
            background: rgba(255, 255, 255, 0.05); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 16px; 
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }
        
        .btn-gradient { background: linear-gradient(135deg, var(--primary), var(--secondary)); border: none; color: #fff; font-weight: bold; }
        .btn-gradient:hover { filter: brightness(1.1); color: #fff; }
        
        .search-box { 
            background: rgba(0,0,0,0.4); 
            border: 1px solid var(--primary); 
            color: white; 
            border-radius: 10px; 
            padding: 12px;
        }
        .search-box:focus { background: rgba(0,0,0,0.6); color: white; border-color: var(--secondary); box-shadow: 0 0 10px var(--secondary); }
        .search-box::placeholder { color: rgba(255,255,255,0.5); }

        .info-card { border-right: 3px solid var(--primary); padding-right: 15px; background: rgba(0,0,0,0.2); border-radius: 8px; padding: 10px; }
        
        .img-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
        .img-preview { width: 100%; height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid var(--secondary); transition: transform 0.2s; cursor: pointer; }
        .img-preview:hover { transform: scale(1.1); z-index: 10; }

        pre { max-height: 600px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); }
        
        body.code-only-mode { overflow: hidden; }
        body.code-only-mode .main-ui, body.code-only-mode .theme-badge { display: none !important; }
        body.code-only-mode .code-section { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            z-index: 9999; background: var(--bg); padding: 0; margin: 0; 
        }
        body.code-only-mode .code-container { width: 100%; height: 100%; margin: 0; max-width: none; }
        body.code-only-mode pre { 
            height: calc(100vh - 50px) !important; 
            max-height: none !important; 
            border-radius: 0; 
            margin: 0;
        }
        
        .theme-badge { 
            position: fixed; bottom: 20px; left: 20px; 
            background: var(--primary); color: #000; 
            padding: 5px 15px; border-radius: 20px; 
            font-weight: bold; font-size: 12px; box-shadow: 0 0 15px var(--primary);
        }
    </style>
</head>
<body class="container py-4">
    
    <div class="main-ui text-center mb-4">
        <h1 class="display-5" style="color: var(--primary); font-weight: 800; text-shadow: 0 0 15px var(--primary);">Web-Scanner Pro</h1>
        <p class="opacity-75">סורק אתרים מתקדם | מצב: <strong>{{ theme.name }}</strong></p>
        
        <div class="d-flex justify-content-center gap-2 mt-3">
            <!-- שים לב: הכפתור מוביל ל /app1 -->
            <a href="/html" class="btn btn-sm btn-outline-light">החלף עיצוב רנדומלי 🎲</a>
        </div>
    </div>

    <div class="main-ui row justify-content-center">
        <div class="col-lg-8">
            <div class="glass-card p-4 mb-4">
                <form action="/app1" method="GET" class="row g-2">
                    <div class="col-md-9">
                        <input type="text" name="url" class="form-control search-box" placeholder="הכנס כתובת אתר (למשל ynet.co.il)" value="{{ url }}" required>
                        <input type="hidden" name="theme_idx" value="{{ theme_index }}">
                    </div>
                    <div class="col-md-3">
                        <button type="submit" class="btn btn-gradient w-100 h-100">סרוק כעת 🚀</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    {% if error %}
    <div class="alert alert-danger text-center glass-card border-danger">
        <h4>שגיאה בסריקה ⚠️</h4>
        <p>{{ error }}</p>
    </div>
    {% endif %}

    {% if html_content %}
    <div class="main-ui row justify-content-center mb-4">
        <div class="col-lg-10">
            <div class="glass-card p-4">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <div class="info-card h-100">
                            <h5 style="color: var(--secondary)">📄 פרטי דף</h5>
                            <strong>כותרת:</strong> {{ metadata.title }}<br>
                            <small class="d-block mt-2"><strong>תיאור:</strong> {{ metadata.description[:100] }}...</small>
                            <div class="mt-3 badge bg-light text-dark">סה"כ תווים: {{ html_content|length }}</div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="info-card h-100">
                            <h5 style="color: var(--secondary)">🖼️ תמונות שנמצאו ({{ metadata.total_images }})</h5>
                            {% if metadata.images %}
                                <div class="img-grid mt-2">
                                    {% for img in metadata.images %}
                                        <a href="{{ img }}" target="_blank"><img src="{{ img }}" class="img-preview" onerror="this.style.display='none'"></a>
                                    {% endfor %}
                                </div>
                            {% else %}
                                <p>לא נמצאו תמונות נגישות.</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="code-section row justify-content-center">
        <div class="col-lg-12 code-container">
            <div class="d-flex justify-content-between align-items-center mb-2 px-3">
                <h5 class="m-0 text-light">קוד מקור (Source Code)</h5>
                <div>
                    <button class="btn btn-sm btn-outline-info" onclick="copyCode()">העתק הכל 📋</button>
                    <button class="btn btn-sm btn-warning" onclick="toggleCodeOnly()">מצב מסך מלא 🖥️</button>
                    <button class="btn btn-sm btn-danger exit-btn d-none" onclick="toggleCodeOnly()">✖ יציאה</button>
                </div>
            </div>
            <pre><code id="main-code" class="language-html">{{ html_content | e }}</code></pre>
        </div>
    </div>
    {% endif %}

    <div class="theme-badge">Design: {{ theme.name }}</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>
        function toggleCodeOnly() {
            document.body.classList.toggle('code-only-mode');
            document.querySelector('.exit-btn').classList.toggle('d-none');
        }

        function copyCode() {
            const code = document.getElementById('main-code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                const btn = document.querySelector('.btn-outline-info');
                const originalText = btn.textContent;
                btn.textContent = 'הועתק! ✅';
                setTimeout(() => btn.textContent = originalText, 2000);
            });
        }
    </script>
</body>
</html>
"""

# שינוי הנתיב (Route) להיות /app1 כנדרש
@app.route('/', methods=['GET'])
def proxy():
    target_url = request.args.get('url', '').strip()
    theme_idx_arg = request.args.get('theme_idx')
    
    # ניהול עיצוב: בחירה אקראית או שמירה על הקיים
    if theme_idx_arg and theme_idx_arg.isdigit():
        idx = int(theme_idx_arg) % len(THEMES)
        selected_theme = THEMES[idx]
        current_theme_index = idx
    else:
        selected_theme = random.choice(THEMES)
        current_theme_index = THEMES.index(selected_theme)

    html_content = None
    error = None
    metadata = {}

    if target_url:
        target_url = fix_url(target_url) 
        try:
            # הוספת User-Agent כדי שהאתרים לא יחסמו את הסורק
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(target_url, headers=headers, timeout=10)
            
            # קידוד קריטי לעברית
            response.encoding = response.apparent_encoding 
            
            html_content = response.text
            metadata = extract_data(html_content, target_url)

        except requests.exceptions.MissingSchema:
            error = "כתובת לא תקינה. וודא שהכתובת מתחילה ב-http או https"
        except requests.exceptions.ConnectionError:
            error = "לא ניתן להתחבר לשרת. בדוק את הכתובת."
        except Exception as e:
            error = f"שגיאה כללית: {str(e)}"

    return render_template_string(HTML_PAGE, 
                                 html_content=html_content, 
                                 error=error, 
                                 url=target_url, 
                                 theme=selected_theme,
                                 theme_index=current_theme_index,
                                 metadata=metadata)

if __name__ == '__main__':
    # מפעיל את האפליקציה (ניתן לגשת דרך http://127.0.0.1:5000/app1)
    app.run(debug=True, port=5000)
