# Tamil-Handwritten-OCR
OCR system for digitizing handwritten Tamil text and translating printed English documents to Tamil using AI-driven models and NLP techniques.

# 📜 AI-Based OCR Solution for Digitizing and Translating Handwritten Tamil Documents

An AI-driven Optical Character Recognition (OCR) platform designed to convert handwritten Tamil text from scanned images into digital format, with an optional translation feature for printed English text into Tamil. The system integrates a custom-trained CRNN model, pretrained OCR frameworks, and advanced NLP-based post-processing for clean, accurate text extraction.

---

## 🎯 Objectives

- Convert handwritten Tamil documents into machine-readable digital text.
- Translate printed English text into Tamil for multilingual accessibility.
- Provide a clean, user-friendly web interface supporting multiple image uploads.
- Enhance recognition accuracy using a hybrid OCR architecture and NLP-driven text cleaning.
- Contribute to cultural and linguistic preservation by digitizing valuable regional scripts.

---

## 📦 System Modules

- **User Authentication:** Secure registration and login system using SQLite3.
- **OCR Processing:** Hybrid text extraction using EasyOCR and a custom CRNN model.
- **Text Cleaning:** Removes noise, normalizes Unicode characters, and corrects spelling errors.
- **Translation Module:** Converts printed English text into Tamil via neural translation APIs.
- **Post-Processing:** NLP-based grammar refinement and contextual error correction.
- **User Interface:** Streamlit + ReactJS dashboard supporting multiple file uploads and real-time result previews.
- **Database:** SQLite3 database management for user records.

---

## 🖥️ System Requirements

### 🔧 Hardware

- **Laptop:** Acer Nitro 5, Intel Core i5-11400H, 8GB RAM, NVIDIA GTX 1650
- **Display:** 15.6” FHD LED Backlit IPS Display

### 🛠️ Software & Libraries

| Library / Tool      | Version |
|:--------------------|:----------|
| Python               | 3.11.x |
| Numpy                | 1.26.4 |
| OpenCV               | 4.5.4 |
| Pillow (PIL)         | 9.0.1 |
| TensorFlow           | 2.17.0 |
| EasyOCR              | 1.6.2 |
| Streamlit            | 1.43.2 |
| Matplotlib           | 3.9.4 |
| Scikit-learn         | 1.0.2 |
| Seaborn              | 0.13.2 |
| IndicNLP Library     | 0.81 |
| SymSpellPy           | 6.7.7 |
| Googletrans          | 4.0.0rc1 |
| Kymatio              | 0.4.9 |
| Transformers         | 4.41.1 |

---

## 📊 Dataset Overview

- **Handwritten Tamil Characters:** 156 distinct character classes.
- **Total Samples:** 125,000 images.
  - 100,000 for training
  - 15,000 for validation
  - 10,000 for testing
- **Preprocessing:** Grayscale conversion, CLAHE enhancement, noise removal, and resizing (300×300 px).
- **Tamil Word Corpus:** Text corpus used for CRNN sequence training and NLP post-processing.

---

## 🚀 How to Run the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ocr-tamil-handwritten.git
   cd ocr-tamil-handwritten
2. **Create and activate a Python virtual environment**
   ```bash
   conda create -n ocr-env python=3.11
   conda activate ocr-env
3. **Install required libraries**
   ```bash
   pip install -r requirements.txt
4. **Launch the Streamlit application**
   ```bash
   streamlit run app.py

   

