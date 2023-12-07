"""
File: 3_train_hand_recognition.py
Author: Marco Domingo
Description: Example on how to train a model to recognize hand gestures using the dataset from the previous step.

MIT License
Copyright (c) 2023 Marco Domingo
See the [MIT License](https://opensource.org/licenses/MIT) for details.
"""


import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

EPOCHS = 100
BATCH_SIZE = 8

# Define the path to your dataset
dataset_path = "mixed-dataset"

# Function to load and preprocess the dataset
def load_dataset(dataset_path, image_size=(128, 128)):
    data = []
    labels = []

    for class_label in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_label)

        # Check if the item is a directory
        if os.path.isdir(class_path):
            for filename in os.listdir(class_path):
                img_path = os.path.join(class_path, filename)

                # Read and preprocess the image
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, image_size)
                img = img / 255.0
                img = np.expand_dims(img, axis=(-1))

                # Append the image and label to the lists
                data.append(img)
                labels.append(int(class_label))

    return np.array(data), np.array(labels)

# Load the dataset
X, y = load_dataset(dataset_path)

# Convert labels to one-hot encoding
y = to_categorical(y, num_classes=6)

# Split the dataset into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(128, 128, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(6, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Uncomment the following lines for retraining
# model.load_weights("./models/path_to_your_model.h5")

# Define a ModelCheckpoint callback to save the model with the best validation loss
checkpoint_path = "./models/codiax_model_{epoch:02d}_loss_{val_loss:.2f}.h5"
checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True, mode='min', verbose=1)

# Print model summary
model.summary()

# Train the model with the ModelCheckpoint callback
history = model.fit(X_train, y_train, batch_size=BATCH_SIZE, validation_data=(X_test, y_test),
                    epochs=EPOCHS, verbose=1, callbacks=[checkpoint])

# Save the final trained model
model.save("./models/codiax_model.h5")
