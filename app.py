from flask import Flask, render_template, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caption', methods=['POST'])
def caption():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    image = Image.open(filepath).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(debug=True)
import json
from datetime import datetime

@app.route('/caption', methods=['POST'])
def caption():
    ...
    caption = processor.decode(out[0], skip_special_tokens=True)

    history_path = 'history.json'
    history = []
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
    
    history.append({
        'filename': file.filename,
        'caption': caption,
        'timestamp': datetime.now().isoformat()
    })
    
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)

    return jsonify({'caption': caption})
@app.route('/gallery')
def gallery():
    history = []
    history_path = 'history.json'
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
    return render_template('gallery.html', history=history)
