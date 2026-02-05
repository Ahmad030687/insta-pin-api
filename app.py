from flask import Flask, request, jsonify
import requests
import re

# 1. Sabse pehle app ko define karna zaroori hai (Error fix)
app = Flask(__name__)

# Ahmad RDX Stealth Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

@app.route('/')
def home():
    return "🦅 Ahmad RDX Pinterest Private API is ONLINE."

# ---------------------------------------------------------
# 🖼️ PINTEREST HD SCRAPER (Standalone Build)
# ---------------------------------------------------------
@app.route('/pinterest-api')
def pinterest_api():
    query = request.args.get('q')
    limit = int(request.args.get('limit', 6))
    
    if not query:
        return jsonify({"status": False, "msg": "Query (q) is missing!"})

    try:
        # Pinterest Search URL
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Regex to find HD (736x) image links
        images = re.findall(r'https://i.pinimg.com/736x/.*?\.jpg', response.text)
        
        # Cleaning and unique links
        final_list = [img.replace('\\', '') for img in list(dict.fromkeys(images))[:limit]]

        if final_list:
            return jsonify({
                "status": True,
                "query": query,
                "count": len(final_list),
                "result": final_list,
                "engine": "Ahmad-RDX-Scraper-v1"
            })
        else:
            return jsonify({"status": False, "msg": "No images found for this query."})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    # Render ke liye port 8080 ya 10000 zaroori hai
    app.run(host='0.0.0.0', port=8080)
    
