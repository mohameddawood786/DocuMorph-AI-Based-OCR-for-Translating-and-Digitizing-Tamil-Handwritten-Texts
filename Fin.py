import os
import cv2
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint

# Paths
dataset_dir = '0-155'
train1_dir = 'train1_data'
test1_dir = 'test1_data'

# Create train and test directories
os.makedirs(train1_dir, exist_ok=True)
os.makedirs(test1_dir, exist_ok=True)

# Image Preprocessing Function
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    img = cv2.resize(img, (128, 128))  # Resize to 128x128
    img = cv2.GaussianBlur(img, (5, 5), 0)  # Noise reduction
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img = img / 255.0  # Normalize
    return img

# Splitting dataset
for category in os.listdir(dataset_dir):
    category_path = os.path.join(dataset_dir, category)
    if not os.path.isdir(category_path):
        continue
    os.makedirs(os.path.join(train1_dir, category), exist_ok=True)
    os.makedirs(os.path.join(test1_dir, category), exist_ok=True)
    images = [os.path.join(category_path, img) for img in os.listdir(category_path)]
    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)
    for img in train_images:
        shutil.copy(img, os.path.join(train1_dir, category, os.path.basename(img)))
    for img in test_images:
        shutil.copy(img, os.path.join(test1_dir, category, os.path.basename(img)))
print("Data split into train and test sets!")

# Data Augmentation
train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=20, width_shift_range=0.2, 
                                   height_shift_range=0.2, shear_range=0.2, zoom_range=0.2,
                                   horizontal_flip=True, fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255)

# Load Data
train_generator = train_datagen.flow_from_directory(train1_dir, target_size=(128, 128),
                                                    batch_size=32, color_mode='grayscale',
                                                    class_mode='categorical')
test_generator = test_datagen.flow_from_directory(test1_dir, target_size=(128, 128),
                                                  batch_size=32, color_mode='grayscale',
                                                  class_mode='categorical')

# CNN Model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Model Checkpoint
checkpoint = ModelCheckpoint("best_tamil_ocr_mod.h5", monitor='val_accuracy', save_best_only=True, mode='max')

# Train Model
model.fit(train_generator, epochs=10, validation_data=test_generator, callbacks=[checkpoint])

print("Model trained and best model saved!")
