# ---------------------------------------------------------
# 📸 INSTAGRAM: THE UNSTOPPABLE SCRAPER (v4.0 - Stealth Mode)
# ---------------------------------------------------------
@app.route('/ig-info')
def ig_info():
    username = request.args.get('username')
    if not username: return jsonify({"status": False})
    
    # Mirror 1: Instanavigation (Bypass Block)
    try:
        url = f"https://instanavigation.com/user-profile/{username}"
        # Random User-Agent change
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Data extraction logic based on Instanavigation structure
            name = soup.find('h1').text.strip() if soup.find('h1') else username
            stats = soup.find_all('div', class_='stats-item') # Posts, Followers, Following
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
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Simple extraction for backup
        return jsonify({
            "status": True,
            "full_name": username,
            "profile_pic_url_hd": soup.find('img', id='profile_img')['src'],
            "source": "SaveInsta"
        })
    except:
        return jsonify({"status": False, "msg": "Instagram servers are very tight right now. Try again later."})
        
