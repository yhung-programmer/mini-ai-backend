from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Translator ---
translator = Translator()

# =======================
# 🤖 Assistant endpoint
# =======================
@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.json
    query = data.get("query", "").lower()
    response = "I didn't understand that."

    if "youtube" in query:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube"
    elif "play music" in query:
        webbrowser.open("https://open.spotify.com")
        response = "Playing music"
    elif "search" in query:
        search_term = query.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(url)
        response = f"Searching for {search_term}"

    # Just return response (no server TTS)
    return jsonify({"response": response})


# =======================
# 🎤 Speech recognition
# =======================
@app.route("/speech", methods=["GET"])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =======================
# 🌍 Translation endpoint
# =======================
@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text")
    dest_lang = data.get("target_lang", "fr")  # default French if not chosen

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translation = translator.translate(text, dest=dest_lang)
        return jsonify({"translated": translation.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
