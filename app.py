from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# =======================
# 🤖 Assistant endpoint
# =======================
@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    query = data.get("query", "").lower()

    response = {"text": f"You said: {query}", "url": None}

    # 🔹 Handle "open X" commands
    if query.startswith("open "):
        site = query.replace("open ", "").strip()

        websites = {
            "youtube": "https://www.youtube.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "instagram": "https://www.instagram.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "tiktok": "https://www.tiktok.com",
        }

        if site in websites:
            response = {"text": f"Open {site.title()}", "url": websites[site]}
        else:
            response = {"text": f"Open {site.title()}", "url": f"https://{site}.com"}

    # 🔹 Handle "search X" commands
    elif query.startswith("search "):
        search_term = query.replace("search ", "").strip()
        search_url = f"https://www.google.com/search?q={search_term}"
        response = {"text": f"Search results for {search_term}", "url": search_url}

    return jsonify(response)



# =======================
# 🌍 Translation endpoint
# =======================
@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text")
    dest_lang = data.get("target_lang", "fr")  # default = French

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translated = GoogleTranslator(source="auto", target=dest_lang).translate(text)
        return jsonify({"translated": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is running ✅"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
