from flask import Flask, request, jsonify
from easyocr import Reader
from PIL import Image
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    file = request.files['image']
    img = Image.open(file)

    # Step 1: OCR - Extract text
    reader = Reader(["ja", "zh", "pt"])  # Adjust for supported languages
    results = reader.readtext(img)

    # Step 2: Translate text (e.g., from Japanese to English)
    translated_text = []
    for result in results:
        original_text = result[1]
        translated = GoogleTranslator(source='auto', target='en').translate(original_text)
        translated_text.append(translated)

    # Step 3: Send back the translated text
    return jsonify({"translated_text": translated_text})

if __name__ == "__main__":
    app.run(debug=True)
