import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from PIL import Image

# Define directories
train_dir = 'D:\\Kaggle\\Cataract\\train'

# Image Data Generator
datagen = ImageDataGenerator(
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

# Training and validation generators
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',  # or 'categorical' if more than 2 classes
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',  # or 'categorical' if more than 2 classes
    subset='validation'
)

# Build model
model = load_model('model.h5')

# Streamlit app
st.title("Cataract Image Classification")

# Display a batch of images with augmentation
def display_images(generator, num_images=9):
    images, labels = next(generator)
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    axes = axes.flatten()
    for img, ax in zip(images[:num_images], axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)

# Sidebar for user inputs
st.sidebar.title("Options")
if st.sidebar.button("Show Training Images"):
    st.write("Displaying Training Images with Augmentation")
    display_images(train_generator)

if st.sidebar.button("Show Validation Images"):
    st.write("Displaying Validation Images with Augmentation")
    display_images(validation_generator)



# Upload image for prediction
st.sidebar.title("Predict Cataract")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    

    # Preprocess the image
    img = image.resize((150, 150))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.

    # Make a prediction
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:
        st.write("The image is classified as: Mature Cataract")
    else:
        st.write("The image is classified as: Immature Cataract")
