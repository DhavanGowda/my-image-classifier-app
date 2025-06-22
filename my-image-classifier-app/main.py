from flask import Flask, request, render_template
from google.cloud import vision

app = Flask(__name__)

client = vision.ImageAnnotatorClient()

@app.route('/', methods=['GET', 'POST'])
def index():
    labels = []
    if request.method == 'POST':
        image_file = request.files['image']
        content = image_file.read()

        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]

    return render_template('index.html', labels=labels)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
