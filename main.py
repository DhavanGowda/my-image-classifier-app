from flask import Flask, render_template, request, redirect, url_for
from google.cloud import vision
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_url = None

    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load image into Vision API
        client = vision.ImageAnnotatorClient()
        with open(filepath, 'rb') as image_file:
            content = image_file.read()
            image = vision.Image(content=content)
            response = client.label_detection(image=image)
            labels = response.label_annotations
            result = ', '.join([label.description for label in labels])

        image_url = url_for('static', filename=f'uploads/{filename}')

    return render_template('index.html', result=result, image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
