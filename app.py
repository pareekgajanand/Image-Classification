import os
from flask import Flask, request, render_template
import base64
import tensorflow as tf
model_path = os.path.join(os.path.dirname(__file__), '6_class_image.h5')
load_image_model = tf.keras.models.load_model(model_path)


def load_and_prep_image(file_path, img_shape=224):
    img = tf.io.read_file(file_path)
    img = tf.image.decode_image(img)
    img = tf.image.resize(img, size=[img_shape, img_shape])
    img = img / 255.
    return img

class_names = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']

def pred_and_plot(model, file_path, class_names=class_names):
    img = load_and_prep_image(file_path)
    pred = model.predict(tf.expand_dims(img, axis=0))
    if len(pred[0]) > 1:
        pred_class = class_names[tf.argmax(pred[0])]
    else:
        pred_class = class_names[int(tf.round(pred))]
    return pred_class

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

# Define a path to store the uploaded files temporarily
upload_folder = "uploads"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        if image:
            print("Image Uploaded")
            # Save the uploaded file to a temporary location
            temp_file_path = os.path.join(upload_folder, "uploaded_image.jpg")
            image.save(temp_file_path)
            response_message = pred_and_plot(load_image_model, temp_file_path, class_names)
            return render_template('result.html', message=response_message)
    response_message = 'No image selected.'
    return render_template('result.html', message=response_message)

if __name__ == '__main__':
    app.run(debug=True, port=8085)
