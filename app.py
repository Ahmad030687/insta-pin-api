import requests
import re
from flask import Flask, request, jsonify

# ... (baaki code ke niche ye add karein)

# ---------------------------------------------------------
# 🖼️ PINTEREST HD SCRAPER (Premium Build)
# ---------------------------------------------------------
@app.route('/pinterest-api')
def pinterest_api():
    query = request.args.get('q')
    # Kitni images chahiye? Default 6
    limit = int(request.args.get('limit', 6))
    
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    try:
        # Pinterest Search URL
        url = f"https://www.pinterest.com/search/pins/?q={query}"
        
        # Professional Header taake Pinterest block na kare
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Logic: Hum HTML mein se wo links dhoondenge jo '736x' (HD) folder mein hain
        # Regex pattern jo Pinterest ke image servers ko target karta hai
        images = re.findall(r'https://i.pinimg.com/736x/.*?\.jpg', response.text)
        
        # Cleanup: Duplicates khatam karein aur limit lagayein
        unique_images = list(dict.fromkeys(images))
        final_images = unique_images[:limit]

        if final_images:
            return jsonify({
                "status": True,
                "query": query,
                "count": len(final_images),
                "result": final_images,
                "engine": "Ahmad-RDX-Scraper-v1"
            })
        else:
            return jsonify({"status": False, "msg": "No images found for this query."})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})
        
