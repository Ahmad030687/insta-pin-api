from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)

# 🛡️ Ahmad RDX Premium Headers (iPhone Simulation)
PRO_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

@app.route('/')
def home():
    return "🦅 Ahmad RDX God-Mode API is LIVE & SHIELDED."

# ---------------------------------------------------------
# 📸 INSTAGRAM: ULTIMATE FALLBACK (Mirror 1: Picuki, Mirror 2: Imginn)
# ---------------------------------------------------------
@app.route('/ig-info')
def ig_info():
    username = request.args.get('username')
    if not username: return jsonify({"status": False})
    
    # --- Try Mirror 1: Picuki ---
    try:
        url = f"https://www.picuki.com/profile/{username}"
        res = requests.get(url, headers=PRO_HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            name = soup.find('h1', class_='profile-name-bottom').text.strip() if soup.find('h1', class_='profile-name-bottom') else username
            stats = soup.find_all('span', class_='profile-info-stats')
            dp = soup.find('div', class_='profile-avatar').find('img')['src']
            return jsonify({
                "status": True, "full_name": name, "username": username,
                "followers": stats[1].text.strip(), "posts_count": stats[0].text.strip(),
                "profile_pic_url_hd": dp, "source": "Picuki"
            })
    except: pass

    # --- Try Mirror 2: Imginn (Fallback) ---
    try:
        url = f"https://imginn.com/{username}/"
        res = requests.get(url, headers=PRO_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return jsonify({
            "status": True,
            "full_name": soup.find('div', class_='info').find('h2').text.strip(),
            "followers": soup.find_all('span', class_='count')[1].text,
            "profile_pic_url_hd": soup.find('div', class_='avatar').find('img')['src'],
            "source": "Imginn"
        })
    except:
        return jsonify({"status": False, "msg": "Both IG mirrors are currently blocking Render IP."})

# ---------------------------------------------------------
# 🖼️ PINTEREST: DEEP SCRAPER (JSON Extraction)
# ---------------------------------------------------------
@app.route('/pin-search')
def pin_search():
    query = request.args.get('q')
    num = int(request.args.get('number', 6))
    
    try:
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        res = requests.get(url, headers=PRO_HEADERS, timeout=10)
        
        # Pinterest hides data in <script id="__PJS_DATA__"> or similar
        # We use a broad regex to catch all 736x (HD) or originals images
        images = re.findall(r'https://i.pinimg.com/736x/.*?\.jpg', res.text)
        
        if not images:
            # Try finding direct JSON links in script tags
            images = re.findall(r'"url":"(https://i.pinimg.com/originals/.*?\.jpg)"', res.text)
        
        # Cleanup links (Remove backslashes)
        final_list = [img.replace('\\', '') for img in list(dict.fromkeys(images))[:num]]

        return jsonify({
            "status": True if final_list else False,
            "result": final_list,
            "count": len(final_list)
        })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
