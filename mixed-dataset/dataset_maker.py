"""
File: dataset_maker.py
Author: Marco Domingo
Description: 
Example on how to create a dataset for training a model to recognize hand gestures.
The dataset is created by capturing images from the camera and saving them in the respective folders.

MIT License
Copyright (c) 2023 Marco Domingo
See the [MIT License](https://opensource.org/licenses/MIT) for details.
"""

import cv2
import datetime
import os

# Get the absolute path to the current script location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Open the camera (0 corresponds to the default camera, you can change it if needed)
cap = cv2.VideoCapture(0)

# Set the frame dimensions
frame_width = 640
frame_height = 480

# Set the capture dimensions
cap.set(3, frame_width)
cap.set(4, frame_height)

# Set the ROI size
roi_size = 256

# Initialize a dictionary to store the image counts for each folder
image_counts = {str(i): 0 for i in range(6)}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Mirror the camera by flipping horizontally
    frame = cv2.flip(frame, 1)

    # Draw a bounding box on the frame
    top_left = (int((frame_width - roi_size) / 2), int((frame_height - roi_size) / 2))
    bottom_right = (top_left[0] + roi_size, top_left[1] + roi_size)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Get the region of interest (ROI)
    roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Resize the ROI to 256x256
    roi = cv2.resize(roi, (roi_size, roi_size))

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Display the frame with bounding box
    cv2.imshow('Frame with ROI', frame)

    # Display the grayscale ROI
    cv2.imshow('Grayscale ROI', gray_roi)

    # Get the key pressed by the user
    key = cv2.waitKey(1) & 0xFF

    # Save the grayscale ROI in the respective folder based on the key pressed
    if key in range(48, 54):  # ASCII codes for '0' to '5'
        folder_path = str(key - 48)  # Convert ASCII code to folder name

        # Create absolute paths for saving images
        folder_abs_path = os.path.join(script_dir, folder_path)
        img_filename = os.path.join(folder_abs_path, f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}.png")
        
        try:
            cv2.imwrite(img_filename, gray_roi)

            # Check if the image is saved before updating counts and displaying
            if os.path.isfile(img_filename):
                # Update image count and display
                image_counts[folder_path] += 1
                total_counts_str = ' '.join([f'{key}:{value}' for key, value in image_counts.items()])
                print(f"Image saved in folder {folder_path}. Total images added -- {total_counts_str}")
            else:
                print(f"Failed to save image in folder {folder_path}")
        except Exception as e:
            print(f"Error saving image in folder {folder_path}: {e}")

    # Break the loop if 'q' is pressed
    elif key == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
