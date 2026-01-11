import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load the pre-trained model
model = load_model('model.h5')

# Image Data Generator
train_dir = 'D:\\Kaggle\\Cataract\\train'
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)
validation_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# Route for the home page
@app.route('/')
def home():
    # Get training images for immature and mature categories
    immature_dir = os.path.join(train_dir, 'immature')
    mature_dir = os.path.join(train_dir, 'mature')
    
    immature_images = ['train/immature/' + f for f in os.listdir(immature_dir) if os.path.isfile(os.path.join(immature_dir, f))][:3]
    mature_images = ['train/mature/' + f for f in os.listdir(mature_dir) if os.path.isfile(os.path.join(mature_dir, f))][:3]
    
    return render_template('index.html', immature_images=immature_images, mature_images=mature_images)

# Route to handle image uploads and predictions
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess the image
        image = Image.open(filepath).convert('RGB')
        image = image.resize((150, 150))
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.

        # Make a prediction
        prediction = model.predict(img_array)
        result = "Mature Cataract" if prediction[0][0] > 0.5 else "Immature Cataract"

        return jsonify({'result': result, 'filepath': filename})

# Route to display uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to serve training images
@app.route('/train/<path:filename>')
def train_file(filename):
    return send_from_directory(train_dir, filename)

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
