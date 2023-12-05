"""
File: 2_test_example.py
Author: Marco Domingo
Description: Example on how to test your model on a set of images and calculate the accuracy.
For the workshop's purposes this is used to test python installation and dependencies particularly ML libraries.

MIT License
Copyright (c) 2023 Marco Domingo
See the [MIT License](https://opensource.org/licenses/MIT) for details.
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score

# Load your trained model
model = load_model('models/simple_model.h5')

# Path to the test dataset
test_folder = 'fingers/test'

# Function to get the label from the filename
def get_label(filename):
    return int(filename.split('_')[-1][0])

# Function to predict the number of fingers
def predict_fingers(model, img_path):
    img = image.load_img(img_path, target_size=(128, 128), color_mode='grayscale')  # Adjust the target size and color mode
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the pixel values to be between 0 and 1
    prediction = model.predict(img_array)
    return np.argmax(prediction)  # Assuming your classes start from 0

# Get six random images from the test folder
test_images = random.sample(os.listdir(test_folder), 6)

# Get the true and predicted labels for the random images
true_labels = []
predicted_labels = []

# Plot the images with labels and predictions
plt.figure(num='Test Predictions',figsize=(15, 10))

for i, image_name in enumerate(test_images, 1):
    img_path = os.path.join(test_folder, image_name)
    true_label = get_label(image_name)
    predicted_label = predict_fingers(model, img_path)

    true_labels.append(true_label)
    predicted_labels.append(predicted_label)

    plt.subplot(2, 3, i)
    img = image.load_img(img_path, color_mode='grayscale')
    plt.imshow(img, cmap='gray')
    plt.title(f'True: {true_label}, Predicted: {predicted_label}')
    plt.axis('off')

# Calculate accuracy for the random images
accuracy = accuracy_score(true_labels, predicted_labels)
print(f'Accuracy for Randomly Selected Images: {accuracy * 100:.2f}%')

plt.show()
