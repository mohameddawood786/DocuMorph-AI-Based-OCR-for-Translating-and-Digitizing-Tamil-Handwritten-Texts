import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
import time
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

# ------------------------- 1. Load Dataset -------------------------

dataset_dir = 'Dataset'  # Main folder containing class subfolders

# Initialize lists to store features (X) and labels (y)
X = []
y = []

# Iterate over the dataset directory and load images
for label, category in enumerate(os.listdir(dataset_dir)):
    category_path = os.path.join(dataset_dir, category)
    if os.path.isdir(category_path):
        for image_name in os.listdir(category_path):
            image_path = os.path.join(category_path, image_name)
            img = cv2.imread(image_path)
            img_resized = cv2.resize(img, (128, 128))  # Resize image to 128x128

            # Append the flattened image and its corresponding label
            X.append(img_resized)
            y.append(label)  # Use folder name as the label (i.e., category index)

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Normalize the image data (if needed)
X = X / 255.0

# Convert labels to categorical (one-hot encoding)
y = to_categorical(y)

# ------------------------- 2. Split Data -------------------------

# Hold-Out Validation
start_time = time.time()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
# Train model (replace with your model fitting code)
# model.fit(X_train, y_train)
y_pred = model.predict(X_test)  # Replace with actual prediction
holdout_accuracy = accuracy_score(y_test, y_pred)
holdout_time = time.time() - start_time

# k-Fold Cross-Validation
start_time = time.time()
kf = StratifiedKFold(n_splits=5)
fold_accuracies = []
for train_index, val_index in kf.split(X, y):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]
    # Train model (replace with your model fitting code)
    # model.fit(X_train, y_train)
    y_pred = model.predict(X_val)  # Replace with actual prediction
    fold_accuracies.append(accuracy_score(y_val, y_pred))
kfold_accuracy = np.mean(fold_accuracies)
kfold_time = time.time() - start_time

# ------------------------- 3. Print Results -------------------------
print(f"Hold-Out Accuracy: {holdout_accuracy} Time: {holdout_time} seconds")
print(f"k-Fold Accuracy: {kfold_accuracy} Time: {kfold_time} seconds")
