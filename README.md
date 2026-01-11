# Cataract Maturity Classification

A premium, deep-learning-powered web application for classifying cataract maturity from ocular images. This project utilizes a Convolutional Neural Network (CNN) backend with a modern, glassmorphism-styled frontend.

## 🌟 Features

-   **Deep Learning Model**: Classifies images as "Immature Cataract" or "Mature Cataract" using a custom-trained Keras/TensorFlow model.
-   **Premium UI**: A sleek, medical-themed interface featuring glassmorphism effects and animated backgrounds.
-   **Instant Analysis**: AJAX-based prediction system for analyzing scans without page reloads.
-   **Drag & Drop**: Intuitive file upload zone with instant image preview.
-   **Sample Gallery**: Built-in training samples to test the model immediately.

## 🛠️ Tech Stack

-   **Backend**: Python, Flask, TensorFlow, Keras
-   **Frontend**: HTML5, CSS3 (Custom Animations), JavaScript (Fetch API)
-   **Data Processing**: NumPy, Pillow

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Pratham0405/Cataract_Maturity_Classification.git
    cd Cataract_Maturity_Classification
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python main.py
    ```

5.  **Access the App**
    Open your browser and navigate to `http://localhost:5000`.

## 📂 Project Structure

```
├── main.py              # Flask Application Entry Point
├── model.h5             # Pre-trained CNN Model
├── static/
│   ├── style.css        # Premium Styling
│   ├── script.js        # Frontend Logic
│   └── uploads/         # Temp folder for uploads
├── templates/
│   └── index.html       # Single Page Application
├── requirements.txt     # Python Dependencies
└── README.md            # Project Documentation
```

## ⚠️ Note

This application is for demonstration and educational purposes only. It is not intended to be a replacement for professional medical diagnosis.
