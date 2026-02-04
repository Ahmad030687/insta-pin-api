from flask import Flask, request, jsonify, Response
import requests
import yt_dlp
import google.generativeai as genai
from bs4 import BeautifulSoup
import re
import base64
import random
import string

app = Flask(__name__)

# 🔑 API KEYS (Ahmad RDX Configuration)
GEMINI_KEY = "AIzaSyBogHNOLXqUiX8r1YQ-bXzLMk4UsB7W2lk"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------------------------------------------------------
# 🌍 1. HEALTH CHECK & HOME
# ---------------------------------------------------------
@app.route('/')
def home():
    return "🦅 Ahmad RDX Private API Server is ONLINE."

# ---------------------------------------------------------
# 📧 2. PREMIUM MAIL SYSTEM (Mail.tm)
# ---------------------------------------------------------
@app.route('/gen-mail')
def gen_mail():
    try:
        domain = requests.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        email = f"{user}@{domain}"
        password = "AhmadRdxPassword123"
        
        requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
        return jsonify({"status": True, "email": email, "password": password})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/check-mail')
def check_mail():
    email = request.args.get('email')
    password = "AhmadRdxPassword123"
    try:
        token_res = requests.post("https://api.mail.tm/token", json={"address": email, "password": password}).json()
        token = token_res['token']
        headers = {"Authorization": f"Bearer {token}"}
        msgs = requests.get("https://api.mail.tm/messages", headers=headers).json()['hydra:member']
        
        if not msgs:
            return jsonify({"new_mail": False})
        
        last_msg_id = msgs[0]['id']
        detail = requests.get(f"https://api.mail.tm/messages/{last_msg_id}", headers=headers).json()
        return jsonify({
            "new_mail": True,
            "from": detail['from']['address'],
            "subject": detail['subject'],
            "body": detail['text'],
            "date": detail['createdAt']
        })
    except:
        return jsonify({"new_mail": False})

# ---------------------------------------------------------
# 🎥 3. SOCIAL DOWNLOADER (TikTok, FB, Insta)
# ---------------------------------------------------------
@app.route('/social-dl')
def social_dl():
    target_url = request.args.get('url')
    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            return jsonify({
                "status": True, 
                "title": info.get('title', 'Video'),
                "url": info.get('url'),
                "source": info.get('extractor_key')
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# Video stream karne ke liye proxy (File attachment ke liye zaroori hai)
@app.route('/proxy-dl')
def proxy_dl():
    try:
        token = request.args.get('token')
        real_url = base64.b64decode(token).decode('utf-8')
        res = requests.get(real_url, stream=True)
        return Response(res.iter_content(chunk_size=1024), content_type=res.headers['Content-Type'])
    except:
        return "Error", 400

# ---------------------------------------------------------
# 🧠 4. GEMINI SMART ENGINE (Chat + Draw Logic)
# ---------------------------------------------------------
@app.route('/gemini-all')
def gemini_all():
    prompt = request.args.get('q')
    if not prompt: return jsonify({"status": False})
    try:
        instruction = f"Determine if user wants to DRAW or TALK. If DRAW, reply ONLY 'DRAW: <prompt>'. User: {prompt}"
        response = model.generate_content(instruction)
        reply = response.text
        if "DRAW:" in reply:
            img_prompt = reply.replace("DRAW:", "").strip()
            return jsonify({"type": "image", "prompt": img_prompt, "url": f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?model=flux&nologo=true"})
        return jsonify({"type": "text", "reply": reply})
    except:
        return jsonify({"type": "text", "reply": "Ahmad bhai, server busy hai!"})

# ---------------------------------------------------------
# 📸 5. PRIVATE SCRAPERS (IG & Pinterest)
# ---------------------------------------------------------
@app.route('/ig-info')
def ig_info():
    user = request.args.get('username')
    try:
        res = requests.get(f"https://imginn.com/{user}/")
        soup = BeautifulSoup(res.text, 'html.parser')
        return jsonify({
            "status": True,
            "full_name": soup.find('div', class_='info').find('h2').text.strip(),
            "followers": soup.find_all('span', class_='count')[1].text,
            "posts_count": soup.find_all('span', class_='count')[0].text,
            "profile_pic_url_hd": soup.find('div', class_='avatar').find('img')['src']
        })
    except:
        return jsonify({"status": False})

@app.route('/pin-search')
def pin_search():
    query = request.args.get('q')
    try:
        res = requests.get(f"https://www.pinterest.com/search/pins/?q={query}")
        images = list(set(re.findall(r'https://i.pinimg.com/736x/.*?\.jpg', res.text)))[:6]
        return jsonify({"status": True, "result": images})
    except:
        return jsonify({"status": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
  
