# ----------------- IMPORT PACKAGES ------------------------

import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib
import matplotlib.pyplot as plt 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tkinter.filedialog import askopenfilename

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import cv2
import matplotlib.image as mpimg



# ------------------------- READ INPUT IMAGE -------------------------


filename = askopenfilename()
img = mpimg.imread(filename)
plt.imshow(img)

plt.axis ('off')
# plt.savefig("Ori.png")
plt.title('Original Image')



# ------------------------- PREPROCESS -------------------------

#==== RESIZE IMAGE ====

resized_image = cv2.resize(img,(300,300))
img_resize_orig = cv2.resize(img,((50, 50)))

fig = plt.figure()
plt.title('RESIZED IMAGE')
plt.imshow(resized_image)
plt.axis ('off')
plt.show()
   
         
#==== GRAYSCALE IMAGE ====



SPV = np.shape(img)

try:            
    gray1 = cv2.cvtColor(img_resize_orig, cv2.COLOR_BGR2GRAY)
    
except:
    gray1 = img_resize_orig
   
fig = plt.figure()
plt.title('GRAY SCALE IMAGE')
plt.imshow(gray1)
plt.axis ('off')
plt.show()




# ------------------------- 3.FEATURE EXTRACTION -------------------------


#=== MEAN STD DEVIATION ===

mean_val = np.mean(gray1)
median_val = np.median(gray1)
var_val = np.var(gray1)
features_extraction = [mean_val,median_val,var_val]

print("-------------------------------------")
print("        Feature Extraction          ")
print("-------------------------------------")
print()
print(features_extraction)





import os
import shutil
from sklearn.model_selection import train_test_split

# Paths
dataset_dir = 'Dataset'  # Main folder containing class subfolders
train_dir = 'train_data'       # Directory where training data will go
test_dir = 'test_data'         # Directory where testing data will go

# Create the train and test directories
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Loop over each subfolder (class) in Dataset_Tamil
for category in os.listdir(dataset_dir):
    category_path = os.path.join(dataset_dir, category)

    # Skip if it's not a folder (in case there are any non-folder files)
    if not os.path.isdir(category_path):
        continue

    # Create corresponding class folders in train and test
    os.makedirs(os.path.join(train_dir, category), exist_ok=True)
    os.makedirs(os.path.join(test_dir, category), exist_ok=True)

    # Get all image files in the category
    images = [os.path.join(category_path, image) for image in os.listdir(category_path)]
    
    # Split the data into 80% for training and 20% for testing
    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)

    # Move the training images to train directory
    for img in train_images:
        shutil.copy(img, os.path.join(train_dir, category, os.path.basename(img)))

    # Move the testing images to test directory
    for img in test_images:
        shutil.copy(img, os.path.join(test_dir, category, os.path.basename(img)))

print("Data has been split into train and test sets!")





import tensorflow as tf
from tensorflow.keras import models, layers, optimizers
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tkinter.filedialog import askopenfilename
import numpy as np
import os
import cv2
from kymatio import Scattering2D




from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data Preprocessing with ImageDataGenerator
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values to [0, 1]
    rotation_range=20,  # Random rotations
    width_shift_range=0.2,  # Horizontal shifts
    height_shift_range=0.2,  # Vertical shifts
    shear_range=0.2,  # Shearing transformations
    zoom_range=0.2,  # Zoom transformations
    horizontal_flip=True,  # Flip images horizontally
    fill_mode='nearest'  # Fill missing pixels
)

test_datagen = ImageDataGenerator(rescale=1./255)  # Only rescaling for test data

# Flow data from directories
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),  # Resize all images to 128x128 pixels
    batch_size=32,
    class_mode='categorical',  # Multi-class classification
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(128, 128),  # Resize all images to 128x128 pixels
    batch_size=32,
    class_mode='categorical',  # Multi-class classification
    shuffle=False  # No shuffling for evaluation
)



from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Build the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(train_generator.class_indices), activation='softmax')  # Output layer
])

# Compile the model
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])




# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=10,
    validation_data=test_generator,
    validation_steps=test_generator.samples // test_generator.batch_size
)




# Evaluate the model on test data
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")

model.save('cnn_model.h5')


################## CRNN



# -------------------- Building the CRNN Model ----------------------

def build_crnn_model(input_shape, num_classes):
    inputs = layers.Input(shape=input_shape)

    # Convolutional Layers (feature extraction)
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)

    # Recurrent Layer (LSTM/GRU for sequence learning)
    x = layers.Reshape((-1, 128))(x)  # Flatten for RNN
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)

    # Output Layer (character probabilities)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

