import cv2
import numpy as np
import paho.mqtt.publish as publish
import json
from tensorflow.keras.models import load_model

# Replace "broker_ip" with the actual IP address of your MQTT broker, in the final case the RPi
broker_ip = "localhost"

# Load your trained model
model = load_model("./models/mixed_deep_model_checkpoint.h5")  # Replace with the path to your saved model

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

# Initialize the previous prediction value
previous_prediction = None

# Set the confidence threshold
confidence_threshold = 0.45

while True:
    ret, frame = cap.read()

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

    # Preprocess the grayscale ROI for model input
    processed_roi = cv2.resize(gray_roi, (128, 128))  # Assuming your model expects input shape (128, 128, 1)
    processed_roi = processed_roi / 255.0
    processed_roi = np.expand_dims(processed_roi, axis=(0, -1))  # Add batch and channel dimensions

    # Make a prediction using the model
    prediction = model.predict(processed_roi, verbose=0)

    # Get the predicted class and confidence levels
    predicted_class = np.argmax(prediction)
    confidence_levels = prediction[0]
    prediction_text = f"Prediction: Class {predicted_class}"
    cv2.putText(gray_roi, prediction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Grayscale ROI with Prediction', gray_roi)

    # Publish on MQTT if the prediction changes and is over the confidence threshold
    if previous_prediction is None or predicted_class != previous_prediction:
        if confidence_levels[predicted_class] > confidence_threshold:
            message = {"speed": 2*int(predicted_class)}
            publish.single("Dyson-NST-at-codiax", json.dumps(message), hostname=broker_ip)
            print(f"Published: Topic - Dyson-NST-at-codiax, Message - {message}, confidence : {confidence_levels[predicted_class]:.3f}")
            previous_prediction = predicted_class

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()