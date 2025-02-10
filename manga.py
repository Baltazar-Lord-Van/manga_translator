import os
from flask import Flask, request, jsonify
from easyocr import Reader
from PIL import Image
from deep_translator import DeeplTranslator  # Using DeepL instead of Google Translate

app = Flask(__name__)

# Load API Key from environment variables (set this in Render)
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
S
@app.route("/")
def home():
    return jsonify({"message": "Manga Translator API is running!"})

@app.route("/translate", methods=["POST"])
def translate():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    img = Image.open(file)

    # Step 1: OCR - Extract text
    reader = Reader(["ja", "zh", "pt"])  # Supports Japanese, Chinese, and Portuguese
    results = reader.readtext(img)

    # Step 2: Translate text using DeepL
    translated_text = []
    translator = DeeplTranslator(DEEPL_API_KEY, target="en")  # Translate to English

    for result in results:
        original_text = result[1]  # Extract detected text
        translated = translator.translate(original_text)
        translated_text.append(translated)

    # Step 3: Send back the translated text
    return jsonify({"translated_text": translated_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
