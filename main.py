from flask import Flask, render_template, request, redirect
from google.cloud import vision
from google.cloud import storage
from werkzeug.utils import secure_filename
import os
import uuid

# Set your GCS bucket name here:
GCS_BUCKET_NAME = 'my-image-classifier-bucket-987654321'  # <== replace this!

# Init Flask app
app = Flask(__name__)

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

        # Prepare filename and read image content
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        content = file.read()

        # Upload image to GCS bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(unique_filename)
        blob.upload_from_string(content, content_type=file.content_type)

        # Make URL public
        blob.make_public()
        image_url = blob.public_url

        # Vision API call
        client = vision.ImageAnnotatorClient()
        image = vision.Image(source=vision.ImageSource(image_uri=image_url))
        response = client.label_detection(image=image)
        labels = response.label_annotations

        result = ', '.join([label.description for label in labels])

    return render_template('index.html', result=result, image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
