from flask import Flask, request, jsonify, Response
import requests
from bs4 import BeautifulSoup
import re
import random

app = Flask(__name__)

# Professional Headers taake server ko lage hum asli browser hain
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

@app.route('/')
def home():
    return "🦅 Ahmad RDX Ultra-Stable API is ONLINE."

# ---------------------------------------------------------
# 📸 NEW INSTAGRAM SCRAPER (Picuki Engine - High Stability)
# ---------------------------------------------------------
@app.route('/ig-info')
def ig_info():
    username = request.args.get('username')
    if not username: return jsonify({"status": False})
    
    try:
        url = f"https://www.picuki.com/profile/{username}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        if res.status_code != 200:
            return jsonify({"status": False, "msg": "Mirror blocked. Try later."})
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Profile Data Extraction
        name = soup.find('h1', class_='profile-name-bottom').text.strip() if soup.find('h1', class_='profile-name-bottom') else username
        stats = soup.find_all('span', class_='profile-info-stats')
        # stats[0] = posts, stats[1] = followers, stats[2] = following
        
        dp = soup.find('div', class_='profile-avatar').find('img')['src'] if soup.find('div', class_='profile-avatar') else ""
        bio = soup.find('div', class_='profile-description').text.strip() if soup.find('div', class_='profile-description') else "No Bio"

        return jsonify({
            "status": True,
            "full_name": name,
            "username": username,
            "followers": stats[1].text.strip() if len(stats) > 1 else "N/A",
            "posts_count": stats[0].text.strip() if len(stats) > 0 else "N/A",
            "profile_pic_url_hd": dp,
            "biography": bio
        })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# ---------------------------------------------------------
# 🖼️ NEW PINTEREST SCRAPER (Deep Search Engine)
# ---------------------------------------------------------
@app.route('/pin-search')
def pin_search():
    query = request.args.get('q')
    num = int(request.args.get('number', 6))
    
    try:
        # Pinterest mobile search logic
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        # Regex for different image sizes (HD, Medium, Small)
        # 2026 Pattern Matcher
        images = re.findall(r'https://i.pinimg.com/736x/.*?\.jpg|https://i.pinimg.com/originals/.*?\.jpg', res.text)
        
        # Cleanup & Unique links
        final_list = list(dict.fromkeys(images))[:num]
        
        if not final_list:
            # Last resort fallback
            final_list = re.findall(r'https://i.pinimg.com/236x/.*?\.jpg', res.text)[:num]

        return jsonify({
            "status": True if final_list else False,
            "result": final_list
        })
    except:
        return jsonify({"status": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
