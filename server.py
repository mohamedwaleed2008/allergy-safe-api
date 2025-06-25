from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze-menu', methods=['POST'])
def analyze_menu():
    image = request.files.get('menu')
    allergies = request.form.get('allergies', '')
    if not image or not allergies:
        return jsonify({'error': 'Missing image or allergies'}), 400

    allergies_list = [a.strip().lower() for a in allergies.split(',')]
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    safe_items = []
    unsafe_items = []

    for line in lines:
        if any(allergy in line.lower() for allergy in allergies_list):
            unsafe_items.append(line)
        else:
            safe_items.append(line)

    return jsonify({
        'safe_items': safe_items,
        'unsafe_items': unsafe_items
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
