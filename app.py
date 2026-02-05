from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Ahmad RDX Ultra-Stealth Headers (iPhone Identity)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

@app.route('/')
def home():
    return "🦅 Ahmad RDX Pinterest Private API v2.0 is ONLINE."

# ---------------------------------------------------------
# 🖼️ PINTEREST HD SCRAPER (Deep Scan Build)
# ---------------------------------------------------------
@app.route('/pinterest-api')
def pinterest_api():
    query = request.args.get('q')
    limit = int(request.args.get('limit', 6))
    
    if not query:
        return jsonify({"status": False, "msg": "Query (q) missing!"})

    try:
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Ahmad Bhai: Hum teen tarah ke links dhoondenge
        # 1. Standard HD (736x)
        # 2. Original Quality (originals)
        # 3. Alternative HD (236x fallback)
        
        patterns = [
            r'https://i.pinimg.com/736x/.*?\.jpg',
            r'https://i.pinimg.com/originals/.*?\.jpg',
            r'https://i.pinimg.com/236x/.*?\.jpg'
        ]
        
        all_images = []
        for pattern in patterns:
            found = re.findall(pattern, response.text)
            all_images.extend(found)

        # Safai (Cleanup): Backslashes hatana aur duplicates khatam karna
        clean_images = [img.replace('\\', '') for img in list(dict.fromkeys(all_images))]
        
        # Result limit
        final_list = clean_images[:limit]

        if final_list:
            return jsonify({
                "status": True,
                "query": query,
                "count": len(final_list),
                "result": final_list,
                "engine": "Ahmad-RDX-DeepScan-v2"
            })
        else:
            return jsonify({
                "status": False, 
                "msg": "No images found. Pinterest layout might have changed.",
                "debug_info": "Headers sent, but regex failed to match."
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