# -------------------- Data Generator ----------------------

# Image Data Generator for Training and Testing
train_datagen = ImageDataGenerator(rescale=1./255, 
                                   width_shift_range=0.2, 
                                   height_shift_range=0.2, 
                                   zoom_range=0.2, 
                                   horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    train_dir, 
    target_size=(300, 300), 
    batch_size=32, 
    class_mode=None, 
    shuffle=True
)

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    test_dir, 
    target_size=(300, 300), 
    batch_size=32, 
    class_mode=None, 
    shuffle=False
)

# -------------------- Training the Model ----------------------

# Define input shape and number of classes (based on your dataset)
input_shape = (300, 300, 3)  # Resized image size
num_classes = len(train_generator.class_indices)  # Number of classes

# Build and train the CRNN model
model = build_crnn_model(input_shape, num_classes)
model.summary()

# Train the model
model.fit(train_generator, epochs=10, validation_data=test_generator)

# -------------------- Evaluate the Model ----------------------

# Evaluate on test data
test_loss, test_accuracy = model.evaluate(test_generator)

print(f"Test Accuracy: {test_accuracy*100:.2f}%")





# -------------------- Custom Data Generator ----------------------
from tensorflow.keras import models, layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from tensorflow.keras.utils import Sequence


class OCRDataGenerator(Sequence):
    def __init__(self, image_paths, labels, batch_size, image_size, shuffle=True):
        self.image_paths = image_paths
        self.labels = labels
        self.batch_size = batch_size
        self.image_size = image_size
        self.shuffle = shuffle
        self.indices = np.arange(len(self.image_paths))
        self.on_epoch_end()

    def __len__(self):
        # Returns the number of batches per epoch
        return int(np.floor(len(self.image_paths) / self.batch_size))

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        # Get the batch of image indices
        batch_indices = self.indices[index * self.batch_size: (index + 1) * self.batch_size]
        batch_images = [self.image_paths[i] for i in batch_indices]
        batch_labels = [self.labels[i] for i in batch_indices]

        # Process the images
        images = np.array([cv2.resize(cv2.imread(img_path), self.image_size) for img_path in batch_images])
        images = images / 255.0  # Normalize to [0, 1]

        # Process the labels (need encoding as one-hot)
        label_encoded = np.array(batch_labels)

        return images, label_encoded

    def get_labels(self):
        return self.labels

# -------------------- Building the CRNN Model ----------------------

def build_crnn_model(input_shape, num_classes):
    inputs = layers.Input(shape=input_shape)

    # Convolutional Layers (feature extraction)
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)

    # Recurrent Layer (LSTM/GRU for sequence learning)
    x = layers.Reshape((-1, 128))(x)  # Flatten for RNN
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)

    # Output Layer (character probabilities)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

# -------------------- Data Generator Setup ----------------------

# Load dataset paths and labels
image_paths = []
labels = []

# Assuming labels are in text files or can be manually assigned
# Example: labels for training images (replace with actual labels)
for category in os.listdir(dataset_dir):
    category_path = os.path.join(dataset_dir, category)
    if os.path.isdir(category_path):
        for image_file in os.listdir(category_path):
            image_path = os.path.join(category_path, image_file)
            label = category  # You need to replace this with actual text from labels
            image_paths.append(image_path)
            labels.append(label)

# Split dataset into training and testing
train_paths, test_paths, train_labels, test_labels = train_test_split(image_paths, labels, test_size=0.2, random_state=42)

# Create custom generators
train_generator = OCRDataGenerator(train_paths, train_labels, batch_size=32, image_size=(300, 300))
test_generator = OCRDataGenerator(test_paths, test_labels, batch_size=32, image_size=(300, 300))

# -------------------- Training the Model ----------------------

# Define input shape and number of classes (based on your dataset)
input_shape = (300, 300, 3)  # Resized image size
num_classes = len(set(labels))  # Number of classes (replace with actual number)

# Build and train the CRNN model
model = build_crnn_model(input_shape, num_classes)
model.summary()

# Train the model
model.fit(train_generator, epochs=10, validation_data=test_generator)

# -------------------- Evaluate the Model ----------------------

# Evaluate on test data
test_loss, test_accuracy = model.evaluate(test_generator)

print(f"Test Accuracy: {test_accuracy*100:.2f}%")










