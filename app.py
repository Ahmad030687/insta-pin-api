from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# 🛡️ Ahmad RDX Stealth Headers
PRO_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

@app.route('/')
def home():
    return "🦅 Ahmad RDX Private API Server is ONLINE & READY."

# ---------------------------------------------------------
# 🖼️ PINTEREST HD SCRAPER (Premium Build)
# ---------------------------------------------------------
@app.route('/pinterest-api')
def pinterest_api():
    query = request.args.get('q')
    limit = int(request.args.get('limit', 6))
    
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    try:
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        response = requests.get(url, headers=PRO_HEADERS, timeout=10)
        
        # Regex to find HD (736x) or Originals images
        images = re.findall(r'https://i.pinimg.com/736x/.*?\.jpg', response.text)
        
        # Unique and clean links
        final_images = [img.replace('\\', '') for img in list(dict.fromkeys(images))[:limit]]

        if final_images:
            return jsonify({
                "status": True,
                "query": query,
                "count": len(final_images),
                "result": final_images,
                "engine": "Ahmad-RDX-Scraper-v1"
            })
        else:
            return jsonify({"status": False, "msg": "No images found."})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# ---------------------------------------------------------
# 📸 INSTAGRAM: STEALTH SCRAPER (v4.0)
# ---------------------------------------------------------
@app.route('/ig-info')
def ig_info():
    username = request.args.get('username')
    if not username: return jsonify({"status": False, "msg": "Username missing"})
    
    # Mirror 1: Instanavigation
    try:
        url = f"https://instanavigation.com/user-profile/{username}"
        res = requests.get(url, headers=PRO_HEADERS, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            name = soup.find('h1').text.strip() if soup.find('h1') else username
            stats = soup.find_all('div', class_='stats-item')
            dp = soup.find('div', class_='user-avatar').find('img')['src'] if soup.find('div', class_='user-avatar') else ""
            
            return jsonify({
                "status": True,
                "full_name": name,
                "username": username,
                "followers": stats[1].find('span').text.strip() if len(stats) > 1 else "N/A",
                "posts_count": stats[0].find('span').text.strip() if len(stats) > 0 else "N/A",
                "profile_pic_url_hd": dp,
                "source": "InstaNav"
            })
    except: pass

    # Mirror 2: Save-Insta Fallback
    try:
        url = f"https://www.save-insta.com/profile-downloader/?username={username}"
        res = requests.get(url, headers=PRO_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        dp_img = soup.find('img', id='profile_img')
        if dp_img:
            return jsonify({
                "status": True,
                "full_name": username,
                "profile_pic_url_hd": dp_img['src'],
                "source": "SaveInsta"
            })
    except: pass

    return jsonify({"status": False, "msg": "Both Instagram mirrors are currently blocking requests."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
            
